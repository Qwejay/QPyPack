#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyPack - 自动化 Python 构建与打包工具
支持引擎: PyInstaller / Nuitka / cx_Freeze
"""

import sys
import os
import shutil
import subprocess
import tempfile
import re
import time
import stat
import ast
from pathlib import Path

# 屏蔽 DirectWrite 遗留位图字体扫描警告
os.environ["QT_LOGGING_RULES"] = "qt.text.font.db=false"

# 设置高 DPI 自动缩放
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
                             QPushButton, QLabel, QLineEdit, QFileDialog, QCheckBox, QTabWidget, 
                             QComboBox, QFrame, QStackedLayout, QFormLayout, QTextEdit, 
                             QGraphicsOpacityEffect, QGroupBox, QSizePolicy, QGridLayout,
                             QMessageBox, QInputDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSettings, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent, QTextCursor, QIcon, QPixmap


# ======================== 获取 Python 标准库集合 ========================
def get_stdlib_names():
    libs = {'os', 'sys', 're', 'math', 'time', 'datetime', 'json', 'urllib', 'sqlite3', 'csv', 
            'subprocess', 'shutil', 'threading', 'multiprocessing', 'queue', 'socket', 
            'collections', 'itertools', 'functools', 'random', 'hashlib', 'base64', 
            'binascii', 'xml', 'logging', 'argparse', 'typing', 'pathlib', 'traceback', 
            'warnings', 'tempfile', 'platform', 'zipfile', 'tarfile', 'gzip', 'bz2', 
            'lzma', 'hmac', 'ssl', 'email', 'http', 'uuid', 'io', 'contextlib', 'winreg'}
    if sys.version_info >= (3, 10):
        libs.update(sys.stdlib_module_names)
    return libs

STD_LIBS = get_stdlib_names()


def get_python_executable():
    """
    获取宿主 Python 解释器路径。
    若本打包工具已被打包为独立可执行文件运行，则在系统 PATH 中寻找 python 解释器。
    """
    if getattr(sys, 'frozen', False):
        return shutil.which("python") or shutil.which("python3") or "python"
    return sys.executable


# ======================== IO 异常处理与强制删除组件 ========================
def remove_readonly(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except:
        pass

def robust_rmtree(path: Path, retries=15, delay=0.8):
    if not path.exists():
        return True
    for _ in range(retries):
        try:
            shutil.rmtree(path, onerror=remove_readonly)
            if not path.exists():
                return True
        except:
            time.sleep(delay)
    return False


# ======================== 界面动画组件 ========================
class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        
        self.animation_group = QParallelAnimationGroup()
        self.pos_anim = QPropertyAnimation(self, b"geometry")
        self.pos_anim.setDuration(120)
        self.pos_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        self.op_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.op_anim.setDuration(120)
        
        self.animation_group.addAnimation(self.pos_anim)
        self.animation_group.addAnimation(self.op_anim)
        self.is_hovered = False

    def enterEvent(self, event):
        if not self.is_hovered and self.isEnabled():
            self.is_hovered = True
            geom = self.geometry()
            self.pos_anim.setStartValue(geom)
            self.pos_anim.setEndValue(geom.adjusted(0, -1, 0, -1))
            self.op_anim.setStartValue(1.0)
            self.op_anim.setEndValue(0.88)
            self.animation_group.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.is_hovered and self.isEnabled():
            self.is_hovered = False
            geom = self.geometry()
            self.pos_anim.setStartValue(geom)
            self.pos_anim.setEndValue(geom.adjusted(0, 1, 0, 1))
            self.op_anim.setStartValue(0.88)
            self.op_anim.setEndValue(1.0)
            self.animation_group.start()
        super().leaveEvent(event)


class DropArea(QFrame):
    fileDropped = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QFrame { background-color: #fafafa; border: 1px dashed #dee2e6; border-radius: 4px; }
            QFrame:hover { background-color: #f1f3f5; border-color: #ced4da; }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        self.tip_label = QLabel("📥 拖拽主脚本 (.py) 至此区域 ( 或点击浏览 )")
        self.tip_label.setAlignment(Qt.AlignCenter)
        self.tip_label.setStyleSheet("color: #6c757d; font-size: 9pt; font-weight: 500;")
        layout.addWidget(self.tip_label)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().lower().endswith('.py'):
                event.acceptProposedAction()
                self.setStyleSheet("QFrame { background-color: #e9ecef; border: 1px dashed #adb5bd; border-radius: 4px; }")

    def dragLeaveEvent(self, event):
        self.setStyleSheet("QFrame { background-color: #fafafa; border: 1px dashed #dee2e6; border-radius: 4px; } QFrame:hover { background-color: #f1f3f5; border-color: #ced4da; }")

    def dropEvent(self, event: QDropEvent):
        self.dragLeaveEvent(event)
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if path.lower().endswith('.py'):
                self.fileDropped.emit(path)
                self.tip_label.setText(f"✅ 已装载工程: {os.path.basename(path)}")
                self.tip_label.setStyleSheet("color: #198754; font-size: 9pt; font-weight: bold;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            fp, _ = QFileDialog.getOpenFileName(self, "选择 Python 源代码文件", "", "Python Scripts (*.py)")
            if fp:
                self.fileDropped.emit(fp)
                self.tip_label.setText(f"✅ 已装载工程: {os.path.basename(fp)}")
                self.tip_label.setStyleSheet("color: #198754; font-size: 9pt; font-weight: bold;")

    def reset(self):
        self.tip_label.setText("📥 拖拽主脚本 (.py) 至此区域 ( 或点击浏览 )")
        self.tip_label.setStyleSheet("color: #6c757d; font-size: 9pt; font-weight: 500;")


# ======================== 核心构建服务 ========================
class PackingThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, params):
        super().__init__()
        self.params = params
        self.process = None
        self._is_cancelled = False
        self.venv_dir = None
        self.temp_workpath = None
        self.temp_out_dir = None

    def cancel(self):
        self._is_cancelled = True
        if self.process:
            try:
                if os.name == "nt":
                    # 在 Windows 下终止整个子进程树，防止编译器残留锁死文件
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.process.pid)], capture_output=True)
                else:
                    self.process.kill()
            except:
                pass

    def run_cmd_realtime(self, cmd, cwd=None):
        if self._is_cancelled: return False
        try:
            self.process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding='utf-8', errors='replace', cwd=cwd
            )
            while True:
                line = self.process.stdout.readline()
                if not line and self.process.poll() is not None:
                    break
                if line:
                    self.progress.emit(line.strip())
            return self.process.returncode == 0
        except Exception as e:
            self.progress.emit(f"[系统异常] 进程错误: {e}")
            return False

    def run(self):
        # 优雅解决新机器环境卡阻：在当前执行环境注册此环境变量，让所有版本的 Nuitka 自动同意下载依赖
        os.environ["NUITKA_ACCEPT_DOWNLOADS"] = "yes"
        
        engine = self.params['engine']
        pip_idx = self.params.get('pip_index_url', '').strip() or "https://pypi.tuna.tsinghua.edu.cn/simple"
        try:
            self.progress.emit("[预处理] 清理遗留缓存...")
            robust_rmtree(Path.cwd() / "build")
            robust_rmtree(Path.cwd() / "dist")
            
            script_path = self.params['script_path']
            script_dir = Path(script_path).parent
            if "OneDrive" in str(script_path):
                self.progress.emit("[警告] 工程位于 OneDrive 同同步目录中，文件可能被锁定导致构建失败，建议将工程迁移至本地路径。")
            
            # 虚拟环境
            if self.params['use_venv']:
                self.progress.emit("[环境预配置] 正在初始化 Python 虚拟环境...")
                self.venv_dir = Path(tempfile.mkdtemp(prefix="pypack_env_"))
                host_py = get_python_executable()
                if not self.run_cmd_realtime([host_py, "-m", "venv", str(self.venv_dir)]):
                    self.finished.emit(False, "虚拟环境初始化失败，请检查系统权限。")
                    return
                python_exe = str(self.venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python"))
            else:
                self.progress.emit("[环境警告] 虚拟环境已禁用，使用全局 Python。")
                python_exe = get_python_executable()

            # 安装引擎
            if engine == "Nuitka":
                engine_pkg = "nuitka[onefile]"
            elif engine == "cx_Freeze":
                engine_pkg = "cx_Freeze"
            else:
                engine_pkg = "pyinstaller"
            self.progress.emit(f"[环境配置] 正在通过镜像源 {pip_idx} 部署依赖包...")
            self.run_cmd_realtime([python_exe, "-m", "pip", "install", "-U", "pip", "-i", pip_idx, "-q"])
            self.run_cmd_realtime([python_exe, "-m", "pip", "install", engine_pkg, "-i", pip_idx, "-q"])
            if engine == "PyInstaller":
                self.run_cmd_realtime([python_exe, "-m", "pip", "install", "pillow", "-i", pip_idx, "-q"])
            
            # 依赖解析
            if self.params.get('use_reqs'):
                req_file = script_dir / "requirements.txt"
                if req_file.exists():
                    self.progress.emit(f"[依赖解析] 同步工程内 {req_file.name}...")
                    self.run_cmd_realtime([python_exe, "-m", "pip", "install", "-r", str(req_file), "-i", pip_idx])
                else:
                    self.progress.emit("[依赖解析] 未找到 requirements.txt，执行 AST 静态扫描...")
                    try:
                        with open(script_path, encoding='utf-8', errors='ignore') as f:
                            code = f.read()
                        third_party = set()
                        try:
                            # 采用标准库 AST 分析，精准获取顶层依赖并过滤注释/伪导入
                            tree = ast.parse(code, filename=str(script_path))
                            for node in ast.walk(tree):
                                if isinstance(node, ast.Import):
                                    for alias in node.names:
                                        third_party.add(alias.name.split('.')[0])
                                elif isinstance(node, ast.ImportFrom):
                                    if node.level == 0 and node.module:
                                        third_party.add(node.module.split('.')[0])
                        except Exception:
                            # 语法不完备时回退到正则扫描
                            imports = re.findall(r'^\s*(?:from|import)\s+([a-zA-Z0-9_]+)', code, re.M)
                            third_party = set(imports)
                        
                        third_party = {m for m in third_party if m not in STD_LIBS}
                        if third_party:
                            self.progress.emit(f"发现外部依赖模块: {', '.join(third_party)}")
                            for pkg in third_party:
                                if self._is_cancelled: break
                                self.progress.emit(f"[自动同步] 正在安装 {pkg}...")
                                self.run_cmd_realtime([python_exe, "-m", "pip", "install", pkg, "-i", pip_idx, "-q"])
                    except Exception as e:
                        self.progress.emit(f"[扫描异常] {e}")

            if self._is_cancelled:
                self.finished.emit(False, "构建已被中断。")
                return

            # 构建命令生成
            self.progress.emit(f"[编译阶段] 启动 {engine} 构建...")
            cmd = []
            app_name = self.params['app_name']
            noconsole = self.params.get('noconsole')

            if engine == "PyInstaller":
                self.temp_workpath = Path(tempfile.mkdtemp(prefix="pypack_build_"))
                cmd = [python_exe, "-m", "PyInstaller", "--clean", "-y",
                       f"--workpath={self.temp_workpath}",
                       f"--name={app_name}"]
                if self.params.get('onefile'): cmd.append("--onefile")
                else: cmd.append("--onedir")
                if noconsole: cmd.append("--noconsole")
                if self.params.get('icon'): cmd.extend(["--icon", self.params['icon']])
                if self.params.get('version_file'): cmd.extend(["--version-file", self.params['version_file']])
                
                # 只有在本地存在 UPX 目录时才显式传参，否则让 PyInstaller 寻找环境变量
                if self.params.get('upx'):
                    upx_dir = Path.cwd() / "upx"
                    if upx_dir.exists():
                        cmd.append(f"--upx-dir={upx_dir}")
                
                for imp in self.params.get('hidden_imports', '').split(','):
                    imp = imp.strip()
                    if imp: cmd.extend(["--hidden-import", imp])
                for d in self.params.get('add_data', '').split(','):
                    d = d.strip()
                    if d: cmd.extend(["--add-data", d])

            elif engine == "Nuitka":
                self.temp_out_dir = Path(tempfile.mkdtemp(prefix="nuitka_out_"))
                cmd = [python_exe, "-m", "nuitka", "--remove-output", "--assume-yes-for-downloads",
                       f"--output-dir={self.temp_out_dir}",
                       f"--output-filename={app_name}.exe"]
                if self.params.get('onefile'): cmd.append("--onefile")
                else: cmd.append("--standalone")
                if noconsole: cmd.append("--windows-console-mode=disable")
                
                if self.params.get('icon'): cmd.append(f"--windows-icon-from-ico={self.params['icon']}")
                if self.params.get('ver_comp'): cmd.append(f"--company-name={self.params['ver_comp']}")
                if self.params.get('ver_desc'): cmd.append(f"--product-name={self.params['ver_desc']}")
                if self.params.get('ver_ver'): cmd.append(f"--file-version={self.params['ver_ver']}")
                
                try:
                    with open(script_path, encoding='utf-8', errors='ignore') as f:
                        if 'PyQt5' in f.read():
                            cmd.append("--enable-plugin=pyqt5")
                            self.progress.emit("[自动检测] 已启用 PyQt5 插件")
                except: pass
                for imp in self.params.get('hidden_imports', '').split(','):
                    imp = imp.strip()
                    if imp: cmd.append(f"--include-module={imp}")
                for d in self.params.get('add_data', '').split(','):
                    d = d.strip()
                    if d:
                        parts = d.split(':', 1)
                        if len(parts) == 2:
                            cmd.extend(["--include-data-files", f"{parts[0]}={parts[1]}"])
                        else:
                            self.progress.emit(f"[警告] 附加资源格式错误，应为 src:dest，忽略: {d}")

            elif engine == "cx_Freeze":
                cmd = [python_exe, "-m", "cx_Freeze", str(script_path),
                       f"--target-dir=dist/{app_name}",
                       f"--target-name={app_name}.exe"]
                if noconsole:
                    cmd.append("--base=Win32GUI")
                else:
                    cmd.append("--base=Console")
                if self.params.get('icon'): cmd.extend(["--icon", self.params['icon']])
                for imp in self.params.get('hidden_imports', '').split(','):
                    imp = imp.strip()
                    if imp: cmd.extend(["--include-modules", imp])
                add_data_list = []
                for d in self.params.get('add_data', '').split(','):
                    d = d.strip()
                    if d:
                        parts = d.split(':', 1)
                        if len(parts) == 2:
                            add_data_list.append(f"{parts[0]}={parts[1]}")
                        else:
                            self.progress.emit(f"[警告] 附加资源格式错误，应为 src:dest，忽略: {d}")
                if add_data_list:
                    cmd.extend(["--include-files", ";".join(add_data_list)])

            if engine in ["PyInstaller", "Nuitka"]:
                cmd.append(str(script_path))

            success = self.run_cmd_realtime(cmd, cwd=str(Path.cwd()))
            if self._is_cancelled:
                self.finished.emit(False, "构建已被中断。")
                return

            # 归档产物
            self.progress.emit("[阶段收尾] 归档产物...")
            if engine == "PyInstaller":
                src_out = Path.cwd() / "dist" / (f"{app_name}.exe" if self.params['onefile'] else app_name)
            elif engine == "Nuitka":
                src_out = self.temp_out_dir / (f"{app_name}.exe" if self.params['onefile'] else f"{app_name}.dist")
            elif engine == "cx_Freeze":
                # cx_Freeze 的产物是整个目录。若单独移出 exe 将缺失运行库。
                src_out = Path.cwd() / "dist" / app_name

            final_out = script_dir / src_out.name
            if success and src_out.exists():
                try:
                    self.progress.emit(f"[产物归档] 提取至: {final_out.resolve()}")
                    if final_out.exists():
                        robust_rmtree(final_out) if final_out.is_dir() else final_out.unlink(missing_ok=True)
                    shutil.move(str(src_out), str(final_out))
                except Exception as e:
                    self.progress.emit(f"[归档异常] {e}")
            else:
                self.progress.emit(f"[错误] 未找到产物: {src_out}")

            if self.params.get('clean_all'):
                self.progress.emit("[清理] 删除临时文件...")
                for p in [self.venv_dir, self.temp_workpath, self.temp_out_dir]:
                    if p and p.exists(): robust_rmtree(p)
                robust_rmtree(Path.cwd() / "dist")
                for p in ["build", "__pycache__", f"{app_name}.build", f"{app_name}.dist", f"{app_name}.onefile-build"]:
                    robust_rmtree(Path.cwd() / p)
                Path(f"{app_name}.spec").unlink(missing_ok=True)
                if self.params.get('version_file'):
                    Path(self.params['version_file']).unlink(missing_ok=True)

            if success and final_out.exists():
                self.finished.emit(True, f"[构建成功] 应用程序已交付。\n路径: {final_out.resolve()}")
            else:
                self.finished.emit(False, "[构建失败] 请检查日志排查错误。")

        except Exception as e:
            self.finished.emit(False, f"[系统异常] {str(e)}")


# ======================== 界面核心控制层 ========================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("PyPack", "Universal")
        self.script_path = ""
        self.thread = None
        self.init_style()
        self._load_settings()
        self.init_ui()
        self._load_window_icon()

    def init_style(self):
        self.setWindowTitle("PyPack 1.0.1 - 自动化构建工具")
        self.setStyleSheet("""
            QMainWindow { background-color: #fdfdfd; }
            QLabel { color: #343a40; font-size: 9pt; }
            QGroupBox { border: 1px solid #e9ecef; border-radius: 4px; margin-top: 6px; padding: 10px 8px 6px 8px; color: #212529; }
            QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 3px; color: #6c757d; font-size: 9pt; }
            
            /* 统一输入控件与下拉框基础样式 */
            QLineEdit, QTextEdit, QComboBox { 
                padding: 3px 6px; 
                border: 1px solid #dee2e6; 
                border-radius: 4px; 
                font-size: 9pt; 
                background: #ffffff; 
                color: #212529; 
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus { 
                border-color: #86b7fe; 
            }
            
            /* 下拉框细节美化，去除原生自带的灰色按钮边框与渐变 */
            QComboBox { 
                padding-right: 22px; 
            }
            QComboBox::drop-down { 
                subcontrol-origin: padding; 
                subcontrol-position: top right; 
                width: 20px; 
                border-left-width: 0px; 
                border-top-right-radius: 4px; 
                border-bottom-right-radius: 4px; 
            }
            /* 采用优雅的 SVG 箭头代替原生灰色小三角 */
            QComboBox::down-arrow { 
                image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='none' stroke='%236c757d' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'></polyline></svg>"); 
                width: 10px; 
                height: 10px; 
            }
            /* 统一下拉选项菜单（QAbstractItemView）的边框与悬浮高亮样式 */
            QComboBox QAbstractItemView { 
                border: 1px solid #dee2e6; 
                border-radius: 4px; 
                background-color: #ffffff; 
                selection-background-color: #0d6efd; 
                selection-color: #ffffff; 
                outline: none; 
            }

            QCheckBox { font-size: 9pt; padding: 1px 0; color: #343a40; spacing: 5px; }
            QCheckBox::indicator { width: 13px; height: 13px; border: 1px solid #adb5bd; border-radius: 2px; background: white; }
            QCheckBox::indicator:checked { background: #0d6efd; border-color: #0d6efd; image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='white'><path d='M20.285 6.375l-1.2-1.2-8.085 8.085-4.2-4.2-1.2 1.2 5.4 5.4z'/></svg>"); }
            QCheckBox::indicator:hover { border-color: #6c757d; }
            QTabWidget::pane { border: 1px solid #e9ecef; background: #ffffff; border-radius: 4px; top: -1px; }
            QTabBar::tab { background: #f8f9fa; border: 1px solid #e9ecef; padding: 4px 10px; margin-right: 2px; border-top-left-radius: 4px; border-top-right-radius: 4px; color: #6c757d; font-size: 9pt; }
            QTabBar::tab:selected { background: #ffffff; border-bottom-color: #ffffff; color: #0d6efd; font-weight: bold; }
        """)

    def _load_settings(self):
        if self.settings.value("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))
        else:
            self.setGeometry(150, 100, 620, 520)

    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            self.thread.cancel()
            self.thread.wait()
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def _load_window_icon(self):
        if getattr(sys, 'frozen', False):
            base_dir = Path(sys.executable).parent
        else:
            base_dir = Path(__file__).resolve().parent
        
        # 多后缀不区分大小写检索，提高跨平台抗风险能力
        for name in ["ICON.ICO", "icon.ico", "logo.ico", "ICON.PNG", "icon.png"]:
            icon_path = base_dir / name
            if icon_path.exists():
                self.setWindowIcon(QIcon(str(icon_path)))
                break

    def update_icon_preview(self, path):
        if path and Path(path).exists():
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                self.icon_preview.setPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                return
        self.icon_preview.clear()

    def init_ui(self):
        self.setMinimumSize(500, 440) 
        central = QWidget()
        self.setCentralWidget(central)
        self.stacked = QStackedLayout(central)

        self.main_panel = QWidget()
        main_lay = QVBoxLayout(self.main_panel)
        main_lay.setContentsMargins(10, 10, 10, 10)
        main_lay.setSpacing(6)

        self.drop_area = DropArea(self)
        self.drop_area.setFixedHeight(65)
        self.drop_area.fileDropped.connect(self.on_script_selected)
        main_lay.addWidget(self.drop_area)

        self.tabs = QTabWidget()
        basic = QWidget()
        adv = QWidget()
        self.tabs.addTab(basic, "常规配置")
        self.tabs.addTab(adv, "高级选项")

        self.setup_basic(basic)
        self.setup_adv(adv)
        main_lay.addWidget(self.tabs)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                color: #495057;
                font-family: Consolas, "Courier New", monospace;
                font-size: 8.5pt;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 4px;
                line-height: 1.2;
            }
        """)
        self.log.setFixedHeight(100)
        main_lay.addWidget(self.log)

        btn_lay = QHBoxLayout()
        self.reset_btn = AnimatedButton("重置")
        self.reset_btn.setStyleSheet("QPushButton { background: #f8f9fa; color: #495057; border: 1px solid #dee2e6; padding: 4px 10px; border-radius: 4px; font-size: 9pt; } QPushButton:hover { background: #e9ecef; }")
        self.reset_btn.clicked.connect(self.reset_all)
        
        self.open_btn = AnimatedButton("打开输出目录")
        self.open_btn.setStyleSheet("QPushButton { background: #198754; color: white; border: none; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 9pt; } QPushButton:hover { background: #157347; }")
        self.open_btn.clicked.connect(self.open_dist)
        self.open_btn.setVisible(False)
        
        self.pack_btn = AnimatedButton("开始构建")
        self.pack_btn.setStyleSheet("QPushButton { background: #0d6efd; color: white; border: none; padding: 5px 16px; border-radius: 4px; font-weight: bold; font-size: 9pt; } QPushButton:hover { background: #0b5ed7; }")
        self.pack_btn.clicked.connect(self.toggle_pack)

        btn_lay.addWidget(self.reset_btn)
        btn_lay.addStretch()
        btn_lay.addWidget(self.open_btn)
        btn_lay.addWidget(self.pack_btn)
        main_lay.addLayout(btn_lay)

        self.stacked.addWidget(self.main_panel)

        self.statusBar = self.statusBar()
        self.status_label = QLabel("就绪")
        self.statusBar.addWidget(self.status_label)

        self.on_engine_changed(0)

    def setup_basic(self, tab):
        lay = QVBoxLayout(tab)
        lay.setContentsMargins(10, 10, 10, 10)
        lay.setSpacing(6)

        form = QFormLayout()
        form.setSpacing(5)
        form.setContentsMargins(0, 0, 0, 0)

        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["PyInstaller", "Nuitka", "cx_Freeze"])
        self.engine_combo.currentIndexChanged.connect(self.on_engine_changed)
        form.addRow("构建引擎:", self.engine_combo)

        # 添加入口脚本浏览按钮，极大程度改善无拖拽习惯时的选包体验
        self.script_edit = QLineEdit()
        self.script_edit.setPlaceholderText("可直接拖拽文件至上方或点击右侧浏览")
        script_btn = QPushButton("浏览...")
        script_btn.setCursor(Qt.PointingHandCursor)
        script_btn.setStyleSheet("QPushButton { padding: 3px 8px; border: 1px solid #dee2e6; border-radius: 4px; background: #f8f9fa; font-size: 9pt; } QPushButton:hover { background: #e9ecef; }")
        script_btn.clicked.connect(self.select_script)
        h_script = QHBoxLayout()
        h_script.setSpacing(6)
        h_script.addWidget(self.script_edit)
        h_script.addWidget(script_btn)
        form.addRow("入口脚本:", h_script)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("[可选] 留空则与入口脚本同名")
        form.addRow("输出名称:", self.name_edit)

        self.icon_edit = QLineEdit()
        self.icon_edit.textChanged.connect(self.update_icon_preview)
        self.icon_preview = QLabel()
        self.icon_preview.setFixedSize(24, 24)
        self.icon_preview.setScaledContents(True)
        self.icon_preview.setStyleSheet("border: 1px solid #dee2e6; border-radius: 2px;")
        
        icon_btn = QPushButton("浏览...")
        icon_btn.setCursor(Qt.PointingHandCursor)
        icon_btn.setStyleSheet("QPushButton { padding: 3px 8px; border: 1px solid #dee2e6; border-radius: 4px; background: #f8f9fa; font-size: 9pt; } QPushButton:hover { background: #e9ecef; }")
        icon_btn.clicked.connect(self.select_icon)
        
        h = QHBoxLayout()
        h.setSpacing(6)
        h.addWidget(self.icon_edit)
        h.addWidget(self.icon_preview)
        h.addWidget(icon_btn)
        form.addRow("应用图标:", h)

        lay.addLayout(form)

        checks_group = QGroupBox("打包选项")
        grid = QGridLayout(checks_group)
        grid.setContentsMargins(8, 8, 8, 8)
        grid.setSpacing(6)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        self.venv_check = QCheckBox("使用虚拟环境 (Venv)")
        self.venv_check.setChecked(True)
        self.onefile_check = QCheckBox("单文件模式 (OneFile)")
        self.onefile_check.setChecked(True)
        self.noconsole_check = QCheckBox("隐藏控制台 (GUI)")
        self.noconsole_check.setChecked(True)
        self.reqs_check = QCheckBox("自动解析依赖")
        self.reqs_check.setChecked(True)
        self.clean_all_check = QCheckBox("清理临时文件并归档")
        self.clean_all_check.setChecked(True)

        grid.addWidget(self.venv_check, 0, 0)
        grid.addWidget(self.noconsole_check, 0, 1)
        grid.addWidget(self.onefile_check, 1, 0)
        grid.addWidget(self.reqs_check, 1, 1)
        grid.addWidget(self.clean_all_check, 2, 0, 1, 2)

        lay.addWidget(checks_group)
        lay.addStretch()

    def setup_adv(self, tab):
        lay = QVBoxLayout(tab)
        lay.setContentsMargins(10, 10, 10, 10)
        lay.setSpacing(6)
        
        form = QFormLayout()
        form.setSpacing(5)
        form.setContentsMargins(0, 0, 0, 0)

        # PIP 源配置（修改马上通过 QSettings 保存，在打包时生效）
        self.pip_source_edit = QLineEdit()
        self.pip_source_edit.setPlaceholderText("默认: https://pypi.tuna.tsinghua.edu.cn/simple")
        self.pip_source_edit.setText(self.settings.value("pip_index_url", "https://pypi.tuna.tsinghua.edu.cn/simple"))
        self.pip_source_edit.textChanged.connect(lambda text: self.settings.setValue("pip_index_url", text))
        form.addRow("PIP 镜像源:", self.pip_source_edit)

        self.hidden_edit = QLineEdit()
        self.hidden_edit.setPlaceholderText("例如: pandas, PyQt5 (逗号分隔)")
        scan_btn = QPushButton("AST 扫描")
        scan_btn.setCursor(Qt.PointingHandCursor)
        scan_btn.setStyleSheet("QPushButton { padding: 3px 8px; border: 1px solid #dee2e6; border-radius: 4px; background: #f8f9fa; font-size: 9pt; } QPushButton:hover { background: #e9ecef; }")
        scan_btn.clicked.connect(self.auto_scan_hidden)
        h = QHBoxLayout()
        h.setSpacing(6)
        h.addWidget(self.hidden_edit)
        h.addWidget(scan_btn)
        form.addRow("隐式依赖:", h)

        self.add_data_edit = QLineEdit()
        self.add_data_edit.setPlaceholderText("源:目标 (例如: data/*:data)")
        add_res_btn = QPushButton("添加")
        add_res_btn.setCursor(Qt.PointingHandCursor)
        add_res_btn.setStyleSheet("QPushButton { padding: 3px 8px; border: 1px solid #dee2e6; border-radius: 4px; background: #f8f9fa; font-size: 9pt; } QPushButton:hover { background: #e9ecef; }")
        add_res_btn.clicked.connect(self.add_resource)
        h_res = QHBoxLayout()
        h_res.setSpacing(6)
        h_res.addWidget(self.add_data_edit)
        h_res.addWidget(add_res_btn)
        form.addRow("附加资源:", h_res)

        self.upx_check = QCheckBox("启用 UPX 压缩 (仅 PyInstaller)")
        form.addRow("", self.upx_check)

        self.info_group = QGroupBox("版本元数据 (Metadata)")
        info_lay = QFormLayout()
        info_lay.setContentsMargins(8, 8, 8, 8)
        info_lay.setSpacing(5)
        self.ver_ver = QLineEdit("1.0.1")
        self.ver_comp = QLineEdit("Developer Studio")
        self.ver_desc = QLineEdit("Windows Executable Application")
        info_lay.addRow("版本序列:", self.ver_ver)
        info_lay.addRow("发行公司:", self.ver_comp)
        info_lay.addRow("文件描述:", self.ver_desc)
        self.info_group.setLayout(info_lay)

        lay.addLayout(form)
        lay.addWidget(self.info_group)
        lay.addStretch()

    def on_engine_changed(self, index):
        engine = self.engine_combo.currentText()
        self.onefile_check.setVisible(engine in ("PyInstaller", "Nuitka"))
        self.upx_check.setVisible(engine == "PyInstaller")
        self.info_group.setVisible(engine != "cx_Freeze")
        if engine == "Nuitka":
            self.show_status("提示：Nuitka 编译可能触发杀软拦截，建议将路径加入白名单。", "info")
        else:
            self.show_status("引擎已切换", "info")

    def auto_scan_hidden(self):
        if not self.script_path:
            self.show_status("请先选择脚本", "error")
            return
        try:
            with open(self.script_path, encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            # 使用 AST 解析依赖
            hidden = set()
            try:
                tree = ast.parse(code, filename=self.script_path)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            hidden.add(alias.name.split('.')[0])
                    elif isinstance(node, ast.ImportFrom):
                        if node.level == 0 and node.module:
                            hidden.add(node.module.split('.')[0])
            except Exception:
                # 兼容未完成编写的代码
                imports = re.findall(r'^\s*(?:from|import)\s+([a-zA-Z0-9_]+)', code, re.M)
                hidden = set(imports)

            hidden = [m for m in hidden if m not in STD_LIBS]
            self.hidden_edit.setText(','.join(hidden))
            self.show_status(f"已捕获 {len(hidden)} 项外部模块", "success")
        except Exception as e:
            self.show_status(f"扫描失败: {e}", "error")

    def select_script(self):
        fp, _ = QFileDialog.getOpenFileName(self, "选择 Python 源代码文件", "", "Python Scripts (*.py)")
        if fp:
            self.on_script_selected(fp)

    def on_script_selected(self, path):
        self.script_path = path
        self.script_edit.setText(path)
        self.name_edit.setText(Path(path).stem)
        script_dir = Path(path).parent
        
        # 支持不区分大小写的 icon 自动加载
        auto_icon = None
        for name in ["ICON.ICO", "icon.ico", "logo.ico"]:
            trial = script_dir / name
            if trial.exists():
                auto_icon = trial
                break
                
        if auto_icon:
            current_icon = self.icon_edit.text().strip()
            if not current_icon or not Path(current_icon).exists():
                self.icon_edit.setText(str(auto_icon))
                
        self.show_status(f"当前工程: {Path(path).name}", "success")
        self.drop_area.tip_label.setText(f"✅ 已装载工程: {os.path.basename(path)}")
        self.drop_area.tip_label.setStyleSheet("color: #198754; font-size: 9pt; font-weight: bold;")

    def select_icon(self):
        p, _ = QFileDialog.getOpenFileName(self, "选择图标", "", "Icon Files (*.ico)")
        if p:
            self.icon_edit.setText(p)

    def add_resource(self):
        choice = QMessageBox.question(self, "添加资源", "请选择要添加的资源类型：\n“是” - 选择文件\n“否” - 选择文件夹",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if choice == QMessageBox.Yes:
            files, _ = QFileDialog.getOpenFileNames(self, "选择资源文件", "", "All Files (*)")
            for f in files:
                default_dest = Path(f).name
                dest, ok = QInputDialog.getText(self, "目标路径", f"输入目标相对路径（默认为 {default_dest}）:", text=default_dest)
                if ok:
                    dest = dest.strip() if dest else default_dest
                    src_dest = f"{f}:{dest}"
                    current = self.add_data_edit.text().strip()
                    if current:
                        self.add_data_edit.setText(current + ", " + src_dest)
                    else:
                        self.add_data_edit.setText(src_dest)
        else:
            folder = QFileDialog.getExistingDirectory(self, "选择资源文件夹")
            if folder:
                default_dest = Path(folder).name
                dest, ok = QInputDialog.getText(self, "目标路径", f"输入目标相对路径（默认为 {default_dest}）:", text=default_dest)
                if ok:
                    dest = dest.strip() if dest else default_dest
                    src_dest = f"{folder}:{dest}"
                    current = self.add_data_edit.text().strip()
                    if current:
                        self.add_data_edit.setText(current + ", " + src_dest)
                    else:
                        self.add_data_edit.setText(src_dest)

    def toggle_pack(self):
        if self.thread and self.thread.isRunning():
            self.thread.cancel()
            self.pack_btn.setText("开始构建")
            self.pack_btn.setStyleSheet("QPushButton { background: #0d6efd; color: white; border: none; padding: 5px 16px; border-radius: 4px; font-weight: bold; font-size: 9pt; } QPushButton:hover { background: #0b5ed7; }")
            self.show_status("已终止构建进程。", "error")
        else:
            self.start_pack()

    def start_pack(self):
        # 兼容手动在文本框中直接填写路径的情况
        manual_path = self.script_edit.text().strip()
        if manual_path and Path(manual_path).exists():
            self.script_path = manual_path

        if not self.script_path or not Path(self.script_path).exists():
            self.show_status("脚本路径无效", "error")
            return

        app_name = self.name_edit.text().strip() or Path(self.script_path).stem
        engine = self.engine_combo.currentText()

        # 生成 PyInstaller 版本文件
        version_file = None
        if engine == "PyInstaller" and self.ver_ver.text().strip():
            try:
                content = f'''VSVersionInfo(ffi=FixedFileInfo(filevers=(1,0,0,0),prodvers=(1,0,0,0),mask=0x3f,flags=0x0,OS=0x40004,fileType=0x1,subtype=0x0,date=(0,0)),kids=[StringFileInfo([StringTable('040904B0',[StringStruct('CompanyName','{self.ver_comp.text()}'),StringStruct('FileDescription','{self.ver_desc.text()}'),StringStruct('FileVersion','{self.ver_ver.text()}'),StringStruct('ProductVersion','{self.ver_ver.text()}'),StringStruct('OriginalFilename','{app_name}.exe')])])])'''
                version_file = Path(f"{app_name}_version.txt")
                version_file.write_text(content, encoding='utf-8')
            except:
                pass

        params = {
            'engine': engine,
            'script_path': Path(self.script_path),
            'app_name': app_name,
            'onefile': self.onefile_check.isChecked() if engine != "cx_Freeze" else False,
            'noconsole': self.noconsole_check.isChecked(),
            'icon': self.icon_edit.text().strip(),
            'use_reqs': self.reqs_check.isChecked(),
            'hidden_imports': self.hidden_edit.text(),
            'add_data': self.add_data_edit.text(),
            'upx': self.upx_check.isChecked() if engine == "PyInstaller" else False,
            'use_venv': self.venv_check.isChecked(),
            'clean_all': self.clean_all_check.isChecked(),
            'version_file': str(version_file) if version_file else None,
            'ver_comp': self.ver_comp.text() if engine != "cx_Freeze" else "",
            'ver_desc': self.ver_desc.text() if engine != "cx_Freeze" else "",
            'ver_ver': self.ver_ver.text() if engine != "cx_Freeze" else "",
            'pip_index_url': self.pip_source_edit.text().strip()
        }

        self.log.clear()
        self.open_btn.setVisible(False)
        self.pack_btn.setText("终止构建")
        self.pack_btn.setStyleSheet("QPushButton { background: #dc3545; color: white; border: none; padding: 5px 16px; border-radius: 4px; font-weight: bold; font-size: 9pt; } QPushButton:hover { background: #bb2d3b; }")

        self.thread = PackingThread(params)
        self.thread.progress.connect(self.append_log)
        self.thread.finished.connect(self.on_pack_finished)
        self.thread.start()
        self.show_status(f"[{engine}] 构建任务执行中...", "info")

    def on_pack_finished(self, success, msg):
        self.pack_btn.setText("开始构建")
        self.pack_btn.setStyleSheet("QPushButton { background: #0d6efd; color: white; border: none; padding: 5px 16px; border-radius: 4px; font-weight: bold; font-size: 9pt; } QPushButton:hover { background: #0b5ed7; }")
        self.append_log("\n" + "━"*60 + "\n" + msg)
        if success:
            self.show_status("构建完成", "success")
            self.open_btn.setVisible(True)
        else:
            self.show_status("构建失败", "error")

    def open_dist(self):
        if self.clean_all_check.isChecked() and self.script_path:
            target_dir = Path(self.script_path).parent
        else:
            target_dir = Path("dist")
        if target_dir.exists():
            try:
                os.startfile(target_dir)
            except: pass

    def reset_all(self):
        self.script_path = ""
        for w in [self.script_edit, self.name_edit, self.icon_edit, self.hidden_edit, self.add_data_edit]:
            w.clear()
        self.icon_preview.clear()
        self.log.clear()
        self.drop_area.reset()
        self.open_btn.setVisible(False)
        self.show_status("工作区已重置", "success")

    def show_status(self, text, typ="info"):
        colors = {"success":"#198754", "error":"#dc3545", "info":"#6c757d"}
        self.status_label.setStyleSheet(f"color: {colors.get(typ, '#6c757d')}; font-weight: bold;")
        self.status_label.setText(text)

    def append_log(self, msg):
        self.log.append(msg)
        cursor = self.log.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log.setTextCursor(cursor)


def main():
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Microsoft YaHei", 9))
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
