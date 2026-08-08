import sys
import json
import ast
import re
from pathlib import Path

try:
    import keyring
except ImportError:
    print("[ERROR] 请先安装 keyring 库以启用密钥安全存储: pip install keyring")
    sys.exit(1)

try:
    import openai
except ImportError:
    print("[ERROR] 请先安装 openai 库: pip install openai")
    sys.exit(1)

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QLabel,
    QComboBox, QLineEdit, QProgressBar, QStatusBar, QToolBar, QDialog,
    QFormLayout, QMessageBox, QMenu, QAbstractItemView, QSpinBox
)
from PySide6.QtCore import Qt, QThread, Signal, QSettings
from PySide6.QtGui import QFont, QColor, QPalette, QKeySequence, QShortcut

# ==================== Constants ====================
BASE_DIR = Path(__file__).parent.resolve()
MAIN_PY = BASE_DIR / "main.py"
LOCALES_DIR = BASE_DIR / "locales"

ALL_LANGS = {
    "zh_CN": "简体中文", "zh_TW": "繁體中文", "ja_JP": "日本語", "ko_KR": "한국어",
    "de_DE": "Deutsch", "fr_FR": "Français", "es_ES": "Español", "ru_RU": "Русский",
    "pt_BR": "Português (Brasil)", "it_IT": "Italiano", "nl_NL": "Nederlands",
    "pl_PL": "Polski", "tr_TR": "Türkçe", "vi_VN": "Tiếng Việt", "th_TH": "ไทย", "ar_SA": "العربية"
}

# ==================== Core Helpers ====================
def safe_write_json(file_path: Path, data: dict):
    LOCALES_DIR.mkdir(parents=True, exist_ok=True)
    temp_path = file_path.with_suffix('.tmp')
    try:
        temp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp_path.replace(file_path)
    except Exception as e:
        if temp_path.exists(): temp_path.unlink()
        raise e

def is_technical(text: str) -> bool:
    val = text.strip()
    if not val: return False
    patterns = [
        r'^Python(\s+[\d.]+)?$', r'^v?[\d.]+(-\w+)?$', r'^\w+\.\w+$',
        r'^(PyPI|pip|PyInstaller|Nuitka|venv|conda|wheel|QPyPack|GUI|UI|URL|API|ID|OK|Cancel)$',
        r'^[A-Z0-9_]+$', r'^\[[A-Z0-9_-]+\]$', r'^https?://\S+$', r'^\{[a-zA-Z0-9_]+\}$'
    ]
    return any(re.match(p, val, re.I) for p in patterns)

def validate_placeholders(original: str, translated: str) -> str:
    orig_vars = set(re.findall(r'\{([a-zA-Z0-9_]+)\}', original))
    trans_vars = set(re.findall(r'\{([a-zA-Z0-9_]+)\}', translated))
    missing, extra = orig_vars - trans_vars, trans_vars - orig_vars
    errs = []
    if missing: errs.append(f"缺 {{{','.join(missing)}}}")
    if extra: errs.append(f"多 {{{','.join(extra)}}}")
    return " | ".join(errs)

def extract_keys_and_zh_cn(py_path: Path) -> tuple[list, dict]:
    if not py_path.exists(): return [], {}
    tree = ast.parse(py_path.read_text(encoding="utf-8"))
    keys_set, zh_cn_dict = set(), {}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "ZH_CN_DICT" and isinstance(node.value, ast.Dict):
                    for k, v in zip(node.value.keys, node.value.values):
                        if isinstance(getattr(k, 'value', None), str):
                            keys_set.add(k.value)
                            if isinstance(getattr(v, 'value', None), str): zh_cn_dict[k.value] = v.value
        if isinstance(node, ast.Call):
            func = node.func
            if (isinstance(func, ast.Name) and func.id in ("_", "t")) or \
               (isinstance(func, ast.Attribute) and func.attr in ("t", "_")):
                if node.args and isinstance(getattr(node.args[0], 'value', None), str):
                    keys_set.add(node.args[0].value)
    return sorted(keys_set), zh_cn_dict

def clean_llm_json(raw_str: str) -> dict:
    clean_str = re.sub(r'^```json\s*|^```\s*|```$', '', raw_str.strip(), flags=re.I | re.M).strip()
    try:
        return json.loads(clean_str)
    except:
        return {}


class TranslationWorker(QThread):
    progress = Signal(int, int)
    batch_done = Signal(dict)
    finished_all = Signal()

    def __init__(self, cfg, lang_name, keys: list):
        super().__init__()
        self.cfg, self.lang_name, self.keys = cfg, lang_name, keys
        self.cancel_flag = False

    def run(self):
        client = openai.OpenAI(api_key=self.cfg["api_key"], base_url=self.cfg.get("base_url"))
        batch_size = self.cfg["batch_size"]
        
        for i in range(0, len(self.keys), batch_size):
            if self.cancel_flag: break
            batch_keys = self.keys[i:i+batch_size]
            
            id_map = {str(idx): k for idx, k in enumerate(batch_keys)}
            sys_prompt = f"Translate the following UI strings to {self.lang_name}. Output ONLY a valid JSON object keeping the exact same numeric keys."
            
            try:
                resp = client.chat.completions.create(
                    model=self.cfg["model"],
                    messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": json.dumps(id_map, ensure_ascii=False)}
                    ],
                    temperature=0.1, response_format={"type": "json_object"}
                )
                raw_json = clean_llm_json(resp.choices[0].message.content)
                result = {id_map[k]: str(v) for k, v in raw_json.items() if k in id_map and str(v).strip()}
                self.batch_done.emit(result)
            except Exception:
                pass
                
            self.progress.emit(min(i + batch_size, len(self.keys)), len(self.keys))
        self.finished_all.emit()


class MultiLangWorker(QThread):
    progress = Signal(int, int, str)
    finished_all = Signal()

    def __init__(self, cfg, all_keys: list):
        super().__init__()
        self.cfg = cfg
        self.all_keys = all_keys
        self.cancel_flag = False

    def run(self):
        client = openai.OpenAI(api_key=self.cfg["api_key"], base_url=self.cfg.get("base_url"))
        batch_size = self.cfg["batch_size"]
        targets = [c for c in ALL_LANGS if c != "zh_CN"]

        for lang_idx, code in enumerate(targets):
            if self.cancel_flag: break
            lang_name = ALL_LANGS[code]
            self.progress.emit(lang_idx, len(targets), f"正在处理: {lang_name} ({code})")

            file_path = LOCALES_DIR / f"{code}.json"
            data = json.loads(file_path.read_text("utf-8")) if file_path.exists() else {}

            missing = [k for k in self.all_keys if not data.get(k) and not is_technical(k)]
            if not missing:
                continue

            for i in range(0, len(missing), batch_size):
                if self.cancel_flag: break
                batch_keys = missing[i:i+batch_size]
                id_map = {str(idx): k for idx, k in enumerate(batch_keys)}
                sys_prompt = f"Translate the following UI strings to {lang_name}. Output ONLY a valid JSON object keeping the exact same numeric keys."

                try:
                    resp = client.chat.completions.create(
                        model=self.cfg["model"],
                        messages=[
                            {"role": "system", "content": sys_prompt},
                            {"role": "user", "content": json.dumps(id_map, ensure_ascii=False)}
                        ],
                        temperature=0.1, response_format={"type": "json_object"}
                    )
                    raw_json = clean_llm_json(resp.choices[0].message.content)
                    for k, v in raw_json.items():
                        if k in id_map and str(v).strip():
                            data[id_map[k]] = str(v)
                except Exception:
                    pass

            if not self.cancel_flag:
                safe_write_json(file_path, data)

        self.progress.emit(len(targets), len(targets), "全库补全完成！")
        self.finished_all.emit()

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ API 设置")
        self.setMinimumWidth(400)
        self.settings = QSettings("QPyPack", "i18nFast")
        
        layout = QFormLayout(self)
        
        saved_key = keyring.get_password("QPyPack_i18n", "api_key") or ""
        
        self.key_ed = QLineEdit(saved_key)
        self.key_ed.setEchoMode(QLineEdit.EchoMode.Password)
        self.url_ed = QLineEdit(self.settings.value("base_url", "https://api.deepseek.com"))
        self.mod_ed = QLineEdit(self.settings.value("model", "deepseek-chat"))
        self.batch_sp = QSpinBox(); self.batch_sp.setRange(5, 100); self.batch_sp.setValue(int(self.settings.value("batch_size", 30)))
        
        layout.addRow("API Key:", self.key_ed)
        layout.addRow("Base URL:", self.url_ed)
        layout.addRow("Model:", self.mod_ed)
        layout.addRow("批次大小:", self.batch_sp)
        
        btn = QPushButton("保存")
        btn.clicked.connect(self.save)
        layout.addRow("", btn)

    def save(self):
        api_key = self.key_ed.text().strip()
        
        if api_key:
            keyring.set_password("QPyPack_i18n", "api_key", api_key)
        else:
            try: keyring.delete_password("QPyPack_i18n", "api_key")
            except: pass

        self.settings.setValue("base_url", self.url_ed.text().strip())
        self.settings.setValue("model", self.mod_ed.text().strip())
        self.settings.setValue("batch_size", self.batch_sp.value())
        
        if self.settings.contains("api_key"):
            self.settings.remove("api_key")
            
        self.accept()

    @staticmethod
    def get_cfg():
        s = QSettings("QPyPack", "i18nFast")
        api_key = keyring.get_password("QPyPack_i18n", "api_key") or ""
        return {"api_key": api_key, "base_url": s.value("base_url", ""), 
                "model": s.value("model", "deepseek-chat"), "batch_size": int(s.value("batch_size", 30))}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QPyPack i18n Translation Studio - 1.0.1")
        self.resize(1200, 800)
        self.all_keys, self.zh_cn_dict, self.current_data = [], {}, {}
        self.worker = None

        self._setup_ui()
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self._save_file)
        self._load_source()

    def _setup_ui(self):
        toolbar = QToolBar("ToolBar")
        self.addToolBar(toolbar)
        
        self.btn_scan = QPushButton("🔄 刷新源码")
        self.btn_scan.clicked.connect(self._load_source)
        toolbar.addWidget(self.btn_scan)
        toolbar.addSeparator()

        self.lang_combo = QComboBox()
        for k, v in ALL_LANGS.items(): self.lang_combo.addItem(f"{v} ({k})", k)
        self.lang_combo.currentIndexChanged.connect(self._switch_lang)
        toolbar.addWidget(self.lang_combo)

        self.btn_trans = QPushButton("🤖 翻译当前缺失")
        self.btn_trans.clicked.connect(self._translate_missing)
        toolbar.addWidget(self.btn_trans)

        self.btn_save = QPushButton("💾 保存当前")
        self.btn_save.clicked.connect(self._save_file)
        toolbar.addWidget(self.btn_save)
        toolbar.addSeparator()

        self.btn_trans_all = QPushButton("🌐 一键全库补全并保存")
        self.btn_trans_all.setStyleSheet("color: #ffffff; font-weight: bold; background: #2563eb;")
        self.btn_trans_all.clicked.connect(self._translate_all)
        toolbar.addWidget(self.btn_trans_all)
        
        self.btn_save_all = QPushButton("📦 批量清理废弃词条")
        self.btn_save_all.clicked.connect(self._save_all_files)
        toolbar.addWidget(self.btn_save_all)
        toolbar.addSeparator()

        self.btn_cfg = QPushButton("⚙ 设置")
        self.btn_cfg.clicked.connect(lambda: SettingsDialog(self).exec())
        toolbar.addWidget(self.btn_cfg)

        central = QWidget()
        self.setCentralWidget(central)
        lay = QVBoxLayout(central)

        f_lay = QHBoxLayout()
        self.search_box = QLineEdit(); self.search_box.setPlaceholderText("🔍 搜索...")
        self.search_box.textChanged.connect(self._filter_table)
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["全部", "仅缺失", "仅异常"])
        self.filter_combo.currentIndexChanged.connect(self._filter_table)
        self.lbl_stats = QLabel("就绪")
        f_lay.addWidget(self.search_box, 1)
        f_lay.addWidget(self.filter_combo)
        f_lay.addWidget(self.lbl_stats)
        lay.addLayout(f_lay)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Key (源码 / 英文)", "参考 (简体中文)", "译文 (双击编辑)"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 350); self.table.setColumnWidth(1, 300)
        self.table.setStyleSheet("QTableWidget::item { padding: 4px; font-size: 13px; }")
        self.table.itemChanged.connect(self._on_item_changed)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._ctx_menu)
        lay.addWidget(self.table)

        self.progress = QProgressBar(); self.progress.hide()
        lay.addWidget(self.progress)
        self.statusBar = QStatusBar(); self.setStatusBar(self.statusBar)

    def _load_source(self):
        self.all_keys, self.zh_cn_dict = extract_keys_and_zh_cn(MAIN_PY)
        if self.lang_combo.count() > 0: self._switch_lang()

    def _switch_lang(self):
        if self.worker and self.worker.isRunning(): self.worker.cancel_flag = True
        
        code = self.lang_combo.currentData()
        file_path = LOCALES_DIR / f"{code}.json"
        self.current_data = json.loads(file_path.read_text("utf-8")) if file_path.exists() else {}
        
        for k in self.all_keys:
            if k not in self.current_data and is_technical(k):
                self.current_data[k] = k

        self._render_table()

    def _render_table(self):
        self.table.blockSignals(True)
        self.table.setRowCount(len(self.all_keys))
        for row, k in enumerate(self.all_keys):
            it_k = QTableWidgetItem(k); it_k.setFlags(it_k.flags() & ~Qt.ItemFlag.ItemIsEditable)
            it_zh = QTableWidgetItem(self.zh_cn_dict.get(k, "")); it_zh.setFlags(it_zh.flags() & ~Qt.ItemFlag.ItemIsEditable); it_zh.setForeground(QColor("#6b7280"))
            it_tr = QTableWidgetItem(self.current_data.get(k, ""))
            
            self.table.setItem(row, 0, it_k)
            self.table.setItem(row, 1, it_zh)
            self.table.setItem(row, 2, it_tr)
            self._validate_row(row, k, it_tr.text())
            
        self.table.blockSignals(False)
        self._filter_table()

    def _on_item_changed(self, item):
        if item.column() != 2: return
        row = item.row()
        key = self.table.item(row, 0).text()
        val = item.text().strip()
        self.current_data[key] = val
        self._validate_row(row, key, val)
        self._update_stats()

    def _validate_row(self, row, key, val):
        item = self.table.item(row, 2)
        if not val:
            item.setBackground(QColor("#fee2e2")) # Missing: Red
            item.setToolTip("缺失")
        else:
            err = validate_placeholders(key, val)
            if err:
                item.setBackground(QColor("#fef08a")) # Error: Orange
                item.setToolTip(err)
            else:
                item.setBackground(QColor("#dcfce3")) # OK: Green
                item.setToolTip("✓")

    def _filter_table(self):
        query = self.search_box.text().lower()
        mode = self.filter_combo.currentIndex()
        
        for r in range(self.table.rowCount()):
            k = self.table.item(r, 0).text().lower()
            zh = self.table.item(r, 1).text().lower()
            tr = self.table.item(r, 2).text().lower()
            
            is_match = (query in k or query in zh or query in tr)
            
            if mode == 1: # Missing
                is_match = is_match and not tr
            elif mode == 2: # Error
                is_match = is_match and bool(tr) and validate_placeholders(self.table.item(r,0).text(), self.table.item(r,2).text())
                
            self.table.setRowHidden(r, not is_match)
        self._update_stats()

    def _update_stats(self):
        missing = sum(1 for k in self.all_keys if not self.current_data.get(k))
        self.lbl_stats.setText(f"总计: {len(self.all_keys)} | 缺失: {missing}")

    def _ctx_menu(self, pos):
        if not self.table.itemAt(pos): return
        row = self.table.itemAt(pos).row()
        key = self.table.item(row, 0).text()
        menu = QMenu()
        menu.addAction("🤖 AI 翻译此词条").triggered.connect(lambda: self._start_trans([key]))
        menu.addAction("🗑️ 清空此词条").triggered.connect(lambda: self.table.item(row, 2).setText(""))
        menu.exec(self.table.viewport().mapToGlobal(pos))

    def _translate_missing(self):
        keys = [k for k in self.all_keys if not self.current_data.get(k)]
        if not keys: return QMessageBox.information(self, "完成", "无需补充翻译！")
        self._start_trans(keys)

    def _start_trans(self, keys: list):
        cfg = SettingsDialog.get_cfg()
        if not cfg["api_key"]: return SettingsDialog(self).exec()
        
        self.progress.show(); self.progress.setMaximum(len(keys)); self.progress.setValue(0)
        self._set_ui_locked(True)
        
        lang_name = ALL_LANGS.get(self.lang_combo.currentData(), "")
        self.worker = TranslationWorker(cfg, lang_name, keys)
        self.worker.progress.connect(lambda c, t: self.progress.setValue(c))
        self.worker.batch_done.connect(self._on_batch_done)
        self.worker.finished_all.connect(self._on_trans_finish)
        self.worker.start()

    def _on_batch_done(self, result_dict: dict):
        self.table.blockSignals(True)
        for k, v in result_dict.items():
            self.current_data[k] = v
            for r in range(self.table.rowCount()):
                if self.table.item(r, 0).text() == k:
                    self.table.item(r, 2).setText(v)
                    self._validate_row(r, k, v)
                    break
        self.table.blockSignals(False)
        self._update_stats()

    def _on_trans_finish(self):
        self.progress.hide()
        self._set_ui_locked(False)
        self.statusBar.showMessage("✅ 当前语言翻译任务完成！", 5000)

    def _translate_all(self):
        cfg = SettingsDialog.get_cfg()
        if not cfg["api_key"]: return SettingsDialog(self).exec()

        ret = QMessageBox.question(self, "确认", "是否立即遍历补全剩余 15 种语言的缺失词条？（完成后自动保存）")
        if ret != QMessageBox.StandardButton.Yes: return

        self._save_file()
        safe_write_json(LOCALES_DIR / "zh_CN.json", {k: self.zh_cn_dict.get(k, k) for k in self.all_keys})

        self.progress.show(); self.progress.setValue(0)
        self._set_ui_locked(True)

        self.worker = MultiLangWorker(cfg, self.all_keys)
        self.worker.progress.connect(self._on_multi_progress)
        self.worker.finished_all.connect(self._on_multi_finish)
        self.worker.start()

    def _on_multi_progress(self, current, total, text):
        self.progress.setMaximum(total)
        self.progress.setValue(current)
        self.statusBar.showMessage(f"⏳ {text} ({current}/{total})")

    def _on_multi_finish(self):
        self.progress.hide()
        self._set_ui_locked(False)
        self.statusBar.showMessage("🌐 全库补全及保存已全部完成！", 8000)
        self._switch_lang()

    def _save_file(self):
        code = self.lang_combo.currentData()
        safe_write_json(LOCALES_DIR / f"{code}.json", {k: self.current_data[k] for k in self.all_keys if self.current_data.get(k)})
        self.statusBar.showMessage(f"✅ {code}.json 保存成功", 3000)

    def _save_all_files(self):
        self._save_file()
        safe_write_json(LOCALES_DIR / "zh_CN.json", {k: self.zh_cn_dict.get(k, k) for k in self.all_keys})
        
        count = 0
        for code in ALL_LANGS:
            if code == "zh_CN": continue
            p = LOCALES_DIR / f"{code}.json"
            if p.exists():
                data = json.loads(p.read_text("utf-8"))
                clean = {k: v for k, v in data.items() if k in self.all_keys}
                if len(clean) != len(data): 
                    safe_write_json(p, clean)
                    count += 1
        self.statusBar.showMessage(f"📦 已清理并更新了 {count} 个语言文件的废弃词条！", 5000)

    def _set_ui_locked(self, locked: bool):
        self.btn_trans.setEnabled(not locked)
        self.btn_trans_all.setEnabled(not locked)
        self.btn_save.setEnabled(not locked)
        self.btn_save_all.setEnabled(not locked)
        self.lang_combo.setEnabled(not locked)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
