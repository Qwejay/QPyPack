import sys
import os
import shutil
import subprocess
import tempfile
import re
import time
import stat
import json
import locale
import math
import threading
import configparser
from pathlib import Path

if os.name == 'nt':
    import winreg

os.environ["QT_LOGGING_RULES"] = "qt.text.font.db=false"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
                             QPushButton, QLabel, QLineEdit, QFileDialog, QCheckBox,
                             QComboBox, QFrame, QStackedLayout, QFormLayout, QTextEdit, 
                             QGraphicsOpacityEffect, QGroupBox, QGridLayout, QTabWidget,
                             QMessageBox, QInputDialog, QFileIconProvider, QSizePolicy, QScrollArea,
                             QGraphicsDropShadowEffect, QSpinBox)
from PySide6.QtCore import Qt, QThread, Signal, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QFileInfo, QVariantAnimation, QTimer, QPointF, QRectF, QRect
from PySide6.QtGui import QFont, QDragEnterEvent, QDropEvent, QTextCursor, QIcon, QPixmap, QPainter, QColor, QPen
from PySide6.QtSvg import QSvgRenderer

__app_name__ = "QPyPack"
__version__ = "2.4.2"
__author__ = "QwejayHuang"
__company__ = "QwejayHuang"
__description__ = "自动化 Python 脚本打包构建工具"

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

_CONFIG_DIR = Path.home() / ".qpypack"
_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = (_CONFIG_DIR / "config.ini").as_posix()

DEFAULT_MAPPINGS = {
    'win32com': 'pywin32', 'win32api': 'pywin32', 'win32con': 'pywin32', 'win32gui': 'pywin32',
    'win32clipboard': 'pywin32', 'win32print': 'pywin32', 'win32file': 'pywin32', 'win32security': 'pywin32',
    'cv2': 'opencv-python', 'PIL': 'pillow', 'Pillow': 'pillow', 'bs4': 'beautifulsoup4', 'sklearn': 'scikit-learn',
    'yaml': 'pyyaml', 'fitz': 'pymupdf', 'dotenv': 'python-dotenv'
}

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        config['Mappings'] = DEFAULT_MAPPINGS
        config['Settings'] = {
            'engine': 'PyInstaller', 'pip_index': 'https://pypi.tuna.tsinghua.edu.cn/simple',
            'onefile': 'True', 'noconsole': 'True', 'clean_all': 'True',
            'auto_icon': 'True', 'use_venv': 'True', 'use_reqs': 'True',
            'use_pipreqs': 'True', 'upx': 'False', 'concise_log': 'True',
            'cpu_cores': str(os.cpu_count() or 2), 'upx_path': '',
            'exclude_modules': '', 'out_mode': '0', 'custom_out_dir': '',
            'sound_notify': 'True', 'auto_save_log': 'False'
        }
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                config.write(f)
        except: pass
    else:
        config.read(CONFIG_FILE, encoding='utf-8')
        if 'Mappings' not in config: config['Mappings'] = DEFAULT_MAPPINGS
        if 'Settings' not in config: config['Settings'] = {}
        default_updates = {
            'concise_log': 'True',
            'cpu_cores': str(os.cpu_count() or 2),
            'upx_path': '',
            'exclude_modules': '',
            'out_mode': '0',
            'custom_out_dir': '',
            'sound_notify': 'True',
            'auto_save_log': 'False'
        }
        updated = False
        for k, v in default_updates.items():
            if k not in config['Settings']:
                config['Settings'][k] = v
                updated = True
        if updated:
            try: save_config(config)
            except: pass
    return config

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            config.write(f)
    except: pass

def is_cloud_locked(filepath):
    try:
        with open(filepath, 'rb') as f:
            return b"__CLOUDSYNC_ENC__" in f.read(1024)
    except (PermissionError, OSError):
        return True
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
        "        if isinstance(node, ast.Import): imports.update(a.name.split('.')[0] for a in node.names)\n"
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
        flags = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
        proc = subprocess.run([python_exe, "-c", code_snippet, script_path], 
                              capture_output=True, text=True, env=env, creationflags=flags)
        m = re.search(r'__QPYPACK_RES__:(.*)', proc.stdout)
        if m:
            return set(json.loads(m.group(1).strip()))
        return set()
    except:
        return set()

def get_svg_icon(name, color="#5F6368", size=24):
    path_data = MATERIAL_ICONS.get(name, "")
    svg_str = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{size}" height="{size}"><path fill="{color}" d="{path_data}"/></svg>'
    renderer = QSvgRenderer()
    renderer.load(svg_str.encode('utf-8'))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)

def get_svg_pixmap(name, color="#5F6368", size=64):
    return get_svg_icon(name, color, size).pixmap(size, size)

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
    if sys.version_info >= (3, 10): libs.update(sys.stdlib_module_names)
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
        
    if os.name == 'nt':
        try:
            py = shutil.which("py")
            if py:
                clean_env = os.environ.copy()
                clean_env.pop("PYTHONHOME", None)
                clean_env.pop("PYTHONPATH", None)
                proc = subprocess.Popen(
                    [py, "-c", "import sys; print(sys.executable)"], 
                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                    text=True, env=clean_env, creationflags=subprocess.CREATE_NO_WINDOW
                )
                out, _ = proc.communicate(timeout=3)
                if out and os.path.exists(out.strip()): 
                    candidates.append(out.strip())
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

    for cand in candidates:
        cand = os.path.normpath(cand)
        if not os.path.exists(cand): continue
        
        if os.name == 'nt' and "WindowsApps" in cand:
            try:
                if os.path.getsize(cand) == 0: continue
            except: continue
            
        clean_env = os.environ.copy()
        clean_env.pop("PYTHONHOME", None)
        clean_env.pop("PYTHONPATH", None)
        
        try:
            flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            proc = subprocess.run(
                [cand, "-V"], capture_output=True, env=clean_env, 
                creationflags=flags, timeout=3
            )
            if proc.returncode == 0:
                return cand
        except:
            continue
            
    return "python"

def get_python_executable():
    if getattr(sys, 'frozen', False) or '__compiled__' in globals():
        return find_system_python()
        
    exe_name = Path(sys.executable).name.lower()
    if exe_name in ('python.exe', 'python3.exe', 'pythonw.exe', 'python', 'python3'):
        return sys.executable
        
    return find_system_python()

def remove_readonly(func, path, exc_info):
    try: os.chmod(path, stat.S_IWRITE); func(path)
    except: pass

def robust_rmtree(path: Path, retries=15, delay=0.8):
    if not path.exists(): return True
    for _ in range(retries):
        try:
            shutil.rmtree(path, onerror=remove_readonly)
            if not path.exists(): return True
        except: time.sleep(delay)
    return False

def parse_add_data(add_data_str):
    datas = []
    for d in add_data_str.split(','):
        d = d.strip()
        if not d: continue
        if ":" in d:
            last_colon_idx = d.rfind(':')
            if last_colon_idx > 1:
                src_path = d[:last_colon_idx].strip()
                dst_path = d[last_colon_idx+1:].strip()
            else:
                src_path = d.strip()
                dst_path = "."
        else:
            src_path = d.strip()
            dst_path = "."
        datas.append((src_path, dst_path))
    return datas

def play_alert(success=True):
    try:
        if os.name == 'nt':
            import winsound
            winsound.MessageBeep(winsound.MB_OK if success else winsound.MB_ICONHAND)
        else:
            sys.stdout.write('\a')
            sys.stdout.flush()
    except:
        pass


class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
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
        if not self.pixmap or self.pixmap.isNull():
            return
            
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
        
        pix_rect = QRect(
            int(center_x - draw_size / 2), 
            int(icon_center_y - draw_size / 2), 
            draw_size, 
            draw_size
        )
        scaled_pix = self.pixmap.scaled(draw_size, draw_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap(pix_rect, scaled_pix)
        painter.end()


class DropArea(QFrame):
    fileDropped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DropArea") 
        self.setAcceptDrops(True)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            #DropArea { background-color: #f8f9fa; border: 2px dashed #dadce0; border-radius: 12px; }
            #DropArea:hover { background-color: #f1f3f4; border: 2px dashed #bdc1c6; }
        """)
        self.init_ui()

    def _get_default_pixmap(self, size=88):
        icon_path = get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            pixmap = QIcon(icon_path).pixmap(size, size)
            if not pixmap.isNull():
                return pixmap
        return get_svg_pixmap('python', color="#9AA0A6", size=size)

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
        
        self.label = QLabel("将 Python 脚本 (.py/.pyw) 拖拽至此处\n或 点击浏览文件")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("QLabel { background: transparent; color: #5F6368; font-size: 16px; font-weight: bold; border: none; }")
        layout.addWidget(self.label)
        
        layout.addSpacing(8)
        
        self.sub_label = QLabel("智能解析工程依赖、静态附件及隐藏模块树")
        self.sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sub_label.setStyleSheet("QLabel { background: transparent; color: #9AA0A6; font-size: 13px; border: none; }")
        layout.addWidget(self.sub_label)
        
        layout.addStretch(1)

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
            fp, _ = QFileDialog.getOpenFileName(
                self, 
                "选择 Python 源代码文件", 
                "", 
                "Python Scripts (*.py *.pyw);;All Files (*)"
            )
            if fp: self.fileDropped.emit(fp)

    def set_loading(self, filename):
        pixmap = get_svg_pixmap('package', color="#1A73E8", size=88)
        self.icon_widget.set_file_pixmap(pixmap, 88)
        self.label.setText(f"文件已加载：{filename}")
        self.label.setStyleSheet("QLabel { background: transparent; color: #1A73E8; font-size: 16px; font-weight: bold; border: none; }")
        self.sub_label.setText("正在分析依赖与元数据，请稍候...")

    def set_success(self, filename, custom_icon_path=None):
        pixmap = None
        if custom_icon_path and Path(custom_icon_path).exists():
            pixmap = QIcon(str(custom_icon_path)).pixmap(88, 88)
            if pixmap.isNull():
                pixmap = None
                
        if not pixmap:
            pixmap = get_svg_pixmap('package', color="#1A73E8", size=88)
            
        self.icon_widget.set_file_pixmap(pixmap, 88)
            
        self.label.setText(f"文件已加载：{filename}")
        self.label.setStyleSheet("QLabel { background: transparent; color: #1A73E8; font-size: 16px; font-weight: bold; border: none; }")
        self.sub_label.setText("系统准备就绪，随时可启动构建引擎")

    def start_build_anim(self):
        self.sub_label.setText("构建引擎运行中：正在执行模块分析与环境封装...")
        self.icon_widget.start_building()

    def stop_build_anim(self):
        self.icon_widget.stop_building()

    def show_success(self, custom_icon_path=None):
        size = 128
        pixmap_set = False
        if custom_icon_path and Path(custom_icon_path).exists():
            pix = QIcon(str(custom_icon_path)).pixmap(size, size)
            if not pix.isNull():
                self.icon_widget.set_custom_pixmap(pix, size)
                pixmap_set = True
                
        if not pixmap_set:
            if self.icon_widget.base_pixmap and not self.icon_widget.base_pixmap.isNull():
                self.icon_widget.set_custom_pixmap(self.icon_widget.base_pixmap, size)
            else:
                self.icon_widget.set_custom_pixmap(get_svg_pixmap('check', color="#1E8E3E", size=size), size)
            
        self.icon_widget.start_success()
            
        self.label.setText("构建任务圆满完成！")
        self.label.setStyleSheet("QLabel { background: transparent; color: #1E8E3E; font-size: 20px; font-weight: bold; border: none; }")
        self.sub_label.setText("您可以打开输出目录查看产物，或重置工作区")

    def show_failure(self):
        size = 128
        self.icon_widget.set_custom_pixmap(get_svg_pixmap('close', color="#D93025", size=size), size)
        self.icon_widget.start_failure()
        
        self.label.setText("构建任务异常中断！")
        self.label.setStyleSheet("QLabel { background: transparent; color: #D93025; font-size: 20px; font-weight: bold; border: none; }")
        self.sub_label.setText("请查阅下方的执行日志报告以进行问题排查")
        
    def reset(self):
        self.icon_widget.reset()
        self.label.setText("将 Python 脚本 (.py/.pyw) 拖拽至此处\n或 点击浏览文件")
        self.label.setStyleSheet("QLabel { background: transparent; color: #5F6368; font-size: 16px; font-weight: bold; border: none; }")
        self.sub_label.setText("智能解析工程依赖、静态附件及隐藏模块树")


class SettingsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_win = parent
        
        self.upx_check = None 
        self.upx_path_container = None
        self.app_scroll_area = None
        self.form_dest = None
        self.form_perf = None
        
        self.setStyleSheet("""
            SettingsPanel { background-color: white; }
            QLabel { color: #3c4043; font-size: 13px; font-weight: bold; background: transparent; }
            QComboBox, QLineEdit, QSpinBox { color: #3c4043; font-size: 13px; padding: 6px 10px; border: 1px solid #dadce0; border-radius: 6px; background: #fff; min-height: 24px; }
            QComboBox:hover, QLineEdit:hover, QSpinBox:hover { border-color: #bdc1c6; }
            QComboBox:focus, QLineEdit:focus, QSpinBox:focus { border-color: #1A73E8; }
            QGroupBox { border: 1px solid #e8eaed; border-radius: 8px; margin-top: 15px; padding-top: 15px; background-color: #f8f9fa; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; left: 15px; top: 0px; color: #1A73E8; font-weight: bold; font-size: 13px; padding: 0 5px; background: transparent; }
            QCheckBox { font-size: 13px; color: #3c4043; spacing: 8px; background: transparent; }
            QCheckBox::indicator { width: 16px; height: 16px; border: 1px solid #bdc1c6; border-radius: 4px; background: white; }
            QCheckBox::indicator:checked { background: #1A73E8; border-color: #1A73E8; image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='white'><path d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/></svg>"); }
            QPushButton.ToolBtn { padding: 5px 12px; border: 1px solid #dadce0; border-radius: 6px; background: #f1f3f4; font-size: 12px; font-weight: bold; color: #5f6368;}
            QPushButton.ToolBtn:hover { background: #e8eaed; color: #202124; }
            QTabWidget::pane { border: 1px solid #e8eaed; border-radius: 8px; background: white; top: -1px; }
            QTabBar::tab { background: #f1f3f4; border: 1px solid #e8eaed; padding: 10px 20px; margin-right: 4px; border-top-left-radius: 8px; border-top-right-radius: 8px; color: #5f6368; font-weight: bold; font-size: 13px; }
            QTabBar::tab:selected { background: white; border-bottom-color: white; color: #1A73E8; }
            QTabBar::tab:hover:!selected { background: #e8eaed; }
        """)
        self.init_ui()
        self.load_from_config()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15) 
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.tabs = QTabWidget()
        self.tab_basic = QWidget()
        self.tab_env = QWidget()
        self.tab_meta = QWidget()
        self.tab_app = QWidget()
        
        self.tabs.addTab(self.tab_basic, get_svg_icon('package', "#1A73E8"), " 产物元数据")
        self.tabs.addTab(self.tab_env, get_svg_icon('python', "#1A73E8"), " 编译控制")
        self.tabs.addTab(self.tab_meta, get_svg_icon('info', "#1A73E8"), " 资源与沙盒")
        self.tabs.addTab(self.tab_app, get_svg_icon('settings', "#1A73E8"), " 软件设置")
        
        self.build_basic_tab()
        self.build_env_tab()
        self.build_meta_tab()
        self.build_app_tab()
        layout.addWidget(self.tabs)
        
        btn_lay = QHBoxLayout()
        btn_lay.setContentsMargins(0, 5, 0, 0)
        btn_lay.setSpacing(12)
        
        self.btn_reset = AnimatedButton("")
        self.btn_reset.setFixedSize(44, 44)
        self.btn_reset.setIcon(get_svg_icon('refresh', "#5F6368"))
        self.btn_reset.setToolTip("恢复默认配置")
        self.btn_reset.setStyleSheet(self.parent_win.icon_btn_style)
        self.btn_reset.clicked.connect(self.parent_win.reset_all)
        btn_lay.addWidget(self.btn_reset)
        
        self.btn_save = AnimatedButton(" 保存并返回工作区")
        self.btn_save.setFixedHeight(44)
        self.btn_save.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_save.setIcon(get_svg_icon('check', "white"))
        self.btn_save.setStyleSheet(self.parent_win.primary_btn_style)
        self.btn_save.clicked.connect(self.parent_win.save_settings_and_return)
        btn_lay.addWidget(self.btn_save)

        self.btn_back = AnimatedButton("")
        self.btn_back.setFixedSize(44, 44)
        self.btn_back.setIcon(get_svg_icon('back', "#5F6368"))
        self.btn_back.setToolTip("放弃修改并返回")
        self.btn_back.setStyleSheet(self.parent_win.icon_btn_style)
        self.btn_back.clicked.connect(self.parent_win.show_main)
        btn_lay.addWidget(self.btn_back)
        
        layout.addLayout(btn_lay)

    def load_from_config(self):
        config = load_config()
        if 'Settings' in config:
            s = config['Settings']
            self.engine_combo.setCurrentText(s.get('engine', 'PyInstaller'))
            self.onefile_check.setChecked(s.getboolean('onefile', True))
            self.noconsole_check.setChecked(s.getboolean('noconsole', True))
            self.clean_all_check.setChecked(s.getboolean('clean_all', True))
            self.auto_icon_check.setChecked(s.getboolean('auto_icon', True))
            self.pip_source_edit.setText(s.get('pip_index', 'https://pypi.tuna.tsinghua.edu.cn/simple'))
            self.venv_check.setChecked(s.getboolean('use_venv', True))
            self.reqs_check.setChecked(s.getboolean('use_reqs', True))
            self.pipreqs_check.setChecked(s.getboolean('use_pipreqs', True))
            
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

    def save_to_config(self):
        config = load_config()
        if 'Settings' not in config: config['Settings'] = {}
        s = config['Settings']
        s['engine'] = self.engine_combo.currentText()
        s['onefile'] = str(self.onefile_check.isChecked())
        s['noconsole'] = str(self.noconsole_check.isChecked())
        s['clean_all'] = str(self.clean_all_check.isChecked())
        s['auto_icon'] = str(self.auto_icon_check.isChecked())
        s['pip_index'] = self.pip_source_edit.text().strip()
        s['use_venv'] = str(self.venv_check.isChecked())
        s['use_reqs'] = str(self.reqs_check.isChecked())
        s['use_pipreqs'] = str(self.pipreqs_check.isChecked())
        if self.upx_check:
            s['upx'] = str(self.upx_check.isChecked())
        s['upx_path'] = self.upx_path_edit.text().strip()
        s['cpu_cores'] = str(self.cores_spin.value())
        s['exclude_modules'] = self.exclude_edit.text().strip()
        s['out_mode'] = str(self.out_mode_combo.currentIndex())
        s['custom_out_dir'] = self.out_dir_edit.text().strip()
        s['concise_log'] = str(self.concise_log_check.isChecked())
        s['sound_notify'] = str(self.sound_notify_check.isChecked())
        s['auto_save_log'] = str(self.auto_save_log_check.isChecked())
        save_config(config)

    def build_basic_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        content.setStyleSheet("background: white;")
        lay = QVBoxLayout(content)
        lay.setContentsMargins(15, 15, 15, 15)
        
        grp_core = QGroupBox("核心参数")
        form_core = QFormLayout(grp_core)
        form_core.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form_core.setContentsMargins(15, 20, 15, 15)
        form_core.setVerticalSpacing(12)
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("留空则与入口脚本同名")
        form_core.addRow("输出名称:", self.name_edit)
        
        self.icon_edit = QLineEdit()
        self.icon_preview = QLabel()
        self.icon_preview.setFixedSize(28, 28)
        self.icon_preview.setScaledContents(True)
        self.icon_edit.textChanged.connect(self.update_icon_preview)
        btn_icon = QPushButton("浏览...")
        btn_icon.setProperty("class", "ToolBtn")
        btn_icon.clicked.connect(self.select_icon)
        h_icon = QHBoxLayout()
        h_icon.addWidget(self.icon_edit)
        h_icon.addWidget(self.icon_preview)
        h_icon.addWidget(btn_icon)
        form_core.addRow("应用图标:", h_icon)
        lay.addWidget(grp_core)

        grp_mode = QGroupBox("打包模式")
        grid_mode = QGridLayout(grp_mode)
        grid_mode.setContentsMargins(15, 20, 15, 15)
        grid_mode.setVerticalSpacing(15)
        
        self.onefile_check = QCheckBox("单文件模式 (OneFile)")
        self.noconsole_check = QCheckBox("隐藏控制台 (GUI模式)")
        
        grid_mode.addWidget(self.onefile_check, 0, 0)
        grid_mode.addWidget(self.noconsole_check, 0, 1)
        lay.addWidget(grp_mode)
        
        self.grp_meta = QGroupBox("版本元数据 (Metadata)")
        meta_form = QFormLayout(self.grp_meta)
        meta_form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        meta_form.setContentsMargins(15, 20, 15, 15)
        meta_form.setVerticalSpacing(12)
        
        self.ver_ver = QLineEdit("1.0.0")
        self.ver_comp = QLineEdit("My Studio")
        self.ver_desc = QLineEdit("Python Executable")
        meta_form.addRow("版本序列:", self.ver_ver)
        meta_form.addRow("发行公司:", self.ver_comp)
        meta_form.addRow("文件描述:", self.ver_desc)
        lay.addWidget(self.grp_meta)
        
        lay.addStretch() 
        scroll.setWidget(content)
        main_lay = QVBoxLayout(self.tab_basic)
        main_lay.setContentsMargins(0,0,0,0)
        main_lay.addWidget(scroll)

    def build_env_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        content.setStyleSheet("background: white;")
        lay = QVBoxLayout(content)
        lay.setContentsMargins(15, 15, 15, 15)
        
        grp_engine = QGroupBox("编译器引擎")
        form_engine = QFormLayout(grp_engine)
        form_engine.setContentsMargins(15, 20, 15, 15)
        form_engine.setVerticalSpacing(12)
        
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["PyInstaller", "Nuitka"])
        self.engine_combo.currentIndexChanged.connect(self.on_engine_changed)
        form_engine.addRow("构建引擎选择:", self.engine_combo)
        lay.addWidget(grp_engine)

        grp_modules = QGroupBox("精细化模块过滤")
        form_mod = QFormLayout(grp_modules)
        form_mod.setContentsMargins(15, 20, 15, 15)
        form_mod.setVerticalSpacing(12)
        
        self.exclude_edit = QLineEdit()
        self.exclude_edit.setPlaceholderText("例如: tkinter, matplotlib (排除打包，减少体积)")
        form_mod.addRow("屏蔽指定模块:", self.exclude_edit)
        lay.addWidget(grp_modules)

        grp_dep = QGroupBox("包与依赖分析机制")
        dep_lay = QVBoxLayout(grp_dep)
        dep_lay.setContentsMargins(15, 20, 15, 15)
        dep_lay.setSpacing(15)

        grid_dep = QGridLayout()
        self.reqs_check = QCheckBox("优先读取 requirements.txt")
        self.pipreqs_check = QCheckBox("启用 pipreqs 深度代码分析")
        
        grid_dep.addWidget(self.reqs_check, 0, 0)
        grid_dep.addWidget(self.pipreqs_check, 0, 1)
        dep_lay.addLayout(grid_dep)

        form_dep = QFormLayout()
        form_dep.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.hidden_edit = QLineEdit()
        self.hidden_edit.setPlaceholderText("例如: pandas, PyQt5 (逗号分隔)")
        btn_scan = QPushButton("AST 扫描")
        btn_scan.setProperty("class", "ToolBtn")
        btn_scan.clicked.connect(self.auto_scan_hidden)
        h_hid = QHBoxLayout()
        h_hid.addWidget(self.hidden_edit)
        h_hid.addWidget(btn_scan)
        form_dep.addRow("隐式依赖:", h_hid)
        dep_lay.addLayout(form_dep)
        lay.addWidget(grp_dep)
        
        lay.addStretch()
        
        scroll.setWidget(content)
        main_lay = QVBoxLayout(self.tab_env)
        main_lay.setContentsMargins(0,0,0,0)
        main_lay.addWidget(scroll)

    def build_meta_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        content.setStyleSheet("background: white;")
        lay = QVBoxLayout(content)
        lay.setContentsMargins(15, 15, 15, 15)
        
        grp_res = QGroupBox("附加资源归档")
        form_res = QFormLayout(grp_res)
        form_res.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form_res.setContentsMargins(15, 20, 15, 15)
        form_res.setVerticalSpacing(12)
        
        self.add_data_edit = QLineEdit()
        self.add_data_edit.setPlaceholderText("例如: data/model.bin:data")
        btn_add = QPushButton("添加...")
        btn_add.setProperty("class", "ToolBtn")
        btn_add.clicked.connect(self.add_resource)
        h_res = QHBoxLayout()
        h_res.addWidget(self.add_data_edit)
        h_res.addWidget(btn_add)
        form_res.addRow("附加资源:", h_res)
        lay.addWidget(grp_res)

        grp_env = QGroupBox("执行环境隔离")
        form_env = QFormLayout(grp_env)
        form_env.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form_env.setContentsMargins(15, 20, 15, 15)
        form_env.setVerticalSpacing(12)
        
        self.pip_source_edit = QLineEdit()
        form_env.addRow("PIP 镜像:", self.pip_source_edit)
        
        self.venv_check = QCheckBox("启用独立沙盒打包环境 (Venv)")
        form_env.addRow("", self.venv_check)
        lay.addWidget(grp_env)
        
        lay.addStretch()
        
        scroll.setWidget(content)
        main_lay = QVBoxLayout(self.tab_meta)
        main_lay.setContentsMargins(0,0,0,0)
        main_lay.addWidget(scroll)

    def build_app_tab(self):
        self.app_scroll_area = QScrollArea()
        self.app_scroll_area.setWidgetResizable(True)
        self.app_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.app_scroll_area.setStyleSheet("background: transparent;")
        
        content = QWidget()
        content.setStyleSheet("background: white;")
        lay = QVBoxLayout(content)
        lay.setContentsMargins(15, 15, 15, 15)
        
        # 编译资源限制组
        self.form_perf = QFormLayout()
        grp_perf = QGroupBox("编译资源限制与压缩优化")
        grp_perf.setLayout(self.form_perf)
        self.form_perf.setContentsMargins(15, 20, 15, 15)
        self.form_perf.setVerticalSpacing(12)
        
        self.cores_spin = QSpinBox()
        self.cores_spin.setRange(1, os.cpu_count() or 4)
        self.cores_spin.setValue(os.cpu_count() or 2)
        self.form_perf.addRow("并发编译线程数:", self.cores_spin)
        
        self.upx_check = QCheckBox("启用 PyInstaller UPX 压缩优化")
        self.upx_check.toggled.connect(self.on_upx_toggled)
        self.form_perf.addRow("", self.upx_check)
        
        self.upx_path_edit = QLineEdit()
        self.upx_path_edit.setPlaceholderText("留空则在全局环境或当前目录下自动定位 UPX...")
        self.btn_upx_path = QPushButton("选择...")
        self.btn_upx_path.setProperty("class", "ToolBtn")
        self.btn_upx_path.clicked.connect(self.select_upx_path)
        
        self.upx_path_container = QWidget()
        self.upx_path_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.upx_path_container.setMinimumHeight(32)
        h_upx = QHBoxLayout(self.upx_path_container)
        h_upx.setContentsMargins(0, 0, 0, 0)
        h_upx.setSpacing(6)
        h_upx.addWidget(self.upx_path_edit)
        h_upx.addWidget(self.btn_upx_path)
        self.form_perf.addRow("自定义 UPX 目录:", self.upx_path_container)
        lay.addWidget(grp_perf)
        
        # 产物保存路径策略组
        self.form_dest = QFormLayout()
        grp_dest = QGroupBox("构建产物保存路径")
        grp_dest.setLayout(self.form_dest)
        self.form_dest.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.form_dest.setContentsMargins(15, 20, 15, 15)
        self.form_dest.setVerticalSpacing(12)
        
        self.out_mode_combo = QComboBox()
        self.out_mode_combo.addItems(["默认路径 (保存在源脚本所在同目录)", "保存到自定义输出目录"])
        self.out_mode_combo.currentIndexChanged.connect(self.on_out_mode_changed)
        self.form_dest.addRow("保存位置模式:", self.out_mode_combo)
        
        self.out_dir_edit = QLineEdit()
        self.out_dir_edit.setPlaceholderText("选择自定义输出保存路径...")
        self.out_dir_edit.setMinimumWidth(150)
        self.btn_out_dir = QPushButton("浏览...")
        self.btn_out_dir.setFixedWidth(75)
        self.btn_out_dir.setProperty("class", "ToolBtn")
        self.btn_out_dir.clicked.connect(self.select_out_dir)
        
        self.out_dir_container = QWidget()
        self.out_dir_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.out_dir_container.setMinimumHeight(32)
        h_out_dir = QHBoxLayout(self.out_dir_container)
        h_out_dir.setContentsMargins(0, 0, 0, 0)
        h_out_dir.setSpacing(6)
        h_out_dir.addWidget(self.out_dir_edit)
        h_out_dir.addWidget(self.btn_out_dir)
        self.form_dest.addRow("自定义目录路径:", self.out_dir_container)
        lay.addWidget(grp_dest)

        # 偏好控制与反馈组
        grp_app = QGroupBox("偏好习惯与通知反馈")
        grid_app = QGridLayout(grp_app)
        grid_app.setContentsMargins(15, 20, 15, 15)
        grid_app.setVerticalSpacing(15)
        
        self.concise_log_check = QCheckBox("启用简洁日志模式 (自动屏蔽警告与垃圾调试信息)")
        self.clean_all_check = QCheckBox("编译结束后自动清理临时缓存文件目录")
        self.auto_icon_check = QCheckBox("自动匹配入口脚本同目录下的同名ico图标")
        self.sound_notify_check = QCheckBox("编译构建任务结束时发出声音反馈提示")
        self.auto_save_log_check = QCheckBox("打包结束后自动在目标输出目录导出运行日志 (.log)")
        
        grid_app.addWidget(self.concise_log_check, 0, 0)
        grid_app.addWidget(self.clean_all_check, 1, 0)
        grid_app.addWidget(self.auto_icon_check, 2, 0)
        grid_app.addWidget(self.sound_notify_check, 3, 0)
        grid_app.addWidget(self.auto_save_log_check, 4, 0)
        lay.addWidget(grp_app)
        
        lay.addStretch()
        
        self.app_scroll_area.setWidget(content)
        main_lay = QVBoxLayout(self.tab_app)
        main_lay.setContentsMargins(0,0,0,0)
        main_lay.addWidget(self.app_scroll_area)

    def on_engine_changed(self):
        if getattr(self, 'upx_check', None) is not None and getattr(self, 'form_perf', None) is not None:
            engine = self.engine_combo.currentText()
            is_pyi = (engine == "PyInstaller")
            self.upx_check.setVisible(is_pyi)
            self.form_perf.setRowVisible(self.upx_path_container, is_pyi and self.upx_check.isChecked())

    def on_upx_toggled(self, checked):
        if getattr(self, 'form_perf', None) is not None:
            self.form_perf.setRowVisible(self.upx_path_container, checked)
            if checked and getattr(self, 'app_scroll_area', None) is not None:
                QTimer.singleShot(50, lambda: self.app_scroll_area.ensureWidgetVisible(self.upx_path_container))

    def on_out_mode_changed(self, index):
        show_custom = (index == 1)
        if getattr(self, 'form_dest', None) is not None:
            self.form_dest.setRowVisible(self.out_dir_container, show_custom)
            if show_custom and getattr(self, 'app_scroll_area', None) is not None:
                QTimer.singleShot(50, lambda: self.app_scroll_area.ensureWidgetVisible(self.out_dir_container))

    def select_out_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择输出保存目录")
        if d:
            self.out_dir_edit.setText(Path(d).resolve().as_posix())

    def select_upx_path(self):
        d = QFileDialog.getExistingDirectory(self, "选择 UPX 工具根目录")
        if d:
            self.upx_path_edit.setText(Path(d).resolve().as_posix())

    def update_icon_preview(self, path):
        if path and Path(path).exists():
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                self.icon_preview.setPixmap(pixmap.scaled(28, 28, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                return
        self.icon_preview.clear()

    def select_icon(self):
        p, _ = QFileDialog.getOpenFileName(self, "选择图标", "", "Icon Files (*.ico *.svg)")
        if p: self.icon_edit.setText(Path(p).resolve().as_posix())

    def auto_scan_hidden(self):
        script_path = self.parent_win.script_path
        if not script_path: return QMessageBox.warning(self, "构建约束", "请先加载有效的 Python 源代码文件！")
        if is_cloud_locked(script_path):
            return QMessageBox.warning(self, "I/O 错误", "目标脚本处于云盘加密或锁定状态，请解密后重试。")
            
        try:
            python_exe = get_python_executable()
            hidden = extract_imports_via_ast(script_path, python_exe)
            hidden = [m for m in hidden if m not in STD_LIBS]
            self.hidden_edit.setText(','.join(hidden))
            QMessageBox.information(self, "AST 分析完成", f"语法树解析成功，共定位到 {len(hidden)} 项非标准库依赖。")
        except Exception as e: 
            QMessageBox.warning(self, "分析异常", f"AST 语法树解析过程中发生异常: {e}")

    def add_resource(self):
        choice = QMessageBox.question(self, "添加资源", "Yes=文件, No=文件夹", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if choice == QMessageBox.StandardButton.Yes:
            files, _ = QFileDialog.getOpenFileNames(self, "选择文件", "", "All Files (*)")
            for f in files:
                f = Path(f).resolve().as_posix()
                default_dest = Path(f).name
                dest, ok = QInputDialog.getText(self, "相对路径", f"目标位置:", text=default_dest)
                if ok:
                    dest = dest.strip().replace('\\', '/') if dest else default_dest
                    curr = self.add_data_edit.text().strip()
                    self.add_data_edit.setText(f"{curr}, {f}:{dest}" if curr else f"{f}:{dest}")
        else:
            folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
            if folder:
                folder = Path(folder).resolve().as_posix()
                default_dest = Path(folder).name
                dest, ok = QInputDialog.getText(self, "相对路径", f"目标位置:", text=default_dest)
                if ok:
                    dest = dest.strip().replace('\\', '/') if dest else default_dest
                    curr = self.add_data_edit.text().strip()
                    self.add_data_edit.setText(f"{curr}, {folder}:{dest}" if curr else f"{folder}:{dest}")


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
            if v_match: 
                version = v_match.group(1)
                
            c_match = re.search(r'^(?:__company__|COMPANY)\s*=\s*[\'"]([^\'"]+)[\'"]', content, re.M | re.I)
            if c_match: 
                author = c_match.group(1)
            else:
                a_match = re.search(r'^(?:__author__|AUTHOR)\s*=\s*[\'"]([^\'"]+)[\'"]', content, re.M | re.I)
                if a_match: 
                    author = a_match.group(1)
                
            n_match = re.search(r'^(?:__title__|__app_name__|APP_NAME)\s*=\s*[\'"]([^\'"]+)[\'"]', content, re.M | re.I)
            if n_match: 
                app_name = n_match.group(1)
                
            d_match = re.search(r'^(?:__description__|DESCRIPTION)\s*=\s*[\'"]([^\'"]+)[\'"]', content, re.M | re.I)
            if d_match: 
                desc = d_match.group(1)
        except:
            pass

        try:
            python_exe = get_python_executable()
            script_imports = extract_imports_via_ast(self.path, python_exe)
        except:
            pass

        self.analysis_done.emit(app_name, version, author, desc, script_imports)


class PackingThread(QThread):
    progress = Signal(str)
    finished = Signal(bool, str)

    def __init__(self, params):
        super().__init__()
        self.params = params
        self.process = None
        self._is_cancelled = False
        self.venv_dir = None
        self.temp_workpath = None
        self.temp_out_dir = None
        self.all_raw_logs = []  

    def cancel(self):
        self._is_cancelled = True
        if self.process:
            try:
                if os.name == "nt": subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.process.pid)], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                else: self.process.kill()
            except: pass

    def run_cmd(self, cmd, cwd=None, timeout=None):
        if self._is_cancelled: return False
        
        timer = None
        is_timeout = [False]
        cmd_raw_lines = []  
        
        clean_env = os.environ.copy()
        clean_env.pop("PYTHONHOME", None)
        clean_env.pop("PYTHONPATH", None)
        
        try:
            kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.STDOUT, "cwd": cwd, 
                      "text": True, "errors": "replace", "env": clean_env}
            if os.name == 'nt': kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
            
            self.process = subprocess.Popen(cmd, **kwargs)
            
            if timeout:
                def kill_proc():
                    is_timeout[0] = True
                    try:
                        if os.name == "nt":
                            subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.process.pid)], 
                                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        else:
                            self.process.kill()
                    except:
                        pass
                timer = threading.Timer(timeout, kill_proc)
                timer.start()

            buffer = []
            last_emit = time.time()
            
            def is_noisy_line(l):
                l_lower = l.lower()
                if "error:" in l_lower:
                    return False
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
            
            if buffer:
                self.progress.emit('\n'.join(buffer))
                
            self.process.wait()
            
            if is_timeout[0]:
                self.progress.emit(f"[System] 子进程执行超时 (>{timeout}s)，已自动中断并继续执行后续流水线...")
                return False
                
            success = self.process.returncode == 0
            
            if not success and self.params.get('concise_log', True) and cmd_raw_lines:
                self.progress.emit("\n" + "!"*10 + " [诊断回溯: 以下是由于该环节执行异常产生的完整原始日志] " + "!"*10)
                self.progress.emit('\n'.join(cmd_raw_lines))
                self.progress.emit("!"*60 + "\n")
                
            return success
        except FileNotFoundError as e:
            cmd_name = cmd[0] if isinstance(cmd, list) and cmd else str(cmd)
            if "python" in str(cmd_name).lower():
                self.progress.emit(f"[Error] 宿主环境异常：无法定位 Python 解释器，请检查系统环境变量配置。")
            else:
                self.progress.emit(f"[Error] 进程调用失败：缺失系统指令或程序 \"{cmd_name}\" ({e})")
            return False
        except Exception as e:
            self.progress.emit(f"[Error] 子进程执行发生系统级异常: {e}")
            return False
        finally:
            if timer:
                timer.cancel()

    def sanitize_script(self, orig_path: Path):
        if is_cloud_locked(orig_path):
            return None, False, "目标脚本处于云盘加密或锁定状态，请解密后重试。"
        
        if not self.params['noconsole']:
            try:
                raw = orig_path.read_bytes()
                try: code = raw.decode('utf-8-sig')
                except: code = raw.decode(locale.getpreferredencoding(), errors='ignore')
                
                pause_code = "\n" + "#"*30 + "\n" + (
                    "try:\n"
                    "    import sys\n"
                    "    if sys.platform == 'win32':\n"
                    "        import ctypes\n"
                    "        kernel32 = ctypes.windll.kernel32\n"
                    "        process_list = (ctypes.c_uint * 10)()\n"
                    "        num_processes = kernel32.GetConsoleProcessList(process_list, 10)\n"
                    "        if num_processes <= 2:\n"
                    "            input('\\n执行完毕，按回车键退出...')\n"
                    "except:\n"
                    "    pass\n"
                )
                
                temp_dir = Path(tempfile.gettempdir())
                temp_file = temp_dir / f"qpypack_build_target_{int(time.time())}.py"
                temp_file.write_text(code + pause_code, encoding='utf-8')
                return temp_file, True, ""
            except Exception as e:
                self.progress.emit(f"[Warn] 注入控制台防闪退机制失败: {e}")
                
        return orig_path, False, ""

    def detect_python_syntax_errors(self):
        import re
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
        is_temp = False
        build_script_path = None
        ext = ".exe" if os.name == "nt" else ""

        try:
            self.progress.emit("[Init] 正在初始化工作区并清理历史残留数据...")
            robust_rmtree(Path.cwd() / "build")
            robust_rmtree(Path.cwd() / "dist")
            
            script_path = Path(self.params['script_path']).resolve()
            script_dir = script_path.parent
            
            build_script_path, is_temp, err_msg = self.sanitize_script(script_path)
            if not build_script_path and err_msg: return self.finished.emit(False, f"[Error] I/O 异常: {err_msg}")
            script_posix = build_script_path.as_posix()

            system_python_exe = get_python_executable()
            self.progress.emit(f"[Env] 宿主解释器路径: {system_python_exe}")

            script_imports = set()
            try:
                script_imports = extract_imports_via_ast(script_posix, system_python_exe)
            except Exception as e:
                self.progress.emit(f"[Warn] 源码 AST 预处理异常: {e}")

            pip_args = ["-i", pip_idx] if pip_idx else []
            
            if self.params['use_venv']:
                self.progress.emit("[Env] 正在分配独立隔离的虚拟环境 (Virtual Environment)...")
                self.venv_dir = Path(tempfile.mkdtemp(prefix="qpypack_env_")).resolve()
                if not self.run_cmd([system_python_exe, "-m", "venv", self.venv_dir.as_posix()]):
                    return self.finished.emit(False, "[Error] 虚拟环境(venv)创建失败。宿主 Python 环境可能存在内核文件缺失或权限受限。")
                python_exe = (self.venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")).as_posix()
                
                self.progress.emit("[Env] 正在同步并升级 Pip 构建工具链...")
                self.run_cmd([python_exe, "-m", "pip", "install", "--upgrade", "pip", "-q"] + pip_args)
            else: 
                python_exe = system_python_exe

            engine_pkg = "nuitka" if engine == "Nuitka" else "pyinstaller"
            
            self.progress.emit(f"[Env] 正在配置基础构建引擎 ({engine_pkg} & 核心支持库)...")
            core_pkgs = [engine_pkg]
            if engine == "PyInstaller": 
                core_pkgs.append("pillow")
            elif engine == "Nuitka":
                core_pkgs.append("zstandard")
            self.run_cmd([python_exe, "-m", "pip", "install", "-q"] + core_pkgs + pip_args)
                      
            if self.params.get('use_reqs'):
                req_file = script_dir / "requirements.txt"
                if req_file.exists():
                    self.progress.emit("[Deps] 阶段 1/3: 正在读取并部署清单依赖 (requirements.txt)...")
                    try:
                        if is_cloud_locked(req_file): raise ValueError("清单文件被安全锁定")
                        raw_req = req_file.read_bytes()
                        try: req_content = raw_req.decode('utf-8-sig')
                        except: req_content = raw_req.decode(locale.getpreferredencoding(), errors='ignore')
                        
                        temp_req = Path(tempfile.gettempdir()) / f"qpypack_temp_reqs_{int(time.time())}.txt"
                        temp_req.write_text(req_content, encoding='utf-8')
                        self.run_cmd([python_exe, "-m", "pip", "install", "-q", "-r", temp_req.as_posix()] + pip_args)
                        temp_req.unlink(missing_ok=True)
                    except Exception as e: self.progress.emit(f"[Warn] 清单解析或网络请求异常: {e}")

            if self.params.get('use_pipreqs'):
                self.progress.emit("[Deps] 阶段 2/3: 正在启动深度依赖分析 (Pipreqs)...")
                self.run_cmd([python_exe, "-m", "pip", "install", "pipreqs", "-q"] + pip_args)
                temp_pipreqs = Path(tempfile.gettempdir()) / f"qpypack_pipreqs_{int(time.time())}.txt"
                
                pypi_server = None
                if pip_idx:
                    pypi_server = re.sub(r'/simple/?$', '/pypi', pip_idx.strip(), flags=re.I).rstrip('/')
                
                pipreqs_cmd = [
                    python_exe, "-m", "pipreqs.pipreqs", script_dir.as_posix(), 
                    "--encoding", "utf-8", "--force", "--savepath", temp_pipreqs.as_posix()
                ]
                if pypi_server: 
                    pipreqs_cmd.extend(["--pypi-server", pypi_server])
                    self.progress.emit(f"[Deps] 依赖分析镜像地址: {pypi_server}")
                
                if self.run_cmd(pipreqs_cmd, timeout=15) and temp_pipreqs.exists():
                    self.run_cmd([python_exe, "-m", "pip", "install", "-q", "-r", temp_pipreqs.as_posix()] + pip_args)
                    temp_pipreqs.unlink(missing_ok=True)

            config = load_config()
            known_mappings = DEFAULT_MAPPINGS.copy()
            if 'Mappings' in config:
                for k, v in config['Mappings'].items():
                    known_mappings[k] = v
            
            local_files = {p.stem.lower() for p in script_dir.glob("*")}
            ast_pkgs = [
                known_mappings.get(m, m) 
                for m in script_imports 
                if m not in STD_LIBS and m.lower() not in local_files
            ]
            
            if ast_pkgs:
                self.progress.emit(f"[Deps] 阶段 3/3: 启动 AST 源码扫描...")
                self.progress.emit(f"==> [Deps] 正在对齐隐式依赖项: {', '.join(ast_pkgs)}")
                if not self.run_cmd([python_exe, "-m", "pip", "install", "-q"] + ast_pkgs + pip_args):
                    self.progress.emit("[Warn] 批量依赖同步存在冲突，正在降级为逐项安全安装模式...")
                    for pkg in ast_pkgs:
                        self.run_cmd([python_exe, "-m", "pip", "install", "-q", pkg] + pip_args)

            if self._is_cancelled: return self.finished.emit(False, "[System] 构建任务已被用户主动终止。")

            self.progress.emit(f"[Build] 正在初始化 {engine} 编译引擎，执行可执行程序生成任务...")
            cmd = []
            app_name = self.params['app_name']
            icon_path = Path(self.params['icon']).resolve().as_posix() if self.params.get('icon') else None

            if engine == "PyInstaller":
                self.temp_workpath = Path(tempfile.mkdtemp(prefix="qpypack_build_")).resolve()
                cmd = [python_exe, "-m", "PyInstaller", "--clean", "--noconfirm", f"--workpath={self.temp_workpath.as_posix()}", f"--name={app_name}"]
                
                if self.params['onefile']: cmd.append("--onefile")
                else: cmd.append("--onedir")
                
                if self.params['noconsole']: cmd.append("--noconsole")

                if icon_path: 
                    cmd.extend(["--icon", icon_path])
                    cmd.extend(["--add-data", f"{icon_path}{os.pathsep}."])
                    
                if self.params.get('version_file') and os.name == "nt": cmd.extend(["--version-file", self.params['version_file']])
                if self.params.get('upx'):
                    upx_dir_custom = self.params.get('upx_path', '').strip()
                    if upx_dir_custom and Path(upx_dir_custom).exists():
                        cmd.append(f"--upx-dir={upx_dir_custom}")
                    else:
                        upx_dir_default = (Path.cwd() / "upx").resolve()
                        if upx_dir_default.exists(): cmd.append(f"--upx-dir={upx_dir_default.as_posix()}")
                
                for imp in self.params.get('hidden_imports', '').split(','):
                    if imp.strip(): cmd.extend(["--hidden-import", imp.strip()])
                
                for src, dst in parse_add_data(self.params.get('add_data', '')):
                    cmd.extend(["--add-data", f"{src}{os.pathsep}{dst}"])
                
                for excl in self.params.get('exclude_modules', '').split(','):
                    if excl.strip(): cmd.extend(["--exclude-module", excl.strip()])
                        
            elif engine == "Nuitka":
                self.temp_out_dir = Path(tempfile.mkdtemp(prefix="nuitka_out_")).resolve()
                cmd = [python_exe, "-m", "nuitka", "--remove-output", "--assume-yes-for-downloads",
                       f"--output-dir={self.temp_out_dir.as_posix()}", f"--output-filename={app_name}{ext}"]
                
                cores = self.params.get('cpu_cores', os.cpu_count() or 2)
                cmd.append(f"--jobs={cores}")
                
                if self.params['onefile']: cmd.append("--onefile")
                else: cmd.append("--standalone")
                
                if self.params['noconsole']: cmd.append("--windows-console-mode=disable")
                
                if icon_path: 
                    if os.name == "nt":
                        cmd.append(f"--windows-icon-from-ico={icon_path}")
                    elif sys.platform == "darwin" and icon_path.endswith(".icns"):
                        cmd.append(f"--macos-app-icon={icon_path}")
                    cmd.append(f"--include-data-files={Path(icon_path).resolve().as_posix()}={Path(icon_path).name}")
                    
                if os.name == "nt":
                    if self.params.get('ver_comp'): cmd.append(f"--company-name={self.params['ver_comp']}")
                    if self.params.get('ver_desc'): cmd.append(f"--product-name={self.params['ver_desc']}")
                    if self.params.get('ver_ver'): cmd.append(f"--file-version={self.params['ver_ver']}")
                    
                cmd.append("--enable-plugin=anti-bloat")
                
                if 'PyQt5' in script_imports: cmd.append("--enable-plugin=pyqt5")
                elif 'PyQt6' in script_imports: cmd.append("--enable-plugin=pyqt6")
                elif 'PySide2' in script_imports: cmd.append("--enable-plugin=pyside2")
                elif 'PySide6' in script_imports: cmd.append("--enable-plugin=pyside6")
                
                if 'numpy' in script_imports: cmd.append("--enable-plugin=numpy")
                if 'matplotlib' in script_imports: cmd.append("--enable-plugin=matplotlib")
                if 'tkinter' in script_imports: cmd.append("--enable-plugin=tk-inter")
                
                for imp in self.params.get('hidden_imports', '').split(','):
                    if imp.strip(): cmd.append(f"--include-module={imp.strip()}")
                
                for src, dst in parse_add_data(self.params.get('add_data', '')):
                    src_path = Path(src)
                    if src_path.is_dir():
                        cmd.append(f"--include-data-dir={src_path.resolve().as_posix()}={dst}")
                    else:
                        cmd.append(f"--include-data-files={src_path.resolve().as_posix()}={dst}")

                for excl in self.params.get('exclude_modules', '').split(','):
                    if excl.strip(): cmd.append(f"--exclude-module={excl.strip()}")

            cmd.append(script_posix)

            success = self.run_cmd(cmd, cwd=Path.cwd().resolve().as_posix())
            if self._is_cancelled: return self.finished.emit(False, "[System] 构建任务已被用户主动终止。")

            self.progress.emit("[Pack] 编译阶段完成，正在提取并归档最终可执行产物...")
            cwd = Path.cwd().resolve()
            if engine == "PyInstaller": src_out = cwd / "dist" / (f"{app_name}{ext}" if self.params['onefile'] else app_name)
            elif engine == "Nuitka": src_out = self.temp_out_dir / (f"{app_name}{ext}" if self.params['onefile'] else f"{app_name}.dist")

            out_mode = int(self.params.get('out_mode', 0))
            custom_out = self.params.get('custom_out_dir', '').strip()
            if out_mode == 1 and custom_out:
                try:
                    final_out_dir = Path(custom_out)
                    final_out_dir.mkdir(parents=True, exist_ok=True)
                except:
                    final_out_dir = script_dir
            else:
                final_out_dir = script_dir

            final_out = final_out_dir / src_out.name
            if success and src_out.exists():
                try:
                    if final_out.exists():
                        if final_out.is_dir(): shutil.rmtree(final_out, ignore_errors=True)
                        else: final_out.unlink(missing_ok=True)
                    shutil.move(src_out.as_posix(), final_out.as_posix())
                except Exception as e: self.progress.emit(f"[Error] 产物转移异常，文件可能被系统防御机制拦截或占用: {e}")
            else: self.progress.emit(f"[Error] 构建目标缺失，未能在沙盒中定位到有效产物: {src_out}")

            if success and final_out.exists(): 
                self.progress.emit("[Pack] 正在校验最终程序完整性...")
                if self.params.get('auto_save_log') and self.all_raw_logs:
                    try:
                        log_file = final_out_dir / f"qpypack_build_{app_name}.log"
                        log_file.write_text('\n'.join(self.all_raw_logs), encoding='utf-8')
                        self.progress.emit(f"[Log] 打包日志已被导出至: {log_file.as_posix()}")
                    except: pass
                self.finished.emit(True, f"[Success] 构建结束！路径: {final_out.resolve().as_posix()}")
            else: 
                err_info = self.detect_python_syntax_errors()
                if err_info["is_code_error"]:
                    msg = (
                        f"[❌ 语法错误] 检测到您的 Python 源代码存在语法/缩进问题！\n"
                        f"  - 错误文件: {err_info['file']}\n"
                        f"  - 错误类型: {err_info['type']}\n"
                        f"  - 错误位置: 第 {err_info['line']} 行附近\n"
                        f"  - 错误描述: {err_info['desc']}\n"
                        f"\n提示: 此问题为源码本身不合规导致。请先修复脚本错误并能正常执行，然后再尝试打包。"
                    )
                else:
                    if self.params.get('concise_log', True) and self.all_raw_logs:
                        self.progress.emit("\n" + "!"*10 + " [诊断提示: 以下为全局完整运行日志汇总] " + "!"*10)
                        self.progress.emit('\n'.join(self.all_raw_logs[-100:])) 
                    msg = "[Failed] 构建任务异常中断，请参阅上方运行日志以排查错误。"
                self.finished.emit(False, msg)
                
        except Exception as e:
            if self.params.get('concise_log', True) and self.all_raw_logs:
                self.progress.emit("\n" + "!"*10 + " [系统诊断: 崩溃前全局原始日志] " + "!"*10)
                self.progress.emit('\n'.join(self.all_raw_logs[-100:]))
            self.finished.emit(False, f"[System Error] 发生未处理的严重错误: {str(e)}")
        finally:
            if is_temp and build_script_path and build_script_path.exists():
                try: build_script_path.unlink()
                except: pass
                
            if self.params.get('version_file'):
                try: Path(self.params['version_file']).unlink(missing_ok=True)
                except: pass
                
            if self.params.get('temp_icon_file'):
                try: Path(self.params['temp_icon_file']).unlink(missing_ok=True)
                except: pass
                
            if self.params['clean_all']:
                self.progress.emit("[Clean] 正在释放工作区，抹除虚拟环境与沙盒临时数据...")
                for p in [self.venv_dir, self.temp_workpath, self.temp_out_dir]:
                    if p and p.exists(): robust_rmtree(p)
                    
                cwd = Path.cwd().resolve()
                app_name = self.params.get('app_name', 'app')
                robust_rmtree(cwd / "dist")
                for p in ["build", "__pycache__", f"{app_name}.build", f"{app_name}.dist", f"{app_name}.onefile-build"]:
                    robust_rmtree(cwd / p)
                Path(cwd / f"{app_name}.spec").unlink(missing_ok=True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.script_path = ""
        self.thread = None
        self.analysis_thread = None
        self.current_state = "idle" 
        self.init_style()
        self.init_ui()

    def init_style(self):
        self.setWindowTitle(f"{__app_name__} {__version__} - {__author__}")
        
        self.setMinimumSize(610, 560)
        self.resize(610, 560)
        
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
        
        self.icon_btn_style = """
            QPushButton { background-color: #f1f3f4; border: 1px solid transparent; border-radius: 8px; }
            QPushButton:hover { background-color: #e8eaed; }
            QPushButton:pressed { background-color: #dadce0; }
        """
        self.primary_btn_style = """
            QPushButton { background-color: #1A73E8; color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: bold; }
            QPushButton:hover { background-color: #1B66C9; } QPushButton:pressed { background-color: #174EA6; }
        """
        self.danger_btn_style = """
            QPushButton { background-color: #D93025; color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: bold; }
            QPushButton:hover { background-color: #C5221F; } QPushButton:pressed { background-color: #A50E0E; }
        """
        self.success_btn_style = """
            QPushButton { background-color: #1E8E3E; color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: bold; }
            QPushButton:hover { background-color: #188038; } QPushButton:pressed { background-color: #137333; }
        """

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
        self.btn_right.setToolTip("构建配置")
        self.btn_right.setStyleSheet(self.icon_btn_style)
        self.btn_right.clicked.connect(self.show_settings)
        btn_layout.addWidget(self.btn_right)

        layout.addLayout(btn_layout)
        self.stacked_layout.addWidget(self.main_panel)

        self.settings_panel = SettingsPanel(self)
        self.stacked_layout.addWidget(self.settings_panel)
        self.stacked_layout.setCurrentWidget(self.main_panel)
        
        self.statusBar = self.statusBar()
        self.status_label = QLabel(" 状态: 就绪")
        self.statusBar.addWidget(self.status_label)

        self.update_ui_state("idle")

    def update_ui_state(self, state):
        self.current_state = state
        
        self.btn_right.setEnabled(state != "building")
        self.drop_area.setAcceptDrops(state != "building")
        
        if state in ("idle", "ready"):
            is_log_open = self.log_container.isVisible()
            icon_name = 'expand_less' if is_log_open else 'expand_more'
            self.btn_left.setIcon(get_svg_icon(icon_name, "#5F6368"))
            self.btn_left.setToolTip("显示/隐藏执行日志")
            
            self.btn_main.setText(" 开始构建")
            self.btn_main.setIcon(get_svg_icon('play', "white"))
            self.btn_main.setStyleSheet(self.primary_btn_style)
            
        elif state == "building":
            is_log_open = self.log_container.isVisible()
            icon_name = 'expand_less' if is_log_open else 'expand_more'
            self.btn_left.setIcon(get_svg_icon(icon_name, "#5F6368"))
            self.btn_left.setToolTip("显示/隐藏执行日志")
            
            self.btn_main.setText(" 停止构建")
            self.btn_main.setIcon(get_svg_icon('stop', "white"))
            self.btn_main.setStyleSheet(self.danger_btn_style)
            
        elif state in ("done", "failed"):
            self.btn_left.setIcon(get_svg_icon('refresh', "#5F6368"))
            self.btn_left.setToolTip("重置工作区")
            
            if state == "done":
                self.btn_main.setText(" 打开输出目录")
                self.btn_main.setIcon(get_svg_icon('folder', "white"))
                self.btn_main.setStyleSheet(self.success_btn_style)
            else:
                self.btn_main.setText(" 重新构建")
                self.btn_main.setIcon(get_svg_icon('refresh', "white"))
                self.btn_main.setStyleSheet(self.danger_btn_style)

    def on_left_btn_clicked(self):
        if self.current_state in ("done", "failed"):
            self.reset_all()
        else:
            self.toggle_log()

    def on_main_btn_clicked(self):
        if self.current_state in ("idle", "ready", "failed"):
            self.start_pack()
        elif self.current_state == "building":
            self.cancel_pack()
        elif self.current_state == "done":
            self.open_dist()

    def toggle_log(self):
        if self.log_container.isVisible():
            self.log_container.hide()
        else:
            self.log_container.show()
        self.update_ui_state(self.current_state)

    def show_settings(self):
        self._animate_switch(self.settings_panel)

    def show_main(self):
        self._animate_switch(self.main_panel)

    def save_settings_and_return(self):
        self.settings_panel.save_to_config()
        self.show_main()

    def _animate_switch(self, target_widget):
        self.anim = QPropertyAnimation(self.stacked_layout.currentWidget(), b"geometry")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.setStartValue(self.stacked_layout.currentWidget().geometry())
        self.stacked_layout.setCurrentWidget(target_widget)
        self.anim.setEndValue(target_widget.geometry())
        self.anim.start()

    def on_script_selected(self, path):
        path = Path(path).resolve().as_posix()
        
        if is_cloud_locked(path):
            QMessageBox.critical(self, "加载失败", "目标脚本处于云盘加密或锁定状态，请解密后重试。")
            return

        self.script_path = path
        
        self.drop_area.set_loading(Path(path).name)
        self.status_label.setText(f" 状态: 正在解析 {Path(path).name} ...")
        self.btn_main.setEnabled(False)
        
        if self.analysis_thread and self.analysis_thread.isRunning():
            self.analysis_thread.disconnect()
            self.analysis_thread.terminate()
            self.analysis_thread.wait()
            
        self.analysis_thread = ScriptAnalysisThread(path)
        self.analysis_thread.analysis_done.connect(self.on_analysis_finished)
        self.analysis_thread.start()

    def on_analysis_finished(self, app_name, version, author, desc, script_imports):
        path = self.script_path
        if not path: return

        if version:
            self.settings_panel.ver_ver.setText(version)
        else:
            self.settings_panel.ver_ver.setText("1.0.0")
            
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
            for name in ["ICON.ICO", "icon.ico", "logo.ico", "icon.svg", "logo.svg"]:
                trial = script_dir / name
                if trial.exists():
                    auto_icon = trial
                    curr = self.settings_panel.icon_edit.text()
                    if not curr or not Path(curr).exists():
                        self.settings_panel.icon_edit.setText(trial.resolve().as_posix())
                    break
                
        self.drop_area.set_success(Path(path).name, custom_icon_path=auto_icon)
        
        status_suffix = "，已配置为【保留控制台】模式" if not has_gui else "，已配置为GUI模式"
        self.status_label.setText(f" 状态: 已锁定源文件 {Path(path).name}{status_suffix}")
        
        if not self.log_container.isVisible(): self.toggle_log()
        self.log.clear()
        self.append_log(f"[System] 源文件绑定成功: {path}")
        if not has_gui:
            self.append_log("[System] 检测到该脚本不包含常见 GUI 图形框架。已为您保留控制台。")
        self.btn_main.setEnabled(True)
        self.update_ui_state("ready")

    def cancel_pack(self):
        if self.thread and self.thread.isRunning():
            self.thread.cancel()
            self.status_label.setText(" 状态: 任务已被用户主动终止")
            self.drop_area.stop_build_anim()
            self.update_ui_state("ready")

    def start_pack(self):
        if not self.script_path or not Path(self.script_path).exists():
            QMessageBox.warning(self, "构建约束", "请先加载有效的 Python 源代码文件！")
            return

        sp = self.settings_panel
        app_name = sp.name_edit.text().strip() or Path(self.script_path).stem
        engine = sp.engine_combo.currentText()

        version_file = None
        if engine == "PyInstaller" and sp.ver_ver.text().strip():
            try:
                v_str = sp.ver_ver.text().strip()
                v_nums = re.findall(r'\d+', v_str)
                v_tuple = ",".join((v_nums + ['0', '0', '0', '0'])[:4])
                
                content = f'''VSVersionInfo(ffi=FixedFileInfo(filevers=({v_tuple}),prodvers=({v_tuple}),mask=0x3f,flags=0x0,OS=0x40004,fileType=0x1,subtype=0x0,date=(0,0)),kids=[StringFileInfo([StringTable('040904B0',[StringStruct('CompanyName','{sp.ver_comp.text()}'),StringStruct('FileDescription','{sp.ver_desc.text()}'),StringStruct('FileVersion','{v_str}'),StringStruct('ProductVersion','{v_str}'),StringStruct('OriginalFilename','{app_name}.exe')])])])'''
                version_file = Path(tempfile.gettempdir()) / f"qpypack_{app_name}_version.txt"
                version_file.write_text(content, encoding='utf-8')
            except: pass

        icon_path_str = sp.icon_edit.text().strip()
        temp_icon_file = None
        if icon_path_str and Path(icon_path_str).exists():
            icon_path = Path(icon_path_str)
            if icon_path.suffix.lower() == '.svg':
                try:
                    renderer = QSvgRenderer()
                    if renderer.load(icon_path.as_posix()):
                        pixmap = QPixmap(256, 256)
                        pixmap.fill(Qt.GlobalColor.transparent)
                        painter = QPainter(pixmap)
                        renderer.render(painter)
                        painter.end()
                        
                        temp_ico = Path(tempfile.gettempdir()) / f"qpypack_temp_icon_{int(time.time())}.ico"
                        if pixmap.save(temp_ico.as_posix(), "ICO"):
                            icon_path_str = temp_ico.as_posix()
                            temp_icon_file = temp_ico.as_posix()
                        else:
                            temp_png = Path(tempfile.gettempdir()) / f"qpypack_temp_icon_{int(time.time())}.png"
                            if pixmap.save(temp_png.as_posix(), "PNG"):
                                icon_path_str = temp_png.as_posix()
                                temp_icon_file = temp_png.as_posix()
                except Exception as e:
                    self.append_log(f"[Warn] SVG 图标解析异常: {e}")
                
                if not temp_icon_file:
                    icon_path_str = None
                    self.append_log("[Warn] SVG 桌面图标转换失败，已自动降级为无图标模式构建以确保成功。")

        params = {
            'engine': engine,
            'script_path': self.script_path,
            'app_name': app_name,
            'onefile': sp.onefile_check.isChecked(),
            'noconsole': sp.noconsole_check.isChecked(),
            'icon': icon_path_str,
            'use_reqs': sp.reqs_check.isChecked(),
            'use_pipreqs': sp.pipreqs_check.isChecked(),
            'hidden_imports': sp.hidden_edit.text(),
            'add_data': sp.add_data_edit.text(),
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
            'pip_index_url': sp.pip_source_edit.text().strip(),
            'concise_log': sp.concise_log_check.isChecked(),
            'auto_save_log': sp.auto_save_log_check.isChecked()
        }

        self.log.clear()
        if not self.log_container.isVisible(): self.toggle_log()
            
        self.thread = PackingThread(params)
        self.thread.progress.connect(self.append_log)
        self.thread.finished.connect(self.on_pack_finished)
        self.thread.start()
        
        self.status_label.setText(f" 状态: 正在使用 {engine} 执行构建...")
        self.update_ui_state("building")
        self.drop_area.start_build_anim()

    def on_pack_finished(self, success, msg):
        self.append_log("\n" + "━"*50 + "\n" + msg)
        self.drop_area.stop_build_anim()
        
        if self.settings_panel.sound_notify_check.isChecked():
            play_alert(success)
            
        if success:
            icon_path = self.settings_panel.icon_edit.text().strip()
            self.drop_area.show_success(icon_path)
            self.status_label.setText(" 状态: 构建完成 ✅")
            self.update_ui_state("done")
        else:
            self.drop_area.show_failure()
            self.status_label.setText(" 状态: 构建失败 ❌")
            self.update_ui_state("failed")

    def open_dist(self):
        if self.settings_panel.out_mode_combo.currentIndex() == 1:
            target = Path(self.settings_panel.out_dir_edit.text().strip())
        elif self.settings_panel.clean_all_check.isChecked() and self.script_path:
            target = Path(self.script_path).parent
        else: 
            target = Path.cwd() / "dist"
            
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
        self.settings_panel.add_data_edit.clear()
        self.log.clear()
        if self.log_container.isVisible(): self.toggle_log()
        self.drop_area.reset()
        self.status_label.setText(" 状态: 工作区已重置")
        self.update_ui_state("idle")

    def append_log(self, msg):
        self.log.append(msg)
        self.log.ensureCursorVisible()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Microsoft YaHei", 9))
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()