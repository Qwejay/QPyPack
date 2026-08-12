import sys
import json
import re
import time
from pathlib import Path
import ast

try:
    import keyring
except ImportError:
    print("[ERROR] 请先安装 keyring 库: pip install keyring")
    sys.exit(1)

try:
    import openai
except ImportError:
    print("[ERROR] 请先安装 openai 库: pip install openai")
    sys.exit(1)

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QLabel,
    QComboBox, QLineEdit, QProgressBar, QStatusBar, QDialog, QFrame,
    QFormLayout, QMessageBox, QMenu, QSpinBox
)
from PySide6.QtCore import Qt, QThread, Signal, QSettings
from PySide6.QtGui import QColor, QKeySequence, QShortcut, QCloseEvent, QFont

BASE_DIR = Path(__file__).parent.resolve()
MAIN_PY = BASE_DIR / "main.py"
LOCALES_DIR = BASE_DIR / "locales"

ALL_LANGS = {
    "zh_CN": "简体中文", "zh_TW": "繁體中文", "ja_JP": "日本語", "ko_KR": "한국어",
    "de_DE": "Deutsch", "fr_FR": "Français", "es_ES": "Español", "ru_RU": "Русский",
    "pt_BR": "Português (Brasil)", "it_IT": "Italiano", "nl_NL": "Nederlands",
    "pl_PL": "Polski", "tr_TR": "Türkçe", "vi_VN": "Tiếng Việt", "th_TH": "ไทย", "ar_SA": "阿拉伯语"
}

LANG_TARGET_NAMES = {
    "zh_CN": "Simplified Chinese", "zh_TW": "Traditional Chinese", "ja_JP": "Japanese",
    "ko_KR": "Korean", "de_DE": "German", "fr_FR": "French", "es_ES": "Spanish",
    "ru_RU": "Russian", "pt_BR": "Portuguese (Brazil)", "it_IT": "Italian",
    "nl_NL": "Dutch", "pl_PL": "Polish", "tr_TR": "Turkish", "vi_VN": "Vietnamese",
    "th_TH": "Thai", "ar_SA": "Arabic"
}

HANZI_LANGS = ("ja_JP", "zh_TW")

SIMPLIFIED_ONLY = set(
    "设门见东长时电话语说读书图网页击关闭应变换转载输编辑码软复选择确认继续结构"
    "权环约风险级类项组键库释译验证签线缓进赖败强议拟统检测单显优层该络驱动盘备"
    "贴终圆锁连执务请带过还这为们么样对题问试华钱银铁简觉卖买贝员观计让记论访详"
    "间闻济脑际专业临节钟钥纸录归荐灵鲜齐团�区医压厂历县双发变叠"
)

def _has_han(text: str) -> bool:
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def _has_kana(text: str) -> bool:
    return bool(re.search(r'[\u3040-\u30ff]', text))

def is_wrong_language(key: str, val: str, lang_code: str, zh_cn_dict: dict) -> bool:
    """
    判断一条译文是否是错误语言(混入了中文)。
    - 非中日繁语言(阿拉伯/法/西/俄/韩...): 出现任何汉字即判错。
    - 日文/繁体: 仅当命中简体专属字符, 或与简体原文完全相同时判错。
      合法的日文汉字词(出力先/保存/環境変数等)永不误杀。
    """
    if not val or lang_code == "zh_CN":
        return False

    if lang_code not in HANZI_LANGS:
        return _has_han(val)

    if not _has_han(val):
        return False

    if any(ch in SIMPLIFIED_ONLY for ch in val):
        return True

    zh_ref = zh_cn_dict.get(key, "").strip()
    if zh_ref and val.strip() == zh_ref:
        return True

    if lang_code == "ja_JP" and "，" in val and not _has_kana(val):
        return True

    return False

def is_technical(text: str) -> bool:
    if not text: return False
    exact = {'pypi', 'pip', 'pyinstaller', 'nuitka', 'venv', 'conda', 'wheel',
             'qpypack', 'github', 'ui', 'gui', 'api', 'url', 'ast', 'ok'}
    val = text.strip().lower()
    if val in exact: return True
    if re.match(r'^v?[\d]+\.[\d.]+(-\w+)?$', val): return True
    if re.match(r'^https?://\S+$', val): return True
    if re.match(r'^\{[a-zA-Z0-9_]+\}$', val): return True
    return False

def enforce_format(original: str, translated: str) -> str:
    if not translated: return ""
    s = str(translated).strip()
    tag = re.match(r'^(\[[A-Za-z\s]+\])', original)
    if tag:
        s = re.sub(r'^\[.*?\]\s*', '', s).strip()
        s = f"{tag.group(1)} {s}"
    if original.endswith("...") and not s.endswith("..."):
        s += "..."
    elif original.endswith(":") and not s.endswith(":"):
        s += ":"
    return s

def clean_llm_json(raw: str) -> dict:
    s = re.sub(r'^```json\s*|^```\s*|```$', '', raw.strip(), flags=re.I | re.M).strip()
    try:
        return json.loads(s)
    except Exception:
        a, b = s.find('{'), s.rfind('}')
        if a != -1 and b != -1:
            try: return json.loads(s[a:b + 1])
            except Exception: pass
        return {}

def extract_value(v) -> str:
    if isinstance(v, str): return v.strip()
    if isinstance(v, dict):
        for k in ("translation", "translated", "target", "text"):
            if k in v and isinstance(v[k], str): return v[k].strip()
        for x in v.values():
            if isinstance(x, str): return x.strip()
        if v: return str(list(v.values())[0]).strip()
    return str(v).strip()

def write_json(path: Path, data: dict):
    LOCALES_DIR.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    try:
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.replace(path)
    except Exception as e:
        if tmp.exists(): tmp.unlink()
        raise e

def load_lang(code: str) -> dict:
    p = LOCALES_DIR / f"{code}.json"
    if not p.exists(): return {}
    try:
        raw = json.loads(p.read_text("utf-8"))
        return {k: str(v).strip() for k, v in raw.items() if str(v).strip()}
    except Exception:
        return {}

def extract_keys(py_path: Path) -> tuple[list, dict]:
    if not py_path.exists(): return [], {}
    tree = ast.parse(py_path.read_text(encoding="utf-8"))
    keys, zh = set(), {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "ZH_CN_DICT" and isinstance(node.value, ast.Dict):
                    for k, v in zip(node.value.keys, node.value.values):
                        if isinstance(getattr(k, 'value', None), str):
                            keys.add(k.value)
                            if isinstance(getattr(v, 'value', None), str):
                                zh[k.value] = v.value
        if isinstance(node, ast.Call):
            f = node.func
            if (isinstance(f, ast.Name) and f.id in ("_", "t")) or \
               (isinstance(f, ast.Attribute) and f.attr in ("t", "_")):
                if node.args and isinstance(getattr(node.args[0], 'value', None), str):
                    keys.add(node.args[0].value)
    return sorted(keys), zh

def patch_zh_dict(py_path: Path, pairs: dict) -> bool:
    if not py_path.exists() or not pairs: return False
    lines = py_path.read_text(encoding="utf-8").splitlines()
    idx = next((i for i, ln in enumerate(lines)
                if re.search(r'["\']Unknown["\']\s*:\s*["\']未知["\']', ln)), -1)
    if idx == -1: return False
    if idx > 0 and lines[idx - 1].strip() and not lines[idx - 1].rstrip().endswith((',', '{')):
        lines[idx - 1] = lines[idx - 1].rstrip() + ','
    new = [f"    {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},"
           for k, v in pairs.items()]
    lines[idx:idx] = new
    tmp = py_path.with_suffix('.py.tmp')
    try:
        tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")
        tmp.replace(py_path)
        return True
    except Exception as e:
        if tmp.exists(): tmp.unlink()
        raise e

class BaseWorker(QThread):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.cancel = False
        self.client = openai.OpenAI(api_key=cfg["api_key"], base_url=cfg.get("base_url") or None)

    def _call(self, sys_prompt: str, payload: dict) -> dict:
        for i in range(3):
            if self.cancel: return {}
            try:
                r = self.client.chat.completions.create(
                    model=self.cfg["model"],
                    messages=[{"role": "system", "content": sys_prompt},
                              {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
                    temperature=0.1, response_format={"type": "json_object"}, timeout=60)
                if self.cancel: return {}
                p = clean_llm_json(r.choices[0].message.content)
                if len(p) == 1 and isinstance(list(p.values())[0], dict):
                    p = list(p.values())[0]
                return p
            except Exception:
                if self.cancel: return {}
                time.sleep(2 ** i)
        return {}

    @staticmethod
    def _prompt(code: str) -> str:
        target = LANG_TARGET_NAMES.get(code, "English")
        lines = [
            "You are a professional software localization expert.",
            f"Translate the given English UI strings into {target}.",
            "Output ONLY a flat JSON object mapping the exact input IDs to translated strings.",
            "Keep placeholders like {count}, {pkgs}, {path} EXACTLY unchanged.",
        ]
        if code == "zh_TW":
            lines.append("Output Traditional Chinese (繁體中文) ONLY. NEVER output Simplified Chinese characters.")
        elif code == "ja_JP":
            lines.append("Output natural Japanese ONLY. NEVER output Simplified Chinese characters.")
        elif code == "ko_KR":
            lines.append("Output Korean (한글) ONLY. Do NOT use any Chinese characters.")
        elif code != "zh_CN":
            lines.append(f"Output {target} ONLY. Do NOT output any Chinese characters.")
        return "\n".join(lines)

    def translate_batch(self, keys: list, code: str, zh: dict) -> dict:
        """请求 -> 质检 -> 重试 -> 丢弃 的闭环。只有通过质检的译文才返回。"""
        pending = list(keys)
        out = {}
        target = LANG_TARGET_NAMES.get(code, code)
        base = self._prompt(code)

        for attempt in range(3):
            if not pending or self.cancel: break
            prompt = base
            if attempt > 0:
                prompt += (f"\n\nCRITICAL: Your last output contained WRONG language "
                           f"(Chinese characters). Translate STRICTLY into {target}. "
                           f"Absolutely NO Simplified Chinese characters allowed.")
            payload = {str(i): k for i, k in enumerate(pending)}
            idmap = {str(i): k for i, k in enumerate(pending)}
            raw = self._call(prompt, payload)
            if self.cancel: break

            rest = []
            for sid, key in idmap.items():
                v = raw.get(sid)
                if v is None:
                    rest.append(key); continue
                val = enforce_format(key, extract_value(v))
                if val and not is_wrong_language(key, val, code, zh):
                    out[key] = val
                else:
                    rest.append(key)
            pending = rest

        if pending:
            print(f"[{code}] {len(pending)} 条译文质检失败, 已丢弃保持空缺(绝不写入错误内容)。")
        return out


class SingleWorker(BaseWorker):
    progress = Signal(int, int)
    batch_done = Signal(dict)
    done = Signal()

    def __init__(self, cfg, code, keys, zh):
        super().__init__(cfg)
        self.code, self.keys, self.zh = code, keys, zh

    def run(self):
        bs = self.cfg["batch_size"]
        for i in range(0, len(self.keys), bs):
            if self.cancel: break
            res = self.translate_batch(self.keys[i:i + bs], self.code, self.zh)
            if self.cancel: break
            self.batch_done.emit(res)
            self.progress.emit(min(i + bs, len(self.keys)), len(self.keys))
        self.done.emit()


class AllWorker(BaseWorker):
    progress = Signal(int, int, str)
    done = Signal()

    def __init__(self, cfg, all_keys, zh):
        super().__init__(cfg)
        self.all_keys, self.zh = all_keys, zh

    def run(self):
        bs = self.cfg["batch_size"]
        targets = [c for c in ALL_LANGS if c != "zh_CN"]
        for idx, code in enumerate(targets):
            if self.cancel: break
            self.progress.emit(idx, len(targets), f"处理: {ALL_LANGS[code]} ({code})")
            data = load_lang(code)
            missing = [k for k in self.all_keys if not is_technical(k) and not data.get(k)]
            for i in range(0, len(missing), bs):
                if self.cancel: break
                data.update(self.translate_batch(missing[i:i + bs], code, self.zh))
            if not self.cancel:
                for k in self.all_keys:
                    if is_technical(k): data[k] = k
                write_json(LOCALES_DIR / f"{code}.json",
                           {k: data[k] for k in self.all_keys if k in data})
        self.progress.emit(len(targets), len(targets), "全库补全完成！")
        self.done.emit()


class ZhWorker(BaseWorker):
    finished_sig = Signal(bool, int, str)

    def __init__(self, cfg, keys):
        super().__init__(cfg)
        self.keys = keys

    def run(self):
        bs = self.cfg["batch_size"]
        pairs = {}
        prompt = ("Translate the English UI strings to Simplified Chinese (简体中文). "
                  "Keep placeholders like {count} unchanged. Output ONLY a flat JSON object.")
        for i in range(0, len(self.keys), bs):
            if self.cancel: break
            batch = self.keys[i:i + bs]
            raw = self._call(prompt, {str(j): k for j, k in enumerate(batch)})
            idmap = {str(j): k for j, k in enumerate(batch)}
            for sid, key in idmap.items():
                if sid in raw:
                    val = enforce_format(key, extract_value(raw[sid]))
                    if val: pairs[key] = val
        if self.cancel: return
        if pairs:
            try:
                ok = patch_zh_dict(MAIN_PY, pairs)
                self.finished_sig.emit(ok, len(pairs),
                                       "" if ok else "未能在 main.py 找到锚点 'Unknown':'未知'")
            except Exception as e:
                self.finished_sig.emit(False, 0, str(e))
        else:
            self.finished_sig.emit(False, 0, "AI 未返回有效数据")

ACCENT, ACCENT_D = "#6366f1", "#4f46e5"
DANGER, DANGER_D = "#ef4444", "#dc2626"
SUCCESS = "#10b981"

QSS = f"""
QMainWindow, QWidget#Root {{ background:#f1f5f9; }}
QFrame#Header {{ background:#fff; border-bottom:1px solid #e2e8f0; }}
QLabel#Title {{ font-size:18px; font-weight:800; color:#0f172a; }}
QLabel#Sub {{ font-size:11px; color:#94a3b8; }}
QFrame#Card {{ background:#fff; border:1px solid #e2e8f0; border-radius:12px; }}
QComboBox {{ background:#fff; color:#0f172a; border:1px solid #cbd5e1; border-radius:8px;
    padding:7px 12px; font-size:13px; min-height:20px; }}
QComboBox:hover {{ border-color:{ACCENT}; }}
QComboBox::drop-down {{ border:none; width:24px; }}
QComboBox QAbstractItemView {{ background:#fff; border:1px solid #e2e8f0; border-radius:8px;
    selection-background-color:#eef2ff; selection-color:{ACCENT_D}; padding:4px; outline:none; }}
QComboBox#Lang {{ font-size:14px; font-weight:700; min-width:220px; }}
QLineEdit {{ background:#fff; color:#0f172a; border:1px solid #cbd5e1; border-radius:8px;
    padding:7px 12px; font-size:13px; selection-background-color:{ACCENT}; selection-color:#fff; }}
QLineEdit:focus {{ border:1px solid {ACCENT}; }}
QPushButton {{ background:#fff; color:#334155; border:1px solid #cbd5e1; border-radius:8px;
    padding:8px 14px; font-size:13px; font-weight:600; }}
QPushButton:hover {{ background:#f8fafc; border-color:#94a3b8; }}
QPushButton:disabled {{ color:#cbd5e1; background:#f8fafc; border-color:#e2e8f0; }}
QPushButton#Primary {{ background:{ACCENT}; color:#fff; border:none; }}
QPushButton#Primary:hover {{ background:{ACCENT_D}; }}
QPushButton#Primary:disabled {{ background:#c7d2fe; }}
QPushButton#Danger {{ background:#fff; color:{DANGER_D}; border:1px solid #fecaca; }}
QPushButton#Danger:hover {{ background:#fef2f2; border-color:{DANGER}; }}
QPushButton#Stop {{ background:{DANGER}; color:#fff; border:none; }}
QPushButton#Stop:hover {{ background:{DANGER_D}; }}
QPushButton#Stop:disabled {{ background:#fca5a5; }}
QPushButton#Success {{ background:#fff; color:#047857; border:1px solid #a7f3d0; }}
QPushButton#Success:hover {{ background:#ecfdf5; border-color:{SUCCESS}; }}
QTableWidget {{ background:#fff; border:1px solid #e2e8f0; border-radius:12px;
    gridline-color:#f1f5f9; outline:none; }}
QTableWidget::item {{ padding:6px 10px; border-bottom:1px solid #f1f5f9; }}
QTableWidget::item:selected {{ background:#eef2ff; color:#0f172a; }}
QHeaderView::section {{ background:#f8fafc; color:#475569; font-size:12px; font-weight:700;
    padding:10px; border:none; border-bottom:2px solid #e2e8f0; }}
QTableWidget QLineEdit {{ border:2px solid {ACCENT}; border-radius:4px; padding:2px 6px; }}
QProgressBar {{ background:#e2e8f0; border:none; border-radius:6px; height:8px; font-size:0px; }}
QProgressBar::chunk {{ background:{ACCENT}; border-radius:6px; }}
QStatusBar {{ background:#fff; color:#64748b; border-top:1px solid #e2e8f0; font-size:12px; }}
QStatusBar::item {{ border:none; }}
QScrollBar:vertical {{ background:transparent; width:10px; margin:2px; }}
QScrollBar::handle:vertical {{ background:#cbd5e1; border-radius:5px; min-height:30px; }}
QScrollBar::handle:vertical:hover {{ background:#94a3b8; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height:0; }}
QMenu {{ background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:5px; }}
QMenu::item {{ padding:7px 18px; border-radius:6px; font-size:13px; color:#334155; }}
QMenu::item:selected {{ background:#eef2ff; color:{ACCENT_D}; }}
"""

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("API 设置")
        self.setMinimumWidth(460)
        self.setStyleSheet(QSS + "QDialog{background:#fff;} QLabel{font-size:13px;color:#334155;font-weight:600;}")
        self.s = QSettings("QPyPack", "i18nFast")
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24); root.setSpacing(16)
        t = QLabel("⚙  翻译服务配置")
        t.setStyleSheet("font-size:16px;font-weight:800;color:#0f172a;")
        root.addWidget(t)
        form = QFormLayout(); form.setSpacing(12)
        self.key = QLineEdit(keyring.get_password("QPyPack_i18n", "api_key") or "")
        self.key.setEchoMode(QLineEdit.EchoMode.Password); self.key.setPlaceholderText("sk-...")
        self.url = QLineEdit(self.s.value("base_url", "https://api.deepseek.com"))
        self.mod = QLineEdit(self.s.value("model", "deepseek-chat"))
        self.bs = QSpinBox(); self.bs.setRange(5, 100)
        self.bs.setValue(int(self.s.value("batch_size", 20)))
        self.bs.setStyleSheet("QSpinBox{border:1px solid #cbd5e1;border-radius:8px;padding:6px 10px;font-size:13px;}")
        form.addRow("API Key", self.key); form.addRow("Base URL", self.url)
        form.addRow("Model", self.mod); form.addRow("批次大小", self.bs)
        root.addLayout(form)
        row = QHBoxLayout(); row.addStretch()
        c = QPushButton("取消"); c.clicked.connect(self.reject)
        sv = QPushButton("保存"); sv.setObjectName("Primary"); sv.clicked.connect(self.save)
        row.addWidget(c); row.addWidget(sv)
        root.addLayout(row)

    def save(self):
        k = self.key.text().strip()
        if k: keyring.set_password("QPyPack_i18n", "api_key", k)
        else:
            try: keyring.delete_password("QPyPack_i18n", "api_key")
            except: pass
        self.s.setValue("base_url", self.url.text().strip())
        self.s.setValue("model", self.mod.text().strip())
        self.s.setValue("batch_size", self.bs.value())
        self.accept()

    @staticmethod
    def cfg():
        s = QSettings("QPyPack", "i18nFast")
        return {"api_key": keyring.get_password("QPyPack_i18n", "api_key") or "",
                "base_url": s.value("base_url", ""),
                "model": s.value("model", "deepseek-chat"),
                "batch_size": int(s.value("batch_size", 20))}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QPyPack i18n Studio")
        self.resize(1480, 860)
        self.setStyleSheet(QSS)
        self.all_keys, self.zh_dict, self.data, self.unmapped = [], {}, {}, []
        self.worker = None
        self.zh_worker = None
        self._ui()
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self._save)
        self._load()

    def _btn(self, text, slot, obj="", tip=""):
        b = QPushButton(text)
        if obj: b.setObjectName(obj)
        if tip: b.setToolTip(tip)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.clicked.connect(slot)
        return b

    def _badge(self, text, color, bg):
        l = QLabel(text)
        l.setStyleSheet(f"QLabel{{background:{bg};color:{color};font-size:12px;font-weight:700;padding:4px 12px;border-radius:12px;}}")
        return l

    def _ui(self):
        root = QWidget(); root.setObjectName("Root")
        self.setCentralWidget(root)
        outer = QVBoxLayout(root); outer.setContentsMargins(0, 0, 0, 0); outer.setSpacing(0)

        header = QFrame(); header.setObjectName("Header"); header.setFixedHeight(64)
        h = QHBoxLayout(header); h.setContentsMargins(24, 0, 24, 0); h.setSpacing(14)
        logo = QLabel("🌐"); logo.setStyleSheet("font-size:26px;")
        tb = QVBoxLayout(); tb.setSpacing(0)
        t1 = QLabel("i18n Translation Studio"); t1.setObjectName("Title")
        t2 = QLabel("QPyPack 多语言智能翻译工作台"); t2.setObjectName("Sub")
        tb.addWidget(t1); tb.addWidget(t2)
        h.addWidget(logo); h.addLayout(tb); h.addSpacing(20)
        h.addWidget(self._label("当前语言"))
        self.lang = QComboBox(); self.lang.setObjectName("Lang")
        for k, v in ALL_LANGS.items(): self.lang.addItem(f"{v}  ·  {k}", k)
        self.lang.currentIndexChanged.connect(self._switch)
        h.addWidget(self.lang); h.addStretch()
        self.bg_total = self._badge("总计 0", "#475569", "#f1f5f9")
        self.bg_miss = self._badge("缺失 0", "#b45309", "#fef3c7")
        self.bg_leak = self._badge("残留 0", DANGER_D, "#fee2e2")
        h.addWidget(self.bg_total); h.addWidget(self.bg_miss); h.addWidget(self.bg_leak)
        h.addSpacing(6)
        self.b_cfg = self._btn("⚙  设置", lambda: SettingsDialog(self).exec())
        h.addWidget(self.b_cfg)
        outer.addWidget(header)

        bar = QFrame(); bar.setStyleSheet("QFrame{background:#fff;border-bottom:1px solid #e2e8f0;}")
        b = QHBoxLayout(bar); b.setContentsMargins(24, 12, 24, 12); b.setSpacing(10)
        self.b_trans = self._btn("🤖  翻译当前缺失", self._trans_missing, "Primary")
        self.b_all = self._btn("🌐  全库补全并保存", self._trans_all, "Primary")
        self.b_re = self._btn("🔥  重译当前语言", self._retrans, "Danger")
        self.b_stop = self._btn("🛑  停止", self._cancel, "Stop"); self.b_stop.setEnabled(False)
        b.addWidget(self.b_trans); b.addWidget(self.b_all); b.addWidget(self.b_re); b.addWidget(self.b_stop)
        sep = QFrame(); sep.setFixedWidth(1); sep.setStyleSheet("background:#e2e8f0;")
        b.addWidget(sep)
        self.b_clean = self._btn("🧽  清理错误残留", self._clean, "Danger",
                                 "字符级精准清除混入的简体中文，绝不误杀日文汉字")
        self.b_patch = self._btn("✨  补全主程序中文", self._patch, "Success")
        b.addWidget(self.b_clean); b.addWidget(self.b_patch); b.addStretch()
        self.b_scan = self._btn("🔄  刷新源码", self._load)
        self.b_save = self._btn("💾  保存当前", self._save)
        self.b_saveall = self._btn("📦  批量清理保存", self._save_all)
        self.b_fix = self._btn("🧹  规范化标签", self._fix_tags)
        for x in (self.b_scan, self.b_save, self.b_saveall, self.b_fix): b.addWidget(x)
        outer.addWidget(bar)

        body = QWidget(); bl = QVBoxLayout(body)
        bl.setContentsMargins(24, 18, 24, 12); bl.setSpacing(14)
        filt = QFrame(); filt.setObjectName("Card")
        fl = QHBoxLayout(filt); fl.setContentsMargins(14, 10, 14, 10); fl.setSpacing(10)
        self.search = QLineEdit(); self.search.setPlaceholderText("🔍  搜索英文 Key / 中文参考 / 译文…")
        self.search.textChanged.connect(self._filter)
        self.fmode = QComboBox(); self.fmode.addItems(["全部条目", "仅缺失", "仅未映射中文", "⚠️ 仅错误语言残留"])
        self.fmode.setFixedWidth(180); self.fmode.currentIndexChanged.connect(self._filter)
        fl.addWidget(self.search, 1); fl.addWidget(self.fmode)
        bl.addWidget(filt)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Key（英文原文）", "参考（简体中文）", "译文（双击编辑）"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 380); self.table.setColumnWidth(1, 300)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(38)
        self.table.setShowGrid(False)
        self.table.itemChanged.connect(self._edited)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._menu)
        bl.addWidget(self.table, 1)
        self.progress = QProgressBar(); self.progress.hide()
        bl.addWidget(self.progress)
        outer.addWidget(body, 1)

        self.status = QStatusBar(); self.setStatusBar(self.status)
        self.status.showMessage("就绪")

    def _label(self, txt):
        l = QLabel(txt); l.setStyleSheet("color:#64748b;font-size:12px;font-weight:600;")
        return l

    def _stop(self):
        for a in ('worker', 'zh_worker'):
            w = getattr(self, a, None)
            if w and w.isRunning():
                w.cancel = True; w.quit(); w.wait(2000)

    def _cancel(self):
        self._stop(); self.progress.hide(); self._lock(False)
        self.status.showMessage("🛑 已取消任务", 5000)

    def closeEvent(self, e: QCloseEvent):
        self._stop(); super().closeEvent(e)

    def _lock(self, locked):
        for x in (self.b_trans, self.b_re, self.b_all, self.b_patch, self.b_save,
                  self.b_saveall, self.b_scan, self.b_fix, self.b_clean, self.b_cfg, self.lang):
            x.setEnabled(not locked)
        self.b_stop.setEnabled(locked)

    def _load(self):
        self._stop()
        self.all_keys, self.zh_dict = extract_keys(MAIN_PY)
        self.unmapped = [k for k in self.all_keys if k not in self.zh_dict and not is_technical(k)]
        if self.lang.count() > 0: self._switch()

    def _switch(self):
        self._stop()
        code = self.lang.currentData()
        self.data = load_lang(code)
        if code == "zh_CN":
            for k in self.all_keys:
                if not self.data.get(k) and k in self.zh_dict:
                    self.data[k] = self.zh_dict[k]
        for k in self.all_keys:
            if k not in self.data and is_technical(k):
                self.data[k] = k
        self._render()

    def _render(self):
        self.table.blockSignals(True)
        self.table.setRowCount(len(self.all_keys))
        for r, k in enumerate(self.all_keys):
            ik = QTableWidgetItem(k)
            ik.setFlags(ik.flags() & ~Qt.ItemFlag.ItemIsEditable)
            ik.setForeground(QColor("#475569"))
            zh = self.zh_dict.get(k, "")
            iz = QTableWidgetItem(zh)
            iz.setFlags(iz.flags() & ~Qt.ItemFlag.ItemIsEditable)
            iz.setForeground(QColor("#dc2626") if not zh else QColor("#64748b"))
            raw = self.data.get(k, "")
            val = enforce_format(k, raw) if raw else ""
            it = QTableWidgetItem(val)
            self.table.setItem(r, 0, ik); self.table.setItem(r, 1, iz); self.table.setItem(r, 2, it)
            self._mark(r, k, val)
        self.table.blockSignals(False)
        self._filter()

    def _edited(self, item):
        if item.column() != 2: return
        r = item.row()
        key = self.table.item(r, 0).text()
        val = enforce_format(key, item.text().strip())
        if val: self.data[key] = val
        else: self.data.pop(key, None)
        self.table.blockSignals(True); item.setText(val); self.table.blockSignals(False)
        self._mark(r, key, val); self._stats()

    def _mark(self, r, key, val):
        it = self.table.item(r, 2)
        code = self.lang.currentData()
        if not val:
            it.setBackground(QColor("#fef2f2")); it.setForeground(QColor("#94a3b8")); it.setToolTip("缺失")
        elif is_wrong_language(key, val, code, self.zh_dict):
            it.setBackground(QColor("#fef9c3")); it.setForeground(QColor("#0f172a"))
            it.setToolTip("警告: 检测到简体中文泄漏！")
        else:
            it.setBackground(QColor("#ffffff")); it.setForeground(QColor("#0f172a")); it.setToolTip("✓ 已翻译")

    def _filter(self):
        q = self.search.text().lower()
        mode = self.fmode.currentIndex()
        code = self.lang.currentData()
        for r in range(self.table.rowCount()):
            k = self.table.item(r, 0).text()
            zh = self.table.item(r, 1).text().lower()
            tr = self.table.item(r, 2).text()
            m = (q in k.lower() or q in zh or q in tr.lower())
            if mode == 1: m = m and not tr
            elif mode == 2: m = m and not zh
            elif mode == 3: m = m and is_wrong_language(k, tr, code, self.zh_dict)
            self.table.setRowHidden(r, not m)
        self._stats()

    def _stats(self):
        code = self.lang.currentData()
        d = load_lang(code)
        if code == "zh_CN":
            for k in self.all_keys:
                if not d.get(k) and k in self.zh_dict:
                    d[k] = self.zh_dict[k]
        miss = sum(1 for k in self.all_keys if not is_technical(k) and not d.get(k))
        leak = sum(1 for k, v in d.items() if is_wrong_language(k, v, code, self.zh_dict))
        self.bg_total.setText(f"总计 {len(self.all_keys)}")
        self.bg_miss.setText(f"缺失 {miss}")
        self.bg_leak.setText(f"残留 {leak}")

    def _menu(self, pos):
        if not self.table.itemAt(pos): return
        r = self.table.itemAt(pos).row()
        key = self.table.item(r, 0).text()
        m = QMenu()
        m.addAction("🤖  AI 翻译此词条").triggered.connect(lambda: self._start([key]))
        m.addAction("🗑️  清空此词条").triggered.connect(lambda: self.table.item(r, 2).setText(""))
        m.exec(self.table.viewport().mapToGlobal(pos))

    def _clean(self):
        msg = ("确定扫描并清除所有语言里的【简体中文泄漏】吗？\n"
               "清除后变为空白，可点击【全库补全并保存】重译。\n\n"
               "判断为字符级物理识别：非中日繁语言含汉字即清除；日文/繁体仅当命中简体专属字符才清除，绝不误杀合法汉字。")
        if QMessageBox.question(self, "确认清理", msg) != QMessageBox.StandardButton.Yes:
            return
        cnt = files = 0
        for code in ALL_LANGS:
            if code == "zh_CN": continue
            p = LOCALES_DIR / f"{code}.json"
            if not p.exists(): continue
            d = load_lang(code)
            clean = {}; dirty = False
            for k, v in d.items():
                if is_wrong_language(k, v, code, self.zh_dict):
                    dirty = True; cnt += 1
                else:
                    clean[k] = v
            if dirty:
                write_json(p, clean); files += 1
        if cnt:
            QMessageBox.information(self, "清理完成",
                                    f"清理了 {files} 个文件中的 {cnt} 处简体泄漏！\n\n请点击【🌐 全库补全并保存】重译。")
            self._switch()
        else:
            QMessageBox.information(self, "检查完毕", "未发现任何简体中文泄漏！")

    def _missing_keys(self):
        code = self.lang.currentData()
        d = load_lang(code)
        if code == "zh_CN":
            for k in self.all_keys:
                if not d.get(k) and k in self.zh_dict:
                    d[k] = self.zh_dict[k]
        return [k for k in self.all_keys if not is_technical(k) and not d.get(k)]

    def _trans_missing(self):
        keys = self._missing_keys()
        if not keys: return QMessageBox.information(self, "完成", "当前语言无缺失翻译！")
        self._start(keys)

    def _retrans(self):
        if QMessageBox.question(self, "确认", "强制重译当前语言全部词条？") == QMessageBox.StandardButton.Yes:
            self._start([k for k in self.all_keys if not is_technical(k)])

    def _start(self, keys):
        cfg = SettingsDialog.cfg()
        if not cfg["api_key"]: return SettingsDialog(self).exec()
        self._stop(); self.progress.show()
        self.progress.setMaximum(len(keys)); self.progress.setValue(0)
        self._lock(True); self.status.showMessage("🤖 正在翻译…")
        self.worker = SingleWorker(cfg, self.lang.currentData(), keys, self.zh_dict)
        self.worker.progress.connect(lambda c, t: self.progress.setValue(c))
        self.worker.batch_done.connect(self._batch)
        self.worker.done.connect(self._trans_fin)
        self.worker.start()

    def _batch(self, res):
        self.table.blockSignals(True)
        for k, v in res.items():
            fv = enforce_format(k, v)
            if not fv: continue
            self.data[k] = fv
            for r in range(self.table.rowCount()):
                if self.table.item(r, 0).text() == k:
                    self.table.item(r, 2).setText(fv); self._mark(r, k, fv); break
        self.table.blockSignals(False)
        self._stats()

    def _trans_fin(self):
        self._save(); self.progress.hide(); self._lock(False)
        self.status.showMessage("✅ 翻译完成并已保存！", 5000)

    def _trans_all(self):
        cfg = SettingsDialog.cfg()
        if not cfg["api_key"]: return SettingsDialog(self).exec()
        if QMessageBox.question(self, "确认", "并发补全全部 15 种语言的缺失词条？\n\n写入前逐条语言质检，任何简体中文都会被拒绝并保持空缺。") != QMessageBox.StandardButton.Yes:
            return
        self._stop(); self.progress.show(); self.progress.setValue(0); self._lock(True)
        self.worker = AllWorker(cfg, self.all_keys, self.zh_dict)
        self.worker.progress.connect(lambda c, t, txt: (self.progress.setMaximum(t), self.progress.setValue(c), self.status.showMessage(txt)))
        self.worker.done.connect(self._all_fin)
        self.worker.start()

    def _all_fin(self):
        self.progress.hide(); self._lock(False)
        self.status.showMessage("🌐 全库补全完成！", 8000)
        self._switch()

    def _patch(self):
        if not self.unmapped: return QMessageBox.information(self, "完美", "所有词条均已有中文映射！")
        cfg = SettingsDialog.cfg()
        if not cfg["api_key"]: return SettingsDialog(self).exec()
        if QMessageBox.question(self, "确认", f"将 {len(self.unmapped)} 条缺失英文翻译为中文并写入 main.py？") != QMessageBox.StandardButton.Yes:
            return
        self._stop(); self.progress.show(); self.progress.setRange(0, 0); self._lock(True)
        self.status.showMessage("✨ 正在补全主程序中文字典…")
        self.zh_worker = ZhWorker(cfg, self.unmapped)
        self.zh_worker.finished_sig.connect(self._patch_fin)
        self.zh_worker.start()

    def _patch_fin(self, ok, cnt, err):
        self.progress.setRange(0, 100); self.progress.hide(); self._lock(False)
        if ok: QMessageBox.information(self, "成功", f"已将 {cnt} 条中文写入 main.py！\n源码已刷新。")
        else: QMessageBox.critical(self, "失败", err)
        self._load()

    def _save(self):
        code = self.lang.currentData()
        out = {}
        for k in self.all_keys:
            if is_technical(k): out[k] = k; continue
            v = self.data.get(k)
            if v: out[k] = enforce_format(k, v)
        write_json(LOCALES_DIR / f"{code}.json", out)
        self.status.showMessage(f"✅ {code}.json 已保存", 3000)

    def _save_all(self):
        self._save()
        zh = load_lang("zh_CN")
        for k in self.all_keys:
            if k in self.zh_dict: zh[k] = enforce_format(k, self.zh_dict[k])
            elif is_technical(k): zh[k] = k
        write_json(LOCALES_DIR / "zh_CN.json", {k: zh[k] for k in self.all_keys if k in zh})
        cnt = 0
        for code in ALL_LANGS:
            if code == "zh_CN": continue
            p = LOCALES_DIR / f"{code}.json"
            if not p.exists(): continue
            d = load_lang(code)
            clean = {}
            for k in self.all_keys:
                if is_technical(k): clean[k] = k
                elif k in d: clean[k] = enforce_format(k, d[k])
            write_json(p, clean); cnt += 1
        self.status.showMessage(f"📦 批量清理并保存了 {cnt} 个语言文件", 5000)

    def _fix_tags(self):
        for code in ALL_LANGS:
            p = LOCALES_DIR / f"{code}.json"
            if not p.exists(): continue
            d = load_lang(code)
            clean = {}
            for k in self.all_keys:
                if code == "zh_CN" and k in self.zh_dict: clean[k] = enforce_format(k, self.zh_dict[k])
                elif is_technical(k): clean[k] = k
                elif k in d: clean[k] = enforce_format(k, d[k])
            write_json(p, clean)
        self.status.showMessage("🧹 规范化了所有文件的日志标签和标点", 5000)
        self._switch()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    f = QFont(); f.setFamilies(["Segoe UI", "Microsoft YaHei", "PingFang SC", "sans-serif"]); f.setPointSize(9)
    app.setFont(f)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
