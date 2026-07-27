import sys
import os
import shutil
import subprocess
import tempfile
import re
import time
import stat
import json
import math
import wave
import struct
import threading
import configparser
import locale
from pathlib import Path

if os.name == 'nt':
    try:
        import winreg
    except ImportError:
        winreg = None
else:
    winreg = None

os.environ["QT_LOGGING_RULES"] = "qt.text.font.db=false;qt.multimedia*=false"

from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
                             QPushButton, QLabel, QLineEdit, QFileDialog, QCheckBox,
                             QComboBox, QFrame, QStackedLayout, QFormLayout, QTextEdit, 
                             QGraphicsOpacityEffect, QGridLayout, QTabWidget,
                             QMessageBox, QInputDialog, QFileIconProvider, QSizePolicy, QScrollArea,
                             QGraphicsDropShadowEffect, QSpinBox, QListWidget, QListWidgetItem,
                             QListView, QStyledItemDelegate, QMenu, QTableWidget, QTableWidgetItem,
                             QHeaderView)
from PySide6.QtCore import (Qt, QThread, Signal, QPropertyAnimation, QEasingCurve, 
                            QParallelAnimationGroup, QFileInfo, QVariantAnimation, 
                            QTimer, QPointF, QRectF, QRect, QSize, QUrl, QLocale, QObject)
from PySide6.QtGui import (QFont, QDragEnterEvent, QDropEvent, QIcon, QPixmap, 
                           QPainter, QColor, QPen, QImage, QImageWriter)
from PySide6.QtSvg import QSvgRenderer

try:
    from PySide6.QtMultimedia import QSoundEffect
    HAS_QT_AUDIO = True
except ImportError:
    HAS_QT_AUDIO = False

__app_name__ = "QPyPack"
__version__ = "2.6.2"
__author__ = "QwejayHuang"
__company__ = "QwejayHuang"
__description__ = "Cross-platform Python Application Packaging Tool"

_CONFIG_DIR = Path.home() / ".qpypack"
_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = (_CONFIG_DIR / "config.ini").as_posix()

ZH_CN_DICT = {
    "Drag & Drop Python script (.py/.pyw) here\nor Click to Browse": "将 Python 脚本 (.py/.pyw) 拖放至此\n或 点击浏览文件",
    "Auto-parse dependencies, resources, and implicit imports": "自动解析依赖、附加资源及隐式导入",
    "Loaded: {filename}": "已载入: {filename}",
    "Parsing metadata...": "正在解析元数据...",
    "Ready, waiting for build.": "就绪，等待构建。",
    "Initializing build...": "初始化构建...",
    "Preparing engine...": "准备引擎...",
    "Build Successful": "构建成功",
    "Open output directory or reset workspace.": "前往输出目录查看，或重置工作区。",
    "Build Failed": "构建失败",
    "Check log output below for troubleshooting.": "请查看下方日志以排查错误。",
    "Status: Ready": " 状态: 准备就绪",
    "Status: Parsing {filename}...": " 状态: 正在解析 {filename}...",
    "Status: Loaded {filename}{mode}": " 状态: 已载入 {filename}{mode}",
    "Status: Packaging ({engine}) ...": " 状态: 构建中 ({engine}) ...",
    "Status: Build Completed": " 状态: 构建完成",
    "Status: Build Failed": " 状态: 构建失败",
    "Status: Workspace Reset": " 状态: 工作区已重置",
    "Start Build": " 开始构建",
    "Stop Build": " 停止构建",
    "Open Directory": " 打开目录",
    "Rebuild": " 重新构建",
    "Save & Return": " 保存并返回",
    "Build Settings": "构建设置",
    "Preferences": "首选项",
    "About": "关于",
    "🚀 Engine": "🚀 构建引擎",
    "📦 Dependencies": "📦 依赖管理",
    "📂 Resources": "📂 附加资源",
    "⚡ Optimization": "⚡ 性能优化",
    "🗺️ Package Map": "🗺️ 包名映射",
    "Engine & Environment": "构建引擎与环境",
    "Execution Mode": "运行模式",
    "Mirrors & Scanner": "镜像源与扫描配置",
    "Additional Resources (Drag & Drop Supported)": "附加资源文件与目录 (支持桌面拖拽)",
    "Performance Optimization": "性能与编译优化",
    "Lock Core Dependencies": "锁定核心依赖版本",
    "Package Name Mappings": "第三方库包名映射表",
    "UI Language:": "界面语言:",
    "App Metadata & Presets": "应用元数据与工程预设",
    "Output Location": "构建产物输出位置",
    "Preferences & System Behavior": "构建偏好与系统行为",
    "Build Engine:": "构建引擎:",
    "Python Interpreter:": "Python 解释器:",
    "Output Name:": "输出名称:",
    "App Icon:": "程序图标:",
    "Primary PIP Index:": "PIP 主镜像源:",
    "Backup PIP Index:": "PIP 备用源:",
    "Requirements File:": "依赖清单 (requirements):",
    "Hidden Imports:": "隐式导入 (Hidden Imports):",
    "Exclude Modules:": "排除模块 (Excludes):",
    "CPU Cores:": "编译并发核心数:",
    "UPX Path:": "UPX 路径:",
    "PyInstaller Version:": "PyInstaller 版本:",
    "Nuitka Version:": "Nuitka 版本:",
    "Pipreqs Version:": "Pipreqs 版本:",
    "Version:": "版本号:",
    "Author/Company:": "开发者/公司:",
    "Description:": "程序描述:",
    "Output Rule:": "输出规则:",
    "Target Directory:": "目标目录:",
    "One-File Mode (--onefile)": "单文件模式 (--onefile)",
    "Hide Console (--noconsole)": "隐藏控制台 (--noconsole)",
    "Use Virtual Environment (Recommended)": "使用独立虚拟环境 (推荐)",
    "Install requirements.txt": "安装 requirements.txt",
    "Analyze Dependencies (pipreqs)": "自动分析依赖 (pipreqs)",
    "Scan Entire Folder": "扫描整个所在目录",
    "Enable UPX Compression": "启用 UPX 压缩",
    "Lite Mode (Exclude Dev/Test Dependencies)": "精简模式 (排除开发/测试依赖)",
    "Concise Log Output": "精简日志输出",
    "Auto-save Build Log": "自动保存构建日志",
    "Auto Extract Icon": "自动提取图标",
    "Clean Temporary Cache After Build": "构建后清理临时缓存",
    "Sound Notification": "构建完成提示音",
    "Browse": "浏览",
    "AST Scan": "AST分析",
    "Add File": "添加文件",
    "Add Dir": "添加目录",
    "Remove Selected": "移除选中",
    "Clear All": "清空",
    "Add Mapping": "添加映射",
    "Restore Defaults": "恢复默认",
    "Export Preset...": "导出预设...",
    "Import Preset...": "导入预设...",
    "Source File Directory": "源文件所在目录",
    "Custom Directory": "自定义目录",
    "Import Name": "代码导入名",
    "PyPI Package Name": "PyPI 包名",
    "Reset to Default Config": "重置为默认配置",
    "Cancel & Return": "放弃修改并返回",
    "Configure Build Settings": "配置构建参数",
    "Toggle Execution Log": "显示/隐藏执行日志",
    "Copy": "复制",
    "Select All": "全选",
    "Clear Log": "清空日志",
    "Export Log...": "导出日志...",
    "A Cross-platform Python Packaging GUI Tool based on PyInstaller & Nuitka": "基于 PyInstaller 和 Nuitka 的 Python 跨平台打包 GUI 工具",
    " [Console]": " [控制台]",
    " [No Console]": " [无控制台]",
    "File": "文件",
    "Directory": "目录",
    "<b>PyInstaller</b>: Fast build speed, excellent compatibility. Ideal for rapid iteration.": "<b>PyInstaller</b>: 构建速度快，兼容性极佳。适合快速迭代与常规应用。",
    "<b>Nuitka</b>: Compiles to native C/C++ binary. Better performance and source code protection.": "<b>Nuitka</b>: 编译为原生 C/C++ 二进制。运行性能更好，且具有源码防反编译保护。",
    "Leave blank to auto-detect system default Python": "留空则自动检测系统默认 Python",
    "Leave blank to auto-match script name": "留空则自动匹配脚本名称",
    "Leave blank to auto-search requirements.txt in current directory": "留空则自动检索当前目录 requirements.txt",
    "Comma separated (e.g. pandas, PyQt5)": "逗号分隔 (如: pandas, PyQt5)",
    "Comma separated (e.g. tkinter, matplotlib)": "逗号分隔 (如: tkinter, matplotlib)",
    "Leave blank to auto-detect from environment variables": "留空则从环境变量自动检测",
    "Dynamically exclude redundant dependencies in build environment, improving speed and reducing size.": "动态排除构建环境冗余依赖，提升构建速度并缩减产物体积。",
    "Double-click to edit target path; Drag & drop supported": "双击修改目标路径；支持直接从桌面拖拽文件或文件夹至此区域",
    "Package mappings have been reset to defaults.": "包名映射已重置为默认值。",
    "Config preset exported to: {path}": "配置预设已导出至: {path}",
    "Config preset imported successfully.": "配置预设已成功导入。",
    "AST scan completed, found {count} dependencies.": "AST 解析完成，共发现 {count} 项依赖。",
    "No log content.": "当前无日志内容。",
    "Log saved to: {path}": "日志已保存至: {path}",
    "Attention: Please check the log for details.": "注意：发生异常，请查看日志详情。",
    "[INFO] Initializing isolated build environment...": "[INFO] 正在初始化隔离构建环境...",
    "[INFO] Python interpreter path: {path}": "[INFO] Python 解释器路径: {path}",
    "[INFO] Creating virtual environment...": "[INFO] 正在创建虚拟环境...",
    "[ERROR] Failed to create virtual environment. Current Python environment might be missing necessary modules or have restricted permissions.": "[ERROR] 虚拟环境创建失败。当前 Python 环境可能缺失必要模块或权限受限。",
    "[INFO] Synchronizing and upgrading pip package manager...": "[INFO] 正在同步并升级 pip 包管理器...",
    "[INFO] Installing build engine [{pkg}] and core compilation dependencies...": "[INFO] 正在安装构建引擎 [{pkg}] 及核心编译依赖...",
    "[INFO] Nuitka Tip: If prompted to download GCC/MinGW compiler on first build, please ensure stable network connection.": "[INFO] Nuitka 提示：若首次构建提示下载 GCC/MinGW 编译器，请保持网络正常。",
    "[INFO] Dependency installation [1/3]: Installing declared dependencies ({filename})...": "[INFO] 依赖安装 [1/3]: 正在安装声明依赖 ({filename})...",
    "[INFO] Dependency installation [2/3]: Calling pipreqs to analyze project dependencies...": "[INFO] 依赖安装 [2/3]: 正在调用 pipreqs 分析项目依赖...",
    "[INFO] Enabled single-file sandbox mode: parsing current script only to prevent pollution from other files.": "[INFO] 已启用单文件沙盒模式：仅对当前脚本解析，防止同目录其他文件污染。",
    "[WARN] Enabled full-directory scan mode: scanning all Python files in the current directory...": "[WARN] 已允许全目录扫描模式：正在扫描当前目录下所有 Python 文件...",
    "[INFO] Dependency analysis service source address: {server}": "[INFO] 依赖分析服务源地址: {server}",
    "[INFO] Querying versions of dependency libraries, please wait...": "[INFO] 正在查询各依赖库的版本，请稍候...",
    "[INFO] Switching to backup PyPI source for retrieval: {url}": "[INFO] 正在切换至备用 PyPI 查询源重新检索: {url}",
    "[INFO] Attempting to scan using compatible encoding...": "[INFO] 正在尝试利用兼容编码进行扫描...",
    "[WARN] pipreqs skipped deep scan, dependencies will be supplemented by AST scanning engine.": "[WARN] pipreqs 已跳过深度扫描，将由 AST 扫描引擎补全依赖。",
    "[INFO] Dependency installation [3/3]: Extracting implicit dependencies via AST static scan...": "[INFO] 依赖安装 [3/3]: 正在通过 AST 静态扫描提取隐式依赖...",
    "[INFO] Parsing and installing implicit import dependencies: {pkgs}": "[INFO] 正在解析并安装隐式导入依赖: {pkgs}",
    "[ERROR] ⚠️ Warning: Failed to install dependency [{pkg}]! May cause runtime crash.": "[ERROR] ⚠️ 警告：依赖库 [{pkg}] 安装失败！可能导致打包后的软件运行时崩溃。",
    "[INFO] Starting {engine} engine to compile binary files...": "[INFO] 正在启动 {engine} 引擎，开始编译二进制文件...",
    "[INFO] Found local MSVC environment, prioritizing native C++ compiler.": "[INFO] 发现本地 MSVC 环境，优先使用原生 C++ 编译器。",
    "[INFO] Lite mode enabled, executing size reduction strategy...": "[INFO] 已开启精简模式，正在执行体积缩减策略...",
    "[WARN] Strongly recommend checking [Virtual Environment] to maximize lite mode effect.": "[WARN] 强烈建议勾选 [虚拟环境] 以最大化精简效果。",
    "[INFO] Enabled Nuitka optimization directives...": "[INFO] 已启用 Nuitka 优化指令...",
    "[INFO] Core compilation completed, extracting and archiving built files...": "[INFO] 编译核心完成，正在提取并归档编译文件...",
    "[ERROR] Product transfer failed, file might be occupied by system process or lack permission: {error}": "[ERROR] 产物移交失败，文件可能被系统进程占用或权限不足: {error}",
    "[ERROR] Could not locate valid executable product in temporary build directory: {path}": "[ERROR] 未在临时构建目录中定位到有效可执行产物: {path}",
    "[INFO] Validating output files and generating final product...": "[INFO] 正在校验输出文件并生成最终产物...",
    "[INFO] Build log exported to: {path}": "[INFO] 编译日志已导出至: {path}",
    "[SUCCESS] Compilation completed, output path: {path}": "[SUCCESS] 编译已完成，输出路径: {path}",
    "[Syntax Error] Source program has syntax or indentation errors!\n  - File: {file}\n  - Type: {type}\n  - Line: near {line}\n  - Desc: {desc}\n\nTip: This is an error in the source code logic. Ensure it runs locally before compiling.": "[语法异常] 源程序存在语法不合规或缩进异常错误！\n  - 错误源文件: {file}\n  - 异常类型: {type}\n  - 异常位置: 第 {line} 行附近\n  - 错误描述: {desc}\n\n提示: 此问题为源码逻辑本身错误。请在确保本地运行无误后，再次执行编译流程。",
    "\n!!!!!!!!!! [Diagnostic Traceback: Full raw log due to execution exception in this step] !!!!!!!!!!": "\n!!!!!!!!!! [诊断回溯: 以下是由于该环节执行异常产生的完整原始日志] !!!!!!!!!!",
    "[FAILED] Compilation interrupted with exceptions, refer to the log for troubleshooting.": "[FAILED] 编译异常中断，请参阅日志以定位排查。",
    "[INFO] Freeing up space, cleaning temporary build environment...": "[INFO] 正在释放空间，清理临时构建环境...",
    "\\nProgram execution completed, press Enter to exit...": "\\n程序执行完毕，按回车键退出...",
    "[ERROR] Target file is locked or encrypted by cloud drive. Please decrypt and try again.": "[ERROR] 目标文件被云盘锁定或加密，请解密后重试。",
    "[ERROR] Please load a valid Python source file first!": "[ERROR] 请先加载有效的 Python 源代码文件！",
    "[ERROR] Exception occurred during AST parsing: {error}": "[ERROR] AST 语法树解析过程中发生异常: {error}",
    "[ERROR] Failed to export preset file: {error}": "[ERROR] 无法导出预设文件: {error}",
    "[ERROR] Preset file format error or corrupted: {error}": "[ERROR] 预设文件格式错误或已被损坏: {error}",
    "[ERROR] Failed to export log file: {error}": "[ERROR] 无法导出日志文件: {error}",
    "[ERROR] Build completed, but the following dependencies failed to install during pre-build:\n\n  👉 {pkgs}\n\n⚠️ Tip: The program might crash at runtime due to missing modules!": "[ERROR] 构建已完成，但预构建阶段以下依赖安装失败：\n\n  👉 {pkgs}\n\n⚠️ 提示：程序运行时可能会因缺少模块导致崩溃！"
}

class TranslationEngine(QObject):
    language_changed = Signal(str)
    DEFAULT_LOCALE = "en_US"

    LANG_META = {
        "en_US": {"native": "English", "flag": "🇺🇸"},
        "zh_CN": {"native": "简体中文", "flag": "🇨🇳"},
        "zh_TW": {"native": "繁體中文", "flag": "🇹🇼"},
        "ja_JP": {"native": "日本語", "flag": "🇯🇵"},
        "ko_KR": {"native": "한국어", "flag": "🇰🇷"},
        "de_DE": {"native": "Deutsch", "flag": "🇩🇪"},
        "fr_FR": {"native": "Français", "flag": "🇫🇷"},
        "es_ES": {"native": "Español", "flag": "🇪🇸"},
        "ru_RU": {"native": "Русский", "flag": "🇷🇺"},
        "pt_BR": {"native": "Português (Brasil)", "flag": "🇧🇷"},
        "it_IT": {"native": "Italiano", "flag": "🇮🇹"},
        "nl_NL": {"native": "Nederlands", "flag": "🇳🇱"},
        "pl_PL": {"native": "Polski", "flag": "🇵🇱"},
        "tr_TR": {"native": "Türkçe", "flag": "🇹🇷"},
        "vi_VN": {"native": "Tiếng Việt", "flag": "🇻🇳"},
        "th_TH": {"native": "ไทย", "flag": "🇹🇭"},
        "ar_SA": {"native": "العربية", "flag": "🇸🇦"},
    }

    def __init__(self, locales_dir: Path):
        super().__init__()
        self.locales_dir = locales_dir
        self.current_lang = self.DEFAULT_LOCALE
        self.translations = {}
        self.fallback_zh_cn = ZH_CN_DICT

    def init_locale(self):
        self.load_all_locales()
        self.current_lang = self.detect_system_language()

    def normalize_locale(self, locale_str: str) -> str:
        if not locale_str or locale_str == "auto":
            return self.detect_system_language()
        clean = locale_str.replace("-", "_")
        parts = clean.split("_")
        if len(parts) >= 2:
            return f"{parts[0].lower()}_{parts[1].upper()}"
        elif len(parts) == 1:
            lang = parts[0].lower()
            mapping = {"zh": "zh_CN", "en": "en_US", "ja": "ja_JP", "ko": "ko_KR", "de": "de_DE", "fr": "fr_FR", "es": "es_ES", "ru": "ru_RU", "pt": "pt_BR"}
            return mapping.get(lang, self.DEFAULT_LOCALE)
        return self.DEFAULT_LOCALE

    def detect_system_language(self) -> str:
        try:
            sys_locale = QLocale.system().name()
        except Exception:
            sys_locale = ""
            
        if sys_locale.startswith("zh"):
            if any(k in sys_locale for k in ("TW", "HK", "MO", "Hant")): return "zh_TW"
            return "zh_CN"
        elif sys_locale.startswith("ja"): return "ja_JP"
        elif sys_locale.startswith("ko"): return "ko_KR"
        elif sys_locale.startswith("de"): return "de_DE"
        elif sys_locale.startswith("fr"): return "fr_FR"
        elif sys_locale.startswith("es"): return "es_ES"
        elif sys_locale.startswith("ru"): return "ru_RU"
        elif sys_locale.startswith("pt"): return "pt_BR"
        return "en_US"

    def load_all_locales(self):
        self.translations.clear()
        if self.locales_dir.exists():
            for p in self.locales_dir.glob("*.json"):
                try:
                    data = json.loads(p.read_text(encoding='utf-8'))
                    code = self.normalize_locale(p.stem)
                    self.translations[code] = data
                except Exception as e:
                    print(f"[i18n] Failed to load {p.name}: {e}")

    def get_available_languages(self) -> dict:
        sys_code = self.detect_system_language()
        if sys_code in self.LANG_META:
            sys_native = self.LANG_META[sys_code]["native"].split(" (")[0]
        else:
            qloc = QLocale(sys_code)
            sys_native = qloc.nativeLanguageName().capitalize() or sys_code

        langs = {"auto": f"System Default ({sys_native})"}
        
        all_codes = set(self.translations.keys()) | {self.DEFAULT_LOCALE, "zh_CN"}
        
        for code in sorted(all_codes):
            if code in self.LANG_META:
                meta = self.LANG_META[code]
                flag = meta.get("flag", "")
                prefix = f"{flag} " if flag and flag != "🌐" else ""
                langs[code] = f"{prefix}{meta['native']}"
            else:
                qloc = QLocale(code)
                native_name = qloc.nativeLanguageName()
                if not native_name or native_name == code:
                    native_name = qloc.languageToString(qloc.language())
                native_name = native_name.capitalize() if native_name else code
                langs[code] = native_name
                
        return langs

    def set_language(self, lang_code: str):
        target = self.normalize_locale(lang_code)
        if target != self.current_lang:
            self.current_lang = target
            self.language_changed.emit(self.current_lang)

    def t(self, text: str, **kwargs) -> str:
        val = text
        if self.current_lang in self.translations and text in self.translations[self.current_lang]:
            val = self.translations[self.current_lang][text]
        elif self.current_lang == "zh_CN" and text in self.fallback_zh_cn:
            val = self.fallback_zh_cn[text]
        if kwargs:
            try: return val.format(**kwargs)
            except Exception: pass
        return val

_LOCALES_DIR = Path(__file__).parent / "locales"
if not _LOCALES_DIR.exists():
    _LOCALES_DIR = _CONFIG_DIR / "locales"
    
I18N = TranslationEngine(_LOCALES_DIR)
I18N.init_locale()

def _(text: str, **kwargs) -> str:
    return I18N.t(text, **kwargs)

PYPI_MIRRORS_GLOBAL = [
    ("PyPI Official (Global Default)", "https://pypi.org/simple"),
    ("Python TestPyPI", "https://test.pypi.org/simple"),
    ("AWS PyPI Mirror (US/EU)", "https://pypi.org/simple"),
    ("Tsinghua University (China)", "https://pypi.tuna.tsinghua.edu.cn/simple"),
    ("Aliyun Cloud (China)", "https://mirrors.aliyun.com/pypi/simple/"),
    ("Tencent Cloud (China)", "https://mirrors.cloud.tencent.com/pypi/simple/"),
    ("Huawei Cloud (China)", "https://repo.huaweicloud.com/repository/pypi/simple/"),
    ("USTC (China)", "https://mirrors.ustc.edu.cn/pypi/simple/"),
]

DEFAULT_MAPPINGS = {
    'acoustid': 'pyacoustid', 'cv2': 'opencv-python', 'PIL': 'pillow', 'Pillow': 'pillow',
    'fitz': 'pymupdf', 'skimage': 'scikit-image', 'vlc': 'python-vlc', 'pyzbar': 'pyzbar',
    'docx': 'python-docx', 'pptx': 'python-pptx', 'bs4': 'beautifulsoup4', 'barcode': 'python-barcode',
    'pdfplumber': 'pdfplumber', 'win32com': 'pywin32', 'win32api': 'pywin32', 'win32con': 'pywin32',
    'win32gui': 'pywin32', 'win32clipboard': 'pywin32', 'win32print': 'pywin32', 'win32file': 'pywin32',
    'win32security': 'pywin32', 'win32process': 'pywin32', 'win32evtlog': 'pywin32', 'win32service': 'pywin32',
    'win32pipe': 'pywin32', 'win32net': 'pywin32', 'win32crypt': 'pywin32', 'pythoncom': 'pywin32',
    'pywintypes': 'pywin32', 'serial': 'pyserial', 'usb': 'pyusb', 'bluetooth': 'pybluez',
    'sklearn': 'scikit-learn', 'yaml': 'pyyaml', 'dateutil': 'python-dateutil', 'jwt': 'PyJWT',
    'Crypto': 'pycryptodome', 'crypto': 'pycryptodome', 'OpenGL': 'PyOpenGL', 'dns': 'dnspython',
    'wx': 'wxPython', 'desktop_notifier': 'desktop-notifier', 'dotenv': 'python-dotenv',
    'telegram': 'python-telegram-bot', 'websocket': 'websocket-client', 'git': 'GitPython',
    'github': 'PyGithub', 'gitlab': 'python-gitlab', 'discord': 'discord.py', 'paho': 'paho-mqtt',
    'socketio': 'python-socketio', 'engineio': 'python-engineio', 'kafka': 'kafka-python',
    'OpenSSL': 'pyOpenSSL', 'ldap': 'python-ldap', 'magic': 'python-magic', 'slugify': 'python-slugify',
    'snappy': 'python-snappy'
}

MATERIAL_ICONS = {
    'settings': 'M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.06-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.73,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.06,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.43-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.49-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z',
    'refresh': 'M17.65,6.35C16.2,4.9,14.21,4,12,4c-4.42,0-7.99,3.58-7.99,8s3.57,8,7.99,8c3.73,0,6.84-2.55,7.73-6h-2.08 c-0.82,2.33-3.04,4-5.65,4c-3.31,0-6-2.69-6-6s2.69-6,6-6c1.66,0,3.14,0.69,4.22,1.78L13,11h7V4L17.65,6.35z',
    'play': 'M8 5v14l11-7z',
    'stop': 'M6 6h12v12H6z',
    'folder': 'M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z',
    'expand_more': 'M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z',
    'expand_less': 'M12 8l-6 6 1.41 1.41L12 10.83l4.59 4.58L18 14z',
    'check': 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z',
    'package': 'M20,2H4C3,2,2,2.9,2,4v3.01C2,7.73,2.43,8.35,3,8.7V20c0,1.1,1.1,2,2,2h14c0.9,0,2-0.9,2-2V8.7c0.57-0.35,1-0.97,1-1.69V4 C22,2.9,21,2,20,2z M19,20H5V9h14V20z M20,7H4V4h16V7z M9,12h6v2H9V12z',
    'back': 'M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z',
    'info': 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z',
    'python': 'M12.06,1.48c-3.14,0-3.52,0.67-3.52,0.67l-0.01,2.44h3.63v0.52H7.43C5.12,5.11,4.5,6.58,4.5,8.81c0,2.34,0.38,3.48,2.3,3.48 h1.14v-1.62c0-1.48,1.23-2.65,2.7-2.65h3.69c1.47,0,2.66-1.19,2.66-2.65V3.88C16.99,1.83,14.67,1.48,12.06,1.48z M10.22,2.83 c0.41,0,0.73,0.33,0.73,0.74c0,0.41-0.33,0.74-0.73,0.74c-0.4,0-0.73-0.33-0.73-0.74C9.49,3.16,9.82,2.83,10.22,2.83z M16.71,9.89 v1.62c0,1.48-1.23,2.65-2.7,2.65H10.3c-1.47,0-2.66,1.19-2.66,2.65v1.49c0,2.05,2.32,2.41,4.92,2.41c3.14,0,3.52-0.67,3.52-0.67 l0.01-2.44h-3.63v-0.52h4.73c2.31,0,2.93-1.47,2.93-3.7c0-2.34-0.38-3.48-2.3-3.48H16.71z M13.88,18.96c0.41,0,0.73,0.33,0.73,0.74c0,0.41-0.33,0.74-0.73,0.74c-0.4,0-0.73-0.33-0.73-0.74C13.15,19.29,13.48,18.96,13.88,18.96z',
    'close': 'M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z'
}

def load_config():
    config = configparser.ConfigParser()
    default_mirror = "https://pypi.org/simple"
    default_backup = "https://test.pypi.org/simple"
    
    if I18N.detect_system_language() == "zh_CN":
        default_mirror = "https://pypi.tuna.tsinghua.edu.cn/simple"
        default_backup = "https://mirrors.aliyun.com/pypi/simple/"

    if not os.path.exists(CONFIG_FILE):
        config['Mappings'] = DEFAULT_MAPPINGS
        config['Settings'] = {
            'language': 'auto',
            'engine': 'PyInstaller', 
            'pip_index': default_mirror,
            'pip_index_backup': default_backup,
            'onefile': 'True', 'noconsole': 'True', 'clean_all': 'True',
            'auto_icon': 'True', 'use_venv': 'True', 'use_reqs': 'True',
            'use_pipreqs': 'True', 'use_pipreqs_dir': 'False', 'upx': 'False', 'concise_log': 'True',
            'cpu_cores': str(os.cpu_count() or 2), 'upx_path': '',
            'exclude_modules': '', 'out_mode': '0', 'custom_out_dir': '',
            'sound_notify': 'True', 'auto_save_log': 'False',
            'use_reqs_file': '', 'add_data_list': '', 'custom_python_path': '',
            'pyi_version': '', 'nuitka_version': '', 'pipreqs_version': '',
            'lite_mode': 'False'
        }
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                config.write(f)
        except: pass
    else:
        config.read(CONFIG_FILE, encoding='utf-8')
        if 'Mappings' not in config: 
            config['Mappings'] = DEFAULT_MAPPINGS
        else:
            updated_map = False
            for k, v in DEFAULT_MAPPINGS.items():
                if k not in config['Mappings']:
                    config['Mappings'][k] = v
                    updated_map = True
            if updated_map:
                try: save_config(config)
                except: pass

        if 'Settings' not in config: config['Settings'] = {}
        
        updated = False
        default_updates = {
            'language': 'auto',
            'pip_index': default_mirror,
            'pip_index_backup': default_backup,
            'concise_log': 'True',
            'cpu_cores': str(os.cpu_count() or 2),
            'upx_path': '',
            'exclude_modules': '',
            'out_mode': '0',
            'custom_out_dir': '',
            'sound_notify': 'True',
            'auto_save_log': 'False',
            'use_reqs_file': '',
            'add_data_list': '',
            'custom_python_path': '',
            'pyi_version': '',
            'nuitka_version': '',
            'pipreqs_version': '',
            'lite_mode': 'False'
        }
        for k, v in default_updates.items():
            if k not in config['Settings']:
                config['Settings'][k] = v
                updated = True
                
        if updated:
            try: save_config(config)
            except: pass
            
    lang_pref = config['Settings'].get('language', 'auto')
    I18N.set_language(lang_pref)
    return config

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            config.write(f)
    except: pass

def create_pleasant_audio_files():
    success_wav = _CONFIG_DIR / "sound_success.wav"
    failure_wav = _CONFIG_DIR / "sound_failure.wav"
    sample_rate = 44100

    if not success_wav.exists():
        try:
            notes = [(523.25, 0.0, 0.35), (659.25, 0.09, 0.35), (784.00, 0.18, 0.35), (1046.50, 0.27, 0.55)]
            total_duration = 0.75
            n_samples = int(sample_rate * total_duration)
            samples = [0.0] * n_samples

            for freq, start, dur in notes:
                start_idx = int(start * sample_rate)
                dur_samples = int(dur * sample_rate)
                for i in range(dur_samples):
                    idx = start_idx + i
                    if idx >= n_samples: break
                    t = i / sample_rate
                    env = math.sin(math.pi * min(1.0, t / 0.025)) * math.exp(-4.2 * (t / dur))
                    val = (math.sin(2 * math.pi * freq * t) * 0.75 + 
                           math.sin(2 * math.pi * freq * 2 * t) * 0.2 +
                           math.sin(2 * math.pi * freq * 3 * t) * 0.05) * env
                    samples[idx] += val * 0.28

            with wave.open(success_wav.as_posix(), 'w') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                packed = b''.join(struct.pack('<h', int(max(-1.0, min(1.0, s)) * 32767)) for s in samples)
                wf.writeframes(packed)
        except Exception: pass

    if not failure_wav.exists():
        try:
            notes = [(392.00, 0.0, 0.3), (311.13, 0.12, 0.45)]
            total_duration = 0.6
            n_samples = int(sample_rate * total_duration)
            samples = [0.0] * n_samples

            for freq, start, dur in notes:
                start_idx = int(start * sample_rate)
                dur_samples = int(dur * sample_rate)
                for i in range(dur_samples):
                    idx = start_idx + i
                    if idx >= n_samples: break
                    t = i / sample_rate
                    env = math.sin(math.pi * min(1.0, t / 0.02)) * math.exp(-3.2 * (t / dur))
                    val = (math.sin(2 * math.pi * freq * t) * 0.8 + 
                           math.sin(2 * math.pi * freq * 2 * t) * 0.2) * env
                    samples[idx] += val * 0.32

            with wave.open(failure_wav.as_posix(), 'w') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                packed = b''.join(struct.pack('<h', int(max(-1.0, min(1.0, s)) * 32767)) for s in samples)
                wf.writeframes(packed)
        except Exception: pass

_AUDIO_EFFECT_REF = None

def play_alert(success=True):
    global _AUDIO_EFFECT_REF
    try:
        config = load_config()
        if not config['Settings'].getboolean('sound_notify', True):
            return
            
        sound_file = _CONFIG_DIR / ("sound_success.wav" if success else "sound_failure.wav")
        if not sound_file.exists():
            create_pleasant_audio_files()

        if sound_file.exists():
            if HAS_QT_AUDIO:
                _AUDIO_EFFECT_REF = QSoundEffect()
                _AUDIO_EFFECT_REF.setSource(QUrl.fromLocalFile(sound_file.as_posix()))
                _AUDIO_EFFECT_REF.setVolume(0.75)
                _AUDIO_EFFECT_REF.play()
            elif os.name == 'nt':
                import winsound
                winsound.PlaySound(sound_file.as_posix(), winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception:
        pass

def is_cloud_locked(filepath):
    try:
        with open(filepath, 'rb') as f:
            return b"__CLOUDSYNC_ENC__" in f.read(1024)
    except Exception:
        return False

def extract_imports_via_ast(script_path, python_exe):
    code_snippet = (
        "import ast, sys, json, re\n"
        "code = ''\n"
        "try:\n"
        "    with open(sys.argv[1], 'rb') as f: raw = f.read()\n"
        "    code = raw.decode('utf-8-sig') if raw.startswith(b'\\xef\\xbb\\xbf') else raw.decode('utf-8', errors='ignore')\n"
        "    imports = set()\n"
        "    for node in ast.walk(ast.parse(code)):\n"
        "        if isinstance(node, ast.Import): imports.update(n.name.split('.')[0] for n in node.names)\n"
        "        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module: imports.add(node.module.split('.')[0])\n"
        "    print('__QPYPACK_RES__:' + json.dumps(list(imports)))\n"
        "except:\n"
        "    try:\n"
        "        m = re.findall(r'^\\s*(?:from|import)\\s+([a-zA-Z0-9_]+)', code, re.M)\n"
        "        print('__QPYPACK_RES__:' + json.dumps(list(set(m))))\n"
        "    except: print('__QPYPACK_RES__:[]')\n"
    )
    try:
        env = os.environ.copy()
        env.pop("PYTHONHOME", None)
        env.pop("PYTHONPATH", None)
        env["PYTHONUTF8"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE, "text": True, "encoding": "utf-8", "env": env}
        if os.name == 'nt': kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        
        proc = subprocess.run([python_exe, "-c", code_snippet, script_path], **kwargs)
        m = re.search(r'__QPYPACK_RES__:(.*)', proc.stdout)
        if m:
            return set(json.loads(m.group(1).strip()))
        return set()
    except:
        return set()

def get_svg_icon(name, color="#5F6368", size=24):
    path_data = MATERIAL_ICONS.get(name, "")
    svg_str = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="{color}" d="{path_data}"/></svg>'
    renderer = QSvgRenderer()
    renderer.load(svg_str.encode('utf-8'))
    
    render_size = max(size * 4, 128)
    pixmap = QPixmap(render_size, render_size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    renderer.render(painter)
    painter.end()
    
    return QIcon(pixmap)

def get_svg_pixmap(name, color="#5F6368", size=64):
    return get_svg_icon(name, color, size).pixmap(size, size)

_ARROW_ICON_PATH = (_CONFIG_DIR / "dropdown_arrow.png").as_posix()

def ensure_arrow_icon():
    if not os.path.exists(_ARROW_ICON_PATH):
        try:
            pix = get_svg_pixmap('expand_more', color="#5F6368", size=32)
            pix.save(_ARROW_ICON_PATH, "PNG")
        except Exception:
            pass

class ComboItemDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        s = super().sizeHint(option, index)
        return QSize(s.width(), max(s.height() + 12, 30))

class TableItemDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setAutoFillBackground(True)
        editor.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff !important;
                color: #111827;
                border: 2px solid #2563eb;
                border-radius: 4px;
                padding: 2px 6px;
                font-size: 12px;
                font-family: Consolas, "Segoe UI", sans-serif;
                selection-background-color: #2563eb;
                selection-color: #ffffff;
            }
        """)
        return editor

def setup_combo_white_theme(combo: QComboBox, min_view_width: int = None):
    ensure_arrow_icon()
    list_view = QListView(combo)
    combo.setView(list_view)
    combo.setItemDelegate(ComboItemDelegate(combo))
    
    if min_view_width and combo.view():
        combo.view().setMinimumWidth(min_view_width)
        combo.view().setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
    if combo.view():
        combo.view().setStyleSheet("""
            QListView {
                background-color: #ffffff; color: #111827; border: 1px solid #d1d5db;
                border-radius: 6px; outline: none; padding: 4px; font-size: 12px;
                font-family: Consolas, "Segoe UI", sans-serif;
                selection-background-color: #2563eb; selection-color: #ffffff;
            }
            QListView::item { background-color: #ffffff; color: #111827; padding: 4px 8px; border-radius: 4px; }
            QListView::item:hover, QListView::item:selected { background-color: #2563eb; color: #ffffff; }
        """)

    arrow_url = _ARROW_ICON_PATH.replace("\\", "/")
    combo.setStyleSheet(f"""
        QComboBox {{
            combobox-popup: 0; background-color: #ffffff; color: #111827;
            border: 1px solid #d1d5db; border-radius: 6px; padding: 5px 26px 5px 10px;
            font-size: 12px; min-height: 22px; font-family: Consolas, "Segoe UI", sans-serif;
            selection-background-color: #2563eb; selection-color: #ffffff;
        }}
        QComboBox:hover {{ border-color: #9ca3af; }}
        QComboBox:focus {{ border-color: #2563eb; }}
        QComboBox::drop-down {{ subcontrol-origin: padding; subcontrol-position: top right; width: 24px; border: none; background: transparent; }}
        QComboBox::down-arrow {{ image: url("{arrow_url}"); width: 14px; height: 14px; }}
        QComboBox QLineEdit {{ background-color: #ffffff; color: #111827; font-size: 12px; selection-background-color: #2563eb; selection-color: #ffffff; }}
    """)
    combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    combo.setMinimumWidth(150)

class DropListWidget(QListWidget):
    itemsDropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls(): event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls(): event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            paths = [u.toLocalFile() for u in urls if u.toLocalFile()]
            if paths: self.itemsDropped.emit(paths)

def get_stdlib_names():
    libs = {'os', 'sys', 're', 'math', 'time', 'datetime', 'json', 'urllib', 'sqlite3', 'csv', 
            'subprocess', 'shutil', 'threading', 'multiprocessing', 'queue', 'socket', 
            'collections', 'itertools', 'functools', 'random', 'hashlib', 'base64', 
            'binascii', 'xml', 'logging', 'argparse', 'typing', 'pathlib', 'traceback', 
            'warnings', 'tempfile', 'platform', 'zipfile', 'tarfile', 'gzip', 'bz2', 
            'lzma', 'hmac', 'ssl', 'email', 'http', 'uuid', 'io', 'contextlib', 'winreg',
            'concurrent', 'ctypes', 'dataclasses', 'enum', 'importlib', 'inspect',
            'pickle', 'copy', 'ast', 'asyncio', 'calendar', 'configparser',
            'curses', 'decimal', 'difflib', 'getopt', 'getpass', 'glob', 'html',
            'mimetypes', 'numbers', 'operator', 'pdb', 'pprint', 'profile', 'pstats',
            'runpy', 'sched', 'secrets', 'selectors', 'shelve', 'shlex',
            'signal', 'site', 'smtpd', 'smtplib', 'sndhdr', 'socketserver',
            'stat', 'statistics', 'string', 'struct', 'symtable', 'sysconfig',
            'syslog', 'tabnanny', 'telnetlib', 'termios', 'future',
            'textwrap', 'timeit', 'tkinter', 'token', 'tokenize', 'trace',
            'tracemalloc', 'tty', 'turtle', 'turtledemo', 'types',
            'unittest', 'uu', 'venv', 'wave', '__future__',
            'weakref', 'webbrowser', 'winsound', 'wsgiref', 'xdrlib',
            'xmlrpc', 'zipapp', 'zipimport', 'zlib', 'zoneinfo'}
    if sys.version_info >= (3, 10):
        libs.update(sys.stdlib_module_names)
    return libs

STD_LIBS = get_stdlib_names()

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    elif '__compiled__' in globals():
        base_path = os.path.dirname(os.path.abspath(__file__))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def find_system_python():
    candidates = []
    for name in ('python', 'python3', 'pythonw'):
        p = shutil.which(name)
        if p: candidates.append(p)
        
    if winreg is not None:
        try:
            py = shutil.which("py")
            if py:
                clean_env = os.environ.copy()
                clean_env.pop("PYTHONHOME", None)
                clean_env.pop("PYTHONPATH", None)
                clean_env["PYTHONUTF8"] = "1"
                proc = subprocess.Popen(
                    [py, "-c", "import sys; print(sys.executable)"], 
                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                    text=True, encoding="utf-8", env=clean_env, creationflags=subprocess.CREATE_NO_WINDOW
                )
                out, _err = proc.communicate(timeout=3)
                if out and os.path.exists(out.strip()): candidates.append(out.strip())
        except: pass
        
        try:
            for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
                try:
                    with winreg.OpenKey(hive, r"SOFTWARE\Python\PythonCore") as core_key:
                        for i in range(winreg.QueryInfoKey(core_key)[0]):
                            sub = winreg.EnumKey(core_key, i)
                            try:
                                with winreg.OpenKey(core_key, rf"{sub}\InstallPath") as pkey:
                                    path = winreg.QueryValueEx(pkey, "")[0]
                                    exe = os.path.join(path, "python.exe")
                                    if os.path.exists(exe): candidates.append(exe)
                            except: pass
                except: pass
        except: pass
        
        search_paths = [
            os.environ.get("LOCALAPPDATA", "") + r"\Programs\Python",
            os.environ.get("PROGRAMFILES", "") + r"\Python",
            os.environ.get("PROGRAMFILES(X86)", "") + r"\Python",
            r"C:\Python", r"C:\Program Files\Python", r"C:\Program Files (x86)\Python"
        ]
        for base in search_paths:
            if base and os.path.exists(base):
                try:
                    for d in os.listdir(base):
                        if d.lower().startswith("python"):
                            exe = os.path.join(base, d, "python.exe")
                            if os.path.exists(exe): candidates.append(exe)
                except: pass
        
        user_profile = os.environ.get("USERPROFILE", "")
        if user_profile:
            for c_dir in ("miniconda3", "anaconda3", "Miniconda3", "Anaconda3"):
                for base in (user_profile, "C:\\", "D:\\"):
                    exe = os.path.join(base, c_dir, "python.exe")
                    if os.path.exists(exe): candidates.append(exe)
    else:
        unix_bases = [
            "/usr/bin", "/usr/local/bin", "/opt/homebrew/bin",
            os.path.expanduser("~/.pyenv/shims"), os.path.expanduser("~/.local/bin")
        ]
        user_profile = os.environ.get("HOME", "") or os.environ.get("USERPROFILE", "")
        if user_profile:
            for c_dir in ("miniconda3", "anaconda3", "mambaforge", ".conda"):
                base_dir = os.path.join(user_profile, c_dir)
                if os.path.exists(base_dir):
                    exe = os.path.join(base_dir, "bin", "python")
                    if os.path.exists(exe): unix_bases.append(os.path.join(base_dir, "bin"))
                    envs_dir = os.path.join(base_dir, "envs")
                    if os.path.exists(envs_dir):
                        try:
                            for env in os.listdir(envs_dir):
                                p_bin = os.path.join(envs_dir, env, "bin")
                                if os.path.exists(p_bin): unix_bases.append(p_bin)
                        except: pass

        for base in unix_bases:
            if os.path.exists(base):
                try:
                    for f in os.listdir(base):
                        if f.startswith("python3") or f == "python":
                            exe = os.path.join(base, f)
                            if os.path.isfile(exe) and os.access(exe, os.X_OK): candidates.append(exe)
                except: pass

    seen = set()
    unique_candidates = []
    for cand in candidates:
        cand = os.path.normpath(cand)
        if cand not in seen:
            seen.add(cand)
            unique_candidates.append(cand)

    for cand in unique_candidates:
        if not os.path.exists(cand): continue
        if os.name == 'nt' and "WindowsApps" in cand:
            try:
                if os.path.getsize(cand) == 0: continue
            except: continue
            
        clean_env = os.environ.copy()
        clean_env.pop("PYTHONHOME", None)
        clean_env.pop("PYTHONPATH", None)
        
        try:
            kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE, "text": True, "encoding": "utf-8", "env": clean_env, "timeout": 3}
            if os.name == 'nt': kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
            proc = subprocess.run([cand, "-V"], **kwargs)
            if proc.returncode == 0: return cand
        except: continue
            
    return "python"

def get_python_executable():
    try:
        config = load_config()
        custom_path = config['Settings'].get('custom_python_path', '').strip()
        if custom_path and os.path.exists(custom_path) and os.path.isfile(custom_path):
            return custom_path
    except Exception: pass

    if getattr(sys, 'frozen', False) or '__compiled__' in globals():
        return find_system_python()
        
    exe_name = Path(sys.executable).name.lower()
    if exe_name in ('python.exe', 'python3.exe', 'pythonw.exe', 'python', 'python3'):
        return sys.executable
        
    return find_system_python()

def remove_readonly(func, path, exc_info):
    try: 
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except: pass

def robust_rmtree(path: Path, retries=15, delay=0.8):
    if not path.exists(): return True
    for _ in range(retries):
        try:
            shutil.rmtree(path, onerror=remove_readonly)
            if not path.exists(): return True
        except: time.sleep(delay)
    return False

def convert_image_to_format(src_path, dest_path, dest_format):
    src = Path(src_path).resolve()
    dst = Path(dest_path).resolve()
    fmt = dest_format.lower()
    
    if sys.platform == "darwin" and fmt == "icns":
        try:
            proc = subprocess.run(["sips", "-s", "format", "icns", src.as_posix(), "--out", dst.as_posix()], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if proc.returncode == 0 and dst.exists(): return True
        except: pass

    try:
        img = QImage(src.as_posix())
        if not img.isNull():
            if fmt == "ico": img = img.scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            elif fmt == "icns": img = img.scaled(512, 512, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            writer = QImageWriter(dst.as_posix(), fmt.upper().encode('utf-8'))
            if writer.write(img): return True
    except: pass

    try:
        from PIL import Image
        img = Image.open(src.as_posix())
        if fmt == "ico":
            img.save(dst.as_posix(), format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
            return True
        elif fmt == "icns":
            img.save(dst.as_posix(), format="ICNS", sizes=[(512, 512), (256, 256), (128, 128), (64, 64)])
            return True
        else:
            img.save(dst.as_posix(), format=dest_format.upper())
            return True
    except: pass
        
    return False

class AnimatedButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        
        self.animation_group = QParallelAnimationGroup()
        self.pos_anim = QPropertyAnimation(self, b"geometry")
        self.pos_anim.setDuration(150)
        self.pos_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.op_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.op_anim.setDuration(200)
        self.op_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.is_hovered = False

    def enterEvent(self, event):
        if not self.is_hovered and self.isEnabled():
            self.is_hovered = True
            geom = self.geometry()
            self.pos_anim.setStartValue(geom)
            self.pos_anim.setEndValue(geom.adjusted(0, -2, 0, -2))
            self.op_anim.setStartValue(1.0)
            self.op_anim.setEndValue(0.85)
            self.animation_group.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.is_hovered and self.isEnabled():
            self.is_hovered = False
            geom = self.geometry()
            self.pos_anim.setStartValue(geom)
            self.pos_anim.setEndValue(geom.adjusted(0, 2, 0, 2))
            self.op_anim.setStartValue(0.85)
            self.op_anim.setEndValue(1.0)
            self.animation_group.start()
        super().leaveEvent(event)

class TargetIconWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.pixmap = None
        self.base_pixmap = None
        self.file_pixmap = None
        self.current_size = 88
        
        self.is_building = False
        self.spin_angle = 0
        self.pulse_value = 0
        
        self.anim_timer = QTimer(self)
        self.anim_timer.setInterval(16)
        self.anim_timer.timeout.connect(self._update_frame)
        
        self.success_effect = QGraphicsDropShadowEffect(self)
        self.success_effect.setOffset(0, 0)
        self.success_effect.setColor(QColor(0, 0, 0, 0))
        self.success_effect.setBlurRadius(0)
        self.setGraphicsEffect(self.success_effect)
        
        self.burst_value = 0.0
        self.burst_anim = QVariantAnimation(self)
        self.burst_anim.setDuration(600)
        self.burst_anim.setLoopCount(1)
        self.burst_anim.setStartValue(0.0)
        self.burst_anim.setEndValue(1.0)
        self.burst_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.burst_anim.valueChanged.connect(self._animate_burst)

        self.shake_offset = 0
        self.shake_anim = QVariantAnimation(self)
        self.shake_anim.setDuration(500)
        self.shake_anim.setStartValue(0)
        self.shake_anim.setEndValue(0)
        self.shake_anim.setKeyValueAt(0.0, 0)
        self.shake_anim.setKeyValueAt(0.1, -12)
        self.shake_anim.setKeyValueAt(0.3, 12)
        self.shake_anim.setKeyValueAt(0.5, -12)
        self.shake_anim.setKeyValueAt(0.7, 12)
        self.shake_anim.setKeyValueAt(0.9, -6)
        self.shake_anim.setKeyValueAt(1.0, 0)
        self.shake_anim.valueChanged.connect(self._animate_shake)

    def set_default_pixmap(self, pixmap, size=88):
        self.base_pixmap = pixmap
        self.pixmap = pixmap
        self.current_size = size
        self.update()
        
    def set_custom_pixmap(self, pixmap, size=88):
        self.pixmap = pixmap
        self.current_size = size
        self.update()

    def set_file_pixmap(self, pixmap, size=88):
        self.file_pixmap = pixmap
        self.pixmap = pixmap
        self.current_size = size
        self.update()

    def start_building(self):
        if getattr(self, 'file_pixmap', None) and not self.file_pixmap.isNull():
            self.pixmap = self.file_pixmap
            self.current_size = 88
            
        self.is_building = True
        self.spin_angle = 0
        self.pulse_value = 0
        self.burst_value = 0.0
        self.shake_offset = 0
        self.success_effect.setColor(QColor(0, 0, 0, 0))
        self.burst_anim.stop()
        self.shake_anim.stop()
        self.anim_timer.start()
        
    def stop_building(self):
        self.is_building = False
        self.anim_timer.stop()
        self.update()
        
    def start_success(self):
        self.stop_building()
        self.success_effect.setBlurRadius(40)
        self.success_effect.setColor(QColor(255, 193, 7, 180))
        self.burst_anim.start()

    def start_failure(self):
        self.stop_building()
        self.success_effect.setBlurRadius(40)
        self.success_effect.setColor(QColor(217, 48, 37, 180))
        self.shake_anim.start()
        
    def reset(self):
        self.stop_building()
        self.burst_anim.stop()
        self.shake_anim.stop()
        self.burst_value = 0.0
        self.shake_offset = 0
        self.success_effect.setColor(QColor(0, 0, 0, 0))
        self.file_pixmap = None
        self.pixmap = self.base_pixmap
        self.current_size = 88
        self.update()
        
    def _update_frame(self):
        self.spin_angle = (self.spin_angle + 4) % 360
        self.pulse_value += 0.05
        self.update()
        
    def _animate_burst(self, val):
        self.burst_value = val
        self.update()

    def _animate_shake(self, val):
        self.shake_offset = val
        self.update()

    def paintEvent(self, event):
        if not self.pixmap or self.pixmap.isNull(): return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        center = self.rect().center()
        center_x = center.x() + int(self.shake_offset)
        icon_center_y = center.y()
        draw_size = self.current_size
        
        if self.is_building:
            radius = (self.current_size / 2) + 12
            pen = QPen(QColor(26, 115, 232, 200))
            pen.setWidth(4)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            
            rect = QRectF(center_x - radius, center.y() - radius, radius * 2, radius * 2)
            span_angle = int((140 + 60 * math.sin(self.pulse_value * 1.5)) * 16)
            start_angle = int(-self.spin_angle * 16)
            painter.drawArc(rect, start_angle, span_angle)
            
        elif self.burst_value > 0.0:
            pop_scale = 1.0 + math.sin(self.burst_value * math.pi) * 0.15
            draw_size = int(self.current_size * pop_scale)
            if self.burst_value < 1.0:
                alpha = int(255 * (1.0 - self.burst_value))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QColor(26, 115, 232, alpha))
                burst_radius_1 = (self.current_size / 2) + 10 + self.burst_value * 40
                dot_size_1 = 8 * (1.0 - self.burst_value)
                for i in range(8):
                    angle = math.radians(i * 45)
                    dx = center_x + math.cos(angle) * burst_radius_1
                    dy = center.y() + math.sin(angle) * burst_radius_1
                    painter.drawEllipse(QPointF(dx, dy), dot_size_1, dot_size_1)
                
                painter.setBrush(QColor(255, 193, 7, alpha))
                burst_radius_2 = (self.current_size / 2) + self.burst_value * 65
                dot_size_2 = 6 * (1.0 - self.burst_value)
                for i in range(8):
                    angle = math.radians(i * 45 + 22.5)
                    dx = center_x + math.cos(angle) * burst_radius_2
                    dy = center.y() + math.sin(angle) * burst_radius_2
                    painter.drawEllipse(QPointF(dx, dy), dot_size_2, dot_size_2)
        
        pix_rect = QRectF(center_x - draw_size / 2.0, icon_center_y - draw_size / 2.0, float(draw_size), float(draw_size))
        scaled_pix = self.pixmap.scaled(
            int(draw_size * self.devicePixelRatioF()), 
            int(draw_size * self.devicePixelRatioF()), 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        scaled_pix.setDevicePixelRatio(self.devicePixelRatioF())
        painter.drawPixmap(pix_rect, scaled_pix, QRectF(scaled_pix.rect()))
        painter.end()

class DropArea(QFrame):
    fileDropped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DropArea") 
        self.setAcceptDrops(True)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.current_filename = None
        self.setStyleSheet("""
            #DropArea { background-color: #f8f9fa; border: 2px dashed #dadce0; border-radius: 12px; }
            #DropArea:hover { background-color: #f1f3f4; border: 2px dashed #bdc1c6; }
        """)
        self.init_ui()
        I18N.language_changed.connect(self.retranslate_ui)

    def _get_default_pixmap(self, size=88):
        icon_path = get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            pixmap = QIcon(icon_path).pixmap(256, 256)
            if not pixmap.isNull(): return pixmap
        return get_svg_pixmap('python', color="#9AA0A6", size=256)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(0)
        layout.addStretch(1)
        
        self.icon_widget = TargetIconWidget(self)
        self.icon_widget.set_default_pixmap(self._get_default_pixmap(88))
        
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        h_layout.addWidget(self.icon_widget)
        h_layout.addStretch(1)
        layout.addLayout(h_layout)
        layout.addSpacing(18)
        
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("QLabel { background: transparent; color: #5F6368; font-size: 16px; font-weight: bold; border: none; }")
        layout.addWidget(self.label)
        
        layout.addSpacing(8)
        
        self.sub_label = QLabel()
        self.sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sub_label.setWordWrap(True)
        self.sub_label.setStyleSheet("QLabel { background: transparent; color: #9AA0A6; font-size: 13px; border: none; }")
        layout.addWidget(self.sub_label)
        layout.addStretch(1)
        
        self.retranslate_ui()

    def retranslate_ui(self):
        if not self.current_filename:
            self.label.setText(_("Drag & Drop Python script (.py/.pyw) here\nor Click to Browse"))
            self.sub_label.setText(_("Auto-parse dependencies, resources, and implicit imports"))
        else:
            self.label.setText(_("Loaded: {filename}", filename=self.current_filename))

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile().lower()
            if file_path.endswith('.py') or file_path.endswith('.pyw'):
                event.acceptProposedAction()
                self.setStyleSheet("#DropArea { background-color: #E8F0FE; border: 2px dashed #1A73E8; border-radius: 12px; }")

    def dragLeaveEvent(self, event):
        self.setStyleSheet("#DropArea { background-color: #f8f9fa; border: 2px dashed #dadce0; border-radius: 12px; } #DropArea:hover { background-color: #f1f3f4; border: 2px dashed #bdc1c6; }")

    def dropEvent(self, event: QDropEvent):
        self.dragLeaveEvent(event)
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith(('.py', '.pyw')):
                self.fileDropped.emit(file_path)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            fp, _filter = QFileDialog.getOpenFileName(
                self, 
                _("Drag & Drop Python script (.py/.pyw) here\nor Click to Browse"), 
                "", 
                "Python Scripts (*.py *.pyw);;All Files (*)"
            )
            if fp: self.fileDropped.emit(fp)

    def set_loading(self, filename):
        self.current_filename = filename
        pixmap = get_svg_pixmap('package', color="#1A73E8", size=88)
        self.icon_widget.set_file_pixmap(pixmap, 88)
        self.label.setText(_("Loaded: {filename}", filename=filename))
        self.label.setStyleSheet("QLabel { background: transparent; color: #1A73E8; font-size: 16px; font-weight: bold; border: none; }")
        self.sub_label.setText(_("Parsing metadata..."))

    def set_success(self, filename, custom_icon_path=None):
        self.current_filename = filename
        pixmap = None
        if custom_icon_path and Path(custom_icon_path).exists():
            pixmap = QIcon(str(custom_icon_path)).pixmap(256, 256)
            if pixmap.isNull(): pixmap = None
                
        if not pixmap:
            pixmap = get_svg_pixmap('package', color="#1A73E8", size=256)
            
        self.icon_widget.set_file_pixmap(pixmap, 88)
        self.label.setText(_("Loaded: {filename}", filename=filename))
        self.label.setStyleSheet("QLabel { background: transparent; color: #1A73E8; font-size: 16px; font-weight: bold; border: none; }")
        self.sub_label.setText(_("Ready, waiting for build."))

    def start_build_anim(self):
        self.label.setText(_("Initializing build..."))
        self.label.setStyleSheet("QLabel { background: transparent; color: #1A73E8; font-size: 16px; font-weight: bold; border: none; }")
        self.sub_label.setText(_("Preparing engine..."))
        self.icon_widget.start_building()

    def stop_build_anim(self):
        self.icon_widget.stop_building()

    def show_success(self, custom_icon_path=None):
        size = 128
        pixmap_set = False
        if custom_icon_path and Path(custom_icon_path).exists():
            pix = QIcon(str(custom_icon_path)).pixmap(256, 256)
            if not pix.isNull():
                self.icon_widget.set_custom_pixmap(pix, size)
                pixmap_set = True
                
        if not pixmap_set:
            if self.icon_widget.base_pixmap and not self.icon_widget.base_pixmap.isNull():
                self.icon_widget.set_custom_pixmap(self.icon_widget.base_pixmap, size)
            else:
                self.icon_widget.set_custom_pixmap(get_svg_pixmap('check', color="#1E8E3E", size=size), size)
            
        self.icon_widget.start_success()
        self.label.setText(_("Build Successful"))
        self.label.setStyleSheet("QLabel { background: transparent; color: #1E8E3E; font-size: 20px; font-weight: bold; border: none; }")
        self.sub_label.setText(_("Open output directory or reset workspace."))

    def show_failure(self):
        size = 128
        self.icon_widget.set_custom_pixmap(get_svg_pixmap('close', color="#D93025", size=size), size)
        self.icon_widget.start_failure()
        
        self.label.setText(_("Build Failed"))
        self.label.setStyleSheet("QLabel { background: transparent; color: #D93025; font-size: 20px; font-weight: bold; border: none; }")
        self.sub_label.setText(_("Check log output below for troubleshooting."))
        
    def reset(self):
        self.current_filename = None
        self.icon_widget.reset()
        self.retranslate_ui()
        self.label.setStyleSheet("QLabel { background: transparent; color: #5F6368; font-size: 16px; font-weight: bold; border: none; }")

class PythonScannerThread(QThread):
    scan_done = Signal(dict)
    
    def run(self):
        candidates = set()
        for name in ('python', 'python3', 'pythonw'):
            p = shutil.which(name)
            if p: candidates.add(os.path.normpath(p))
            
        if winreg is not None:
            try:
                for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
                    try:
                        with winreg.OpenKey(hive, r"SOFTWARE\Python\PythonCore") as core_key:
                            for i in range(winreg.QueryInfoKey(core_key)[0]):
                                sub = winreg.EnumKey(core_key, i)
                                try:
                                    with winreg.OpenKey(core_key, rf"{sub}\InstallPath") as pkey:
                                        path = winreg.QueryValueEx(pkey, "")[0]
                                        exe = os.path.join(path, "python.exe")
                                        if os.path.exists(exe): candidates.add(os.path.normpath(exe))
                                except: pass
                    except: pass
            except: pass
            
            search_paths = [
                os.environ.get("LOCALAPPDATA", "") + r"\Programs\Python",
                os.environ.get("PROGRAMFILES", "") + r"\Python",
                os.environ.get("PROGRAMFILES(X86)", "") + r"\Python",
                r"C:\Python", r"C:\Program Files\Python", r"C:\Program Files (x86)\Python"
            ]
            for base in search_paths:
                if base and os.path.exists(base):
                    try:
                        for d in os.listdir(base):
                            if d.lower().startswith("python"):
                                exe = os.path.join(base, d, "python.exe")
                                if os.path.exists(exe): candidates.add(os.path.normpath(exe))
                    except: pass
            
            user_profile = os.environ.get("USERPROFILE", "")
            if user_profile:
                for c_dir in ("miniconda3", "anaconda3", "Miniconda3", "Anaconda3", ".conda"):
                    for base in (user_profile, "C:\\", "D:\\"):
                        base_dir = os.path.join(base, c_dir)
                        if os.path.exists(base_dir):
                            exe = os.path.join(base_dir, "python.exe")
                            if os.path.exists(exe): candidates.add(os.path.normpath(exe))
                            envs_dir = os.path.join(base_dir, "envs")
                            if os.path.exists(envs_dir):
                                try:
                                    for env in os.listdir(envs_dir):
                                        exe = os.path.join(envs_dir, env, "python.exe")
                                        if os.path.exists(exe): candidates.add(os.path.normpath(exe))
                                except: pass
        else:
            unix_bases = [
                "/usr/bin", "/usr/local/bin", "/opt/homebrew/bin",
                os.path.expanduser("~/.pyenv/shims"), os.path.expanduser("~/.local/bin")
            ]
            user_profile = os.environ.get("HOME", "") or os.environ.get("USERPROFILE", "")
            if user_profile:
                for c_dir in ("miniconda3", "anaconda3", "mambaforge", ".conda"):
                    base_dir = os.path.join(user_profile, c_dir)
                    if os.path.exists(base_dir):
                        exe = os.path.join(base_dir, "bin", "python")
                        if os.path.exists(exe): unix_bases.append(os.path.join(base_dir, "bin"))
                        envs_dir = os.path.join(base_dir, "envs")
                        if os.path.exists(envs_dir):
                            try:
                                for env in os.listdir(envs_dir):
                                    p_bin = os.path.join(envs_dir, env, "bin")
                                    if os.path.exists(p_bin): unix_bases.append(p_bin)
                            except: pass

            for base in unix_bases:
                if os.path.exists(base):
                    try:
                        for f in os.listdir(base):
                            if f.startswith("python3") or f == "python":
                                exe = os.path.join(base, f)
                                if os.path.isfile(exe) and os.access(exe, os.X_OK):
                                    candidates.add(os.path.normpath(exe))
                    except: pass

        resolved_candidates = set()
        for cand in candidates:
            try:
                resolved_path = str(Path(cand).resolve())
                if resolved_path.startswith("\\\\?\\UNC\\"):
                    resolved_path = "\\\\" + resolved_path[8:]
                elif resolved_path.startswith("\\\\?\\"):
                    resolved_path = resolved_path[4:]
                resolved_candidates.add(resolved_path)
            except:
                resolved_candidates.add(os.path.normpath(cand))
        candidates = resolved_candidates

        valid_pythons = {}
        for cand in candidates:
            if os.name == 'nt' and "WindowsApps" in cand:
                try:
                    if os.path.getsize(cand) == 0: continue
                except: continue
            try:
                clean_env = os.environ.copy()
                clean_env.pop("PYTHONHOME", None)
                clean_env.pop("PYTHONPATH", None)
                clean_env["PYTHONUTF8"] = "1"
                clean_env["PYTHONIOENCODING"] = "utf-8"
                kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE, "text": True, "encoding": "utf-8", "env": clean_env, "timeout": 2}
                if os.name == 'nt': kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
                proc = subprocess.run([cand, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"], **kwargs)
                if proc.returncode == 0:
                    ver = proc.stdout.strip()
                    valid_pythons[cand] = ver
            except: pass
        self.scan_done.emit(valid_pythons)

class SettingsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_win = parent
        self.upx_check = None 
        self.upx_path_container = None
        self.out_dir_container = None
        
        self.setStyleSheet("""
            SettingsPanel { background-color: #f9fafb; }
            QLabel { color: #111827; font-size: 13px; font-weight: 600; background: transparent; }
            QLineEdit, QSpinBox { color: #111827; font-size: 12px; padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 6px; background: #ffffff; min-height: 22px; }
            QLineEdit:hover, QSpinBox:hover { border-color: #9ca3af; }
            QLineEdit:focus, QSpinBox:focus { border: 1px solid #2563eb; background: #ffffff; }
            QCheckBox { font-size: 13px; color: #1f2937; spacing: 8px; background: transparent; }
            QCheckBox::indicator { width: 16px; height: 16px; border: 1px solid #d1d5db; border-radius: 4px; background: #ffffff; }
            QCheckBox::indicator:hover { border-color: #2563eb; }
            QCheckBox::indicator:checked { background: #2563eb; border-color: #2563eb; }
            QFrame#SettingCard { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; }
            QFrame#SettingCard:hover { border-color: #cbd5e1; }
            QPushButton.ToolBtn { background: #f3f4f6; border: 1px solid #e5e7eb; border-radius: 6px; padding: 6px 12px; color: #374151; font-weight: 600; font-size: 12px; min-width: 68px; }
            QPushButton.ToolBtn:hover { background: #e5e7eb; color: #111827; border-color: #d1d5db; }
            QPushButton.ToolBtn:pressed { background: #d1d5db; }
            QTabWidget#MainTabWidget::pane { border: none; background: transparent; }
            QTabWidget#MainTabWidget::tab-bar { alignment: center; }
            QTabBar#MainTabBar::tab { background: transparent; border: none; padding: 10px 24px; color: #6b7280; font-weight: 600; font-size: 14px; border-bottom: 2px solid transparent; margin: 0 16px; }
            QTabBar#MainTabBar::tab:selected { color: #2563eb; font-weight: 700; border-bottom: 2px solid #2563eb; }
            QTabBar#MainTabBar::tab:hover:!selected { color: #111827; }
            QTabWidget#SubTabWidget::pane { border: none; background: transparent; }
            QTabWidget#SubTabWidget::tab-bar { alignment: center; }
            QTabBar#SubTabBar::tab { background: #f3f4f6; border: 1px solid #e5e7eb; padding: 6px 16px; color: #4b5563; font-weight: 600; font-size: 12px; margin: 0 4px 10px 4px; border-radius: 6px; }
            QTabBar#SubTabBar::tab:selected { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; font-weight: 700; }
            QTabBar#SubTabBar::tab:hover:!selected { background: #e5e7eb; color: #111827; }
            QListWidget, QTableWidget { border: 1px solid #e5e7eb; border-radius: 6px; background-color: #ffffff; outline: none; font-size: 12px; gridline-color: #f3f4f6; }
            QListWidget::item { padding: 6px 10px; border-bottom: 1px solid #f3f4f6; color: #1f2937; }
            QListWidget::item:selected { background-color: #eff6ff; color: #2563eb; font-weight: 600; }
            QTableWidget::item { padding: 4px 8px; color: #1f2937; border-bottom: 1px solid #f3f4f6; background-color: #ffffff; }
            QTableWidget::item:selected { background-color: #eff6ff; color: #2563eb; font-weight: 600; }
            QHeaderView { background-color: #f8fafc; }
            QHeaderView::section { background-color: #f8fafc; color: #475569; font-size: 12px; font-weight: 700; padding: 6px 10px; border: none; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #f1f5f9; }
            QHeaderView::section:horizontal { border-top: none; }
            QScrollBar:vertical { border: none; background: transparent; width: 6px; margin: 0px; }
            QScrollBar::handle:vertical { background: #d1d5db; min-height: 20px; border-radius: 3px; }
            QScrollBar::handle:vertical:hover { background: #9ca3af; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)
        self.init_ui()
        self.load_from_config()
        
        I18N.language_changed.connect(self.retranslate_ui)

        self.scanner_thread = PythonScannerThread()
        self.scanner_thread.scan_done.connect(self.populate_python_combo)
        self.scanner_thread.start()

    def _create_card(self, title_text=""):
        card = QFrame()
        card.setObjectName("SettingCard")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(12)
        if title_text:
            lbl = QLabel(title_text)
            lbl.setObjectName("CardTitle")
            lbl.setStyleSheet("font-size: 15px; font-weight: 800; color: #1a73e8; margin-bottom: 6px;")
            lay.addWidget(lbl)
        return card, lay

    def _create_scroll_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(content)
        lay.setContentsMargins(0, 5, 0, 15)
        lay.setSpacing(15)
        
        scroll.setWidget(content)
        return scroll, content, lay

    def _get_url_from_combo(self, combo):
        idx = combo.currentIndex()
        if idx >= 0 and combo.currentText() == combo.itemText(idx):
            data = combo.itemData(idx)
            if data: return data
        text = combo.currentText().strip()
        m = re.search(r'https?://[^\s]+', text)
        return m.group(0) if m else text

    def _set_combo_value(self, combo, url_val):
        url_val = (url_val or '').strip()
        if not url_val: return
        for i in range(combo.count()):
            data = combo.itemData(i)
            if data and data.rstrip('/') == url_val.rstrip('/'):
                combo.setCurrentIndex(i)
                return
        combo.setCurrentText(url_val)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15) 
        layout.setContentsMargins(20, 10, 20, 20)
        
        self.tabs = QTabWidget()
        self.tabs.setObjectName("MainTabWidget")
        self.tabs.tabBar().setObjectName("MainTabBar")
        self.tabs.tabBar().setExpanding(False)
        
        self.tab_build = QWidget()
        self.tab_pref_scroll, _cnt_pref, self.lay_pref = self._create_scroll_tab()
        self.tab_about = QWidget()

        self.tabs.addTab(self.tab_build, get_svg_icon('package', "#5F6368", 16), _("Build Settings"))
        self.tabs.addTab(self.tab_pref_scroll, get_svg_icon('settings', "#5F6368", 16), _("Preferences"))
        self.tabs.addTab(self.tab_about, get_svg_icon('info', "#5F6368", 16), _("About"))
        
        self.build_build_master_tab()
        self.build_pref_tab()
        self.build_about_tab()
        layout.addWidget(self.tabs)
        
        btn_lay = QHBoxLayout()
        btn_lay.setContentsMargins(0, 5, 0, 0)
        btn_lay.setSpacing(12)
        
        self.btn_reset = AnimatedButton("")
        self.btn_reset.setFixedSize(44, 44)
        self.btn_reset.setIcon(get_svg_icon('refresh', "#5F6368"))
        self.btn_reset.setToolTip(_("Reset to Default Config"))
        self.btn_reset.setStyleSheet(self.parent_win.icon_btn_style)
        self.btn_reset.clicked.connect(self.parent_win.reset_all)
        btn_lay.addWidget(self.btn_reset)
        
        self.btn_save = AnimatedButton(_("Save & Return"))
        self.btn_save.setFixedHeight(44)
        self.btn_save.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_save.setIcon(get_svg_icon('check', "white"))
        self.btn_save.setStyleSheet(self.parent_win.primary_btn_style)
        self.btn_save.clicked.connect(self.parent_win.save_settings_and_return)
        btn_lay.addWidget(self.btn_save)

        self.btn_back = AnimatedButton("")
        self.btn_back.setFixedSize(44, 44)
        self.btn_back.setIcon(get_svg_icon('back', "#5F6368"))
        self.btn_back.setToolTip(_("Cancel & Return"))
        self.btn_back.setStyleSheet(self.parent_win.icon_btn_style)
        self.btn_back.clicked.connect(self.parent_win.show_main)
        btn_lay.addWidget(self.btn_back)
        
        layout.addLayout(btn_lay)

    def build_build_master_tab(self):
        main_lay = QVBoxLayout(self.tab_build)
        main_lay.setContentsMargins(0, 10, 0, 0)
        
        self.sub_tabs = QTabWidget()
        self.sub_tabs.setObjectName("SubTabWidget")
        self.sub_tabs.tabBar().setObjectName("SubTabBar")
        self.sub_tabs.tabBar().setExpanding(False)
        
        sub_scroll1, _cnt1, lay_sub1 = self._create_scroll_tab()
        sub_scroll2, _cnt2, lay_sub2 = self._create_scroll_tab() 
        sub_scroll3, _cnt3, lay_sub3 = self._create_scroll_tab()
        sub_scroll4, _cnt4, lay_sub4 = self._create_scroll_tab()
        sub_scroll5, _cnt5, lay_sub5 = self._create_scroll_tab()
        
        self.sub_tabs.addTab(sub_scroll1, _("🚀 Engine"))
        self.sub_tabs.addTab(sub_scroll2, _("📦 Dependencies"))
        self.sub_tabs.addTab(sub_scroll3, _("📂 Resources"))
        self.sub_tabs.addTab(sub_scroll4, _("⚡ Optimization"))
        self.sub_tabs.addTab(sub_scroll5, _("🗺️ Package Map"))
        
        self.card_engine, c_lay_engine = self._create_card(_("Engine & Environment"))
        self.form_engine = QFormLayout()
        self.form_engine.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.form_engine.setSpacing(15)
        
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["PyInstaller", "Nuitka"])
        setup_combo_white_theme(self.engine_combo)
        self.engine_combo.currentIndexChanged.connect(self.on_engine_changed)

        self.engine_desc_lbl = QLabel()
        self.engine_desc_lbl.setWordWrap(True)
        self.engine_desc_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.engine_desc_lbl.setStyleSheet("QLabel { background-color: #f8fafc; color: #475569; border: 1px solid #e2e8f0; border-radius: 6px; padding: 9px 18px; font-size: 12px; }")

        engine_cont = QWidget()
        lay_eng = QVBoxLayout(engine_cont)
        lay_eng.setContentsMargins(0, 0, 0, 0)
        lay_eng.setSpacing(4)
        lay_eng.addWidget(self.engine_combo)
        lay_eng.addWidget(self.engine_desc_lbl)
        
        self.python_path_combo = QComboBox()
        self.python_path_combo.setEditable(True)
        self.python_path_combo.setPlaceholderText(_("Leave blank to auto-detect system default Python"))
        setup_combo_white_theme(self.python_path_combo, min_view_width=520)
        
        self.btn_python_path = QPushButton(_("Browse"))
        self.btn_python_path.setProperty("class", "ToolBtn")
        self.btn_python_path.clicked.connect(self.select_python_path)
        
        py_cont = QWidget()
        h_py = QHBoxLayout(py_cont)
        h_py.setContentsMargins(0,0,0,0)
        h_py.addWidget(self.python_path_combo, 1)
        h_py.addWidget(self.btn_python_path)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText(_("Leave blank to auto-match script name"))
        
        self.icon_edit = QLineEdit()
        self.icon_preview = QLabel()
        self.icon_preview.setFixedSize(24, 24)
        self.icon_preview.setScaledContents(True)
        self.icon_edit.textChanged.connect(self.update_icon_preview)
        
        self.btn_icon = QPushButton(_("Browse"))
        self.btn_icon.setProperty("class", "ToolBtn")
        self.btn_icon.clicked.connect(self.select_icon)
        
        icon_cont = QWidget()
        h_icon = QHBoxLayout(icon_cont)
        h_icon.setContentsMargins(0,0,0,0)
        h_icon.addWidget(self.icon_edit, 1)
        h_icon.addWidget(self.icon_preview)
        h_icon.addWidget(self.btn_icon)

        self.lbl_eng_title = QLabel(_("Build Engine:"))
        self.lbl_py_title = QLabel(_("Python Interpreter:"))
        self.lbl_app_title = QLabel(_("Output Name:"))
        self.lbl_icon_title = QLabel(_("App Icon:"))

        self.form_engine.addRow(self.lbl_eng_title, engine_cont)
        self.form_engine.addRow(self.lbl_py_title, py_cont)
        self.form_engine.addRow(self.lbl_app_title, self.name_edit)
        self.form_engine.addRow(self.lbl_icon_title, icon_cont)
        c_lay_engine.addLayout(self.form_engine)

        self.card_mode, c_lay_mode = self._create_card(_("Execution Mode"))
        h_mode = QHBoxLayout()
        self.onefile_check = QCheckBox(_("One-File Mode (--onefile)"))
        self.noconsole_check = QCheckBox(_("Hide Console (--noconsole)"))
        h_mode.addWidget(self.onefile_check)
        h_mode.addWidget(self.noconsole_check)
        h_mode.addStretch()
        c_lay_mode.addLayout(h_mode)

        lay_sub1.addWidget(self.card_engine)
        lay_sub1.addWidget(self.card_mode)
        lay_sub1.addStretch()

        self.card_deps, c_lay_deps = self._create_card(_("Mirrors & Scanner"))
        self.form_deps = QFormLayout()
        self.form_deps.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.form_deps.setSpacing(15)
        
        self.pip_source_combo = QComboBox()
        self.pip_source_combo.setEditable(True)
        setup_combo_white_theme(self.pip_source_combo, min_view_width=520)

        self.pip_backup_combo = QComboBox()
        self.pip_backup_combo.setEditable(True)
        setup_combo_white_theme(self.pip_backup_combo, min_view_width=520)

        for name, url in PYPI_MIRRORS_GLOBAL:
            display_text = f"{name}: {url}"
            self.pip_source_combo.addItem(display_text, url)
            self.pip_backup_combo.addItem(display_text, url)
            
        self.pip_source_combo.currentTextChanged.connect(self._check_pip_mirrors)
        self.pip_backup_combo.currentTextChanged.connect(self._check_pip_mirrors)

        self.reqs_file_edit = QLineEdit()
        self.reqs_file_edit.setPlaceholderText(_("Leave blank to auto-search requirements.txt in current directory"))
        self.btn_reqs = QPushButton(_("Browse"))
        self.btn_reqs.setProperty("class", "ToolBtn")
        self.btn_reqs.clicked.connect(self.select_reqs_file)
        
        reqs_cont = QWidget()
        h_reqs = QHBoxLayout(reqs_cont)
        h_reqs.setContentsMargins(0,0,0,0)
        h_reqs.addWidget(self.reqs_file_edit, 1)
        h_reqs.addWidget(self.btn_reqs)
        
        self.hidden_edit = QLineEdit()
        self.hidden_edit.setPlaceholderText(_("Comma separated (e.g. pandas, PyQt5)"))
        self.btn_scan = QPushButton(_("AST Scan"))
        self.btn_scan.setProperty("class", "ToolBtn")
        self.btn_scan.clicked.connect(self.auto_scan_hidden)
        
        hid_cont = QWidget()
        h_hid = QHBoxLayout(hid_cont)
        h_hid.setContentsMargins(0,0,0,0)
        h_hid.addWidget(self.hidden_edit, 1)
        h_hid.addWidget(self.btn_scan)

        self.exclude_edit = QLineEdit()
        self.exclude_edit.setPlaceholderText(_("Comma separated (e.g. tkinter, matplotlib)"))
        
        self.lbl_pip_main = QLabel(_("Primary PIP Index:"))
        self.lbl_pip_backup = QLabel(_("Backup PIP Index:"))
        self.lbl_reqs = QLabel(_("Requirements File:"))
        self.lbl_hidden = QLabel(_("Hidden Imports:"))
        self.lbl_exclude = QLabel(_("Exclude Modules:"))

        self.form_deps.addRow(self.lbl_pip_main, self.pip_source_combo)
        self.form_deps.addRow(self.lbl_pip_backup, self.pip_backup_combo)
        self.form_deps.addRow(self.lbl_reqs, reqs_cont)
        self.form_deps.addRow(self.lbl_hidden, hid_cont)
        self.form_deps.addRow(self.lbl_exclude, self.exclude_edit)
        c_lay_deps.addLayout(self.form_deps)
        
        c_lay_deps.addSpacing(5)
        g_dep = QGridLayout()
        g_dep.setSpacing(10)
        
        self.venv_check = QCheckBox(_("Use Virtual Environment (Recommended)"))
        self.reqs_check = QCheckBox(_("Install requirements.txt"))
        self.pipreqs_check = QCheckBox(_("Analyze Dependencies (pipreqs)"))
        self.pipreqs_dir_check = QCheckBox(_("Scan Entire Folder"))
        
        g_dep.addWidget(self.venv_check, 0, 0)
        g_dep.addWidget(self.reqs_check, 0, 1)
        g_dep.addWidget(self.pipreqs_check, 1, 0)
        g_dep.addWidget(self.pipreqs_dir_check, 1, 1)
        c_lay_deps.addLayout(g_dep)

        lay_sub2.addWidget(self.card_deps)
        lay_sub2.addStretch()

        self.card_res, c_lay_res = self._create_card(_("Additional Resources (Drag & Drop Supported)"))
        self.add_data_list = DropListWidget()
        self.add_data_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.add_data_list.setFixedHeight(180)
        self.add_data_list.setToolTip(_("Double-click to edit target path; Drag & drop supported"))
        
        self.add_data_list.itemDoubleClicked.connect(self.edit_resource)
        self.add_data_list.itemsDropped.connect(self.on_resources_dropped)
        c_lay_res.addWidget(self.add_data_list)
        
        btn_res_lay = QHBoxLayout()
        self.btn_add_file = QPushButton(_("Add File"))
        self.btn_add_file.setProperty("class", "ToolBtn")
        self.btn_add_file.clicked.connect(self.add_resource_files)
        
        self.btn_add_dir = QPushButton(_("Add Dir"))
        self.btn_add_dir.setProperty("class", "ToolBtn")
        self.btn_add_dir.clicked.connect(self.add_resource_dir)
        
        self.btn_del_res = QPushButton(_("Remove Selected"))
        self.btn_del_res.setProperty("class", "ToolBtn")
        self.btn_del_res.clicked.connect(self.del_resource)
        
        self.btn_clear_res = QPushButton(_("Clear All"))
        self.btn_clear_res.setProperty("class", "ToolBtn")
        self.btn_clear_res.clicked.connect(self.clear_resource)
        
        btn_res_lay.addWidget(self.btn_add_file)
        btn_res_lay.addWidget(self.btn_add_dir)
        btn_res_lay.addWidget(self.btn_del_res)
        btn_res_lay.addWidget(self.btn_clear_res)
        btn_res_lay.addStretch()
        c_lay_res.addLayout(btn_res_lay)

        lay_sub3.addWidget(self.card_res)
        lay_sub3.addStretch()

        self.card_opt, c_lay_opt = self._create_card(_("Performance Optimization"))
        self.form_opt = QFormLayout()
        self.form_opt.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.form_opt.setSpacing(15)
        
        self.cores_spin = QSpinBox()
        self.cores_spin.setRange(1, os.cpu_count() or 4)
        self.cores_spin.setValue(os.cpu_count() or 2)
        
        self.lbl_cpu_cores = QLabel(_("CPU Cores:"))
        self.form_opt.addRow(self.lbl_cpu_cores, self.cores_spin)
        
        self.upx_check = QCheckBox(_("Enable UPX Compression"))
        self.upx_check.toggled.connect(self.on_upx_toggled)
        
        self.upx_path_edit = QLineEdit()
        self.upx_path_edit.setPlaceholderText(_("Leave blank to auto-detect from environment variables"))
        
        self.btn_upx = QPushButton(_("Browse"))
        self.btn_upx.setProperty("class", "ToolBtn")
        self.btn_upx.clicked.connect(self.select_upx_path)
        
        self.upx_path_container = QWidget()
        h_upx = QHBoxLayout(self.upx_path_container)
        h_upx.setContentsMargins(0,0,0,0)
        h_upx.addWidget(self.upx_path_edit, 1)
        h_upx.addWidget(self.btn_upx)
        self.upx_path_container.setVisible(False)
        
        h_upx_row = QHBoxLayout()
        h_upx_row.addWidget(self.upx_check)
        h_upx_row.addWidget(self.upx_path_container)
        
        self.lbl_upx_path = QLabel(_("UPX Path:"))
        self.form_opt.addRow(self.lbl_upx_path, h_upx_row)
        
        self.lite_mode_check = QCheckBox(_("Lite Mode (Exclude Dev/Test Dependencies)"))
        self.lite_mode_check.setStyleSheet("color: #D93025; font-weight: bold;")
        self.lite_mode_check.setToolTip(_("Dynamically exclude redundant dependencies in build environment, improving speed and reducing size."))
        
        c_lay_opt.addLayout(self.form_opt)
        c_lay_opt.addWidget(self.lite_mode_check)

        self.card_ver, c_lay_ver = self._create_card(_("Lock Core Dependencies"))
        self.form_ver = QFormLayout()
        self.form_ver.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.form_ver.setSpacing(15)
        
        self.pyi_ver_edit = QLineEdit()
        self.nuitka_ver_edit = QLineEdit()
        self.pipreqs_ver_edit = QLineEdit()
        
        self.lbl_pyi_ver = QLabel(_("PyInstaller Version:"))
        self.lbl_nuitka_ver = QLabel(_("Nuitka Version:"))
        self.lbl_pipreqs_ver = QLabel(_("Pipreqs Version:"))
        
        self.form_ver.addRow(self.lbl_pyi_ver, self.pyi_ver_edit)
        self.form_ver.addRow(self.lbl_nuitka_ver, self.nuitka_ver_edit)
        self.form_ver.addRow(self.lbl_pipreqs_ver, self.pipreqs_ver_edit)
        c_lay_ver.addLayout(self.form_ver)

        lay_sub4.addWidget(self.card_opt)
        lay_sub4.addWidget(self.card_ver)
        lay_sub4.addStretch()

        self.card_map, c_lay_map = self._create_card(_("Package Name Mappings"))
        self.mapping_table = QTableWidget()
        self.mapping_table.setItemDelegate(TableItemDelegate(self.mapping_table))
        self.mapping_table.setColumnCount(2)
        self.mapping_table.setHorizontalHeaderLabels([_("Import Name"), _("PyPI Package Name")])
        self.mapping_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.mapping_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.mapping_table.setFixedHeight(260)
        c_lay_map.addWidget(self.mapping_table)

        btn_map_lay = QHBoxLayout()
        self.btn_add_map = QPushButton(_("Add Mapping"))
        self.btn_add_map.setProperty("class", "ToolBtn")
        self.btn_add_map.clicked.connect(self.add_mapping_item)
        
        self.btn_del_map = QPushButton(_("Remove Selected"))
        self.btn_del_map.setProperty("class", "ToolBtn")
        self.btn_del_map.clicked.connect(self.delete_mapping_item)
        
        self.btn_reset_map = QPushButton(_("Restore Defaults"))
        self.btn_reset_map.setProperty("class", "ToolBtn")
        self.btn_reset_map.clicked.connect(self.reset_mapping_default)
        
        btn_map_lay.addWidget(self.btn_add_map)
        btn_map_lay.addWidget(self.btn_del_map)
        btn_map_lay.addWidget(self.btn_reset_map)
        btn_map_lay.addStretch()
        c_lay_map.addLayout(btn_map_lay)

        lay_sub5.addWidget(self.card_map)
        lay_sub5.addStretch()
        
        main_lay.addWidget(self.sub_tabs)
        self.on_engine_changed()

    def build_pref_tab(self):
        self.card_lang, c_lay_lang = self._create_card(_("UI Language:"))
        form_lang = QFormLayout()
        self.lang_combo = QComboBox()
        
        for code, name in I18N.get_available_languages().items():
            self.lang_combo.addItem(name, code)
            
        setup_combo_white_theme(self.lang_combo)
        
        self.lbl_lang_title = QLabel(_("UI Language:"))
        form_lang.addRow(self.lbl_lang_title, self.lang_combo)
        c_lay_lang.addLayout(form_lang)

        self.card_meta, c_lay_meta = self._create_card(_("App Metadata & Presets"))
        self.form_meta = QFormLayout()
        self.form_meta.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.form_meta.setSpacing(15)
        
        self.ver_ver = QLineEdit("1.0.0")
        self.ver_comp = QLineEdit("My Studio")
        self.ver_desc = QLineEdit("Python Executable")
        
        self.lbl_ver_title = QLabel(_("Version:"))
        self.lbl_company_title = QLabel(_("Author/Company:"))
        self.lbl_desc_title = QLabel(_("Description:"))
        
        self.form_meta.addRow(self.lbl_ver_title, self.ver_ver)
        self.form_meta.addRow(self.lbl_company_title, self.ver_comp)
        self.form_meta.addRow(self.lbl_desc_title, self.ver_desc)
        c_lay_meta.addLayout(self.form_meta)

        c_lay_meta.addSpacing(10)
        h_preset = QHBoxLayout()
        self.btn_exp_preset = QPushButton(_("Export Preset..."))
        self.btn_exp_preset.setProperty("class", "ToolBtn")
        self.btn_exp_preset.clicked.connect(self.export_preset)
        
        self.btn_imp_preset = QPushButton(_("Import Preset..."))
        self.btn_imp_preset.setProperty("class", "ToolBtn")
        self.btn_imp_preset.clicked.connect(self.import_preset)
        
        h_preset.addWidget(self.btn_exp_preset)
        h_preset.addWidget(self.btn_imp_preset)
        h_preset.addStretch()
        c_lay_meta.addLayout(h_preset)

        self.card1, lay1 = self._create_card(_("Output Location"))
        self.out_mode_combo = QComboBox()
        self.out_mode_combo.addItems([_("Source File Directory"), _("Custom Directory")])
        setup_combo_white_theme(self.out_mode_combo)
        self.out_mode_combo.currentIndexChanged.connect(self.on_out_mode_changed)
        
        self.out_dir_edit = QLineEdit()
        self.btn_out_dir = QPushButton(_("Browse"))
        self.btn_out_dir.setProperty("class", "ToolBtn")
        self.btn_out_dir.clicked.connect(self.select_out_dir)
        
        self.out_dir_container = QWidget()
        h_out_dir = QHBoxLayout(self.out_dir_container)
        h_out_dir.setContentsMargins(0, 0, 0, 0)
        h_out_dir.addWidget(self.out_dir_edit, 1)
        h_out_dir.addWidget(self.btn_out_dir)
        self.out_dir_container.setVisible(False)
        
        self.form_out = QFormLayout()
        self.form_out.setVerticalSpacing(15)
        self.form_out.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        
        self.lbl_out_rule_title = QLabel(_("Output Rule:"))
        self.lbl_target_out_title = QLabel(_("Target Directory:"))
        
        self.form_out.addRow(self.lbl_out_rule_title, self.out_mode_combo)
        self.form_out.addRow(self.lbl_target_out_title, self.out_dir_container)
        lay1.addLayout(self.form_out)

        self.card2, lay2 = self._create_card(_("Preferences & System Behavior"))
        lay2.setSpacing(16)
        
        self.concise_log_check = QCheckBox(_("Concise Log Output"))
        self.auto_save_log_check = QCheckBox(_("Auto-save Build Log"))
        self.auto_icon_check = QCheckBox(_("Auto Extract Icon"))
        self.clean_all_check = QCheckBox(_("Clean Temporary Cache After Build"))
        self.sound_notify_check = QCheckBox(_("Sound Notification"))
        
        for chk in (self.concise_log_check, self.auto_save_log_check, self.auto_icon_check, self.clean_all_check, self.sound_notify_check):
            lay2.addWidget(chk)
            
        self.lay_pref.addWidget(self.card_lang)
        self.lay_pref.addWidget(self.card_meta)
        self.lay_pref.addWidget(self.card1)
        self.lay_pref.addWidget(self.card2)
        self.lay_pref.addStretch()

    def build_about_tab(self):
        main_lay = QVBoxLayout(self.tab_about)
        main_lay.setContentsMargins(40, 20, 40, 20)
        main_lay.setSpacing(15)
        main_lay.addStretch(1)
        
        logo_lbl = QLabel()
        icon_path = get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            high_res_pixmap = QIcon(icon_path).pixmap(256, 256)
            if not high_res_pixmap.isNull():
                logo_pixmap = high_res_pixmap.scaled(110, 110, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                logo_lbl.setPixmap(logo_pixmap)
            else:
                logo_lbl.setPixmap(get_svg_pixmap('package', color="#1A73E8", size=110))
        else:
            logo_lbl.setPixmap(get_svg_pixmap('package', color="#1A73E8", size=110))
            
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_lay.addWidget(logo_lbl)
        
        title_lbl = QLabel(__app_name__)
        title_lbl.setStyleSheet("font-size: 36px; font-weight: 900; color: #202124; letter-spacing: -1px; margin-top: 10px;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_lay.addWidget(title_lbl)
        
        ver_lbl = QLabel(f"Version {__version__}  ·  GPL-3.0")
        ver_lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #1A73E8; margin-bottom: 5px;")
        ver_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_lay.addWidget(ver_lbl)
        
        self.about_desc_lbl = QLabel(_("A Cross-platform Python Packaging GUI Tool based on PyInstaller & Nuitka"))
        self.about_desc_lbl.setStyleSheet("font-size: 14px; color: #5f6368;")
        self.about_desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_lay.addWidget(self.about_desc_lbl)
        main_lay.addSpacing(25)
        
        btn_lay = QHBoxLayout()
        btn_lay.setSpacing(15)
        btn_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        def create_link_btn(text, url):
            btn = QPushButton(text)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton { background-color: #f1f3f4; color: #3c4043; border: none; border-radius: 8px; padding: 10px 20px; font-size: 13px; font-weight: bold; }
                QPushButton:hover { background-color: #e8eaed; color: #1A73E8; }
                QPushButton:pressed { background-color: #dadce0; }
            """)
            btn.clicked.connect(lambda: __import__('webbrowser').open(url))
            return btn
            
        btn_github = create_link_btn("GitHub Repository", "https://github.com/qwejay/QPyPack")
        btn_issue = create_link_btn("Issues & Feedback", "https://github.com/qwejay/QPyPack/issues")
        btn_pypi = create_link_btn("PyPI Home", "https://pypi.org/project/qpypack/")
        
        btn_lay.addWidget(btn_github)
        btn_lay.addWidget(btn_issue)
        btn_lay.addWidget(btn_pypi)
        
        main_lay.addLayout(btn_lay)
        main_lay.addStretch(1) 
        
        rights_lbl = QLabel(f"Copyright © {__company__}.")
        rights_lbl.setStyleSheet("font-size: 12px; color: #bdc1c6; font-weight: bold;")
        rights_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_lay.addWidget(rights_lbl)

    def retranslate_ui(self):
        self.tabs.setTabText(0, _("Build Settings"))
        self.tabs.setTabText(1, _("Preferences"))
        self.tabs.setTabText(2, _("About"))
        
        self.sub_tabs.setTabText(0, _("🚀 Engine"))
        self.sub_tabs.setTabText(1, _("📦 Dependencies"))
        self.sub_tabs.setTabText(2, _("📂 Resources"))
        self.sub_tabs.setTabText(3, _("⚡ Optimization"))
        self.sub_tabs.setTabText(4, _("🗺️ Package Map"))
        
        self.card_engine.findChild(QLabel, "CardTitle").setText(_("Engine & Environment"))
        self.card_mode.findChild(QLabel, "CardTitle").setText(_("Execution Mode"))
        self.card_deps.findChild(QLabel, "CardTitle").setText(_("Mirrors & Scanner"))
        self.card_res.findChild(QLabel, "CardTitle").setText(_("Additional Resources (Drag & Drop Supported)"))
        self.card_opt.findChild(QLabel, "CardTitle").setText(_("Performance Optimization"))
        self.card_ver.findChild(QLabel, "CardTitle").setText(_("Lock Core Dependencies"))
        self.card_map.findChild(QLabel, "CardTitle").setText(_("Package Name Mappings"))
        self.card_lang.findChild(QLabel, "CardTitle").setText(_("UI Language:"))
        self.card_meta.findChild(QLabel, "CardTitle").setText(_("App Metadata & Presets"))
        self.card1.findChild(QLabel, "CardTitle").setText(_("Output Location"))
        self.card2.findChild(QLabel, "CardTitle").setText(_("Preferences & System Behavior"))

        self.lbl_eng_title.setText(_("Build Engine:"))
        self.lbl_py_title.setText(_("Python Interpreter:"))
        self.lbl_app_title.setText(_("Output Name:"))
        self.lbl_icon_title.setText(_("App Icon:"))
        self.lbl_pip_main.setText(_("Primary PIP Index:"))
        self.lbl_pip_backup.setText(_("Backup PIP Index:"))
        self.lbl_reqs.setText(_("Requirements File:"))
        self.lbl_hidden.setText(_("Hidden Imports:"))
        self.lbl_exclude.setText(_("Exclude Modules:"))
        self.lbl_cpu_cores.setText(_("CPU Cores:"))
        self.lbl_upx_path.setText(_("UPX Path:"))
        self.lbl_pyi_ver.setText(_("PyInstaller Version:"))
        self.lbl_nuitka_ver.setText(_("Nuitka Version:"))
        self.lbl_pipreqs_ver.setText(_("Pipreqs Version:"))
        self.lbl_lang_title.setText(_("UI Language:"))
        self.lbl_ver_title.setText(_("Version:"))
        self.lbl_company_title.setText(_("Author/Company:"))
        self.lbl_desc_title.setText(_("Description:"))
        self.lbl_out_rule_title.setText(_("Output Rule:"))
        self.lbl_target_out_title.setText(_("Target Directory:"))

        self.btn_save.setText(_("Save & Return"))
        self.btn_python_path.setText(_("Browse"))
        self.btn_icon.setText(_("Browse"))
        self.btn_reqs.setText(_("Browse"))
        self.btn_scan.setText(_("AST Scan"))
        self.btn_upx.setText(_("Browse"))
        self.btn_out_dir.setText(_("Browse"))
        self.btn_add_file.setText(_("Add File"))
        self.btn_add_dir.setText(_("Add Dir"))
        self.btn_del_res.setText(_("Remove Selected"))
        self.btn_clear_res.setText(_("Clear All"))
        self.btn_add_map.setText(_("Add Mapping"))
        self.btn_del_map.setText(_("Remove Selected"))
        self.btn_reset_map.setText(_("Restore Defaults"))
        self.btn_exp_preset.setText(_("Export Preset..."))
        self.btn_imp_preset.setText(_("Import Preset..."))
        
        self.python_path_combo.setPlaceholderText(_("Leave blank to auto-detect system default Python"))
        self.name_edit.setPlaceholderText(_("Leave blank to auto-match script name"))
        self.reqs_file_edit.setPlaceholderText(_("Leave blank to auto-search requirements.txt in current directory"))
        self.hidden_edit.setPlaceholderText(_("Comma separated (e.g. pandas, PyQt5)"))
        self.exclude_edit.setPlaceholderText(_("Comma separated (e.g. tkinter, matplotlib)"))
        self.upx_path_edit.setPlaceholderText(_("Leave blank to auto-detect from environment variables"))

        self.onefile_check.setText(_("One-File Mode (--onefile)"))
        self.noconsole_check.setText(_("Hide Console (--noconsole)"))
        self.venv_check.setText(_("Use Virtual Environment (Recommended)"))
        self.reqs_check.setText(_("Install requirements.txt"))
        self.pipreqs_check.setText(_("Analyze Dependencies (pipreqs)"))
        self.pipreqs_dir_check.setText(_("Scan Entire Folder"))
        self.upx_check.setText(_("Enable UPX Compression"))
        self.lite_mode_check.setText(_("Lite Mode (Exclude Dev/Test Dependencies)"))
        
        self.concise_log_check.setText(_("Concise Log Output"))
        self.auto_save_log_check.setText(_("Auto-save Build Log"))
        self.auto_icon_check.setText(_("Auto Extract Icon"))
        self.clean_all_check.setText(_("Clean Temporary Cache After Build"))
        self.sound_notify_check.setText(_("Sound Notification"))
        
        self.out_mode_combo.setItemText(0, _("Source File Directory"))
        self.out_mode_combo.setItemText(1, _("Custom Directory"))
        self.mapping_table.setHorizontalHeaderLabels([_("Import Name"), _("PyPI Package Name")])
        self.about_desc_lbl.setText(_("A Cross-platform Python Packaging GUI Tool based on PyInstaller & Nuitka"))

        self.btn_reset.setToolTip(_("Reset to Default Config"))
        self.btn_back.setToolTip(_("Cancel & Return"))
        self.add_data_list.setToolTip(_("Double-click to edit target path; Drag & drop supported"))
        self.lite_mode_check.setToolTip(_("Dynamically exclude redundant dependencies in build environment, improving speed and reducing size."))
        self.on_engine_changed()

    def populate_python_combo(self, py_dict):
        current_text = self.python_path_combo.currentText().strip()
        self.python_path_combo.clear()
        for path, ver in py_dict.items():
            self.python_path_combo.addItem(f"{path} (Python {ver})", path)
            
        if not current_text: current_text = get_python_executable()
            
        if current_text:
            clean_text = current_text
            if " (Python " in clean_text: clean_text = clean_text.split(" (Python ")[0].strip()
            clean_text = os.path.normpath(clean_text).lower()
            
            found = False
            for idx in range(self.python_path_combo.count()):
                item_path = self.python_path_combo.itemData(idx)
                if item_path and os.path.normpath(item_path).lower() == clean_text:
                    self.python_path_combo.setCurrentIndex(idx)
                    found = True
                    break
            if not found: self.python_path_combo.setCurrentText(current_text)

    def populate_mapping_table(self, mappings_dict):
        self.mapping_table.setRowCount(0)
        for imp_name, pypi_name in mappings_dict.items():
            row = self.mapping_table.rowCount()
            self.mapping_table.insertRow(row)
            self.mapping_table.setItem(row, 0, QTableWidgetItem(imp_name))
            self.mapping_table.setItem(row, 1, QTableWidgetItem(pypi_name))

    def add_mapping_item(self):
        imp_name, ok1 = QInputDialog.getText(self, _("Add Mapping"), "Import name (e.g. cv2):")
        if not ok1 or not imp_name.strip(): return
        pypi_name, ok2 = QInputDialog.getText(self, _("Add Mapping"), f"PyPI package name for [{imp_name.strip()}]:")
        if not ok2 or not pypi_name.strip(): return
        
        row = self.mapping_table.rowCount()
        self.mapping_table.insertRow(row)
        self.mapping_table.setItem(row, 0, QTableWidgetItem(imp_name.strip()))
        self.mapping_table.setItem(row, 1, QTableWidgetItem(pypi_name.strip()))

    def delete_mapping_item(self):
        rows = set(item.row() for item in self.mapping_table.selectedItems())
        for r in sorted(rows, reverse=True): self.mapping_table.removeRow(r)

    def reset_mapping_default(self):
        self.populate_mapping_table(DEFAULT_MAPPINGS)
        if hasattr(self.parent_win, "show_notification"):
            self.parent_win.show_notification(_("Package mappings have been reset to defaults."))

    def export_preset(self):
        fp, _filter = QFileDialog.getSaveFileName(self, _("Export Preset..."), "project_config.qpypack", "QPyPack Presets (*.qpypack *.json)")
        if fp:
            try:
                data = {
                    "engine": self.engine_combo.currentText(),
                    "onefile": self.onefile_check.isChecked(),
                    "noconsole": self.noconsole_check.isChecked(),
                    "icon": self.icon_edit.text(),
                    "app_name": self.name_edit.text(),
                    "ver_ver": self.ver_ver.text(),
                    "ver_comp": self.ver_comp.text(),
                    "ver_desc": self.ver_desc.text(),
                    "hidden_imports": self.hidden_edit.text(),
                    "exclude_modules": self.exclude_edit.text(),
                    "use_venv": self.venv_check.isChecked(),
                    "use_reqs": self.reqs_check.isChecked(),
                    "use_pipreqs": self.pipreqs_check.isChecked(),
                    "use_pipreqs_dir": self.pipreqs_dir_check.isChecked(),
                    "reqs_file": self.reqs_file_edit.text(),
                    "pip_source": self._get_url_from_combo(self.pip_source_combo),
                    "pip_backup": self._get_url_from_combo(self.pip_backup_combo),
                    "lite_mode": self.lite_mode_check.isChecked(),
                    "add_data_list": [self.add_data_list.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.add_data_list.count())]
                }
                Path(fp).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
                if hasattr(self.parent_win, "show_notification"):
                    self.parent_win.show_notification(_("Config preset exported to: {path}", path=fp))
            except Exception as e:
                if hasattr(self.parent_win, "show_error_log"):
                    self.parent_win.show_error_log(_("[ERROR] Failed to export preset file: {error}", error=str(e)))

    def import_preset(self):
        fp, _filter = QFileDialog.getOpenFileName(self, _("Import Preset..."), "", "QPyPack Presets (*.qpypack *.json);;All Files (*)")
        if fp:
            try:
                data = json.loads(Path(fp).read_text(encoding='utf-8'))
                if "engine" in data: self.engine_combo.setCurrentText(data["engine"])
                if "onefile" in data: self.onefile_check.setChecked(bool(data["onefile"]))
                if "noconsole" in data: self.noconsole_check.setChecked(bool(data["noconsole"]))
                if "icon" in data: self.icon_edit.setText(data["icon"])
                if "app_name" in data: self.name_edit.setText(data["app_name"])
                if "ver_ver" in data: self.ver_ver.setText(data["ver_ver"])
                if "ver_comp" in data: self.ver_comp.setText(data["ver_comp"])
                if "ver_desc" in data: self.ver_desc.setText(data["ver_desc"])
                if "hidden_imports" in data: self.hidden_edit.setText(data["hidden_imports"])
                if "exclude_modules" in data: self.exclude_edit.setText(data["exclude_modules"])
                if "use_venv" in data: self.venv_check.setChecked(bool(data["use_venv"]))
                if "use_reqs" in data: self.reqs_check.setChecked(bool(data["use_reqs"]))
                if "use_pipreqs" in data: self.pipreqs_check.setChecked(bool(data["use_pipreqs"]))
                if "use_pipreqs_dir" in data: self.pipreqs_dir_check.setChecked(bool(data["use_pipreqs_dir"]))
                if "reqs_file" in data: self.reqs_file_edit.setText(data["reqs_file"])
                if "pip_source" in data: self._set_combo_value(self.pip_source_combo, data["pip_source"])
                if "pip_backup" in data: self._set_combo_value(self.pip_backup_combo, data["pip_backup"])
                if "lite_mode" in data: self.lite_mode_check.setChecked(bool(data["lite_mode"]))
                if "add_data_list" in data:
                    self.add_data_list.clear()
                    for item in data["add_data_list"]:
                        if isinstance(item, (list, tuple)) and len(item) == 3:
                            self._add_resource_item(item[0], item[1], item[2])
                if hasattr(self.parent_win, "show_notification"):
                    self.parent_win.show_notification(_("Config preset imported successfully."))
            except Exception as e:
                if hasattr(self.parent_win, "show_error_log"):
                    self.parent_win.show_error_log(_("[ERROR] Preset file format error or corrupted: {error}", error=str(e)))

    def load_from_config(self):
        config = load_config()
        if 'Settings' in config:
            s = config['Settings']
            lang_code = s.get('language', 'auto')
            for i in range(self.lang_combo.count()):
                if self.lang_combo.itemData(i) == lang_code:
                    self.lang_combo.setCurrentIndex(i); break
                    
            self.engine_combo.setCurrentText(s.get('engine', 'PyInstaller'))
            self.onefile_check.setChecked(s.getboolean('onefile', True))
            self.noconsole_check.setChecked(s.getboolean('noconsole', True))
            self.clean_all_check.setChecked(s.getboolean('clean_all', True))
            self.auto_icon_check.setChecked(s.getboolean('auto_icon', True))
            
            pip_main = s.get('pip_index', 'https://pypi.org/simple')
            self._set_combo_value(self.pip_source_combo, pip_main)

            pip_backup = s.get('pip_index_backup', 'https://test.pypi.org/simple')
            self._set_combo_value(self.pip_backup_combo, pip_backup)

            self.venv_check.setChecked(s.getboolean('use_venv', True))
            self.reqs_check.setChecked(s.getboolean('use_reqs', True))
            self.pipreqs_check.setChecked(s.getboolean('use_pipreqs', True))
            self.pipreqs_dir_check.setChecked(s.getboolean('use_pipreqs_dir', False))
            self.reqs_file_edit.setText(s.get('use_reqs_file', ''))
            self.python_path_combo.setCurrentText(s.get('custom_python_path', ''))
            
            if self.upx_check:
                self.upx_check.setChecked(s.getboolean('upx', False))
                self.on_upx_toggled(self.upx_check.isChecked())
            self.upx_path_edit.setText(s.get('upx_path', ''))
            self.cores_spin.setValue(s.getint('cpu_cores', os.cpu_count() or 2))
            self.exclude_edit.setText(s.get('exclude_modules', ''))
            self.out_mode_combo.setCurrentIndex(int(s.get('out_mode', '0')))
            self.out_dir_edit.setText(s.get('custom_out_dir', ''))
            self.on_out_mode_changed(self.out_mode_combo.currentIndex())
            
            self.concise_log_check.setChecked(s.getboolean('concise_log', True))
            self.sound_notify_check.setChecked(s.getboolean('sound_notify', True))
            self.auto_save_log_check.setChecked(s.getboolean('auto_save_log', False))
            self.lite_mode_check.setChecked(s.getboolean('lite_mode', False))
            
            self.pyi_ver_edit.setText(s.get('pyi_version', ''))
            self.nuitka_ver_edit.setText(s.get('nuitka_version', ''))
            self.pipreqs_ver_edit.setText(s.get('pipreqs_version', ''))
            
            self.add_data_list.clear()
            res_str = s.get('add_data_list', '')
            if res_str:
                for part in res_str.split("|||"):
                    if part.count('|') == 2:
                        r_type, src, dst = part.split('|')
                        self._add_resource_item(r_type, src, dst)

        if 'Mappings' in config:
            self.populate_mapping_table(dict(config['Mappings']))

    def save_to_config(self):
        config = load_config()
        if 'Settings' not in config: config['Settings'] = {}
        s = config['Settings']
        
        idx = self.lang_combo.currentIndex()
        new_lang = self.lang_combo.itemData(idx)
        s['language'] = new_lang
        
        s['engine'] = self.engine_combo.currentText()
        s['onefile'] = str(self.onefile_check.isChecked())
        s['noconsole'] = str(self.noconsole_check.isChecked())
        s['clean_all'] = str(self.clean_all_check.isChecked())
        s['auto_icon'] = str(self.auto_icon_check.isChecked())
        
        s['pip_index'] = self._get_url_from_combo(self.pip_source_combo)
        s['pip_index_backup'] = self._get_url_from_combo(self.pip_backup_combo)

        s['use_venv'] = str(self.venv_check.isChecked())
        s['use_reqs'] = str(self.reqs_check.isChecked())
        s['use_pipreqs'] = str(self.pipreqs_check.isChecked())
        s['use_pipreqs_dir'] = str(self.pipreqs_dir_check.isChecked())
        s['use_reqs_file'] = self.reqs_file_edit.text().strip()
        
        raw_py = self.python_path_combo.currentText().strip()
        if " (Python " in raw_py: raw_py = raw_py.split(" (Python ")[0].strip()
        s['custom_python_path'] = raw_py
        
        if self.upx_check: s['upx'] = str(self.upx_check.isChecked())
        s['upx_path'] = self.upx_path_edit.text().strip()
        s['cpu_cores'] = str(self.cores_spin.value())
        s['exclude_modules'] = self.exclude_edit.text().strip()
        s['out_mode'] = str(self.out_mode_combo.currentIndex())
        s['custom_out_dir'] = self.out_dir_edit.text().strip()
        s['concise_log'] = str(self.concise_log_check.isChecked())
        s['sound_notify'] = str(self.sound_notify_check.isChecked())
        s['auto_save_log'] = str(self.auto_save_log_check.isChecked())
        s['lite_mode'] = str(self.lite_mode_check.isChecked())
        
        s['pyi_version'] = self.pyi_ver_edit.text().strip()
        s['nuitka_version'] = self.nuitka_ver_edit.text().strip()
        s['pipreqs_version'] = self.pipreqs_ver_edit.text().strip()
        
        res_list = []
        for i in range(self.add_data_list.count()):
            r_type, src, dst = self.add_data_list.item(i).data(Qt.ItemDataRole.UserRole)
            res_list.append(f"{r_type}|{src}|{dst}")
        s['add_data_list'] = "|||".join(res_list)

        config['Mappings'] = {}
        for r in range(self.mapping_table.rowCount()):
            k = self.mapping_table.item(r, 0).text().strip()
            v = self.mapping_table.item(r, 1).text().strip()
            if k and v: config['Mappings'][k] = v
        
        save_config(config)
        I18N.set_language(new_lang)

    def _check_pip_mirrors(self):
        sender = self.sender()
        src_text = self.pip_source_combo.currentText()
        bak_text = self.pip_backup_combo.currentText()
        
        if src_text == bak_text and src_text.strip() != "":
            if sender == self.pip_source_combo:
                for i in range(self.pip_backup_combo.count()):
                    if self.pip_backup_combo.itemText(i) != src_text:
                        self.pip_backup_combo.blockSignals(True)
                        self.pip_backup_combo.setCurrentIndex(i)
                        self.pip_backup_combo.blockSignals(False)
                        break
            elif sender == self.pip_backup_combo:
                for i in range(self.pip_source_combo.count()):
                    if self.pip_source_combo.itemText(i) != bak_text:
                        self.pip_source_combo.blockSignals(True)
                        self.pip_source_combo.setCurrentIndex(i)
                        self.pip_source_combo.blockSignals(False)
                        break

    def on_engine_changed(self):
        engine = self.engine_combo.currentText()
        if engine == "PyInstaller":
            self.engine_desc_lbl.setText(_("<b>PyInstaller</b>: Fast build speed, excellent compatibility. Ideal for rapid iteration."))
        else:
            self.engine_desc_lbl.setText(_("<b>Nuitka</b>: Compiles to native C/C++ binary. Better performance and source code protection."))

        if getattr(self, 'upx_check', None) is not None and getattr(self, 'upx_path_container', None) is not None:
            is_pyi = (engine == "PyInstaller")
            self.upx_check.setVisible(is_pyi)
            self.upx_path_container.setVisible(is_pyi and self.upx_check.isChecked())

    def on_upx_toggled(self, checked):
        if getattr(self, 'upx_path_container', None) is not None:
            self.upx_path_container.setVisible(checked)

    def on_out_mode_changed(self, index):
        show_custom = (index == 1)
        if getattr(self, 'out_dir_container', None) is not None:
            self.out_dir_container.setVisible(show_custom)

    def select_out_dir(self):
        d = QFileDialog.getExistingDirectory(self, _("Target Directory:"))
        if d: self.out_dir_edit.setText(Path(d).resolve().as_posix())

    def select_upx_path(self):
        d = QFileDialog.getExistingDirectory(self, _("UPX Path:"))
        if d: self.upx_path_edit.setText(Path(d).resolve().as_posix())

    def select_reqs_file(self):
        f, _filter = QFileDialog.getOpenFileName(self, _("Requirements File:"), "", "Requirements Files (*.txt);;All Files (*)")
        if f: self.reqs_file_edit.setText(Path(f).resolve().as_posix())

    def select_python_path(self):
        exe_filter = "Executable (*.exe);;All Files (*)" if os.name == 'nt' else "All Files (*)"
        f, _filter = QFileDialog.getOpenFileName(self, _("Python Interpreter:"), "", exe_filter)
        if f: self.python_path_combo.setCurrentText(Path(f).resolve().as_posix())

    def update_icon_preview(self, path):
        if path and Path(path).exists():
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                self.icon_preview.setPixmap(pixmap.scaled(28, 28, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                return
        self.icon_preview.clear()

    def select_icon(self):
        p, _filter = QFileDialog.getOpenFileName(self, _("App Icon:"), "", "Icon Files (*.ico *.svg *.png *.icns)")
        if p: self.icon_edit.setText(Path(p).resolve().as_posix())

    def auto_scan_hidden(self):
        script_path = self.parent_win.script_path
        if not hasattr(self.parent_win, "show_notification"): return
        
        if not script_path:
            return self.parent_win.show_error_log(_("[ERROR] Please load a valid Python source file first!"))
        if is_cloud_locked(script_path):
            return self.parent_win.show_error_log(_("[ERROR] Target file is locked or encrypted by cloud drive. Please decrypt and try again."))
            
        try:
            python_exe = get_python_executable()
            hidden = extract_imports_via_ast(script_path, python_exe)
            hidden = [m for m in hidden if m not in STD_LIBS]
            self.hidden_edit.setText(','.join(hidden))
            self.parent_win.show_notification(_("AST scan completed, found {count} dependencies.", count=len(hidden)))
        except Exception as e: 
            self.parent_win.show_error_log(_("[ERROR] Exception occurred during AST parsing: {error}", error=str(e)))

    def on_resources_dropped(self, paths):
        for p_str in paths:
            p = Path(p_str).resolve()
            if p.is_file():
                self._add_resource_item('file', p.as_posix(), ".")
            elif p.is_dir():
                self._add_resource_item('dir', p.as_posix(), p.name)

    def add_resource_files(self):
        files, _filter = QFileDialog.getOpenFileNames(self, _("Add File"), "", "All Files (*)")
        for f in files:
            src = Path(f).resolve().as_posix()
            self._add_resource_item('file', src, ".")
            
    def add_resource_dir(self):
        folder = QFileDialog.getExistingDirectory(self, _("Add Dir"))
        if folder:
            src = Path(folder).resolve().as_posix()
            dst = Path(folder).name
            self._add_resource_item('dir', src, dst)
            
    def _add_resource_item(self, r_type, src, dst):
        tag = _("File") if r_type == 'file' else _("Directory")
        display_text = f"[{tag}] {src}  ->  {dst}"
        item = QListWidgetItem(display_text)
        item.setData(Qt.ItemDataRole.UserRole, (r_type, src, dst))
        self.add_data_list.addItem(item)

    def edit_resource(self, item=None):
        if not item: item = self.add_data_list.currentItem()
        if not item: return
        r_type, src, dst = item.data(Qt.ItemDataRole.UserRole)
        new_dst, ok = QInputDialog.getText(self, "Edit Path", "Target relative path:", text=dst)
        if ok and new_dst:
            new_dst = new_dst.strip().replace('\\', '/')
            if not new_dst: new_dst = "."
            item.setData(Qt.ItemDataRole.UserRole, (r_type, src, new_dst))
            tag = _("File") if r_type == 'file' else _("Directory")
            item.setText(f"[{tag}] {src}  ->  {new_dst}")

    def del_resource(self):
        for item in self.add_data_list.selectedItems():
            self.add_data_list.takeItem(self.add_data_list.row(item))

    def clear_resource(self):
        self.add_data_list.clear()

class ScriptAnalysisThread(QThread):
    analysis_done = Signal(str, str, str, str, set)

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        app_name = Path(self.path).stem
        version = ""
        author = "My Studio"
        desc = "Python Executable"
        script_imports = set()

        try:
            with open(self.path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(10240)
            
            v_match = re.search(r'^(?:__version__|VERSION|version)\s*=\s*[\'"]([^\'"]+)[\'"]', content, re.M | re.I)
            if v_match: version = v_match.group(1)
                
            c_match = re.search(r'^(?:__company__|COMPANY)\s*=\s*[\'"]([^\'"]+)[\'"]', content, re.M | re.I)
            if c_match: 
                author = c_match.group(1)
            else:
                a_match = re.search(r'^(?:__author__|AUTHOR)\s*=\s*[\'"]([^\'"]+)[\'"]', content, re.M | re.I)
                if a_match: author = a_match.group(1)
                
            n_match = re.search(r'^(?:__title__|__app_name__|APP_NAME)\s*=\s*[\'"]([^\'"]+)[\'"]', content, re.M | re.I)
            if n_match: app_name = n_match.group(1)
                
            d_match = re.search(r'^(?:__description__|DESCRIPTION)\s*=\s*[\'"]([^\'"]+)[\'"]', content, re.M | re.I)
            if d_match: desc = d_match.group(1)
        except: pass

        try:
            python_exe = get_python_executable()
            script_imports = extract_imports_via_ast(self.path, python_exe)
        except: pass

        self.analysis_done.emit(app_name, version, author, desc, script_imports)

class PackingThread(QThread):
    progress = Signal(str)
    finished = Signal(bool, str, list)

    def __init__(self, params):
        super().__init__()
        self.params = params
        self.process = None
        self._is_cancelled = False
        self.venv_dir = None
        self.temp_workpath = None
        self.temp_out_dir = None
        self.temp_dist_dir = None
        self.all_raw_logs = []  

    def cancel(self):
        self._is_cancelled = True
        if self.process:
            try:
                if os.name == "nt": 
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.process.pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
                else: 
                    self.process.kill()
            except: pass

    def run_cmd(self, cmd, cwd=None, timeout=None, silent_error=False):
        if self._is_cancelled: return False
        
        timer = None
        is_timeout = [False]
        cmd_raw_lines = []  
        
        clean_env = os.environ.copy()
        clean_env.pop("PYTHONHOME", None)
        clean_env.pop("PYTHONPATH", None)
        
        clean_env["PYTHONUTF8"] = "1"
        clean_env["PYTHONIOENCODING"] = "utf-8"
        clean_env["LANG"] = "en_US.UTF-8"
        clean_env["LC_ALL"] = "en_US.UTF-8"        
        try:
            kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.STDOUT, "cwd": cwd, 
                      "text": True, "encoding": "utf-8", "errors": "replace", "env": clean_env}
            if os.name == 'nt': kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
            
            self.process = subprocess.Popen(cmd, **kwargs)
            
            if timeout:
                def kill_proc():
                    is_timeout[0] = True
                    try:
                        if os.name == "nt":
                            subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.process.pid)], 
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
                        else:
                            self.process.kill()
                    except: pass
                timer = threading.Timer(timeout, kill_proc)
                timer.start()

            buffer = []
            last_emit = time.time()
            
            def is_noisy_line(l):
                l_lower = l.lower()
                if "error:" in l_lower: return False
                if "upx" in l_lower and ("subprocess.calledprocesserror" in l_lower or "notcompressibleexception" in l_lower):
                    return True
                return any(kw in l_lower for kw in ["warning:", "info:", "deprecation:", "userwarning:", "futurewarning:"])

            for line in self.process.stdout:
                if self._is_cancelled:
                    self.process.terminate()
                    return False
                
                stripped = line.rstrip('\r\n')
                cmd_raw_lines.append(stripped)
                self.all_raw_logs.append(stripped)
                
                if self.params.get('concise_log', True) and is_noisy_line(stripped):
                    continue
                
                buffer.append(stripped)
                if len(buffer) >= 15 or (time.time() - last_emit) > 0.1:
                    self.progress.emit('\n'.join(buffer))
                    buffer.clear()
                    last_emit = time.time()
            
            if buffer: self.progress.emit('\n'.join(buffer))
            self.process.wait()
            
            if is_timeout[0]:
                self.progress.emit(f"[WARN] Command timeout (>{timeout}s)")
                return False
                
            success = self.process.returncode == 0
            if not success and not silent_error and self.params.get('concise_log', True) and cmd_raw_lines:
                self.progress.emit(_("\n!!!!!!!!!! [Diagnostic Traceback: Full raw log due to execution exception in this step] !!!!!!!!!!"))
                self.progress.emit('\n'.join(cmd_raw_lines))
                self.progress.emit("!"*60 + "\n")
                
            return success
        except FileNotFoundError as e:
            self.progress.emit(f"[ERROR] Process error: command or binary missing ({e})")
            return False
        except Exception as e:
            self.progress.emit(f"[ERROR] System execution exception: {e}")
            return False
        finally:
            if timer: timer.cancel()

    def run_pip_install(self, python_exe, pkgs_or_args):
        primary_idx = self.params.get('pip_index_url', '').strip()
        backup_idx = self.params.get('pip_index_backup', '').strip()

        pip_args = []
        if primary_idx: pip_args.extend(["-i", primary_idx])
        if backup_idx and backup_idx != primary_idx: pip_args.extend(["--extra-index-url", backup_idx])

        cmd = [python_exe, "-m", "pip", "install"] + pkgs_or_args + pip_args
        success = self.run_cmd(cmd)

        if not success and backup_idx and backup_idx != primary_idx:
            last_logs = "\n".join(self.all_raw_logs[-15:]).lower()
            if "no matching distribution found" in last_logs or "could not find a version" in last_logs:
                return False

            self.progress.emit(_("[INFO] Switching to backup PyPI source for retrieval: {url}", url=backup_idx))
            fallback_cmd = [python_exe, "-m", "pip", "install"] + pkgs_or_args + ["-i", backup_idx]
            success = self.run_cmd(fallback_cmd)

        return success

    def sanitize_script(self, orig_path: Path):
        if is_cloud_locked(orig_path):
            return None, False, _("Target file is locked or encrypted by cloud drive. Please decrypt and try again.")
        
        if not self.params['noconsole']:
            try:
                raw = orig_path.read_bytes()
                try: code = raw.decode('utf-8-sig')
                except: code = raw.decode(locale.getpreferredencoding(), errors='ignore')
                
                pause_prompt_str = _("\\nProgram execution completed, press Enter to exit...")
                pause_code = "\n" + "#"*30 + "\n" + (
                    "try:\n"
                    "    import sys\n"
                    "    if sys.platform == 'win32':\n"
                    "        import ctypes\n"
                    "        kernel32 = ctypes.windll.kernel32\n"
                    "        process_list = (ctypes.c_uint * 10)()\n"
                    "        num_processes = kernel32.GetConsoleProcessList(process_list, 10)\n"
                    "        if num_processes <= 2:\n"
                    f"            input('{pause_prompt_str}')\n"
                    "except:\n"
                    "    pass\n"
                )
                
                temp_file = Path(tempfile.gettempdir()) / f"_qpypack_temp_entry_{int(time.time())}_{orig_path.name}"
                temp_file.write_text(code + pause_code, encoding='utf-8')
                return temp_file, True, ""
            except Exception as e:
                self.progress.emit(f"[WARN] Pause code injection exception: {e}")
                
        return orig_path, False, ""

    def detect_python_syntax_errors(self):
        script_path = self.params['script_path']
        script_name = Path(script_path).name
        log_text = "\n".join(self.all_raw_logs)
        
        file_line_pat = re.compile(r'File "([^"]+)", line (\d+)', re.I)
        err_type_pat = re.compile(r'^(IndentationError|SyntaxError|TabError):\s*(.*)', re.M)
        
        err_matches = list(err_type_pat.finditer(log_text))
        if err_matches:
            last_err = err_matches[-1]
            err_type = last_err.group(1)
            err_desc = last_err.group(2)
            
            err_pos = last_err.start()
            line_no = "未知"
            file_name = script_name
            
            file_line_matches = list(file_line_pat.finditer(log_text))
            for m in reversed(file_line_matches):
                if m.end() < err_pos:
                    matched_filepath = m.group(1)
                    if matched_filepath.endswith(('.py', '.pyw')):
                        line_no = m.group(2)
                        file_name = Path(matched_filepath).name
                        break
                        
            return {
                "is_code_error": True,
                "type": err_type,
                "desc": err_desc,
                "line": line_no,
                "file": file_name
            }
        return {"is_code_error": False}

    def run(self):
        os.environ["NUITKA_ACCEPT_DOWNLOADS"] = "yes"
        engine = self.params['engine']
        pip_idx = self.params.get('pip_index_url', '').strip()
        pip_backup = self.params.get('pip_index_backup', '').strip()
        is_temp = False
        build_script_path = None
        ext = ".exe" if os.name == "nt" else ""
        failed_packages = []

        try:
            self.progress.emit(_("[INFO] Initializing isolated build environment..."))
            script_path = Path(self.params['script_path']).resolve()
            script_dir = script_path.parent
            
            build_script_path, is_temp, err_msg = self.sanitize_script(script_path)
            if not build_script_path and err_msg: return self.finished.emit(False, f"[ERROR] I/O Exception: {err_msg}", [])
            script_posix = build_script_path.as_posix()

            system_python_exe = get_python_executable()
            self.progress.emit(_("[INFO] Python interpreter path: {path}", path=system_python_exe))

            script_imports = set()
            try:
                script_imports = extract_imports_via_ast(script_posix, system_python_exe)
            except Exception as e:
                self.progress.emit(f"[WARN] AST Analysis Exception: {e}")

            if self.params['use_venv']:
                self.progress.emit(_("[INFO] Creating virtual environment..."))
                self.venv_dir = Path(tempfile.mkdtemp(prefix="qpypack_env_")).resolve()
                if not self.run_cmd([system_python_exe, "-m", "venv", self.venv_dir.as_posix()]):
                    return self.finished.emit(False, _("[ERROR] Failed to create virtual environment. Current Python environment might be missing necessary modules or have restricted permissions."), [])
                python_exe = (self.venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")).as_posix()
                
                self.progress.emit(_("[INFO] Synchronizing and upgrading pip package manager..."))
                self.run_pip_install(python_exe, ["--upgrade", "pip", "-q"])
            else: 
                python_exe = system_python_exe

            engine_pkg = "nuitka" if engine == "Nuitka" else "pyinstaller"
            if engine == "Nuitka" and self.params.get('nuitka_version'):
                engine_pkg = f"nuitka=={self.params['nuitka_version']}"
            elif engine == "PyInstaller" and self.params.get('pyi_version'):
                engine_pkg = f"pyinstaller=={self.params['pyi_version']}"
            
            self.progress.emit(_("[INFO] Installing build engine [{pkg}] and core compilation dependencies...", pkg=engine_pkg))
            core_pkgs = [engine_pkg]
            if engine == "PyInstaller": 
                core_pkgs.append("pillow")
            elif engine == "Nuitka":
                core_pkgs.append("zstandard")
                self.progress.emit(_("[INFO] Nuitka Tip: If prompted to download GCC/MinGW compiler on first build, please ensure stable network connection."))
            
            self.run_pip_install(python_exe, ["-q"] + core_pkgs)
                      
            if self.params.get('use_reqs'):
                custom_reqs = self.params.get('reqs_file', '').strip()
                if custom_reqs and Path(custom_reqs).exists():
                    req_file = Path(custom_reqs)
                else:
                    req_file = script_dir / "requirements.txt"
                
                if req_file.exists():
                    self.progress.emit(_("[INFO] Dependency installation [1/3]: Installing declared dependencies ({filename})...", filename=req_file.name))
                    try:
                        if is_cloud_locked(req_file): 
                            raise ValueError("Requirements file is locked")
                        raw_req = req_file.read_bytes()
                        try: req_content = raw_req.decode('utf-8-sig')
                        except: req_content = raw_req.decode(locale.getpreferredencoding(), errors='ignore')
                        
                        temp_req = Path(tempfile.gettempdir()) / f"qpypack_temp_reqs_{int(time.time())}.txt"
                        temp_req.write_text(req_content, encoding='utf-8')
                        self.run_pip_install(python_exe, ["-q", "-r", temp_req.as_posix()])
                        temp_req.unlink(missing_ok=True)
                    except Exception as e: 
                        self.progress.emit(f"[WARN] Requirements install exception: {e}")

            if self.params.get('use_pipreqs'):
                self.progress.emit(_("[INFO] Dependency installation [2/3]: Calling pipreqs to analyze project dependencies..."))
                sandbox_dir = None
                if not self.params.get('use_pipreqs_dir', False):
                    sandbox_dir = Path(tempfile.mkdtemp(prefix="qpypack_sandbox_")).resolve()
                    shutil.copy2(build_script_path, sandbox_dir / build_script_path.name)
                    target_scan_dir = sandbox_dir
                    self.progress.emit(_("[INFO] Enabled single-file sandbox mode: parsing current script only to prevent pollution from other files."))
                else:
                    target_scan_dir = script_dir
                    self.progress.emit(_("[WARN] Enabled full-directory scan mode: scanning all Python files in the current directory..."))

                pipreqs_pkg = "pipreqs"
                if self.params.get('pipreqs_version'):
                    pipreqs_pkg = f"pipreqs=={self.params['pipreqs_version']}"
                    
                self.run_pip_install(python_exe, [pipreqs_pkg, "-q"])
                temp_pipreqs = Path(tempfile.gettempdir()) / f"qpypack_pipreqs_{int(time.time())}.txt"
                
                pypi_server = None
                if pip_idx:
                    pypi_server = re.sub(r'/simple/?$', '/pypi', pip_idx, flags=re.I).rstrip('/')
                
                pipreqs_cmd = [
                    python_exe, "-m", "pipreqs.pipreqs", target_scan_dir.as_posix(), 
                    "--encoding", "utf-8", "--force", "--savepath", temp_pipreqs.as_posix()
                ]
                if pypi_server: 
                    pipreqs_cmd.extend(["--pypi-server", pypi_server])
                    self.progress.emit(_("[INFO] Dependency analysis service source address: {server}", server=pypi_server))
                
                self.progress.emit(_("[INFO] Querying versions of dependency libraries, please wait..."))
                
                success_pipreqs = self.run_cmd(pipreqs_cmd, timeout=120, silent_error=True)
                
                if not success_pipreqs and pip_backup and pip_backup != pip_idx:
                    backup_pypi = re.sub(r'/simple/?$', '/pypi', pip_backup, flags=re.I).rstrip('/')
                    self.progress.emit(_("[INFO] Switching to backup PyPI source for retrieval: {url}", url=backup_pypi))
                    backup_pipreqs_cmd = [c if c != pypi_server else backup_pypi for c in pipreqs_cmd]
                    success_pipreqs = self.run_cmd(backup_pipreqs_cmd, timeout=120, silent_error=True)

                if not success_pipreqs:
                    self.progress.emit(_("[INFO] Attempting to scan using compatible encoding..."))
                    fallback_cmd = ["iso-8859-1" if c == "utf-8" else c for c in pipreqs_cmd]
                    success_pipreqs = self.run_cmd(fallback_cmd, timeout=120, silent_error=True)
                    if not success_pipreqs:
                        self.progress.emit(_("[WARN] pipreqs skipped deep scan, dependencies will be supplemented by AST scanning engine."))
                
                if success_pipreqs and temp_pipreqs.exists():
                    self.run_pip_install(python_exe, ["-q", "-r", temp_pipreqs.as_posix()])
                    temp_pipreqs.unlink(missing_ok=True)
                    
                if sandbox_dir and sandbox_dir.exists():
                    robust_rmtree(sandbox_dir)

            config = load_config()
            known_mappings = DEFAULT_MAPPINGS.copy()
            if 'Mappings' in config:
                for k, v in config['Mappings'].items():
                    known_mappings[k] = v
            
            known_mappings_lower = {k.lower(): v for k, v in known_mappings.items()}

            HARDCODED_SAFETY_MAPPINGS = {
                'pythoncom': 'pywin32', 'pywintypes': 'pywin32', 'win32com': 'pywin32',
                'win32api': 'pywin32', 'win32con': 'pywin32', 'win32gui': 'pywin32',
                'win32clipboard': 'pywin32', 'win32print': 'pywin32', 'win32file': 'pywin32',
                'win32security': 'pywin32', 'win32process': 'pywin32', 'win32evtlog': 'pywin32',
                'win32service': 'pywin32', 'win32pipe': 'pywin32', 'win32net': 'pywin32',
                'win32crypt': 'pywin32', 'cv2': 'opencv-python', 'pil': 'pillow', 'fitz': 'pymupdf', 
                'bs4': 'beautifulsoup4', 'sklearn': 'scikit-learn', 'yaml': 'pyyaml', 'dotenv': 'python-dotenv'
            }
            for k, v in HARDCODED_SAFETY_MAPPINGS.items():
                known_mappings_lower[k.lower()] = v

            local_modules = set()
            for p in script_dir.rglob("*"):
                if any(part.startswith('.') or part.lower() in ('venv', 'env', 'site-packages', 'node_modules', '__pycache__') for part in p.parts):
                    continue
                if p.is_file() and p.suffix.lower() == '.py':
                    local_modules.add(p.stem.lower())
                elif p.is_dir():
                    local_modules.add(p.name.lower())

            ast_pkgs_set = set()
            for m in script_imports:
                if m in STD_LIBS or m.lower() in local_modules: continue
                mapped_name = known_mappings_lower.get(m.lower(), m)
                ast_pkgs_set.add(mapped_name)

            ast_pkgs = sorted(list(ast_pkgs_set))
            
            if ast_pkgs:
                self.progress.emit(_("[INFO] Dependency installation [3/3]: Extracting implicit dependencies via AST static scan..."))
                self.progress.emit(_("[INFO] Parsing and installing implicit import dependencies: {pkgs}", pkgs=', '.join(ast_pkgs)))
                for pkg in ast_pkgs:
                    if not self.run_pip_install(python_exe, ["-q", pkg]):
                        failed_packages.append(pkg)
                        self.progress.emit(_("[ERROR] ⚠️ Warning: Failed to install dependency [{pkg}]! May cause runtime crash.", pkg=pkg))

            if self._is_cancelled: return self.finished.emit(False, "[INFO] Build Cancelled.", failed_packages)

            self.progress.emit(_("[INFO] Starting {engine} engine to compile binary files...", engine=engine))
            cmd = []
            app_name = self.params['app_name']
            icon_path = Path(self.params['icon']).resolve().as_posix() if self.params.get('icon') else None

            if engine == "PyInstaller":
                self.temp_workpath = Path(tempfile.mkdtemp(prefix="qpypack_build_")).resolve()
                self.temp_dist_dir = Path(tempfile.mkdtemp(prefix="qpypack_dist_")).resolve()
                cmd = [
                    python_exe, "-m", "PyInstaller", "--clean", "--noconfirm", 
                    f"--distpath={self.temp_dist_dir.as_posix()}",
                    f"--workpath={self.temp_workpath.as_posix()}", 
                    f"--name={app_name}"
                ]
                
                if self.params['onefile']: cmd.append("--onefile")
                else: cmd.append("--onedir")
                
                if self.params['noconsole']: cmd.append("--noconsole")
                else: cmd.append("--console")

                if icon_path: 
                    cmd.extend(["--icon", icon_path])
                    cmd.extend(["--add-data", f"{icon_path}{os.pathsep}."])
                    
                if self.params.get('version_file') and os.name == "nt": 
                    cmd.extend(["--version-file", self.params['version_file']])
                elif sys.platform == "darwin":
                    comp = self.params.get('ver_comp', 'mycompany').strip().lower().replace(" ", "")
                    bundle_id = f"com.{comp or 'anonymous'}.{app_name.lower().replace(' ', '')}"
                    cmd.extend(["--osx-bundle-identifier", bundle_id])
                    
                if self.params.get('upx'):
                    upx_dir_custom = self.params.get('upx_path', '').strip()
                    if upx_dir_custom and Path(upx_dir_custom).exists():
                        cmd.append(f"--upx-dir={upx_dir_custom}")
                    else:
                        upx_dir_default = (Path.cwd() / "upx").resolve()
                        if upx_dir_default.exists(): cmd.append(f"--upx-dir={upx_dir_default.as_posix()}")
                    if os.name == "nt":
                        cmd.extend(["--upx-exclude=python3.dll", "--upx-exclude=python*.dll", "--upx-exclude=vcruntime140.dll"])
                else:
                    cmd.append("--noupx")
                
                for imp in self.params.get('hidden_imports', '').split(','):
                    if imp.strip(): cmd.extend(["--hidden-import", imp.strip()])
                
                for r_type, src, dst in self.params.get('add_data_list', []):
                    cmd.extend(["--add-data", f"{src}{os.pathsep}{dst}"])
                
                for excl in self.params.get('exclude_modules', '').split(','):
                    if excl.strip(): cmd.extend(["--exclude-module", excl.strip()])

            elif engine == "Nuitka":
                self.temp_out_dir = Path(tempfile.mkdtemp(prefix="nuitka_out_")).resolve()
                cmd = [
                    python_exe, "-m", "nuitka", "--remove-output", "--assume-yes-for-downloads",
                    f"--output-dir={self.temp_out_dir.as_posix()}", 
                    f"--output-filename={app_name}{ext}"
                ]
                
                if os.name == "nt":
                    has_msvc = shutil.which('cl.exe') is not None
                    if not has_msvc:
                        vswhere = Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")) / "Microsoft Visual Studio/Installer/vswhere.exe"
                        if vswhere.exists():
                            try:
                                res = subprocess.run([vswhere.as_posix(), "-latest", "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                                if res.stdout.strip(): has_msvc = True
                            except: pass
                    if has_msvc:
                        cmd.append("--msvc=latest")
                        self.progress.emit(_("[INFO] Found local MSVC environment, prioritizing native C++ compiler."))
                        
                cores = self.params.get('cpu_cores', os.cpu_count() or 2)
                cmd.append(f"--jobs={cores}")
                
                if self.params['onefile']: cmd.append("--onefile")
                else: cmd.append("--standalone")
                
                if self.params['noconsole']: 
                    cmd.append("--windows-console-mode=disable")
                    if sys.platform == "darwin": cmd.append("--macos-create-app-bundle")
                else:
                    cmd.append("--windows-console-mode=force")
                
                if icon_path: 
                    if os.name == "nt": cmd.append(f"--windows-icon-from-ico={icon_path}")
                    elif sys.platform == "darwin": cmd.append(f"--macos-app-icon={icon_path}")
                    cmd.append(f"--include-data-files={Path(icon_path).resolve().as_posix()}={Path(icon_path).name}")
                    
                if os.name == "nt":
                    if self.params.get('ver_comp'): cmd.append(f"--company-name={self.params['ver_comp']}")
                    if self.params.get('ver_desc'): cmd.append(f"--file-description={self.params['ver_desc']}")
                    if self.params.get('app_name'): cmd.append(f"--product-name={self.params['app_name']}")
                    if self.params.get('ver_ver'): 
                        v_str = self.params['ver_ver'].strip()
                        v_nums = re.findall(r'\d+', v_str)
                        v_clean = ".".join((v_nums + ['0', '0', '0', '0'])[:4])
                        cmd.append(f"--file-version={v_clean}")
                        cmd.append(f"--product-version={v_clean}")
                elif sys.platform == "darwin":
                    if self.params.get('ver_comp'): cmd.append(f"--company-name={self.params['ver_comp']}")
                    if self.params.get('ver_ver'): cmd.append(f"--macos-app-version={self.params['ver_ver']}")
                    comp = self.params.get('ver_comp', 'mycompany').strip().lower().replace(" ", "")
                    bundle_id = f"com.{comp or 'anonymous'}.{app_name.lower().replace(' ', '')}"
                    cmd.append(f"--macos-signed-app-name={bundle_id}")
                
                imports_lower = {m.lower() for m in script_imports}
                if 'pyqt5' in imports_lower: cmd.append("--enable-plugin=pyqt5")
                elif 'pyqt6' in imports_lower: cmd.append("--enable-plugin=pyqt6")
                elif 'pyside2' in imports_lower: cmd.append("--enable-plugin=pyside2")
                elif 'pyside6' in imports_lower: cmd.append("--enable-plugin=pyside6")
                
                if 'matplotlib' in imports_lower: cmd.append("--enable-plugin=matplotlib")
                if 'tkinter' in imports_lower: cmd.append("--enable-plugin=tk-inter")
                
                for imp in self.params.get('hidden_imports', '').split(','):
                    if imp.strip(): cmd.append(f"--include-module={imp.strip()}")
                
                for r_type, src, dst in self.params.get('add_data_list', []):
                    src_path = Path(src).resolve().as_posix()
                    if r_type == 'dir':
                        cmd.append(f"--include-data-dir={src_path}={dst}")
                    else:
                        filename = Path(src).name
                        if dst == ".": nuitka_dst = filename
                        else: nuitka_dst = os.path.normpath(os.path.join(dst, filename)).replace('\\', '/')
                        cmd.append(f"--include-data-files={src_path}={nuitka_dst}")

                for excl in self.params.get('exclude_modules', '').split(','):
                    if excl.strip(): cmd.append(f"--nofollow-import-to={excl.strip()}")
                    
            if self.params.get('lite_mode'):
                self.progress.emit(_("[INFO] Lite mode enabled, executing size reduction strategy..."))
                if not self.params.get('use_venv'):
                    self.progress.emit(_("[WARN] Strongly recommend checking [Virtual Environment] to maximize lite mode effect."))
                    
                lite_excludes = ['pip', 'setuptools', 'distutils', 'wheel', 'pydoc']
                for ex in lite_excludes:
                    if engine == "PyInstaller": cmd.append(f"--exclude-module={ex}")
                    elif engine == "Nuitka": cmd.append(f"--nofollow-import-to={ex}")
                    
                if engine == "Nuitka":
                    self.progress.emit(_("[INFO] Enabled Nuitka optimization directives..."))
                    cmd.append("--python-flag=-OO")

            cmd.append(script_posix)

            success = self.run_cmd(cmd, cwd=script_dir.as_posix())
            if self._is_cancelled: return self.finished.emit(False, "[INFO] Build Cancelled.", failed_packages)

            self.progress.emit(_("[INFO] Core compilation completed, extracting and archiving built files..."))
            src_out = None
            if engine == "PyInstaller": 
                if sys.platform == "darwin" and self.params['noconsole']:
                    src_out = self.temp_dist_dir / f"{app_name}.app"
                else:
                    src_out = self.temp_dist_dir / (f"{app_name}{ext}" if self.params['onefile'] else app_name)
            elif engine == "Nuitka": 
                if self.params['onefile']:
                    if sys.platform == "darwin" and self.params['noconsole']:
                        src_out = self.temp_out_dir / f"{app_name}.app"
                    else:
                        src_out = self.temp_out_dir / f"{app_name}{ext}"
                else:
                    if sys.platform == "darwin" and self.params['noconsole']:
                        src_out = self.temp_out_dir / f"{app_name}.app"
                    else:
                        dist_dirs = list(self.temp_out_dir.glob("*.dist"))
                        if dist_dirs: src_out = dist_dirs[0]
                        else: src_out = self.temp_out_dir / f"{app_name}.dist"

            out_mode = int(self.params.get('out_mode', 0))
            custom_out = self.params.get('custom_out_dir', '').strip()
            if out_mode == 1 and custom_out:
                try:
                    final_out_dir = Path(custom_out)
                    final_out_dir.mkdir(parents=True, exist_ok=True)
                except: final_out_dir = script_dir
            else:
                final_out_dir = script_dir
                
            final_out = final_out_dir / (src_out.name if src_out else f"{app_name}{ext}")

            if success and src_out and src_out.exists():
                try:
                    if final_out.exists():
                        if final_out.is_dir(): shutil.rmtree(final_out, onerror=remove_readonly)
                        else: final_out.unlink(missing_ok=True)
                    shutil.move(src_out.as_posix(), final_out.as_posix())
                except Exception as e: 
                    self.progress.emit(_("[ERROR] Product transfer failed, file might be occupied by system process or lack permission: {error}", error=str(e)))
            else: 
                self.progress.emit(_("[ERROR] Could not locate valid executable product in temporary build directory: {path}", path=str(src_out)))

            if success and final_out.exists(): 
                self.progress.emit(_("[INFO] Validating output files and generating final product..."))
                if self.params.get('auto_save_log') and self.all_raw_logs:
                    try:
                        log_file = final_out_dir / f"qpypack_build_{app_name}.log"
                        log_file.write_text('\n'.join(self.all_raw_logs), encoding='utf-8')
                        self.progress.emit(_("[INFO] Build log exported to: {path}", path=log_file.as_posix()))
                    except: pass
                self.finished.emit(True, _("[SUCCESS] Compilation completed, output path: {path}", path=final_out.resolve().as_posix()), failed_packages)
            else: 
                err_info = self.detect_python_syntax_errors()
                if err_info["is_code_error"]:
                    msg = _("[Syntax Error] Source program has syntax or indentation errors!\n  - File: {file}\n  - Type: {type}\n  - Line: near {line}\n  - Desc: {desc}\n\nTip: This is an error in the source code logic. Ensure it runs locally before compiling.", 
                            file=err_info['file'], type=err_info['type'], line=err_info['line'], desc=err_info['desc'])
                else:
                    if self.params.get('concise_log', True) and self.all_raw_logs:
                        self.progress.emit(_("\n!!!!!!!!!! [Diagnostic Traceback: Full raw log due to execution exception in this step] !!!!!!!!!!"))
                        self.progress.emit('\n'.join(self.all_raw_logs[-100:])) 
                    msg = _("[FAILED] Compilation interrupted with exceptions, refer to the log for troubleshooting.")
                self.finished.emit(False, msg, failed_packages)
                
        except Exception as e:
            if self.params.get('concise_log', True) and self.all_raw_logs:
                self.progress.emit(_("\n!!!!!!!!!! [Diagnostic Traceback: Full raw log due to execution exception in this step] !!!!!!!!!!"))
                self.progress.emit('\n'.join(self.all_raw_logs[-100:]))
            self.finished.emit(False, f"[ERROR] {str(e)}", failed_packages)
        finally:
            if is_temp and build_script_path and build_script_path.exists():
                try: 
                    build_script_path.unlink()
                    pycache_dir = script_dir / "__pycache__"
                    if pycache_dir.exists(): robust_rmtree(pycache_dir)
                except: pass
                
            if self.params.get('version_file'):
                try:
                    p = Path(self.params['version_file'])
                    if p.exists(): p.unlink()
                except: pass
                
            if self.params.get('temp_icon_file'):
                try:
                    p = Path(self.params['temp_icon_file'])
                    if p.exists(): p.unlink()
                except: pass
                
            if self.params['clean_all']:
                self.progress.emit(_("[INFO] Freeing up space, cleaning temporary build environment..."))
                for p in [self.venv_dir, self.temp_workpath, self.temp_out_dir, self.temp_dist_dir]:
                    if p and p.exists(): robust_rmtree(p)
                    
                app_name = self.params.get('app_name', 'app')
                for p in ["__pycache__", f"{app_name}.build", f"{app_name}.dist", f"{app_name}.onefile-build"]:
                    robust_rmtree(script_dir / p)
                
                spec_file = script_dir / f"{app_name}.spec"
                if spec_file.exists():
                    try: spec_file.unlink()
                    except: pass

class SmoothSlideOverlay(QWidget):

    def __init__(self, parent, pix_old, pix_new, direction):
        super().__init__(parent)
        self.pix_old = pix_old
        self.pix_new = pix_new
        self.direction = direction 
        self.progress = 0.0
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def set_progress(self, p):
        self.progress = p
        self.update()  

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = float(self.width())
        p = self.progress

        x_old = -w * p * self.direction
        x_new = w * (1.0 - p) * self.direction

        painter.drawPixmap(QPointF(x_old, 0), self.pix_old)
        painter.drawPixmap(QPointF(x_new, 0), self.pix_new)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.script_path = ""
        self.thread = None
        self.analysis_thread = None
        self.current_state = "idle" 
        self.init_style()
        self.init_ui()
        
        I18N.language_changed.connect(self.retranslate_ui)

    def init_style(self):
        self.setWindowTitle(f"{__app_name__} {__version__}")
        self.setMinimumSize(740, 680)
        self.resize(780, 680)
        
        icon_path = get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        elif getattr(sys, 'frozen', False):
            provider = QFileIconProvider()
            exe_icon = provider.icon(QFileInfo(sys.executable))
            if not exe_icon.isNull(): self.setWindowIcon(exe_icon)

        self.setStyleSheet("""
            QMainWindow { background-color: #ffffff; }
            QTextEdit { border: 1px solid #e8eaed; border-radius: 8px; background-color: #f8f9fa; font-family: Consolas, monospace; font-size: 13px; color: #3c4043; padding: 10px; }
            QStatusBar { background-color: #f8f9fa; color: #5f6368; border-top: 1px solid #e8eaed; padding: 5px; }
            QStatusBar QLabel { color: #5f6368; font-size: 13px; padding: 2px; background: transparent; }
        """)
        
        self.icon_btn_style = "QPushButton { background-color: #f1f3f4; border: 1px solid transparent; border-radius: 8px; } QPushButton:hover { background-color: #e8eaed; } QPushButton:pressed { background-color: #dadce0; }"
        self.primary_btn_style = "QPushButton { background-color: #1A73E8; color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: bold; } QPushButton:hover { background-color: #1B66C9; } QPushButton:pressed { background-color: #174EA6; }"
        self.danger_btn_style = "QPushButton { background-color: #D93025; color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: bold; } QPushButton:hover { background-color: #C5221F; } QPushButton:pressed { background-color: #A50E0E; }"
        self.success_btn_style = "QPushButton { background-color: #1E8E3E; color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: bold; } QPushButton:hover { background-color: #188038; } QPushButton:pressed { background-color: #137333; }"

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        self.stacked_layout = QStackedLayout(central)

        self.main_panel = QWidget()
        layout = QVBoxLayout(self.main_panel)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.drop_area = DropArea(self)
        self.drop_area.fileDropped.connect(self.on_script_selected)
        layout.addWidget(self.drop_area, stretch=1)

        self.log_container = QWidget()
        log_lay = QVBoxLayout(self.log_container)
        log_lay.setContentsMargins(0, 0, 0, 0)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(120) 
        self.log.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.log.customContextMenuRequested.connect(self.show_log_context_menu)
        log_lay.addWidget(self.log)
        self.log_container.hide()
        layout.addWidget(self.log_container)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        btn_layout.setContentsMargins(0, 5, 0, 0)

        self.btn_left = AnimatedButton("")
        self.btn_left.setFixedSize(44, 44)
        self.btn_left.setStyleSheet(self.icon_btn_style)
        self.btn_left.clicked.connect(self.on_left_btn_clicked)
        btn_layout.addWidget(self.btn_left)

        self.btn_main = AnimatedButton("")
        self.btn_main.setFixedHeight(44)
        self.btn_main.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_main.clicked.connect(self.on_main_btn_clicked)
        btn_layout.addWidget(self.btn_main)

        self.btn_right = AnimatedButton("")
        self.btn_right.setFixedSize(44, 44)
        self.btn_right.setIcon(get_svg_icon('settings', "#5F6368"))
        self.btn_right.setStyleSheet(self.icon_btn_style)
        self.btn_right.clicked.connect(self.show_settings)
        btn_layout.addWidget(self.btn_right)

        layout.addLayout(btn_layout)
        self.stacked_layout.addWidget(self.main_panel)

        self.settings_panel = SettingsPanel(self)
        self.stacked_layout.addWidget(self.settings_panel)
        self.stacked_layout.setCurrentWidget(self.main_panel)
        
        self.status_bar = self.statusBar()
        self.status_label = QLabel(_("Status: Ready"))
        self.status_bar.addWidget(self.status_label)

        self.copyright_label = QLabel(f"Copyright © {__company__}. ")
        self.copyright_label.setStyleSheet("color: #bdc1c6; font-size: 11px; font-weight: bold; background: transparent; padding-right: 5px;")
        self.status_bar.addPermanentWidget(self.copyright_label)

        self.update_ui_state("idle")

    def show_notification(self, msg, timeout=4000):
        msg = msg.replace('\n', ' ')
        self.statusBar().showMessage(msg, timeout)

    def show_error_log(self, msg):
        if not self.log_container.isVisible():
            self.toggle_log()
        self.append_log(msg, is_error=True)
        self.show_notification(_("Attention: Please check the log for details."), 6000)

    def set_status(self, text):
        self.status_label.setText(text)
        self.adjust_status_bar()

    def adjust_status_bar(self):
        if not hasattr(self, 'status_label') or not hasattr(self, 'copyright_label') or not hasattr(self, 'status_bar'):
            return
        text = self.status_label.text()
        metrics = self.status_label.fontMetrics()
        text_width = metrics.horizontalAdvance(text)
        copyright_width = self.copyright_label.fontMetrics().horizontalAdvance(self.copyright_label.text())
        
        if text_width + copyright_width + 60 > self.status_bar.width():
            self.copyright_label.hide()
        else:
            self.copyright_label.show()

    def retranslate_ui(self):
        self.btn_right.setToolTip(_("Configure Build Settings"))
        is_log_open = self.log_container.isVisible()
        if is_log_open:
            self.btn_left.setToolTip(_("Toggle Execution Log"))
        else:
            if self.current_state in ("done", "failed"):
                self.btn_left.setToolTip(_("Reset to Default Config"))
            else:
                self.btn_left.setToolTip(_("Toggle Execution Log"))
        
        self.update_ui_state(self.current_state)

        if self.current_state == "idle":
            self.set_status(_("Status: Ready"))
        elif self.current_state == "ready":
            mode_suffix = _(" [Console]") if not self.settings_panel.noconsole_check.isChecked() else _(" [No Console]")
            self.set_status(_("Status: Loaded {filename}{mode}", filename=Path(self.script_path).name, mode=mode_suffix))
        elif self.current_state == "building":
            self.set_status(_("Status: Packaging ({engine}) ...", engine=self.settings_panel.engine_combo.currentText()))
        elif self.current_state == "done":
            self.set_status(_("Status: Build Completed"))
        elif self.current_state == "failed":
            self.set_status(_("Status: Build Failed"))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_status_bar()

    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            self.thread.cancel()
            self.thread.wait()
            
        if self.analysis_thread and self.analysis_thread.isRunning():
            self.analysis_thread.terminate()
            self.analysis_thread.wait()
            
        if hasattr(self,'settings_panel') and hasattr(self.settings_panel, 'scanner_thread'):
            if self.settings_panel.scanner_thread and self.settings_panel.scanner_thread.isRunning():
                self.settings_panel.scanner_thread.terminate()
                self.settings_panel.scanner_thread.wait()
                
        super().closeEvent(event)

    def update_ui_state(self, state):
        self.current_state = state
        self.btn_right.setEnabled(state != "building")
        self.drop_area.setAcceptDrops(state != "building")
        
        if state in ("idle", "ready"):
            is_log_open = self.log_container.isVisible()
            icon_name = 'expand_less' if is_log_open else 'expand_more'
            self.btn_left.setIcon(get_svg_icon(icon_name, "#5F6368"))
            
            self.btn_main.setText(_("Start Build"))
            self.btn_main.setIcon(get_svg_icon('play', "white"))
            self.btn_main.setStyleSheet(self.primary_btn_style)
            
        elif state == "building":
            is_log_open = self.log_container.isVisible()
            icon_name = 'expand_less' if is_log_open else 'expand_more'
            self.btn_left.setIcon(get_svg_icon(icon_name, "#5F6368"))
            
            self.btn_main.setText(_("Stop Build"))
            self.btn_main.setIcon(get_svg_icon('stop', "white"))
            self.btn_main.setStyleSheet(self.danger_btn_style)
            
        elif state in ("done", "failed"):
            self.btn_left.setIcon(get_svg_icon('refresh', "#5F6368"))
            if state == "done":
                self.btn_main.setText(_("Open Directory"))
                self.btn_main.setIcon(get_svg_icon('folder', "white"))
                self.btn_main.setStyleSheet(self.success_btn_style)
            else:
                self.btn_main.setText(_("Rebuild"))
                self.btn_main.setIcon(get_svg_icon('refresh', "white"))
                self.btn_main.setStyleSheet(self.danger_btn_style)

    def on_left_btn_clicked(self):
        if self.current_state in ("done", "failed"): self.reset_all()
        else: self.toggle_log()

    def on_main_btn_clicked(self):
        if self.current_state in ("idle", "ready", "failed"): self.start_pack()
        elif self.current_state == "building": self.cancel_pack()
        elif self.current_state == "done": self.open_dist()

    def toggle_log(self):
        if self.log_container.isVisible(): self.log_container.hide()
        else: self.log_container.show()
        self.update_ui_state(self.current_state)

    def show_settings(self): self._animate_switch(self.settings_panel)

    def show_main(self):
        self.settings_panel.load_from_config()
        self._animate_switch(self.main_panel)

    def save_settings_and_return(self):
        self.settings_panel.save_to_config()
        self._animate_switch(self.main_panel)

    def _animate_switch(self, target_widget):
        current_widget = self.stacked_layout.currentWidget()
        if current_widget == target_widget:
            return

        if hasattr(self, 'anim_group') and self.anim_group.state() == QParallelAnimationGroup.State.Running:
            self.anim_group.stop()
        for attr in ('lbl_old', 'lbl_new'):
            if hasattr(self, attr) and getattr(self, attr):
                try: getattr(self, attr).deleteLater()
                except RuntimeError: pass

        pix_old = current_widget.grab()

        self.stacked_layout.setCurrentWidget(target_widget)
        target_widget.setGeometry(current_widget.geometry())
        QApplication.processEvents()
        pix_new = target_widget.grab()

        self.lbl_old = QLabel(self.centralWidget())
        self.lbl_old.setPixmap(pix_old)
        self.lbl_old.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.lbl_old.show()

        self.lbl_new = QLabel(self.centralWidget())
        self.lbl_new.setPixmap(pix_new)
        self.lbl_new.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.lbl_new.show()

        rect = current_widget.geometry()
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        direction = 1 if target_widget == self.settings_panel else -1

        self.lbl_old.setGeometry(x, y, w, h)
        self.lbl_new.setGeometry(x + w * direction, y, w, h)

        self.anim_group = QParallelAnimationGroup(self)
        
        anim_old = QPropertyAnimation(self.lbl_old, b"pos")
        anim_old.setDuration(280)
        anim_old.setEndValue(QPointF(x - w * direction, y))
        anim_old.setEasingCurve(QEasingCurve.Type.OutCubic)

        anim_new = QPropertyAnimation(self.lbl_new, b"pos")
        anim_new.setDuration(280)
        anim_new.setEndValue(QPointF(x, y))
        anim_new.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.anim_group.addAnimation(anim_old)
        self.anim_group.addAnimation(anim_new)

        def cleanup():
            if hasattr(self, 'lbl_old') and self.lbl_old: self.lbl_old.deleteLater()
            if hasattr(self, 'lbl_new') and self.lbl_new: self.lbl_new.deleteLater()

        self.anim_group.finished.connect(cleanup)
        self.anim_group.start()

    def on_script_selected(self, path):
        path = Path(path).resolve().as_posix()
        if is_cloud_locked(path):
            self.show_error_log(_("[ERROR] Target file is locked or encrypted by cloud drive. Please decrypt and try again."))
            return

        if self.script_path and self.script_path != path:
            self.settings_panel.icon_edit.clear()
            self.settings_panel.hidden_edit.clear()
            self.settings_panel.add_data_list.clear()

        self.script_path = path
        self.drop_area.set_loading(Path(path).name)
        self.set_status(_("Status: Parsing {filename}...", filename=Path(path).name))
        
        if self.analysis_thread and self.analysis_thread.isRunning():
            self.analysis_thread.terminate()
            self.analysis_thread.wait()
            
        self.analysis_thread = ScriptAnalysisThread(self.script_path)
        self.analysis_thread.analysis_done.connect(self.on_analysis_finished)
        self.analysis_thread.start()

    def on_analysis_finished(self, app_name, version, author, desc, script_imports):
        path = self.script_path
        if not path: return

        if version: self.settings_panel.ver_ver.setText(version)
        else: self.settings_panel.ver_ver.setText("1.0.0")
            
        self.settings_panel.ver_comp.setText(author)
        self.settings_panel.ver_desc.setText(desc)

        gui_libs = {'pyqt5', 'pyqt6', 'pyside2', 'pyside6', 'tkinter', 'wx', 'kivy', 'libavg'}
        has_gui = any(lib in {m.lower() for m in script_imports} for lib in gui_libs)
        self.settings_panel.noconsole_check.setChecked(has_gui)

        default_output_name = f"{app_name}_{version}" if version else app_name
        self.settings_panel.name_edit.setText(default_output_name)
        
        script_dir = Path(path).parent
        auto_icon = None
        
        if self.settings_panel.auto_icon_check.isChecked():
            preferred_extensions = [".ico", ".icns", ".png", ".svg"]
            if sys.platform == "darwin": preferred_extensions = [".icns", ".png", ".svg", ".ico"]
            elif sys.platform == "linux": preferred_extensions = [".png", ".svg", ".ico", ".icns"]
                
            found = False
            for ext in preferred_extensions:
                for name in ["icon", "logo", "ICON", "LOGO"]:
                    trial = script_dir / f"{name}{ext}"
                    if trial.exists():
                        auto_icon = trial
                        self.settings_panel.icon_edit.setText(trial.resolve().as_posix())
                        found = True
                        break
                if found: break
                
        self.drop_area.set_success(Path(path).name, custom_icon_path=auto_icon)
        mode_suffix = _(" [Console]") if not has_gui else _(" [No Console]")
        self.set_status(_("Status: Loaded {filename}{mode}", filename=Path(path).name, mode=mode_suffix))
        
        if not self.log_container.isVisible(): self.toggle_log()
        self.log.clear()
        self.append_log(_("Loaded: {filename}", filename=path))
        self.btn_main.setEnabled(True)
        self.update_ui_state("ready")

    def cancel_pack(self):
        if self.thread and self.thread.isRunning():
            self.thread.cancel()
            self.set_status(_("Status: Workspace Reset"))
            self.drop_area.stop_build_anim()
            self.update_ui_state("ready")

    def start_pack(self):
        if not self.script_path or not Path(self.script_path).exists():
            self.show_error_log(_("[ERROR] Please load a valid Python source file first!"))
            return

        sp = self.settings_panel
        app_name = sp.name_edit.text().strip() or Path(self.script_path).stem
        engine = sp.engine_combo.currentText()

        version_file = None
        if engine == "PyInstaller" and os.name == "nt" and sp.ver_ver.text().strip():
            try:
                v_str = sp.ver_ver.text().strip()
                v_nums = re.findall(r'\d+', v_str)
                v_tuple = ",".join((v_nums + ['0', '0', '0', '0'])[:4])
                
                comp_escaped = sp.ver_comp.text().replace("'", "\\'")
                desc_escaped = sp.ver_desc.text().replace("'", "\\'")
                v_str_escaped = v_str.replace("'", "\\'")
                
                content = f'''VSVersionInfo(ffi=FixedFileInfo(filevers=({v_tuple}),prodvers=({v_tuple}),mask=0x3f,flags=0x0,OS=0x40004,fileType=0x1,subtype=0x0,date=(0,0)),kids=[StringFileInfo([StringTable('040904B0',[StringStruct('CompanyName','{comp_escaped}'),StringStruct('FileDescription','{desc_escaped}'),StringStruct('FileVersion','{v_str_escaped}'),StringStruct('ProductVersion','{v_str_escaped}'),StringStruct('OriginalFilename','{app_name}.exe')])]),VarFileInfo([VarStruct('Translation',[1033,1200])])])'''
                version_file = Path(tempfile.gettempdir()) / f"qpypack_{app_name}_version.txt"
                version_file.write_text(content, encoding='utf-8')
            except: pass

        icon_path_str = sp.icon_edit.text().strip()
        temp_icon_file = None
        if icon_path_str and Path(icon_path_str).exists():
            icon_path = Path(icon_path_str)
            needed_ext = "ico" if os.name == "nt" else ("icns" if sys.platform == "darwin" else "png")
            
            if icon_path.suffix.lower() != f".{needed_ext}":
                temp_ico_name = f"qpypack_temp_icon_{int(time.time())}.{needed_ext}"
                temp_ico = Path(tempfile.gettempdir()) / temp_ico_name
                if convert_image_to_format(icon_path.as_posix(), temp_ico.as_posix(), needed_ext):
                    icon_path_str = temp_ico.as_posix()
                    temp_icon_file = temp_ico.as_posix()

        add_data_items = [sp.add_data_list.item(i).data(Qt.ItemDataRole.UserRole) for i in range(sp.add_data_list.count())]
        main_pip = sp._get_url_from_combo(sp.pip_source_combo)
        backup_pip = sp._get_url_from_combo(sp.pip_backup_combo)

        params = {
            'engine': engine,
            'script_path': self.script_path,
            'app_name': app_name,
            'onefile': sp.onefile_check.isChecked(),
            'noconsole': sp.noconsole_check.isChecked(),
            'icon': icon_path_str,
            'use_reqs': sp.reqs_check.isChecked(),
            'use_pipreqs': sp.pipreqs_check.isChecked(),
            'use_pipreqs_dir': sp.pipreqs_dir_check.isChecked(),
            'reqs_file': sp.reqs_file_edit.text().strip(),
            'hidden_imports': sp.hidden_edit.text(),
            'add_data_list': add_data_items,
            'upx': sp.upx_check.isChecked() if engine == "PyInstaller" else False,
            'upx_path': sp.upx_path_edit.text().strip(),
            'cpu_cores': sp.cores_spin.value(),
            'exclude_modules': sp.exclude_edit.text().strip(),
            'out_mode': sp.out_mode_combo.currentIndex(),
            'custom_out_dir': sp.out_dir_edit.text().strip(),
            'use_venv': sp.venv_check.isChecked(),
            'clean_all': sp.clean_all_check.isChecked(),
            'version_file': version_file.as_posix() if version_file else None,
            'temp_icon_file': temp_icon_file,
            'ver_comp': sp.ver_comp.text(),
            'ver_desc': sp.ver_desc.text(),
            'ver_ver': sp.ver_ver.text(),
            'pip_index_url': main_pip,
            'pip_index_backup': backup_pip,
            'concise_log': sp.concise_log_check.isChecked(),
            'auto_save_log': sp.auto_save_log_check.isChecked(),
            'lite_mode': sp.lite_mode_check.isChecked(),
            'pyi_version': sp.pyi_ver_edit.text().strip(),
            'nuitka_version': sp.nuitka_ver_edit.text().strip(),
            'pipreqs_version': sp.pipreqs_ver_edit.text().strip()
        }

        self.log.clear()
        if not self.log_container.isVisible(): self.toggle_log()
            
        self.thread = PackingThread(params)
        self.thread.progress.connect(self.append_log)
        self.thread.finished.connect(self.on_pack_finished)
        self.thread.start()
        
        self.set_status(_("Status: Packaging ({engine}) ...", engine=engine))
        self.update_ui_state("building")
        self.drop_area.start_build_anim()

    def on_pack_finished(self, success, msg, failed_pkgs=None):
        self.append_log("\n" + "━"*50 + "\n" + msg)
        self.drop_area.stop_build_anim()
        play_alert(success)
            
        if success:
            icon_path = self.settings_panel.icon_edit.text().strip()
            self.drop_area.show_success(icon_path)
            self.set_status(_("Status: Build Completed"))
            self.update_ui_state("done")
        else:
            self.drop_area.show_failure()
            self.set_status(_("Status: Build Failed"))
            self.update_ui_state("failed")

        if failed_pkgs:
            warn_msg = _("Dependency Missing Warning: {pkgs} failed to install. Check log for details.", pkgs=", ".join(failed_pkgs))
            self.show_notification(warn_msg, 6000)
            err_log = _("[ERROR] Build completed, but the following dependencies failed to install during pre-build:\n\n  👉 {pkgs}\n\n⚠️ Tip: The program might crash at runtime due to missing modules!", pkgs=", ".join(failed_pkgs))
            self.show_error_log(err_log)

    def open_dist(self):
        if self.settings_panel.out_mode_combo.currentIndex() == 1 and self.settings_panel.out_dir_edit.text().strip():
            target = Path(self.settings_panel.out_dir_edit.text().strip())
        else:
            target = Path(self.script_path).parent if self.script_path else Path.cwd()
            
        if target.exists():
            try:
                if os.name == 'nt': os.startfile(target)
                elif sys.platform == 'darwin': subprocess.call(('open', target.as_posix()))
                else: subprocess.call(('xdg-open', target.as_posix()))
            except: pass

    def reset_all(self):
        self.script_path = ""
        self.settings_panel.name_edit.clear()
        self.settings_panel.icon_edit.clear()
        self.settings_panel.hidden_edit.clear()
        self.settings_panel.add_data_list.clear()
        self.log.clear()
        
        if self.log_container.isVisible(): self.toggle_log()
        self.drop_area.reset()
        self.set_status(_("Status: Workspace Reset"))
        self.update_ui_state("idle")

    def append_log(self, msg, is_error=False):
        if is_error:
            safe_msg = msg.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
            self.log.append(f'<span style="color: #D93025; font-weight: bold;">{safe_msg}</span>')
        else:
            self.log.append(msg)
            
        self.log.ensureCursorVisible()

        for line in msg.split('\n'):
            line = line.strip()
            if not line: continue
            
            if line.startswith(("[INFO]", "[WARN]", "[SUCCESS]", "[FAILED]", "[ERROR]")):
                clean_text = line
                for prefix in ("[INFO]", "[WARN]", "[SUCCESS]", "[FAILED]", "[ERROR]"):
                    if clean_text.startswith(prefix):
                        clean_text = clean_text[len(prefix):].strip()
                        break
                
                if self.current_state == "building" and clean_text:
                    if len(clean_text) > 35: clean_text = clean_text[:32] + "..."
                    self.drop_area.label.setText(clean_text)
                    self.drop_area.label.setStyleSheet("QLabel { background: transparent; color: #1A73E8; font-size: 16px; font-weight: bold; border: none; }")

    def show_log_context_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #ffffff; color: #111827; border: 1px solid #d1d5db; border-radius: 8px; padding: 4px; }
            QMenu::item { padding: 6px 20px; border-radius: 4px; font-size: 12px; font-family: Consolas, "Segoe UI", sans-serif; }
            QMenu::item:selected { background-color: #eff6ff; color: #2563eb; font-weight: 600; }
            QMenu::separator { height: 1px; background-color: #e5e7eb; margin: 4px 2px; }
        """)
        
        act_copy = menu.addAction(_("Copy"))
        act_copy.setEnabled(self.log.textCursor().hasSelection())
        act_copy.triggered.connect(self.log.copy)

        act_select_all = menu.addAction(_("Select All"))
        act_select_all.triggered.connect(self.log.selectAll)

        menu.addSeparator()

        act_clear = menu.addAction(_("Clear Log"))
        act_clear.triggered.connect(self.log.clear)

        act_save = menu.addAction(_("Export Log..."))
        act_save.triggered.connect(self.save_log_file)

        menu.exec(self.log.mapToGlobal(pos))

    def save_log_file(self):
        content = self.log.toPlainText()
        if not content.strip():
            return self.show_notification(_("No log content."))
        
        default_name = "build.log"
        if self.script_path:
            default_name = f"qpypack_{Path(self.script_path).stem}.log"
            
        fp, _filter = QFileDialog.getSaveFileName(self, _("Export Log..."), default_name, "Log Files (*.log);;Text Files (*.txt);;All Files (*)")
        if fp:
            try:
                Path(fp).write_text(content, encoding='utf-8')
                self.show_notification(_("Log saved to: {path}", path=fp))
            except Exception as e:
                self.show_error_log(_("[ERROR] Failed to export log file: {error}", error=str(e)))

def main():
    try:
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    except Exception: pass

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    font = QFont()
    font.setFamilies([
        "Segoe UI", "Microsoft YaHei", "PingFang SC", 
        "Hiragino Sans GB", "Noto Sans SC", "Helvetica Neue", "Arial", "sans-serif"
    ])
    font.setPointSize(9)
    app.setFont(font)

    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()