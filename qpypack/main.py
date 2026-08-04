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
import ast
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

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
                             QHeaderView, QDialog, QRadioButton)
from PySide6.QtCore import (Qt, QThread, Signal, QPropertyAnimation, QEasingCurve, 
                            QParallelAnimationGroup, QFileInfo, QVariantAnimation, 
                            QTimer, QPointF, QRectF, QRect, QSize, QUrl, QLocale, QObject)
from PySide6.QtGui import (QFont, QDragEnterEvent, QDropEvent, QIcon, QPixmap, 
                           QPainter, QColor, QPen, QImage, QImageWriter, QDesktopServices)
from PySide6.QtSvg import QSvgRenderer

try:
    from PySide6.QtMultimedia import QSoundEffect
    HAS_QT_AUDIO = True
except ImportError:
    HAS_QT_AUDIO = False

__app_name__ = "QPyPack"
__version__ = "2.7.3"
__author__ = "QwejayHuang"
__company__ = "QwejayHuang"
__description__ = "Modern Cross-Platform Python Packaging GUI Powered by PyInstaller & Nuitka"

_CONFIG_DIR = Path.home() / ".qpypack"
_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = (_CONFIG_DIR / "config.ini").as_posix()

ZH_CN_DICT = {
    # 1. 源镜像名称 (PIP Mirrors)
    "PyPI Official (Global Default)": "PyPI 官方源 (默认)",
    "Python TestPyPI": "TestPyPI 测试源",
    "AWS PyPI Mirror (US/EU)": "AWS PyPI 镜像 (美/欧)",
    "Tsinghua University (China)": "清华大学镜像",
    "Aliyun Cloud (China)": "阿里云镜像",
    "Tencent Cloud (China)": "腾讯云镜像",
    "Huawei Cloud (China)": "华为云镜像",
    "USTC (China)": "中科大镜像",

    # 2. 软件元数据与标语 (Metadata & Taglines)
    "Modern Cross-Platform Python Packaging GUI Powered by PyInstaller & Nuitka": "基于 PyInstaller 与 Nuitka 的现代化跨平台 Python 打包工具",
    "Python Packaging, Reimagined.": "重新定义 Python 应用打包体验",
    "Drop Python source code to start": "拖拽 Python 源码至此开始",
    "Drag & Drop Python script (.py/.pyw) here\nor Click to Browse": "拖拽 Python 脚本 (.py/.pyw) 到此\n或点击浏览",

    # 3. 导航与选项卡 (Tabs & Navigation)
    "Build Settings": "构建设置",
    "Preferences": "偏好设置",
    "About": "关于",
    "Engine": "构建引擎",
    "Dependencies": "依赖管理",
    "Resources": "附加资源",
    "Optimization": "性能优化",
    "Package Map": "包名映射",
    "Execution Log": "执行日志",

    # 4. 主界面状态与引导 (Main UI & Status Prompts)
    "Loaded: {filename}": "已载入: {filename}",
    "Parsing metadata...": "解析元数据...",
    "Ready, waiting for build.": "就绪，等待构建",
    "Initializing build...": "初始化构建...",
    "Preparing engine...": "准备引擎...",
    "Build Successful": "构建成功",
    "Open output directory or reset workspace.": "打开输出目录或重置工作区",
    "Build Failed": "构建失败",
    "Check log output below for troubleshooting.": "请查看下方日志排查问题",
    "Status: Ready": "状态: 就绪",
    "Status: Parsing {filename}...": "状态: 解析 {filename}...",
    "Status: Loaded {filename}{mode}": "状态: 已载入 {filename}{mode}",
    "Status: Packaging ({engine}) ...": "状态: 构建中 ({engine})...",
    "Status: Build Completed": "状态: 构建完成",
    "Status: Build Failed": "状态: 构建失败",
    "Status: Workspace Reset": "状态: 工作区已重置",
    " [Console]": " [控制台]",
    " [No Console]": " [无控制台]",

    # 5. 操作按钮与右键菜单 (Buttons & Context Menus)
    "Start Build": "开始构建",
    "Stop Build": "停止构建",
    "Open Directory": "打开目录",
    "Rebuild": "重新构建",
    "Save & Return": "保存并返回",
    "Browse": "浏览...",
    "AST Scan": "AST 扫描",
    "Add File": "添加文件",
    "Add Dir": "添加目录",
    "Remove Selected": "移除选中项",
    "Clear All": "清空全部",
    "Add Mapping": "添加映射",
    "Restore Defaults": "恢复默认",
    "Export Preset...": "导出预设...",
    "Import Preset...": "导入预设...",
    "Reset to Default Config": "重置默认配置",
    "Cancel & Return": "取消并返回",
    "Cancel": "取消",
    "Configure Build Settings": "构建设置",
    "Toggle Execution Log": "切换日志",
    "Detailed Mode": "详细日志",
    "Concise Mode": "精简日志",
    "Copy": "复制",
    "Select All": "全选",
    "Clear Log": "清空日志",
    "Export Log...": "导出日志...",
    "Reset": "重置",
    "<b>Are you sure you want to reset all preferences?</b><br><span style='color:#64748b; font-size:12px;'>All settings will be restored to default state.</span>":
        "<b>确定重置所有偏好设置？</b><br><span style='color:#64748b; font-size:12px;'>所有设置将恢复为默认状态。</span>",

    # 6. 设置分组卡片与表单标签 (Card Titles & Form Labels)
    "Engine & Environment": "引擎与环境",
    "Execution Mode": "执行模式",
    "Mirrors & Scanner": "镜像与扫描",
    "Additional Resources (Drag & Drop Supported)": "附加资源 (支持拖拽)",
    "Performance Optimization": "性能优化",
    "Lock Core Dependencies": "锁定核心依赖",
    "Package Name Mappings": "包名映射",
    "UI Language:": "界面语言:",
    "App Metadata & Presets": "元数据与预设",
    "Output Location": "输出位置",
    "Preferences & System Behavior": "偏好与行为",
    "Build Engine:": "构建引擎:",
    "Python Interpreter:": "Python 解释器:",
    "Output Name:": "输出名称:",
    "App Icon:": "应用图标:",
    "Primary PIP Index:": "主 PIP 源:",
    "Backup PIP Index:": "备用 PIP 源:",
    "Requirements File:": "依赖清单 (requirements):",
    "Hidden Imports:": "隐式导入 (hidden-imports):",
    "Exclude Modules:": "排除模块 (excludes):",
    "CPU Cores:": "CPU 核心数:",
    "UPX Path:": "UPX 路径:",
    "PyInstaller Version:": "PyInstaller 版本:",
    "Nuitka Version:": "Nuitka 版本:",
    "Version:": "版本:",
    "Author/Company:": "作者/公司:",
    "Description:": "描述:",
    "Output Location:": "保存位置:",
    "Target Directory:": "自定义路径:",
    "Temporary Directory:": "临时目录:",
    "Source Directory (.qpypack_build)": "源码同级目录 (.qpypack_build)",
    "System Temp Directory": "系统 Temp 目录",
    "Source File Directory": "源码同级目录",
    "Custom Directory": "自定义目录",
    "Import Name": "导入名",
    "PyPI Package Name": "PyPI 包名",
    "File": "文件",
    "Directory": "目录",
    "Edit Path": "编辑路径",
    "Target relative path:": "目标相对路径:",
    "Import name (e.g. cv2):": "导入名 (如 cv2):",
    "PyPI package name for [{imp_name}]:": "[{imp_name}] 对应 PyPI 包名:",
    "Script and settings retained. Ready to rebuild.": "已保留当前配置，就绪等待重新构建。",

    # 7. 复选框、占位符与悬停提示 (Checkboxes, Placeholders & Tooltips)
    "One-File Mode (--onefile)": "单文件 (--onefile)",
    "Hide Console (--noconsole)": "隐藏控制台 (--noconsole)",
    "Use Virtual Environment (Recommended)": "使用虚拟环境 (推荐)",
    "Install requirements.txt": "安装 requirements.txt",
    "Analyze Dependencies (AST)": "分析依赖 (原生 AST)",
    "Scan Entire Folder": "扫描整个文件夹",
    "Enable UPX Compression": "启用 UPX 压缩",
    "Lite Mode (Exclude Dev/Test Dependencies)": "精简模式 (排除开发/测试依赖)",
    "Concise Log Output": "精简日志",
    "Auto-save Build Log": "自动保存日志",
    "Auto Extract Icon": "自动提取图标",
    "Clean Temporary Cache After Build": "构建后清理缓存",
    "Sound Notification": "完成提示音",
    "Leave blank to auto-detect system default Python": "留空则自动检测系统 Python",
    "Leave blank to auto-match script name": "留空则自动匹配脚本名",
    "Leave blank to auto-search requirements.txt in current directory": "留空则自动检索当前目录 requirements.txt",
    "Comma separated (e.g. pandas, PyQt5)": "逗号分隔 (如 pandas, PyQt5)",
    "Comma separated (e.g. tkinter, matplotlib)": "逗号分隔 (如 tkinter, matplotlib)",
    "Leave blank to auto-detect from environment variables": "留空则从环境变量自动检测",
    "Dynamically exclude redundant dependencies in build environment, improving speed and reducing size.": "动态排除构建环境的冗余依赖，提升速度并减小体积。",
    "Double-click to edit target path; Drag & drop supported": "双击编辑目标路径；支持拖拽",
    "Double-click to edit target path; Drag & drop supported. Use 'Export Preset' to save for reuse.": "双击编辑目标路径；支持拖拽。建议使用「导出预设」进行保存。",

    # 8. 引擎说明与平台兼容性矩阵 (Engine Help & Platform Matrices)
    "PyInstaller — Bundles Python interpreter and bytecode. Fast build speed, zero configuration (no C compiler needed), and excellent compatibility.":
        "PyInstaller — 打包解释器与字节码。构建迅速，零配置 (无需 C 编译器)，兼容性优异。",

    "Nuitka — Compiles source code into native C/C++ binary. Produces smaller package size, faster execution, and deep anti-decompilation protection (requires C compiler).":
        "Nuitka — 编译为原生 C/C++ 二进制。体积更小，执行更快，具备强抗反编译能力 (需 C 编译器)。",

    '<div style="margin-bottom: 5px;"><b>Python {ver} Platform Matrix:</b></div><span style="color:#16a34a; font-weight:bold;">✔ Windows 7</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Windows 8 / 8.1</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Windows 10 / 11</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ macOS 10.9+</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Linux</span><br><span style="background-color:#f1f5f9; color:#475569; padding:1px 5px; border-radius:3px; font-weight:bold; font-size:10px;">Legacy OS</span> <span style="color:#6b7280; font-size:11px;">Full backward compatibility</span>':
        '<div style="margin-bottom: 5px;"><b>Python {ver} 平台支持：</b></div><span style="color:#16a34a; font-weight:bold;">✔ Windows 7</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Windows 8/8.1</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Windows 10/11</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ macOS 10.9+</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Linux</span><br><span style="background-color:#f1f5f9; color:#475569; padding:1px 5px; border-radius:3px; font-weight:bold; font-size:10px;">兼容旧系统</span> <span style="color:#6b7280; font-size:11px;">支持 Windows 7 及旧版操作系统</span>',

    '<div style="margin-bottom: 5px;"><b>Python {ver} Platform Matrix:</b></div><span style="color:#dc2626; font-weight:bold;">✖ Windows 7</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Windows 8.1</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Windows 10 / 11</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ macOS 10.9+</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Linux</span>':
        '<div style="margin-bottom: 5px;"><b>Python {ver} 平台支持：</b></div><span style="color:#dc2626; font-weight:bold;">✖ Windows 7</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Windows 8.1</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Windows 10/11</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ macOS 10.9+</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Linux</span>',

    '<div style="margin-bottom: 5px;"><b>Python {ver} Platform Matrix:</b></div><span style="color:#dc2626; font-weight:bold;">✖ Windows 7</span> &nbsp;&nbsp; <span style="color:#dc2626; font-weight:bold;">✖ Windows 8 / 8.1</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Windows 10 / 11</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ macOS 10.13+</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Linux</span><br><span style="background-color:#dcfce7; color:#15803d; padding:1px 5px; border-radius:3px; font-weight:bold; font-size:10px;">Nuitka</span> <span style="color:#16a34a; font-size:11px;">Auto-detecting and managing C backend compiler</span>':
        '<div style="margin-bottom: 5px;"><b>Python {ver} 平台支持：</b></div><span style="color:#dc2626; font-weight:bold;">✖ Windows 7</span> &nbsp;&nbsp; <span style="color:#dc2626; font-weight:bold;">✖ Windows 8/8.1</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Windows 10/11</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ macOS 10.13+</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Linux</span><br><span style="background-color:#dcfce7; color:#15803d; padding:1px 5px; border-radius:3px; font-weight:bold; font-size:10px;">Nuitka</span> <span style="color:#16a34a; font-size:11px;">自动检测并管理 C 后端编译器</span>',

    '<div style="margin-bottom: 5px;"><b>Python Interpreter</b></div><span style="color:#6b7280;">Auto-detecting system environment for Windows, macOS & Linux...</span>':
        '<div style="margin-bottom: 5px;"><b>Python 解释器</b></div><span style="color:#6b7280;">自动检测系统环境 (Win/macOS/Linux)...</span>',

    # 9. 构建日志与异常错误提示 (Log Output, Errors & Warnings)
    "[INFO] Build Cancelled.": "[INFO] 构建已取消。",
    "[INFO] Performing pre-flight environment checks...": "[INFO] 执行预构建环境检查...",
    "[INFO] Analyzing source code and project dependencies...": "[INFO] 分析源码与依赖...",
    "[INFO] Initializing isolated build environment...": "[INFO] 初始化构建环境...",
    "[INFO] Playwright detected. Installing built-in browsers (PLAYWRIGHT_BROWSERS_PATH=0)...": "[INFO] 检测到 Playwright。正在安装内置浏览器驱动...",
    "[INFO] Python interpreter path: {path}": "[INFO] Python 路径: {path}",
    "[INFO] Creating virtual environment...": "[INFO] 创建虚拟环境...",
    "[INFO] Synchronizing and upgrading pip package manager...": "[INFO] 更新 pip...",
    "[INFO] Scanning project source code via AST engine...": "[INFO] 使用原生 AST 引擎扫描依赖...",
    "[INFO] Nuitka Tip: If prompted to download GCC/MinGW compiler on first build, please ensure stable network connection.": "[INFO] Nuitka 提示: 首次构建如需下载 GCC/MinGW，请确保网络畅通。",
    "[INFO] Successfully installed compatible versions.": "[INFO] 已成功安装兼容版本。",
    "[INFO] Resolving project dependencies...": "[INFO] 解析项目依赖...",
    "Declared in requirements.txt ({count}): {pkgs}": "依赖声明 ({count}): {pkgs}",
    "Declared in requirements.txt: None": "依赖声明: 无",
    "Discovered via scanner ({count}): {pkgs}": "扫描发现 ({count}): {pkgs}",
    "Auto-patched missing ({count}): {pkgs}": "自动补齐 ({count}): {pkgs}",
    "Manifest complete (No missing packages)": "清单完整 (无缺失包)",
    "Build engine packages ({count}): {pkgs}": "引擎依赖 ({count}): {pkgs}",
    "[INFO] Installing build environment and project dependencies ({count} packages): {pkgs}": "[INFO] 安装依赖 ({count}): {pkgs}",
    "[INFO] Switching to backup PyPI source for retrieval: {url}": "[INFO] 切换备用 PyPI 源: {url}",
    "[INFO] Starting {engine} engine to compile binary files...": "[INFO] 启动 {engine} 引擎编译...",
    "[INFO] Found local MSVC environment, prioritizing native C++ compiler.": "[INFO] 检测到本地 MSVC 环境，优先使用原生 C++ 编译器。",
    "[INFO] Found local Clang environment, prioritizing LLVM Clang compiler.": "[INFO] 检测到本地 Clang 环境，优先使用 LLVM Clang 编译器。",
    "[INFO] Python 3.13+ detected: Using Zig compiler (--zig) as C backend.": "[INFO] Python 3.13+: 使用 Zig 编译器。",
    "[INFO] Using MinGW64 compiler (--mingw64) for C backend.": "[INFO] 使用 MinGW64 编译器。",
    "[INFO] Found local GCC/MinGW-w64 environment, using MinGW64 compiler.": "[INFO] 检测到本地 GCC/MinGW-w64 环境，优先使用 MinGW64 编译器。",
    "[INFO] Found local Zig environment, letting Nuitka manage C backend compilation.": "[INFO] 检测到本地 Zig 环境，由 Nuitka 接管 C 后端编译。",
    "[INFO] No local C compiler detected. Nuitka will automatically download and manage a compatible MinGW-w64 toolchain.": "[INFO] 未检测到本地 C 编译器，Nuitka 将自动下载并管理兼容的 MinGW-w64 工具链。",
    "[INFO] Evaluating system physical memory (Available: {ram:.1f} GB). Adaptive concurrency adjusted: {cores} -> {safe_jobs} ...": "[INFO] 评估系统可用物理内存 ({ram:.1f} GB)，动态调整并发数: {cores} -> {safe_jobs}",
    "[INFO] Stripping icon parameters and automatically rebuilding...": "[INFO] 移除图标参数并重新构建...",
    "[INFO] Lite mode enabled, applying bytecode optimization (-OO) and stripping dev modules...": "[INFO] 启用精简模式，应用字节码优化 (-OO) 并剔除开发环境模块...",
    "[INFO] Compilation completed, archiving built files...": "[INFO] 编译完成，归档构建产物...",
    "[INFO] Validating output files and generating final product...": "[INFO] 校验并生成最终产物...",
    "[INFO] Build log exported to: {path}": "[INFO] 日志已导出: {path}",
    "[INFO] Freeing up space, cleaning temporary build environment...": "[INFO] 清理临时构建环境...",
    "[SUCCESS] Compilation completed, output path: {path}": "[SUCCESS] 构建成功，输出路径: {path}",
    "[WARN] Target project is in a Cloud Sync directory (e.g. OneDrive/Dropbox). Cloud sync may temporarily lock build files.": "[WARN] 项目位于云同步目录，可能锁定构建文件。",
    "[WARN] Specified versions failed to install. Stripping version constraints for automatic compatibility match...": "[WARN] 指定版本安装失败，尝试自动匹配兼容版本...",
    "[WARN] Some dependencies failed to install, build will proceed with risk...": "[WARN] 部分依赖安装失败，继续构建 (有风险)。",
    "[WARN] Low disk space detected on build target drive (Available: {free:.1f} GB, >= 5.0 GB recommended). Build process may interrupt due to disk exhaustion.": "[WARN] 目标磁盘空间不足 (可用: {free:.1f} GB，推荐 >= 5.0 GB)。",
    "[WARN] Memory allocation exception caught (ZstdError / OOM). Triggering memory protection fallback: Retrying in single-thread mode...": "[WARN] 捕获内存分配异常 (ZstdError/OOM)，降级为单线程模式重试...",
    "[WARN] System low memory detected (zstd memory allocation failed). Automatically retrying in single-thread low-memory mode...": "[WARN] 内存不足 (zstd 分配失败)，降级为单线程模式重试...",
    "[WARN] Icon resource writing blocked (possibly locked by system/antivirus), triggering fallback protection...": "[WARN] 图标资源写入被拦截 (可能受安全软件限制)，触发降级机制...",
    "[WARN] Strongly recommend checking [Virtual Environment] to maximize lite mode effect.": "[WARN] 强烈建议启用「虚拟环境」以最大化精简效果。",
    "[WARN] Pause code injection exception: {error}": "[WARN] 注入暂停代码异常: {error}",
    "[WARN] AST Analysis Exception: {error}": "[WARN] AST 分析异常: {error}",
    "[WARN] Read requirements.txt warning: {error}": "[WARN] 读取 requirements.txt 警告: {error}",
    "[WARN] Command timeout (>{timeout}s)": "[WARN] 命令超时 (>{timeout}s)",
    "[WARN] Detected 'requests' or 'httpx'. Auto-bundling 'certifi' certificates to prevent SSL errors.": "[WARN] 检测到网络请求库，自动捆绑 'certifi' 根证书以防止 SSL 异常。",
    "[WARN] Usage of '__file__' detected. In PyInstaller One-File mode, use 'sys._MEIPASS' to reliably locate bundled resource files!": "[WARN] 侦测到 '__file__' 的使用。在 PyInstaller 单文件模式下，请使用 'sys._MEIPASS' 定位资源释放路径，以免引发文件丢失错误。",
    "[INFO] Tip: Packaged executables might be falsely flagged by Windows Defender/Antivirus. Adding exclusions or code-signing is recommended.": "[INFO] 提示: 独立可执行程序可能被安全软件误报。建议将其加入白名单，或为正式发布程序添加代码签名。",
    "[ERROR] Build aborted: Insufficient disk space (NoSpaceLeft / Errno 28). Please clean up drive space (at least 5 GB free space recommended) and try again.": "[ERROR] 构建中止: 磁盘空间不足 (NoSpaceLeft / Errno 28)。建议预留至少 5GB 可用空间。",
    "[ERROR] Output directory is missing write permissions: {error}": "[ERROR] 目标输出目录无写入权限: {error}",
    "[ERROR] Requirements file not found: {path}": "[ERROR] 指定的依赖清单文件不存在: {path}",
    "[ERROR] Insufficient disk space (Available: {free:.1f} GB). At least 0.5 GB is required to safely initialize the build environment.": "[ERROR] 磁盘空间不足 (可用 {free:.1f} GB)。至少需 0.5 GB 才能安全初始化环境。",
    "[ERROR] Python interpreter is invalid or not found: {path}": "[ERROR] Python 解释器无效或未找到: {path}",
    "[ERROR] The specified icon file does not exist: {path}": "[ERROR] 指定的应用图标文件不存在: {path}",
    "[ERROR] Additional resource file/directory not found: {path}": "[ERROR] 附加数据中的文件/目录不存在: {path}",
    "[ERROR] Failed to create virtual environment. Current Python environment might be missing necessary modules or have restricted permissions.": "[ERROR] 虚拟环境创建失败。环境可能缺失模块或权限受限。",
    "[ERROR] Product transfer failed, file might be occupied by system process or lack permission: {error}": "[ERROR] 构建产物转移失败，文件可能被占用或无写入权限: {error}",
    "[ERROR] Could not locate valid executable product in temporary build directory: {path}": "[ERROR] 临时构建目录未找到可执行产物: {path}",
    "[Syntax Error] Source code contains syntax errors, compilation aborted:\n  - File: {file}\n  - Type: {type}\n  - Line: Line {line}\n  - Detail: {desc}\n\nTip: Please ensure the source code runs locally before packaging.": "[ERROR] 源码语法错误，构建中止:\n  - 文件: {file}\n  - 类型: {type}\n  - 行号: {line}\n  - 详情: {desc}\n\n提示: 请确保源码可在本地运行。",
    "[FAILED] Compilation interrupted with exceptions, please click 'Detailed Mode' above the log window for troubleshooting.": "[FAILED] 构建异常中断，请切换至「详细日志」排查原因。",
    "[ERROR] Target file is locked or encrypted by cloud drive. Please decrypt and try again.": "[ERROR] 目标文件被云盘锁定或加密，请解密后重试。",
    "[ERROR] Target file is running or occupied. Please close the existing application and try again.": "[ERROR] 目标程序正在运行或被系统占用。请先关闭该程序后再重新构建。",
    "[WARN] 'multiprocessing' module detected. Ensure 'multiprocessing.freeze_support()' is called under 'if __name__ == \"__main__\":' to prevent infinite process loops (fork bombs).": "[WARN] 检测到 multiprocessing 模块。请确保在 'if __name__ == \"__main__\":' 块内调用 'multiprocessing.freeze_support()'，以防引发无限进程 (Fork Bomb) 死机。",
    "[ERROR] Please load a valid Python source file first!": "[ERROR] 请加载有效的 Python 源码！",
    "[ERROR] Exception occurred during AST parsing: {error}": "[ERROR] AST 解析异常: {error}",
    "[ERROR] Failed to export preset file: {error}": "[ERROR] 导出预设失败: {error}",
    "[ERROR] Preset file format error or corrupted: {error}": "[ERROR] 预设文件格式错误或已损坏: {error}",
    "[ERROR] Failed to export log file: {error}": "[ERROR] 导出日志失败: {error}",
    "[ERROR] Build completed, but the following dependencies failed to install:\n\n  - {pkgs}\n\nNote: The application might raise ModuleNotFoundError at runtime.": "[ERROR] 构建完成，但以下依赖安装失败:\n\n  - {pkgs}\n\n注意: 运行时可能抛出 ModuleNotFoundError。",
    "[ERROR] Process error: command or binary missing ({error})": "[ERROR] 进程错误: 命令或二进制文件缺失 ({error})",
    "[ERROR] System execution exception: {error}": "[ERROR] 系统执行异常: {error}",
    "[ERROR] I/O Exception: {err_msg}": "[ERROR] I/O 异常: {err_msg}",
    "No log content.": "无日志内容。",
    "Log saved to: {path}": "日志已保存: {path}",
    "\\nProgram execution completed, press Enter to exit...": "\\n程序执行完成，按回车键退出...",
    "Project-specific. Not saved to global preferences. Use 'Export Preset' to save config.": 
        "提示：此处资源配置仅对当前项目生效。如需长期复用，请使用「导出预设」。",
    "GitHub Repository": "GitHub 仓库",
    "Issues & Feedback": "问题与反馈",
    "PyPI Home": "PyPI 主页",
    "Sponsor": "赞助支持",
    "QPyPack is a free and open-source tool. If it has improved your efficiency or solved packaging problems, consider buying the author a coffee!": "QPyPack 是一款免费开源工具。如果它提升了您的效率或解决了打包难题，欢迎赞助支持本开源项目。",
    "* Sponsorship is completely voluntary, serves as an unconditional encouragement to the open-source community, and involves no commercial commitments. Thank you for your support!": "* 赞助完全出于自愿，属于对开源社区的无偿鼓励，不涉及任何商业承诺。感谢您的支持！",
    "Python Environment Required": "需要 Python 环境",
    "<b>Python is not detected on your system!</b><br><br>QPyPack requires a Python environment to compile your code.<br>If you haven't installed Python, please download and install it (remember to check <b>'Add Python.exe to PATH'</b> during installation).": "<b>未在系统中检测到有效的 Python 环境</b><br><br>QPyPack 需要依赖 Python 才能编译代码。<br>如果您尚未安装，请前往官网下载安装 (提示：安装界面底部请务必勾选 <b>'Add Python.exe to PATH'</b>)。",
    "Download Python": "前往下载 Python",
    "Python 3.14.6 (Experimental)": "Python 3.14.6 (实验性)",
    "Python 3.13.0": "Python 3.13.0",
    "Python 3.12.4": "Python 3.12.4",
    "Python 3.11.9 (Recommended)": "Python 3.11.9 (推荐)",
    "Python 3.10.11": "Python 3.10.11",
    "Python 3.9.13": "Python 3.9.13",
    "Python 3.8.10 (Win7 Support)": "Python 3.8.10 (Win7 兼容)",
    "Downloading Python {ver}... Please wait.": "正在下载 Python {ver}，请稍候...",
    "Configure Manually": "手动配置路径",
    "Switched to [Build Settings] -> [Engine], please set the Python path.": "已自动切换至【构建设置】->【构建引擎】，请手动指定 Python 解释器路径。",

    # 10. Python 环境管理弹窗 (Python Environment Manager)
    "Python Environment Management": "Python 环境管理",
    "<b>Python Environment Required</b><br><span style='color:#475569; font-size:12px; line-height:1.6;'>Application build depends on a Python interpreter.<br>Please select a version to automatically download, install, and configure environment variables.</span>":
        "<b>需要 Python 编译环境</b><br><span style='color:#475569; font-size:12px; line-height:1.6;'>应用构建需要依赖 Python 解释器。<br>请选择版本以自动下载安装与配置环境变量。</span>",
    "<b>Python Environment Management</b><br><span style='color:#475569; font-size:12px; line-height:1.6;'>Supports switching locally detected Python environments or downloading new versions.</span>":
        "<b>Python 环境管理</b><br><span style='color:#475569; font-size:12px; line-height:1.6;'>支持切换本地已检测到的 Python 环境或下载新版本。</span>",
    "💡 <b>Recommendation:</b> Python <b>3.11.9</b> is recommended for optimal build compatibility and engine support.":
        "💡 <b>建议：</b> 推荐选择 <b>Python 3.11.9</b>，该版本具备最佳的编译兼容性与引擎支持。",
    "View Python": "查看 Python",
    "Locally Detected Pythons": "已检测环境",
    "Download New Version": "下载新版本",
    "Use Selected Environment": "切换至选中环境",
    "No local Python environments detected.": "未检测到本地 Python 环境",
    "Select Python Version to Download:": "选择 Python 版本：",
    "Click to automatically download, install Python, and configure system environment variables.":
        "点击后将自动下载安装 Python 并配置系统环境变量。",
    "One-Click Download & Install": "下载并自动安装",
    "Use Installed Version Directly": "✔ 本地已存在，直接切换",
    "<b><span style='color:#16a34a;'>✔ Detected locally:</span></b><br><span style='color:#475569; font-family:Consolas;'>{path}</span><br><span style='color:#16a34a; font-size:11px;'>Ready to switch directly without re-downloading.</span>":
        "<b><span style='color:#16a34a;'>✔ 本地已检测到此版本：</span></b><br><span style='color:#475569; font-family:Consolas;'>{path}</span><br><span style='color:#16a34a; font-size:11px;'>可直接切换使用，无需重复下载。</span>",
    "Switched to local Python environment: {path}": "已切换 Python 环境: {path}",
    "Download complete. Starting Python installation...": "下载完成，正在安装 Python，请稍候...",
    "Install Complete": "安装完成",
    "Exit Now": "退出软件",
    "Later": "稍后",
    "<b>Python Environment Installed Successfully!</b><br><br>System environment variables updated. Recommended to exit and restart the software to apply changes.":
        "<b>Python 环境安装成功！</b><br><br>建议退出软件后重新打开以生效环境变量。",
    "Python installed. Please restart QPyPack manually later.": "Python 已安装，请稍后手动重启软件。",

    # 11. Python 版本不匹配提示：
    "[Syntax Error] Source code syntax parsing failed, build aborted:\n"
    "  - File: {file}\n"
    "  - Line: Line {line}\n"
    "  - Detail: {desc}\n\n"
    "💡 Tip: This is usually NOT a fault of the packaging tool.\n"
    "Please ensure the [Build Python Version] you selected matches the version you used to [Write/Test the Code].\n"
    "Using newer syntax (e.g., walrus operator :=, type unions |, match-case) in an older Python environment will trigger this error.\n"
    "We recommend going to [Build Settings] -> [Engine] to switch to the correct Python version.":
        "[Syntax Error] 源码语法解析失败，构建中止:\n"
        "  - 文件: {file}\n"
        "  - 行号: {line}\n"
        "  - 详情: {desc}\n\n"
        "💡 提示：这通常不是打包工具的故障。\n"
        "请确认您当前选择的【打包 Python 版本】与您【编写代码时的版本】是否一致。\n"
        "高版本语法（如海象运算符 :=、类型联合 |、match-case 等）在低版本 Python 中会导致此错误。\n"
        "建议前往【构建设置】->【构建引擎】切换至对应版本的 Python。",
        
    "[FAILED] Build interrupted exceptionally!\n\n"
    "🔍 Common Troubleshooting:\n"
    "1. Environment Mismatch (Most Common): The selected Python version is incompatible with your source code. Please go to [Build Settings] to switch to the Python version you normally use for this code.\n"
    "2. Missing Dependencies: Click 'Detailed Mode' above to check for ModuleNotFoundError.\n"
    "3. Antivirus Block: Ensure your security software is not blocking the build process.\n\n"
    "(Note: This is usually caused by environment/code discrepancies rather than the packaging engine itself. Please check the detailed log for exact reasons.)":
        "[FAILED] 构建异常中断！\n\n"
        "🔍 常见原因排查：\n"
        "1. 环境不匹配 (最常见)：您选择的打包 Python 版本与您的源码不兼容。请前往【构建设置】切换为您平时开发运行该代码的 Python 版本。\n"
        "2. 依赖缺失：请点击上方切换至「详细日志」，查看是否有模块未找到 (ModuleNotFoundError)。\n"
        "3. 杀毒软件拦截：请检查是否有安全软件阻止了打包过程。\n\n"
        "（注意：这通常是环境配置与代码差异导致，并非打包引擎本身故障，请查阅详细日志获取确切原因。）",

    "Status: Build Cancelled": "状态: 构建已取消",
    "Build Cancelled": "构建已取消",
    "[INFO] Build Cancelled.": "[INFO] 构建已取消。",
    
    "[WARN] Package '{pkg}' failed to install, skipping...": "[WARN] 包 '{pkg}' 安装失败，已跳过...",
    "Dependency Missing Warning: {pkgs} failed to install. Check log for details.": "依赖缺失警告: {pkgs} 安装失败。详情请查看日志。",
    "[ERROR] Build completed, but the following dependencies failed to install:\n\n  - {pkgs}\n\nNote: The application might raise ModuleNotFoundError at runtime.": 
        "[ERROR] 构建完成，但以下依赖安装失败:\n\n  - {pkgs}\n\n注意: 运行时程序可能会抛出 ModuleNotFoundError。",
        
    "Package mappings have been reset to defaults.": "包名映射已恢复为默认设置。",
    "Global configuration has been reset.": "全局偏好配置已恢复默认。",
    "Config preset exported to: {path}": "配置预设已成功导出至: {path}",
    "Config preset imported successfully.": "配置预设已成功导入。",
    "AST scan completed, found {count} dependencies.": "AST 扫描完成，发现 {count} 个隐式依赖。",
    "Attention: Please check the log for details.": "提示: 请检查下方日志排查详细原因。",
    
    "One-Click Install": "一键安装 Python",
    "Downloading Python {ver}... Please wait.": "正在下载 Python {ver}，请稍候...",
    "Download complete. Starting Python installation...": "下载完成，正在后台安装 Python...",
    "[ERROR] Python installation failed or was cancelled.": "[ERROR] Python 安装失败或已被主动取消。",
    "Python installed. Please restart QPyPack manually later.": "Python 安装完毕。请稍后手动重启 QPyPack 以生效环境变量。",
    "Switched to local Python environment: {path}": "已成功切换至本地 Python 环境: {path}",

    "One-File Mode (--onefile)": "单文件模式 (--onefile)",
    "Folder Mode (--onedir)": "文件夹模式 (--onedir)",
    "Contents Directory (--contents-directory):": "内部资源目录:",
    "Internal directory name for dependencies (default: _internal)": "内部依赖与资源存放目录名 (默认: _internal)",
    "System Default ({sys_native})": "系统默认 ({sys_native})",
    "My Studio": "我的工作室",
    "Python Executable": "Python 可执行程序",
    "Invalid syntax": "无效语法",
    "[INFO] Downloading Playwright browsers via mirror: {url}": "[INFO] 通过镜像下载 Playwright 浏览器: {url}",
    "[INFO] Retrying Playwright browser download via official CDN...": "[INFO] 通过官方 CDN 重试下载 Playwright 浏览器...",
    "[WARN] Playwright browser installation failed across all sources, build will proceed with risk...": "[WARN] 所有 Playwright 浏览器下载源均失败，继续构建 (有风险)...",
    "[WARN] Icon conversion to .icns failed, building without icon.": "[WARN] 图标转换为 .icns 失败，将不使用图标构建。",
    "OK": "确定",
    "Unknown": "未知"
}

class TranslationEngine(QObject):
    language_changed = Signal(str)
    DEFAULT_LOCALE = "en_US"

    LANG_META = {
        "en_US": {"native": "English"},
        "zh_CN": {"native": "简体中文"},
        "zh_TW": {"native": "繁體中文"},
        "ja_JP": {"native": "日本語"},
        "ko_KR": {"native": "한국어"},
        "de_DE": {"native": "Deutsch"},
        "fr_FR": {"native": "Français"},
        "es_ES": {"native": "Español"},
        "ru_RU": {"native": "Русский"},
        "pt_BR": {"native": "Português (Brasil)"},
        "it_IT": {"native": "Italiano"},
        "nl_NL": {"native": "Nederlands"},
        "pl_PL": {"native": "Polski"},
        "tr_TR": {"native": "Türkçe"},
        "vi_VN": {"native": "Tiếng Việt"},
        "th_TH": {"native": "ไทย"},
        "ar_SA": {"native": "العربية"},
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
                    logger.warning("[i18n] Failed to load %s: %s", p.name, e)

    def get_available_languages(self) -> dict:
        sys_code = self.detect_system_language()
        if sys_code in self.LANG_META:
            sys_native = self.LANG_META[sys_code]["native"].split(" (")[0]
        else:
            qloc = QLocale(sys_code)
            sys_native = qloc.nativeLanguageName().capitalize() or sys_code

        langs = {"auto": self.t("System Default ({sys_native})", sys_native=sys_native)}
        all_codes = set(self.translations.keys()) | {self.DEFAULT_LOCALE, "zh_CN"}
        
        for code in sorted(all_codes):
            if code in self.LANG_META:
                langs[code] = self.LANG_META[code]["native"]
            else:
                qloc = QLocale(code)
                native_name = qloc.nativeLanguageName()
                if not native_name or native_name == code:
                    native_name = qloc.languageToString(qloc.language())
                langs[code] = native_name.capitalize() if native_name else code
                
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
    'skimage': 'scikit-image', 'vlc': 'python-vlc', 'pyzbar': 'pyzbar', 'OpenGL': 'PyOpenGL',
    
    'pyside6_addons': 'PySide6', 'pyside6_essentials': 'PySide6',
    'pyside6-addons': 'PySide6', 'pyside6-essentials': 'PySide6',
    'pyqt5-plugins': 'PyQt5', 'pyqt5-tools': 'PyQt5', 'pyqt5_plugins': 'PyQt5',
    
    'fitz': 'pymupdf', 'docx': 'python-docx', 'pptx': 'python-pptx', 
    'bs4': 'beautifulsoup4', 'barcode': 'python-barcode', 'pdfplumber': 'pdfplumber',
    
    'win32com': 'pywin32', 'win32api': 'pywin32', 'win32con': 'pywin32',
    'win32gui': 'pywin32', 'win32clipboard': 'pywin32', 'win32print': 'pywin32', 'win32file': 'pywin32',
    'win32security': 'pywin32', 'win32process': 'pywin32', 'win32evtlog': 'pywin32', 'win32service': 'pywin32',
    'win32pipe': 'pywin32', 'win32net': 'pywin32', 'win32crypt': 'pywin32', 'pythoncom': 'pywin32',
    'pywintypes': 'pywin32',
    
    'serial': 'pyserial', 'usb': 'pyusb', 'bluetooth': 'pybluez', 'dns': 'dnspython',
    'websocket': 'websocket-client', 'paho': 'paho-mqtt', 'socketio': 'python-socketio',
    'engineio': 'python-engineio', 'kafka': 'kafka-python',
    
    'sklearn': 'scikit-learn', 'yaml': 'pyyaml', 'dateutil': 'python-dateutil', 'jwt': 'PyJWT',
    'Crypto': 'pycryptodome', 'wx': 'wxPython', 'desktop_notifier': 'desktop-notifier',
    'dotenv': 'python-dotenv', 'telegram': 'python-telegram-bot', 'git': 'GitPython',
    'github': 'PyGithub', 'gitlab': 'python-gitlab', 'discord': 'discord.py',
    'OpenSSL': 'pyOpenSSL', 'ldap': 'python-ldap', 'magic': 'python-magic', 'slugify': 'python-slugify',
    'snappy': 'python-snappy',
    
    'attr': 'attrs', 'psycopg2': 'psycopg2-binary'
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
    'close': 'M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z',
    'engine': 'M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.6C.4 7 1 10 3 12c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.4-.4.4-1.1 0-1.3z',
    'bolt': 'M11 21h-1l1-7H7.5c-.58 0-.57-.32-.38-.66s.06-.11.08-.15C8.22 11.23 10.3 7.6 13.43 2.15c.18-.32.37-.15.37.15l-1 7h3.5c.58 0 .57.32.38.66s-.06.12-.08.16L11 21z',
    'link': 'M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z'
}

def load_config(retry=True):
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
            'temp_sandbox_mode': '0',
            'sound_notify': 'True', 'auto_save_log': 'False',
            'use_reqs_file': '', 'add_data_list': '', 'custom_python_path': '',
            'pyi_version': '6.21.0', 'nuitka_version': '4.1.3',
            'lite_mode': 'False'
        }
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                config.write(f)
        except: pass
    else:
        try:
            config.read(CONFIG_FILE, encoding='utf-8')
        except Exception:
            if retry:
                try:
                    if os.path.exists(CONFIG_FILE):
                        os.remove(CONFIG_FILE)
                except Exception:
                    pass
                return load_config(retry=False)
            else:
                pass

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
            'temp_sandbox_mode': '0',
            'sound_notify': 'True',
            'auto_save_log': 'False',
            'use_reqs_file': '',
            'add_data_list': '',
            'custom_python_path': '',
            'pyi_version': '6.21.0',
            'nuitka_version': '4.1.3',
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

def is_cloud_sync_path(path_obj: Path) -> bool:
    path_str = path_obj.resolve().as_posix().lower()
    cloud_keywords = [
        'onedrive', 'dropbox', 'icloud', 'google drive', 'googledrive', 'gdrive',
        'box sync', 'box.com', 'pcloud', 'mega', 'megasync', 'nextcloud', 'owncloud',
        'synology', 'seafile', 'tresorit', 'yandex',
        'nutstore', '坚果云', '百度云', '百度网盘', '阿里云盘', 'aliyun', '115', '微云'
    ]
    return any(kw in path_str for kw in cloud_keywords)

def extract_project_imports_via_ast(target_path, scan_dir: bool = False) -> set:
    imports = set()
    target_path = Path(target_path)
    
    if not scan_dir or not target_path.is_dir():
        files_to_scan = [target_path] if target_path.is_file() else []
    else:
        files_to_scan = []
        for root, _, files in os.walk(target_path):
            path_parts = set(Path(root).parts)
            if path_parts & {'__pycache__', '.qpypack_build', '.venv', 'venv', 'build', 'dist', 'env', '.env'}:
                continue
            for file in files:
                if file.endswith(('.py', '.pyw')):
                    files_to_scan.append(Path(root) / file)

    for file_p in files_to_scan:
        try:
            raw = file_p.read_bytes()
            try:
                code = raw.decode('utf-8-sig')
            except Exception:
                code = raw.decode(locale.getpreferredencoding(), errors='ignore')
                
            tree = ast.parse(code, filename=file_p.as_posix())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.update(n.name.split('.')[0] for n in node.names)
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    imports.add(node.module.split('.')[0])
        except Exception:
            pass
    return imports


def query_target_env_packages(python_exe: str) -> dict:
    if not python_exe or not os.path.exists(python_exe):
        return {}
    
    code = (
        "import json\n"
        "try:\n"
        "    try:\n"
        "        from importlib.metadata import packages_distributions\n"
        "    except ImportError:\n"
        "        from importlib_metadata import packages_distributions\n"
        "    res = {k: v[0] for k, v in packages_distributions().items() if v}\n"
        "    print(json.dumps(res))\n"
        "except Exception:\n"
        "    print('{}')\n"
    )
    try:
        clean_env = os.environ.copy()
        clean_env.pop("PYTHONHOME", None)
        clean_env.pop("PYTHONPATH", None)
        kwargs = {"capture_output": True, "text": True, "env": clean_env, "timeout": 8, "errors": "ignore"}
        if os.name == 'nt':
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
            
        proc = subprocess.run([python_exe, "-c", code], **kwargs)
        if proc.returncode == 0 and proc.stdout.strip():
            return json.loads(proc.stdout.strip())
    except Exception:
        pass
    return {}

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
                    text=True, encoding="utf-8", errors="ignore", env=clean_env, creationflags=subprocess.CREATE_NO_WINDOW
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
            "/Library/Frameworks/Python.framework/Versions/Current/bin",
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
        
        if getattr(sys, 'frozen', False) or '__compiled__' in globals():
            try:
                if os.path.samefile(cand, sys.executable):
                    continue
            except Exception:
                pass

        if os.name == 'nt' and "WindowsApps" in cand:
            try:
                if os.path.getsize(cand) == 0: continue
            except: continue
            
        clean_env = os.environ.copy()
        clean_env.pop("PYTHONHOME", None)
        clean_env.pop("PYTHONPATH", None)
        
        try:
            kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE, "text": True, "encoding": "utf-8", "errors": "ignore", "env": clean_env, "timeout": 3}
            if os.name == 'nt': kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
            proc = subprocess.run([cand, "-V"], **kwargs)
            if proc.returncode == 0: return cand
        except: continue
            
    return ""

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

class CustomInputDialog(QDialog):
    def __init__(self, parent, title, label_text, text=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(320)
        self.setStyleSheet("""
            QDialog { background-color: #ffffff; }
            QLabel { font-size: 12px; color: #111827; }
            QLineEdit { padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 12px; }
            QLineEdit:focus { border: 1px solid #2563eb; }
            QPushButton { background-color: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 12px; font-weight: bold; padding: 6px 16px; min-width: 70px; }
            QPushButton:hover { background-color: #e2e8f0; }
            QPushButton#btnOk { background-color: #2563eb; color: #ffffff; border: none; }
            QPushButton#btnOk:hover { background-color: #1d4ed8; }
        """)
        
        lay = QVBoxLayout(self)
        lay.setSpacing(10)
        lay.setContentsMargins(20, 20, 20, 20)
        
        lay.addWidget(QLabel(label_text))
        
        self.edit = QLineEdit(text)
        lay.addWidget(self.edit)
        
        lay.addSpacing(10)
        
        btn_lay = QHBoxLayout()
        btn_lay.addStretch()
        
        self.btn_ok = QPushButton(_("OK"))
        self.btn_ok.setObjectName("btnOk")
        self.btn_ok.clicked.connect(self.accept)
        
        self.btn_cancel = QPushButton(_("Cancel"))
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_lay.addWidget(self.btn_ok)
        btn_lay.addWidget(self.btn_cancel)
        lay.addLayout(btn_lay)
        
    def get_text(self):
        return self.edit.text()

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
    libs = set(sys.builtin_module_names)
    
    if hasattr(sys, 'stdlib_module_names'):
        libs.update(sys.stdlib_module_names)
        
    try:
        import sysconfig
        stdlib_dir = sysconfig.get_path('stdlib')
        if stdlib_dir and os.path.exists(stdlib_dir):
            for f in os.listdir(stdlib_dir):
                if f.endswith('.py'):
                    libs.add(f[:-3])
                elif os.path.isdir(os.path.join(stdlib_dir, f)) and os.path.exists(os.path.join(stdlib_dir, f, '__init__.py')):
                    libs.add(f)
    except Exception:
        pass

    known_std = {
        'abc', 'aifc', 'argparse', 'array', 'ast', 'asynchat', 'asyncio', 'asyncore', 'atexit',
        'audioop', 'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins', 'bz2',
        'calendar', 'cgi', 'cgitb', 'chunk', 'cmap', 'cmath', 'cmd', 'code', 'codecs', 'codeop',
        'collections', 'colorsys', 'compileall', 'concurrent', 'configparser', 'contextlib',
        'contextvars', 'copy', 'copyreg', 'crypt', 'csv', 'ctypes', 'curses', 'dataclasses',
        'datetime', 'dbm', 'decimal', 'difflib', 'dis', 'distutils', 'doctest', 'dummy_threading',
        'email', 'encodings', 'ensurepip', 'enum', 'errno', 'faulthandler', 'fcntl', 'filecmp',
        'fileinput', 'fnmatch', 'formatter', 'fractions', 'ftplib', 'functools', 'gc', 'genericpath',
        'getopt', 'getpass', 'gettext', 'glob', 'graphlib', 'grp', 'gzip', 'hashlib', 'heapq',
        'hmac', 'html', 'http', 'imaplib', 'imghdr', 'imp', 'importlib', 'inspect', 'io',
        'ipaddress', 'itertools', 'json', 'keyword', 'lib2to3', 'linecache', 'locale', 'logging',
        'lzma', 'macpath', 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder',
        'msvcrt', 'multiprocessing', 'netrc', 'nis', 'nntplib', 'numbers', 'opcode', 'operator',
        'optparse', 'os', 'ossaudiodev', 'pathlib', 'pdb', 'pickle', 'pickletools', 'pipes',
        'pkgutil', 'platform', 'plistlib', 'poplib', 'posix', 'posixpath', 'pprint', 'profile',
        'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc', 'queue', 'quopri', 'random',
        're', 'readline', 'reprlib', 'resource', 'rlcompleter', 'runpy', 'sched', 'secrets',
        'select', 'selectors', 'shelve', 'shlex', 'shutil', 'signal', 'site', 'smtpd', 'smtplib',
        'sndhdr', 'socket', 'socketserver', 'spwd', 'sqlite3', 'ssl', 'stat', 'statistics',
        'string', 'stringprep', 'struct', 'subprocess', 'sunau', 'symbol', 'symtable', 'sys',
        'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios', 'textwrap',
        'threading', 'time', 'timeit', 'tkinter', 'token', 'tokenize', 'tomllib', 'trace',
        'tracemalloc', 'tty', 'turtle', 'turtledemo', 'types', 'typing', 'unicodedata', 'unittest',
        'urllib', 'uu', 'uuid', 'venv', 'wave', 'weakref', 'webbrowser', 'winreg', 'winsound',
        'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp', 'zipfile', 'zipimport', 'zlib', 'zoneinfo',
        '__future__', '_thread', '_asyncio'
    }
    libs.update(known_std)
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

def remove_readonly(func, path, exc_info=None):
    try: 
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception: pass

def robust_rmtree(path: Path, retries=15, delay=0.8):
    if not path.exists(): return True
    for _ in range(retries):
        try:
            if sys.version_info >= (3, 12):
                shutil.rmtree(path, onexc=lambda func, p, exc: remove_readonly(func, p))
            else:
                shutil.rmtree(path, onerror=remove_readonly)
            if not path.exists(): return True
        except Exception: time.sleep(delay)
    return False

def convert_image_to_format(src_path, dest_path, dest_format):
    src = Path(src_path).resolve()
    dst = Path(dest_path).resolve()
    fmt = dest_format.lower()
    
    try:
        from PIL import Image
        img = Image.open(src.as_posix())
        if fmt == "ico":
            ico_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
            resample_filter = getattr(Image.Resampling, 'LANCZOS', getattr(Image, 'LANCZOS', Image.BICUBIC))
            img.save(dst.as_posix(), format="ICO", sizes=ico_sizes, resample=resample_filter)
            return True
        elif fmt == "icns":
            img.save(dst.as_posix(), format="ICNS", sizes=[(512, 512), (256, 256), (128, 128), (64, 64)])
            return True
    except Exception:
        pass

    try:
        img = QImage(src.as_posix())
        if not img.isNull():
            if fmt == "ico": 
                img = img.scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            writer = QImageWriter(dst.as_posix(), fmt.upper().encode('utf-8'))
            if writer.write(img): 
                return True
    except Exception:
        pass

    if fmt == "ico":
        try:
            png_bytes = None
            img = QImage(src.as_posix())
            if not img.isNull():
                img_scaled = img.scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                temp_png = Path(tempfile.gettempdir()) / f"qpypack_ico_fallback_{int(time.time())}.png"
                if img_scaled.save(temp_png.as_posix(), "PNG"):
                    png_bytes = temp_png.read_bytes()
                    temp_png.unlink(missing_ok=True)
            elif src.suffix.lower() == '.png':
                png_bytes = src.read_bytes()

            if png_bytes:
                header = struct.pack('<HHH', 0, 1, 1)
                entry = struct.pack('<BBBBHHII', 0, 0, 0, 0, 1, 32, len(png_bytes), 22)
                dst.write_bytes(header + entry + png_bytes)
                return True
        except Exception:
            pass
        
    return False

def get_free_disk_gb(path="."):
    try:
        total, used, free = shutil.disk_usage(path)
        return free / (1024 ** 3)
    except Exception:
        return 10.0

def get_free_ram_gb():
    if os.name == 'nt':
        try:
            import ctypes
            from ctypes import wintypes
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ('dwLength', wintypes.DWORD), ('dwMemoryLoad', wintypes.DWORD),
                    ('ullTotalPhys', ctypes.c_uint64), ('ullAvailPhys', ctypes.c_uint64),
                    ('ullTotalPageFile', ctypes.c_uint64), ('ullAvailPageFile', ctypes.c_uint64),
                    ('ullTotalVirtual', ctypes.c_uint64), ('ullAvailVirtual', ctypes.c_uint64),
                    ('sullAvailExtendedVirtual', ctypes.c_uint64),
                ]
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                return stat.ullAvailPhys / (1024 ** 3)
        except Exception: pass
    elif sys.platform == 'darwin':
        try:
            out = subprocess.check_output(["vm_stat"], text=True, errors="ignore")
            pages_free = 0
            pages_inactive = 0
            page_size = 16384
            for line in out.splitlines():
                if "page size of" in line:
                    m = re.search(r'(\d+)', line)
                    if m: page_size = int(m.group(1))
                elif "Pages free" in line:
                    m = re.search(r'(\d+)', line)
                    if m: pages_free = int(m.group(1))
                elif "Pages inactive" in line:
                    m = re.search(r'(\d+)', line)
                    if m: pages_inactive = int(m.group(1))
            return ((pages_free + pages_inactive) * page_size) / (1024 ** 3)
        except Exception: pass
        
    return 8.0

class AnimatedButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        
        self.op_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.op_anim.setDuration(200)
        self.op_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.is_hovered = False

    def enterEvent(self, event):
        if not self.is_hovered and self.isEnabled():
            self.is_hovered = True
            self.op_anim.stop()
            self.op_anim.setStartValue(self.opacity_effect.opacity())
            self.op_anim.setEndValue(0.80)
            self.op_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.is_hovered and self.isEnabled():
            self.is_hovered = False
            self.op_anim.stop()
            self.op_anim.setStartValue(self.opacity_effect.opacity())
            self.op_anim.setEndValue(1.0)
            self.op_anim.start()
        super().leaveEvent(event)

class TargetIconWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(160, 160)
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
        try:
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
                    burst_radius_1 = (self.current_size / 2) + 5 + self.burst_value * 25
                    dot_size_1 = 8 * (1.0 - self.burst_value)
                    for i in range(8):
                        angle = math.radians(i * 45)
                        dx = center_x + math.cos(angle) * burst_radius_1
                        dy = center.y() + math.sin(angle) * burst_radius_1
                        painter.drawEllipse(QPointF(dx, dy), dot_size_1, dot_size_1)
                    
                    painter.setBrush(QColor(255, 193, 7, alpha))
                    burst_radius_2 = (self.current_size / 2) + self.burst_value * 35
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
            painter.drawPixmap(QPointF(pix_rect.x(), pix_rect.y()), scaled_pix)
        finally:
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
        
        self.label = QLabel(_("Python Packaging, Reimagined."))
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
        pass

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

        valid_pythons = {}

        def check_candidate(cand):
            if getattr(sys, 'frozen', False) or '__compiled__' in globals():
                try:
                    if os.path.samefile(cand, sys.executable):
                        return None
                except Exception:
                    pass

            if os.name == 'nt' and "WindowsApps" in cand:
                try:
                    if os.path.getsize(cand) == 0: return None
                except: return None
            try:
                clean_env = os.environ.copy()
                clean_env.pop("PYTHONHOME", None)
                clean_env.pop("PYTHONPATH", None)
                clean_env["PYTHONUTF8"] = "1"
                clean_env["PYTHONIOENCODING"] = "utf-8"
                kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE, "text": True, "encoding": "utf-8", "errors": "ignore", "env": clean_env, "timeout": 2}
                if os.name == 'nt': kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
                proc = subprocess.run([cand, "-c", "import sys; print(sys.version.split()[0])"], **kwargs)
                if proc.returncode == 0:
                    return (cand, proc.stdout.strip())
            except: pass
            return None

        with ThreadPoolExecutor(max_workers=min(12, len(resolved_candidates) or 1)) as executor:
            results = executor.map(check_candidate, resolved_candidates)
            for res in results:
                if res:
                    valid_pythons[res[0]] = res[1]

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
            QRadioButton { font-size: 13px; color: #1f2937; spacing: 8px; background: transparent; }
            QRadioButton::indicator { width: 16px; height: 16px; border: 1px solid #d1d5db; border-radius: 8px; background: #ffffff; }
            QRadioButton::indicator:hover { border-color: #2563eb; }
            QRadioButton::indicator:checked { background: #2563eb; border-color: #2563eb; }
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
        I18N.language_changed.connect(self.retranslate_ui)
        self.load_from_config()
        self.retranslate_ui()

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

    def on_mode_type_changed(self):
        is_folder = self.rb_onedir.isChecked()
        self.contents_dir_container.setVisible(is_folder)

    def _get_url_from_combo(self, combo):
        idx = combo.currentIndex()
        if idx >= 0 and combo.currentText() == combo.itemText(idx):
            data = combo.itemData(idx)
            if data: return data
        text = combo.currentText().strip()
        m = re.search(r'https?://[^\s]+', text)
        if m:
            return m.group(0).rstrip('/')
        if not text.startswith(('http://', 'https://')):
            return ''
        return text

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
        self.tab_about_scroll, _cnt_abt, self.lay_about = self._create_scroll_tab()

        self.tabs.addTab(self.tab_build, get_svg_icon('package', "#5F6368", 16), _("Build Settings"))
        self.tabs.addTab(self.tab_pref_scroll, get_svg_icon('settings', "#5F6368", 16), _("Preferences"))
        self.tabs.addTab(self.tab_about_scroll, get_svg_icon('info', "#5F6368", 16), _("About"))

        
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
        
        self.sub_tabs.addTab(sub_scroll1, get_svg_icon('engine', "#5F6368", 16), _("Engine"))
        self.sub_tabs.addTab(sub_scroll2, get_svg_icon('package', "#5F6368", 16), _("Dependencies"))
        self.sub_tabs.addTab(sub_scroll3, get_svg_icon('folder', "#5F6368", 16), _("Resources"))
        self.sub_tabs.addTab(sub_scroll4, get_svg_icon('bolt', "#5F6368", 16), _("Optimization"))
        self.sub_tabs.addTab(sub_scroll5, get_svg_icon('link', "#5F6368", 16), _("Package Map"))
        
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
        self.engine_desc_lbl.setStyleSheet("""
            QLabel {
                background-color: #f8fafc;
                color: #334155;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                line-height: 1.5;
            }
        """)

        self.python_desc_lbl = QLabel()
        self.python_desc_lbl.setOpenExternalLinks(True)
        self.python_desc_lbl.setWordWrap(True)
        self.python_desc_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.python_desc_lbl.setStyleSheet("""
            QLabel {
                background-color: #ffffff;
                color: #334155;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 12px;
            }
        """)

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
        self.python_path_combo.currentTextChanged.connect(self.on_python_path_changed)
        
        self.btn_python_path = QPushButton(_("Browse"))
        self.btn_python_path.setProperty("class", "ToolBtn")
        self.btn_python_path.clicked.connect(self.select_python_path)

        self.btn_download_py = QPushButton(_("View Python"))
        self.btn_download_py.setProperty("class", "ToolBtn")
        self.btn_download_py.setToolTip("")
        self.btn_download_py.clicked.connect(self.on_download_python_clicked)
        
        py_cont = QWidget()
        lay_py = QVBoxLayout(py_cont)
        lay_py.setContentsMargins(0, 0, 0, 0)
        lay_py.setSpacing(4)

        h_py_input = QHBoxLayout()
        h_py_input.setContentsMargins(0, 0, 0, 0)
        h_py_input.addWidget(self.python_path_combo, 1)
        h_py_input.addWidget(self.btn_python_path)
        h_py_input.addWidget(self.btn_download_py)

        lay_py.addLayout(h_py_input)
        lay_py.addWidget(self.python_desc_lbl)

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
        v_mode = QVBoxLayout()
        h_radio = QHBoxLayout()

        self.rb_onefile = QRadioButton(_("One-File Mode (--onefile)"))
        self.rb_onedir = QRadioButton(_("Folder Mode (--onedir)"))
        self.noconsole_check = QCheckBox(_("Hide Console (--noconsole)"))

        h_radio.addWidget(self.rb_onefile)
        h_radio.addWidget(self.rb_onedir)
        h_radio.addStretch()
        h_radio.addWidget(self.noconsole_check)

        self.lbl_contents_dir = QLabel(_("Contents Directory (--contents-directory):"))
        self.contents_dir_edit = QLineEdit("_internal")
        self.contents_dir_edit.setPlaceholderText(_("Internal directory name for dependencies (default: _internal)"))

        self.contents_dir_container = QWidget()
        h_contents = QHBoxLayout(self.contents_dir_container)
        h_contents.setContentsMargins(0, 5, 0, 0)
        h_contents.addWidget(self.lbl_contents_dir)
        h_contents.addWidget(self.contents_dir_edit, 1)
        self.contents_dir_container.setVisible(False)

        self.rb_onefile.toggled.connect(self.on_mode_type_changed)
        self.rb_onedir.toggled.connect(self.on_mode_type_changed)

        v_mode.addLayout(h_radio)
        v_mode.addWidget(self.contents_dir_container)
        c_lay_mode.addLayout(v_mode)

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
            display_text = f"{_(name)}: {url}"
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
        self.pipreqs_check = QCheckBox(_("Analyze Dependencies (AST)"))
        self.pipreqs_dir_check = QCheckBox(_("Scan Entire Folder"))
        
        g_dep.addWidget(self.venv_check, 0, 0)
        g_dep.addWidget(self.reqs_check, 0, 1)
        g_dep.addWidget(self.pipreqs_check, 1, 0)
        g_dep.addWidget(self.pipreqs_dir_check, 1, 1)
        c_lay_deps.addLayout(g_dep)

        lay_sub2.addWidget(self.card_deps)
        lay_sub2.addStretch()

        self.card_res, c_lay_res = self._create_card(_("Additional Resources (Drag & Drop Supported)"))
        
        self.lbl_res_hint = QLabel(_("Project-specific. Not saved to global preferences. Use 'Export Preset' to save config."))
        self.lbl_res_hint.setWordWrap(True) 
        self.lbl_res_hint.setStyleSheet("font-size: 12px; color: #6b7280; font-weight: normal; margin-top: -2px; margin-bottom: 6px; line-height: 1.4;")
        c_lay_res.addWidget(self.lbl_res_hint)

        self.add_data_list = DropListWidget()

        self.add_data_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.add_data_list.setMinimumHeight(120)
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
        
        self.lbl_pyi_ver = QLabel(_("PyInstaller Version:"))
        self.lbl_nuitka_ver = QLabel(_("Nuitka Version:"))
        
        self.form_ver.addRow(self.lbl_pyi_ver, self.pyi_ver_edit)
        self.form_ver.addRow(self.lbl_nuitka_ver, self.nuitka_ver_edit)
        c_lay_ver.addLayout(self.form_ver)

        lay_sub4.addWidget(self.card_opt)
        lay_sub4.addWidget(self.card_ver)
        lay_sub4.addStretch()

        self.card_map, c_lay_map = self._create_card(_("Package Name Mappings"))
        self.mapping_table = QTableWidget()
        self.mapping_table.setItemDelegate(TableItemDelegate(self.mapping_table))
        self.mapping_table.setColumnCount(2)
        self.mapping_table.setHorizontalHeaderLabels([_("Import Name"), _("PyPI Package Name")])
        
        self.mapping_table.verticalHeader().setVisible(False)
        
        self.mapping_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.mapping_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.mapping_table.setMinimumHeight(150)
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
        self.ver_comp = QLineEdit(_("My Studio"))
        self.ver_desc = QLineEdit(_("Python Executable"))
        
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
        
        self.btn_reset_config = QPushButton(_("Reset to Default Config"))
        self.btn_reset_config.setProperty("class", "ToolBtn")
        self.btn_reset_config.clicked.connect(self.reset_global_config)
        
        h_preset.addWidget(self.btn_exp_preset)
        h_preset.addWidget(self.btn_imp_preset)
        h_preset.addWidget(self.btn_reset_config)
        h_preset.addStretch()
        c_lay_meta.addLayout(h_preset)

        self.card1, lay1 = self._create_card(_("Output Location"))
        self.out_mode_combo = QComboBox()
        self.out_mode_combo.addItems([_("Source File Directory"), _("Custom Directory")])
        setup_combo_white_theme(self.out_mode_combo)
        self.out_mode_combo.currentIndexChanged.connect(self.on_out_mode_changed)
        
        self.sandbox_mode_combo = QComboBox()
        self.sandbox_mode_combo.addItems([
            _("Source Directory (.qpypack_build)"), 
            _("System Temp Directory")
        ])
        setup_combo_white_theme(self.sandbox_mode_combo)

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
        
        self.lbl_out_rule_title = QLabel(_("Output Location:"))
        self.lbl_target_out_title = QLabel(_("Target Directory:"))
        self.lbl_sandbox_title = QLabel(_("Temporary Directory:"))
        
        self.form_out.addRow(self.lbl_out_rule_title, self.out_mode_combo)
        self.form_out.addRow(self.lbl_target_out_title, self.out_dir_container)
        self.form_out.addRow(self.lbl_sandbox_title, self.sandbox_mode_combo)
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
        main_lay = self.lay_about
        # 缩小上下边距，节省垂直空间，避免出现滚动条
        main_lay.setContentsMargins(40, 10, 40, 10)
        main_lay.setSpacing(15)
        main_lay.addStretch(1)
        
        logo_lbl = QLabel()
        icon_path = get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            high_res_pixmap = QIcon(icon_path).pixmap(256, 256)
            if not high_res_pixmap.isNull():
                logo_pixmap = high_res_pixmap.scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                logo_lbl.setPixmap(logo_pixmap)
            else:
                logo_lbl.setPixmap(get_svg_pixmap('package', color="#1A73E8", size=96))
        else:
            logo_lbl.setPixmap(get_svg_pixmap('package', color="#1A73E8", size=96))
            
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_lay.addWidget(logo_lbl)
        
        # 顶部文字块布局
        text_vlay = QVBoxLayout()
        # 1. 缩小全局基础间距，让“标题”和“一句话标语”紧密贴合
        text_vlay.setSpacing(6)
        text_vlay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_lbl = QLabel(__app_name__)
        title_lbl.setStyleSheet("font-size: 32px; font-weight: 900; color: #202124; letter-spacing: -1px;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_vlay.addWidget(title_lbl)
        
        self.about_desc_lbl = QLabel(_("Modern Cross-Platform Python Packaging GUI Powered by PyInstaller & Nuitka"))
        self.about_desc_lbl.setStyleSheet("font-size: 14px; color: #3c4043;")
        self.about_desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_vlay.addWidget(self.about_desc_lbl)
        
        # 2. 在标语和版权之间额外插入一点空隙，巧妙地拉开层次感
        text_vlay.addSpacing(6)
        
        current_year = time.localtime().tm_year
        year_str = f"2024-{current_year}" if current_year > 2024 else "2024"
        ver_lbl = QLabel(f"Version {__version__}  ·  GPL-3.0  ·  Copyright © {year_str} {__author__}")
        ver_lbl.setStyleSheet("font-size: 12px; color: #8b929a; font-weight: bold;")
        ver_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_vlay.addWidget(ver_lbl)
        
        main_lay.addLayout(text_vlay)
        # 3. 将整个文字块与下方四个按钮的距离适当拉大，增加呼吸感
        main_lay.addSpacing(25)

        btn_lay = QHBoxLayout()
        btn_lay.setSpacing(12)
        btn_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        def create_link_btn(text, url, svg_path, icon_color, bg_color, hover_bg, pressed_bg):
            btn = QPushButton(" " + text)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            
            svg_str = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="{icon_color}" d="{svg_path}"/></svg>'
            renderer = QSvgRenderer()
            renderer.load(svg_str.encode('utf-8'))
            pixmap = QPixmap(48, 48)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            renderer.render(painter)
            painter.end()
            btn.setIcon(QIcon(pixmap))
            
            btn.setStyleSheet(f"""
                QPushButton {{ background-color: {bg_color}; color: #3c4043; border: none; border-radius: 8px; padding: 8px 16px; font-size: 13px; font-weight: bold; }}
                QPushButton:hover {{ background-color: {hover_bg}; color: {icon_color}; }}
                QPushButton:pressed {{ background-color: {pressed_bg}; }}
            """)
            btn.clicked.connect(lambda: __import__('webbrowser').open(url))
            return btn
            
        p_github = "M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.379.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.161 22 16.416 22 12c0-5.523-4.477-10-10-10z"
        p_issue = "M20 8h-2.81c-.45-.78-1.07-1.45-1.82-1.96L17 4.41 15.59 3l-2.17 2.17C12.96 5.06 12.49 5 12 5c-.49 0-.96.06-1.41.17L8.41 3 7 4.41l1.62 1.63C7.88 6.55 7.26 7.22 6.81 8H4v2h2.09c-.05.33-.09.66-.09 1v1H4v2h2v1c0 .34.04.67.09 1H4v2h2.81c1.04 1.79 2.97 3 5.19 3s4.15-1.21 5.19-3H20v-2h-2.09c.05-.33.09-.66.09-1v-1h2v-2h-2v-1c0-.34-.04-.67-.09-1H20V8zm-6 8h-4v-2h4v2zm0-4h-4v-2h4v2z"
        p_pypi = "M12.06,1.48c-3.14,0-3.52,0.67-3.52,0.67l-0.01,2.44h3.63v0.52H7.43C5.12,5.11,4.5,6.58,4.5,8.81c0,2.34,0.38,3.48,2.3,3.48 h1.14v-1.62c0-1.48,1.23-2.65,2.7-2.65h3.69c1.47,0,2.66-1.19,2.66-2.65V3.88C16.99,1.83,14.67,1.48,12.06,1.48z M10.22,2.83 c0.41,0,0.73,0.33,0.73,0.74c0,0.41-0.33,0.74-0.73,0.74C9.49,3.16,9.82,2.83,10.22,2.83z M16.71,9.89 v1.62c0,1.48-1.23,2.65-2.7,2.65H10.3c-1.47,0-2.66,1.19-2.66,2.65v1.49c0,2.05,2.32,2.41,4.92,2.41c3.14,0,3.52-0.67,3.52-0.67 l0.01-2.44h-3.63v-0.52h4.73c2.31,0,2.93-1.47,2.93-3.7c0-2.34-0.38-3.48-2.3-3.48H16.71z M13.88,18.96c0.41,0,0.73,0.33,0.73,0.74c0,0.41-0.33,0.74-0.73,0.74c-0.4,0-0.73-0.33-0.73-0.74C13.15,19.29,13.48,18.96,13.88,18.96z"
        p_heart = "M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"

        self.btn_github = create_link_btn(_("GitHub Repository"), "https://github.com/qwejay/QPyPack", p_github, "#24292e", "#f1f3f4", "#e8eaed", "#dadce0")
        self.btn_issue = create_link_btn(_("Issues & Feedback"), "https://github.com/qwejay/QPyPack/issues", p_issue, "#d93025", "#f1f3f4", "#e8eaed", "#dadce0")
        self.btn_pypi = create_link_btn(_("PyPI Home"), "https://pypi.org/project/qpypack/", p_pypi, "#1A73E8", "#f1f3f4", "#e8eaed", "#dadce0")
        
        self.btn_sponsor = create_link_btn(_("Sponsor"), "https://www.ifdian.net/a/qwejay", p_heart, "#d93025", "#fce8e6", "#fad2cf", "#f6aea9")
        self.btn_sponsor.setStyleSheet(self.btn_sponsor.styleSheet().replace("color: #3c4043;", "color: #d93025;"))
        
        btn_lay.addWidget(self.btn_github)
        btn_lay.addWidget(self.btn_issue)
        btn_lay.addWidget(self.btn_pypi)
        btn_lay.addWidget(self.btn_sponsor)
        
        main_lay.addLayout(btn_lay)
        main_lay.addSpacing(20)
        
        sponsor_vlay = QVBoxLayout()
        sponsor_vlay.setSpacing(12)
        
        self.sponsor_desc_p1 = QLabel(_("QPyPack is a free and open-source tool. If it has improved your efficiency or solved packaging problems, consider buying the author a coffee!"))
        self.sponsor_desc_p1.setWordWrap(True)
        self.sponsor_desc_p1.setStyleSheet("font-size: 12px; color: #5f6368;")
        self.sponsor_desc_p1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sponsor_vlay.addWidget(self.sponsor_desc_p1)
        
        self.sponsor_desc_p2 = QLabel(_("* Sponsorship is completely voluntary, serves as an unconditional encouragement to the open-source community, and involves no commercial commitments. Thank you for your support!"))
        self.sponsor_desc_p2.setWordWrap(True)
        self.sponsor_desc_p2.setStyleSheet("font-size: 11px; color: #9aa0a6;")
        self.sponsor_desc_p2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sponsor_vlay.addWidget(self.sponsor_desc_p2)
        
        main_lay.addLayout(sponsor_vlay)
        main_lay.addStretch(1)


    def retranslate_ui(self):
        self.tabs.setTabText(0, _("Build Settings"))
        self.tabs.setTabText(1, _("Preferences"))
        self.tabs.setTabText(2, _("About"))
        
        self.sub_tabs.setTabText(0, _("Engine"))
        self.sub_tabs.setTabText(1, _("Dependencies"))
        self.sub_tabs.setTabText(2, _("Resources"))
        self.sub_tabs.setTabText(3, _("Optimization"))
        self.sub_tabs.setTabText(4, _("Package Map"))
        
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
        self.lbl_lang_title.setText(_("UI Language:"))
        self.lbl_ver_title.setText(_("Version:"))
        self.lbl_company_title.setText(_("Author/Company:"))
        self.lbl_desc_title.setText(_("Description:"))
        self.lbl_out_rule_title.setText(_("Output Location:"))
        self.lbl_target_out_title.setText(_("Target Directory:"))
        self.lbl_sandbox_title.setText(_("Temporary Directory:"))
        self.sandbox_mode_combo.setItemText(0, _("Source Directory (.qpypack_build)"))
        self.sandbox_mode_combo.setItemText(1, _("System Temp Directory"))

        if hasattr(self, 'pip_source_combo') and hasattr(self, 'pip_backup_combo'):
            cur_main = self._get_url_from_combo(self.pip_source_combo)
            cur_back = self._get_url_from_combo(self.pip_backup_combo)

            self.pip_source_combo.blockSignals(True)
            self.pip_backup_combo.blockSignals(True)

            self.pip_source_combo.clear()
            self.pip_backup_combo.clear()

            for name, url in PYPI_MIRRORS_GLOBAL:
                display_text = f"{_(name)}: {url}"
                self.pip_source_combo.addItem(display_text, url)
                self.pip_backup_combo.addItem(display_text, url)

            self._set_combo_value(self.pip_source_combo, cur_main)
            self._set_combo_value(self.pip_backup_combo, cur_back)

            self.pip_source_combo.blockSignals(False)
            self.pip_backup_combo.blockSignals(False)

        self.btn_save.setText(_("Save & Return"))
        self.btn_python_path.setText(_("Browse"))
        self.btn_download_py.setText(_("View Python"))
        self.btn_download_py.setToolTip("")
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
        self.btn_reset_config.setText(_("Reset to Default Config"))
        
        self.python_path_combo.setPlaceholderText(_("Leave blank to auto-detect system default Python"))
        self.name_edit.setPlaceholderText(_("Leave blank to auto-match script name"))
        self.reqs_file_edit.setPlaceholderText(_("Leave blank to auto-search requirements.txt in current directory"))
        self.hidden_edit.setPlaceholderText(_("Comma separated (e.g. pandas, PyQt5)"))
        self.exclude_edit.setPlaceholderText(_("Comma separated (e.g. tkinter, matplotlib)"))
        self.upx_path_edit.setPlaceholderText(_("Leave blank to auto-detect from environment variables"))

        self.rb_onefile.setText(_("One-File Mode (--onefile)"))
        self.rb_onedir.setText(_("Folder Mode (--onedir)"))
        self.lbl_contents_dir.setText(_("Contents Directory (--contents-directory):"))
        self.contents_dir_edit.setPlaceholderText(_("Internal directory name for dependencies (default: _internal)"))
        self.noconsole_check.setText(_("Hide Console (--noconsole)"))
        self.venv_check.setText(_("Use Virtual Environment (Recommended)"))
        self.reqs_check.setText(_("Install requirements.txt"))
        self.pipreqs_check.setText(_("Analyze Dependencies (AST)"))
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
        self.about_desc_lbl.setText(_("Modern Cross-Platform Python Packaging GUI Powered by PyInstaller & Nuitka"))
        
        if hasattr(self, 'sponsor_desc_p1'):
            self.sponsor_desc_p1.setText(_("QPyPack is a free and open-source tool. If it has improved your efficiency or solved packaging problems, consider buying the author a coffee!"))
            self.sponsor_desc_p2.setText(_("* Sponsorship is completely voluntary, serves as an unconditional encouragement to the open-source community, and involves no commercial commitments. Thank you for your support!"))

        self.btn_reset.setToolTip(_("Reset to Default Config"))
        self.btn_back.setToolTip(_("Cancel & Return"))
        if hasattr(self, 'lbl_res_hint'):
            self.lbl_res_hint.setText(_("Project-specific. Not saved to global preferences. Use 'Export Preset' to save config."))
        self.add_data_list.setToolTip(_("Double-click to edit target path; Drag & drop supported. Use 'Export Preset' to save for reuse."))
        self.lite_mode_check.setToolTip(_("Dynamically exclude redundant dependencies in build environment, improving speed and reducing size."))
        
        if hasattr(self, 'btn_github'):
            self.btn_github.setText(" " + _("GitHub Repository"))
            self.btn_issue.setText(" " + _("Issues & Feedback"))
            self.btn_pypi.setText(" " + _("PyPI Home"))
            self.btn_sponsor.setText(" " + _("Sponsor"))
            
        self.on_engine_changed()
        self.on_python_path_changed()

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

        fm = self.python_path_combo.fontMetrics()
        max_width = 520
        for i in range(self.python_path_combo.count()):
            text_w = fm.horizontalAdvance(self.python_path_combo.itemText(i))
            if text_w > max_width:
                max_width = text_w
                
        if self.python_path_combo.view():
            self.python_path_combo.view().setMinimumWidth(max_width + 36)

        self.on_python_path_changed()

    def populate_mapping_table(self, mappings_dict):
        self.mapping_table.setRowCount(0)
        for imp_name, pypi_name in mappings_dict.items():
            row = self.mapping_table.rowCount()
            self.mapping_table.insertRow(row)
            self.mapping_table.setItem(row, 0, QTableWidgetItem(imp_name))
            self.mapping_table.setItem(row, 1, QTableWidgetItem(pypi_name))

    def add_mapping_item(self):
        dlg1 = CustomInputDialog(self, _("Add Mapping"), _("Import name (e.g. cv2):"))
        if dlg1.exec() != QDialog.DialogCode.Accepted: return
        imp_name = dlg1.get_text().strip()
        if not imp_name: return
        
        dlg2 = CustomInputDialog(self, _("Add Mapping"), _("PyPI package name for [{imp_name}]:", imp_name=imp_name), imp_name)
        if dlg2.exec() != QDialog.DialogCode.Accepted: return
        pypi_name = dlg2.get_text().strip()
        if not pypi_name: return
        
        row = self.mapping_table.rowCount()
        self.mapping_table.insertRow(row)
        self.mapping_table.setItem(row, 0, QTableWidgetItem(imp_name))
        self.mapping_table.setItem(row, 1, QTableWidgetItem(pypi_name))

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
                    "onefile": self.rb_onefile.isChecked(),
                    "contents_dir": self.contents_dir_edit.text().strip(),
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
                if "onefile" in data:
                    if data["onefile"]:
                        self.rb_onefile.setChecked(True)
                    else:
                        self.rb_onedir.setChecked(True)
                if "contents_dir" in data:
                    self.contents_dir_edit.setText(data["contents_dir"])
                self.on_mode_type_changed()
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
            is_onefile = s.getboolean('onefile', True)
            if is_onefile:
                self.rb_onefile.setChecked(True)
            else:
                self.rb_onedir.setChecked(True)
            self.contents_dir_edit.setText(s.get('contents_dir', '_internal'))
            self.on_mode_type_changed()
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
            self.sandbox_mode_combo.setCurrentIndex(int(s.get('temp_sandbox_mode', '0')))
            self.on_out_mode_changed(self.out_mode_combo.currentIndex())
            
            self.concise_log_check.setChecked(s.getboolean('concise_log', True))
            self.sound_notify_check.setChecked(s.getboolean('sound_notify', True))
            self.auto_save_log_check.setChecked(s.getboolean('auto_save_log', False))
            self.lite_mode_check.setChecked(s.getboolean('lite_mode', False))
            
            self.pyi_ver_edit.setText(s.get('pyi_version', '6.21.0'))
            self.nuitka_ver_edit.setText(s.get('nuitka_version', '4.1.3'))
            
            self.add_data_list.clear()

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
        s['onefile'] = str(self.rb_onefile.isChecked())
        s['contents_dir'] = self.contents_dir_edit.text().strip() or '_internal'
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
        s['temp_sandbox_mode'] = str(self.sandbox_mode_combo.currentIndex())
        s['concise_log'] = str(self.concise_log_check.isChecked())
        s['sound_notify'] = str(self.sound_notify_check.isChecked())
        s['auto_save_log'] = str(self.auto_save_log_check.isChecked())
        s['lite_mode'] = str(self.lite_mode_check.isChecked())
        
        s['pyi_version'] = self.pyi_ver_edit.text().strip()
        s['nuitka_version'] = self.nuitka_ver_edit.text().strip()
        
        s['add_data_list'] = ''

        config['Mappings'] = {}
        for r in range(self.mapping_table.rowCount()):
            k = self.mapping_table.item(r, 0).text().strip()
            v = self.mapping_table.item(r, 1).text().strip()
            if k and v: config['Mappings'][k] = v
        
        save_config(config)
        I18N.set_language(new_lang)

    def _check_pip_mirrors(self):
        sender = self.sender()
        src_url = self._get_url_from_combo(self.pip_source_combo)
        bak_url = self._get_url_from_combo(self.pip_backup_combo)
        
        if src_url and bak_url and src_url.rstrip('/') == bak_url.rstrip('/'):
            target_combo = self.pip_backup_combo if sender == self.pip_source_combo else self.pip_source_combo
            for i in range(target_combo.count()):
                item_url = target_combo.itemData(i) or target_combo.itemText(i)
                if item_url and item_url.rstrip('/') != src_url.rstrip('/'):
                    target_combo.blockSignals(True)
                    target_combo.setCurrentIndex(i)
                    target_combo.blockSignals(False)
                    break

    def on_engine_changed(self):
        engine = self.engine_combo.currentText()
        if engine == "PyInstaller":
            self.engine_desc_lbl.setText(_("PyInstaller — Bundles Python interpreter and bytecode. Fast build speed, zero configuration (no C compiler needed), and excellent compatibility."))
        else:
            self.engine_desc_lbl.setText(_("Nuitka — Compiles source code into native C/C++ binary. Produces smaller package size, faster execution, and deep anti-decompilation protection (requires C compiler)."))

        if getattr(self, 'upx_check', None) is not None and getattr(self, 'upx_path_container', None) is not None:
            self.upx_check.setVisible(True)
            self.upx_path_container.setVisible(self.upx_check.isChecked())

    def on_python_path_changed(self, text=""):
        raw_text = text or self.python_path_combo.currentText().strip()
        ver_match = re.search(r'Python\s+(\d+\.\d+)', raw_text, re.I)
        
        ver_str = ver_match.group(1) if ver_match else ""
        if not ver_str:
            m_path = re.search(r'python(\d)(\d+)', raw_text, re.I)
            if m_path: ver_str = f"{m_path.group(1)}.{m_path.group(2)}"

        self.python_desc_lbl.setStyleSheet("QLabel { background-color: #f8fafc; color: #334155; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px; font-size: 12px; line-height: 1.5; }")

        if ver_str:
            try:
                parts = [int(x) for x in ver_str.split('.')]
                major, minor = parts[0], parts[1]
                
                if (major, minor) <= (3, 8):
                    self.python_desc_lbl.setText(_('<div style="margin-bottom: 5px;"><b>Python {ver} Platform Matrix:</b></div><span style="color:#16a34a; font-weight:bold;">✔ Windows 7</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Windows 8 / 8.1</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Windows 10 / 11</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ macOS 10.9+</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Linux</span><br><span style="background-color:#f1f5f9; color:#475569; padding:1px 5px; border-radius:3px; font-weight:bold; font-size:10px;">Legacy OS</span> <span style="color:#6b7280; font-size:11px;">Full backward compatibility</span>', ver=ver_str))
                elif (major, minor) <= (3, 10):
                    self.python_desc_lbl.setText(_('<div style="margin-bottom: 5px;"><b>Python {ver} Platform Matrix:</b></div><span style="color:#dc2626; font-weight:bold;">✖ Windows 7</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Windows 8.1</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Windows 10 / 11</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ macOS 10.9+</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Linux</span>', ver=ver_str))
                else:
                    self.python_desc_lbl.setText(_('<div style="margin-bottom: 5px;"><b>Python {ver} Platform Matrix:</b></div><span style="color:#dc2626; font-weight:bold;">✖ Windows 7</span> &nbsp;&nbsp; <span style="color:#dc2626; font-weight:bold;">✖ Windows 8 / 8.1</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Windows 10 / 11</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ macOS 10.13+</span> &nbsp;&nbsp; <span style="color:#16a34a; font-weight:bold;">✔ Linux</span><br><span style="background-color:#dcfce7; color:#15803d; padding:1px 5px; border-radius:3px; font-weight:bold; font-size:10px;">Nuitka</span> <span style="color:#16a34a; font-size:11px;">Auto-detecting and managing C backend compiler</span>', ver=ver_str))
                return
            except Exception:
                pass

        self.python_desc_lbl.setText(_('<div style="margin-bottom: 5px;"><b>Python Interpreter</b></div><span style="color:#6b7280;">Auto-detecting system environment for Windows, macOS & Linux...</span>'))

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

    def on_download_python_clicked(self):
        if hasattr(self, 'parent_win') and hasattr(self.parent_win, "_trigger_python_download_dialog"):
            self.parent_win._trigger_python_download_dialog(is_missing_mode=False)

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
            hidden = extract_project_imports_via_ast(Path(script_path), False)
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
        
        dlg = CustomInputDialog(self, _("Edit Path"), _("Target relative path:"), text=dst)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            new_dst = dlg.get_text().strip().replace('\\', '/')
            if not new_dst: new_dst = "."
            item.setData(Qt.ItemDataRole.UserRole, (r_type, src, new_dst))
            tag = _("File") if r_type == 'file' else _("Directory")
            item.setText(f"[{tag}] {src}  ->  {new_dst}")

    def del_resource(self):
        for item in self.add_data_list.selectedItems():
            self.add_data_list.takeItem(self.add_data_list.row(item))

    def clear_resource(self):
        self.add_data_list.clear()

    def reset_global_config(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(_("Reset to Default Config"))
        msg_box.setText(_(
            "<b>Are you sure you want to reset all preferences?</b><br>"
            "<span style='color:#64748b; font-size:12px;'>"
            "All settings will be restored to default state."
            "</span>"
        ))
        msg_box.setIcon(QMessageBox.Icon.Warning)

        btn_confirm = msg_box.addButton(_("Reset"), QMessageBox.ButtonRole.AcceptRole)
        btn_cancel = msg_box.addButton(_("Cancel"), QMessageBox.ButtonRole.RejectRole)

        msg_box.setStyleSheet("""
            QMessageBox { background-color: #ffffff; }
            QLabel { color: #111827; font-size: 13px; line-height: 1.4; }
            QPushButton {
                background-color: #f1f5f9; color: #475569; border: 1px solid #cbd5e1;
                border-radius: 6px; font-size: 12px; font-weight: bold;
                padding: 6px 16px; min-width: 70px;
            }
            QPushButton:hover { background-color: #e2e8f0; }
        """)
        btn_confirm.setStyleSheet("""
            QPushButton {
                background-color: #D93025; color: #ffffff; border: none;
                border-radius: 6px; font-size: 12px; font-weight: bold;
                padding: 6px 16px; min-width: 70px;
            }
            QPushButton:hover { background-color: #C5221F; }
            QPushButton:pressed { background-color: #A50E0E; }
        """)

        msg_box.exec()

        if msg_box.clickedButton() == btn_confirm:
            if os.path.exists(CONFIG_FILE):
                try:
                    os.remove(CONFIG_FILE)
                except Exception:
                    pass

            load_config()
            self.load_from_config()

            if hasattr(self.parent_win, "show_notification"):
                self.parent_win.show_notification(_("Global configuration has been reset."))

class ScriptAnalysisThread(QThread):
    analysis_done = Signal(str, str, str, str, set)

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        if self.isInterruptionRequested(): return
        
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

        if self.isInterruptionRequested(): return

        try:
            script_imports = extract_project_imports_via_ast(Path(self.path), False)
        except: pass

        if self.isInterruptionRequested(): return

        self.analysis_done.emit(app_name, version, author, desc, script_imports)

class PackingThread(QThread):
    progress = Signal(str)
    build_finished = Signal(bool, str, list)

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
        
        clean_env = os.environ.copy()
        clean_env.pop("PYTHONHOME", None)
        clean_env.pop("PYTHONPATH", None)
        clean_env["PYTHONUTF8"] = "1"
        clean_env["PYTHONIOENCODING"] = "utf-8"
        clean_env["LANG"] = "en_US.UTF-8"
        clean_env["LC_ALL"] = "en_US.UTF-8"
        clean_env["PYTHONUNBUFFERED"] = "1"
        clean_env["PLAYWRIGHT_BROWSERS_PATH"] = "0"

        primary_idx = self.params.get('pip_index_url', '')
        if any(domain in primary_idx for domain in ['tsinghua', 'aliyun', 'tencent', 'huawei', 'ustc']) or I18N.current_lang == 'zh_CN':
            clean_env["PLAYWRIGHT_DOWNLOAD_HOST"] = "https://npmmirror.com/mirrors/playwright/" 

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
            
            for line in self.process.stdout:
                if self._is_cancelled:
                    try:
                        if self.process:
                            self.process.terminate()
                    except Exception:
                        pass
                    return False
                
                stripped = line.rstrip('\r\n')
                self.all_raw_logs.append(stripped)
                
                buffer.append(stripped)
                if len(buffer) >= 15 or (time.time() - last_emit) > 0.1:
                    self.progress.emit('\n'.join(buffer))
                    buffer.clear()
                    last_emit = time.time()
            
            if buffer: self.progress.emit('\n'.join(buffer))
            self.process.wait()
            
            if is_timeout[0]:
                self.progress.emit(_("[WARN] Command timeout (>{timeout}s)", timeout=timeout))
                return False
                
            return self.process.returncode == 0
        except FileNotFoundError as e:
            self.progress.emit(_("[ERROR] Process error: command or binary missing ({error})", error=str(e)))
            return False
        except Exception as e:
            self.progress.emit(_("[ERROR] System execution exception: {error}", error=str(e)))
            return False
        finally:
            if timer: timer.cancel()
            if self.process and self.process.stdout:
                try:
                    self.process.stdout.close()
                except Exception:
                    pass

    def run_pip_install(self, python_exe, pkgs_or_args):
        primary_idx = self.params.get('pip_index_url', '').strip()
        backup_idx = self.params.get('pip_index_backup', '').strip()

        pip_args = [
            "--default-timeout=120", 
            "--disable-pip-version-check", 
            "--prefer-binary"
        ]
        if primary_idx: pip_args.extend(["-i", primary_idx])
        if backup_idx and backup_idx != primary_idx: pip_args.extend(["--extra-index-url", backup_idx])

        cmd = [python_exe, "-m", "pip", "install"] + pkgs_or_args + pip_args
        success = self.run_cmd(cmd)

        if not success and backup_idx and backup_idx != primary_idx:
            self.progress.emit(_("[INFO] Switching to backup PyPI source for retrieval: {url}", url=backup_idx))
            fallback_cmd = [python_exe, "-m", "pip", "install"] + pkgs_or_args + ["-i", backup_idx, "--disable-pip-version-check", "--prefer-binary"]
            success = self.run_cmd(fallback_cmd)

        return success

    def sanitize_script(self, orig_path: Path):
        if is_cloud_locked(orig_path):
            return None, False, _("[ERROR] Target file is locked or encrypted by cloud drive. Please decrypt and try again.")
        
        if not self.params['noconsole']:
            try:
                raw = orig_path.read_bytes()
                try: code = raw.decode('utf-8-sig')
                except: code = raw.decode(locale.getpreferredencoding(), errors='ignore')
                
                pause_prompt_str = _("\\nProgram execution completed, press Enter to exit...").replace('\\n', '\n')
                
                pause_code = (
                    "# --- QPyPack Auto-injected Console Pause ---\n"
                    "import atexit\n"
                    "def _qpypack_pause():\n"
                    "    try:\n"
                    "        import sys\n"
                    "        if sys.platform == 'win32':\n"
                    "            import ctypes\n"
                    "            if ctypes.windll.kernel32.GetConsoleProcessList((ctypes.c_uint * 10)(), 10) <= 2:\n"
                    f"                input({repr(pause_prompt_str)})\n"
                    "    except:\n"
                    "        pass\n"
                    "atexit.register(_qpypack_pause)\n"
                    "# -------------------------------------------\n\n"
                )
                
                temp_file = orig_path.parent / f"_qpypack_temp_{orig_path.name}"
                try:
                    temp_file.write_text(pause_code + code, encoding='utf-8')
                except PermissionError:
                    temp_file = Path(tempfile.gettempdir()) / f"_qpypack_temp_{orig_path.name}"
                    temp_file.write_text(pause_code + code, encoding='utf-8')
                    os.environ["PYTHONPATH"] = orig_path.parent.as_posix() + os.pathsep + os.environ.get("PYTHONPATH", "")
                    
                return temp_file, True, ""
            except Exception as e:
                self.progress.emit(_("[WARN] Pause code injection exception: {error}", error=str(e)))
                
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
            line_no = _("Unknown")
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
        app_name = self.params.get('app_name', 'app').strip() or 'app'
        pip_idx = self.params.get('pip_index_url', '').strip()
        pip_backup = self.params.get('pip_index_backup', '').strip()
        is_temp = False
        build_script_path = None
        ext = ".exe" if os.name == "nt" else ""
        failed_packages = []

        try:
            if self._is_cancelled:
                return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])

            self.progress.emit(_("[INFO] Analyzing source code and project dependencies..."))
            script_path = Path(self.params['script_path']).resolve()
            script_dir = script_path.parent

            try:
                compile(script_path.read_bytes(), script_path.name, 'exec')
            except SyntaxError as e:
                err_type = type(e).__name__
                msg = _(
                    "[Syntax Error] Source code syntax parsing failed, build aborted:\n"
                    "  - File: {file}\n"
                    "  - Line: Line {line}\n"
                    "  - Detail: {desc}\n\n"
                    "💡 Tip: This is usually NOT a fault of the packaging tool.\n"
                    "Please ensure the [Build Python Version] you selected matches the version you used to [Write/Test the Code].\n"
                    "Using newer syntax (e.g., walrus operator :=, type unions |, match-case) in an older Python environment will trigger this error.\n"
                    "We recommend going to [Build Settings] -> [Engine] to switch to the correct Python version.", 
                    file=script_path.name, type=err_type, line=e.lineno or _("Unknown"), desc=e.msg or _("Invalid syntax")
                )
                return self.build_finished.emit(False, msg, [])

            if self._is_cancelled:
                return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])

            self.progress.emit(_("[INFO] Performing pre-flight environment checks..."))
            
            out_mode = int(self.params.get('out_mode', 0) or 0)
            custom_out = (self.params.get('custom_out_dir') or '').strip()
            target_out_dir = Path(custom_out) if (out_mode == 1 and custom_out) else script_dir
            try:
                target_out_dir.mkdir(parents=True, exist_ok=True)
                test_file = target_out_dir / ".qpypack_write_test"
                test_file.write_text("test")
                test_file.unlink()
            except Exception as e:
                return self.build_finished.emit(False, _("[ERROR] Output directory is missing write permissions: {error}", error=str(e)), [])

            if self.params.get('use_reqs'):
                custom_reqs = (self.params.get('reqs_file') or '').strip()
                if custom_reqs and not Path(custom_reqs).exists():
                    return self.build_finished.emit(False, _("[ERROR] Requirements file not found: {path}", path=custom_reqs), [])

            for r_type, src, dst in (self.params.get('add_data_list') or []):
                if not Path(src).exists():
                    return self.build_finished.emit(False, _("[ERROR] Additional resource file/directory not found: {path}", path=src), [])

            free_disk = get_free_disk_gb(script_dir.as_posix())
            if free_disk < 0.5:
                return self.build_finished.emit(False, _("[ERROR] Insufficient disk space (Available: {free:.1f} GB). At least 0.5 GB is required to safely initialize the build environment.", free=free_disk), [])

            system_python_exe = self.params.get('python_exe')
            if not system_python_exe:
                return self.build_finished.emit(False, _("[ERROR] Python interpreter is invalid or not found: {path}", path="None"), [])

            if is_cloud_sync_path(script_dir):
                self.progress.emit(_("[WARN] Target project is in a Cloud Sync directory (e.g. OneDrive/Dropbox). Cloud sync may temporarily lock build files."))

            build_script_path, is_temp, err_msg = self.sanitize_script(script_path)
            if not build_script_path and err_msg: 
                return self.build_finished.emit(False, _("[ERROR] I/O Exception: {err_msg}", err_msg=err_msg), [])

            script_posix = build_script_path.as_posix()
            script_imports = set()
            try:
                script_imports = extract_project_imports_via_ast(Path(script_posix), False)
            except Exception as e:
                self.progress.emit(_("[WARN] AST Analysis Exception: {error}", error=str(e)))

            known_mappings = self.params.get('mappings', DEFAULT_MAPPINGS.copy())
            known_mappings_lower = {k.lower(): v for k, v in known_mappings.items()}

            def get_canonical_pypi_name(raw_name):
                clean = raw_name.strip().lower().replace('_', '-')
                return known_mappings_lower.get(clean, clean).lower()

            target_std_libs = set(STD_LIBS)
            try:
                cmd_std = [system_python_exe, "-c", "import sys; print(','.join(getattr(sys, 'stdlib_module_names', [])))"]
                kw = {"capture_output": True, "text": True, "timeout": 3, "errors": "ignore"}
                if os.name == 'nt': kw["creationflags"] = subprocess.CREATE_NO_WINDOW
                res = subprocess.run(cmd_std, **kw)
                if res.returncode == 0 and res.stdout.strip():
                    target_std_libs.update(res.stdout.strip().split(','))
            except Exception:
                pass

            def parse_req_line(line):
                line = line.strip()
                if not line or line.startswith('#') or line.startswith('-'):
                    return None, None
                m = re.match(r'^([a-zA-Z0-9_\-\.]+)(.*)$', line)
                if m:
                    pkg_raw = m.group(1)
                    canon_name = get_canonical_pypi_name(pkg_raw)
                    if canon_name.lower() in target_std_libs:
                        return None, None
                    if canon_name.lower() != pkg_raw.lower():
                        full_spec = canon_name
                    else:
                        full_spec = line
                    return canon_name, full_spec
                return None, None

            final_dependencies = {}
            reqs_declared_pkgs = set()
            auto_detected_pkgs = set()
            auto_added_supplements = set()

            if self.params.get('use_reqs'):
                custom_reqs = self.params.get('reqs_file', '').strip()
                req_file = Path(custom_reqs) if (custom_reqs and Path(custom_reqs).exists()) else (script_dir / "requirements.txt")
                if req_file.exists():
                    try:
                        if is_cloud_locked(req_file): raise ValueError("Requirements file is locked")
                        raw_req = req_file.read_bytes()
                        try: req_content = raw_req.decode('utf-8-sig')
                        except: req_content = raw_req.decode(locale.getpreferredencoding(), errors='ignore')
                        
                        for line in req_content.splitlines():
                            canon_name, full_spec = parse_req_line(line)
                            if canon_name and canon_name.lower() not in target_std_libs:
                                final_dependencies[canon_name] = full_spec
                                reqs_declared_pkgs.add(canon_name)
                    except Exception as e:
                        self.progress.emit(_("[WARN] Read requirements.txt warning: {error}", error=str(e)))

            local_modules = {p.stem.lower() for p in script_dir.iterdir() 
                             if (p.is_file() and p.suffix.lower() in ('.py', '.pyw', '.pyd', '.so')) or (p.is_dir() and (p / '__init__.py').exists())}

            for m in script_imports:
                if m.lower() in target_std_libs or m.lower() in local_modules: continue
                canon_name = get_canonical_pypi_name(m)
                if canon_name.lower() in target_std_libs: continue
                auto_detected_pkgs.add(canon_name)
                if canon_name not in final_dependencies:
                    final_dependencies[canon_name] = canon_name
                    auto_added_supplements.add(canon_name)

            if self._is_cancelled:
                return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])

            self.progress.emit(_("[INFO] Initializing isolated build environment..."))
            self.progress.emit(_("[INFO] Python interpreter path: {path}", path=system_python_exe))

            if self.params['use_venv']:
                if self._is_cancelled:
                    return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])
                self.progress.emit(_("[INFO] Creating virtual environment..."))
                self.venv_dir = Path(tempfile.mkdtemp(prefix="qpypack_env_")).resolve()
                if not self.run_cmd([system_python_exe, "-m", "venv", self.venv_dir.as_posix()]):
                    if self._is_cancelled:
                        return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])
                    return self.build_finished.emit(False, _("[ERROR] Failed to create virtual environment. Current Python environment might be missing necessary modules or have restricted permissions."), [])
                python_exe = (self.venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")).as_posix()
                
                if self._is_cancelled:
                    return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])
                self.progress.emit(_("[INFO] Synchronizing and upgrading pip package manager..."))
                self.run_pip_install(python_exe, ["--upgrade", "pip", "-q"])
            else: 
                python_exe = system_python_exe

            if self._is_cancelled:
                return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])

            if self.params.get('use_pipreqs'):
                self.progress.emit(_("[INFO] Scanning project source code via AST engine..."))
                
                scan_dir_mode = self.params.get('use_pipreqs_dir', False)
                scan_target = script_dir if scan_dir_mode else build_script_path
                
                ast_discovered_imports = extract_project_imports_via_ast(scan_target, scan_dir=scan_dir_mode)
                env_pkg_map = query_target_env_packages(system_python_exe)
                
                for m in ast_discovered_imports:
                    if m.lower() in target_std_libs or m.lower() in local_modules:
                        continue
                    canon_name = env_pkg_map.get(m) or get_canonical_pypi_name(m)
                    if canon_name.lower() not in target_std_libs:
                        auto_detected_pkgs.add(canon_name)
                        if canon_name not in final_dependencies:
                            final_dependencies[canon_name] = canon_name
                            auto_added_supplements.add(canon_name)

            engine_pkg = "pyinstaller" if engine == "PyInstaller" else "nuitka"
            if engine == "PyInstaller" and self.params.get('pyi_version'):
                engine_pkg = f"pyinstaller=={self.params['pyi_version']}"
            elif engine == "Nuitka" and self.params.get('nuitka_version'):
                engine_pkg = f"nuitka=={self.params['nuitka_version']}"
            
            engine_pkgs = [engine_pkg]
            if engine == "PyInstaller": 
                engine_pkgs.append("pillow")
                engine_pkgs.append("pyinstaller-hooks-contrib")
            elif engine == "Nuitka":
                engine_pkgs.append("zstandard")

            self.progress.emit(_("[INFO] Resolving project dependencies..."))
            if reqs_declared_pkgs:
                self.progress.emit("  • " + _("Declared in requirements.txt ({count}): {pkgs}", count=len(reqs_declared_pkgs), pkgs=', '.join(sorted(reqs_declared_pkgs))))
            else:
                self.progress.emit("  • " + _("Declared in requirements.txt: None"))
                
            self.progress.emit("  • " + _("Discovered via scanner ({count}): {pkgs}", count=len(auto_detected_pkgs), pkgs=', '.join(sorted(auto_detected_pkgs))))
            
            if auto_added_supplements:
                self.progress.emit("  • " + _("Auto-patched missing ({count}): {pkgs}", count=len(auto_added_supplements), pkgs=', '.join(sorted(auto_added_supplements))))
            else:
                self.progress.emit("  • " + _("Manifest complete (No missing packages)"))

            self.progress.emit("  • " + _("Build engine packages ({count}): {pkgs}", count=len(engine_pkgs), pkgs=', '.join(sorted(engine_pkgs))))

            final_install_dict = {}
            for spec in engine_pkgs + list(final_dependencies.values()):
                m = re.match(r'^([a-zA-Z0-9_\-\.]+)(.*)$', spec.strip())
                if m:
                    base_name = m.group(1).lower()
                    has_ver = bool(m.group(2).strip())
                    if base_name in final_install_dict:
                        existing_has_ver = bool(re.match(r'^[a-zA-Z0-9_\-\.]+[=><!~]', final_install_dict[base_name]))
                        if existing_has_ver and not has_ver:
                            continue
                    final_install_dict[base_name] = spec

            dedup_install_list = [pkg for pkg in list(final_install_dict.values()) if re.split(r'[=><!~]', pkg)[0].strip().lower() not in target_std_libs]

            temp_unified_reqs = Path(tempfile.gettempdir()) / f"qpypack_atomic_reqs_{int(time.time())}.txt"
            temp_unified_reqs.write_text('\n'.join(dedup_install_list), encoding='utf-8')

            total_pkgs = len(dedup_install_list)
            pkg_names_str = ', '.join(sorted(dedup_install_list))
            
            self.progress.emit(_("[INFO] Installing build environment and project dependencies ({count} packages): {pkgs}", count=total_pkgs, pkgs=pkg_names_str))

            if self._is_cancelled:
                temp_unified_reqs.unlink(missing_ok=True)
                return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])

            if not self.run_pip_install(python_exe, ["-q", "-r", temp_unified_reqs.as_posix()]):
                if self._is_cancelled:
                    temp_unified_reqs.unlink(missing_ok=True)
                    return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])

                self.progress.emit(_("[WARN] Specified versions failed to install. Stripping version constraints for automatic compatibility match..."))
                
                flex_install_list = [re.split(r'[=><!~]', pkg)[0].strip() for pkg in dedup_install_list]
                
                installed_any = False
                for pkg in flex_install_list:
                    if self._is_cancelled:
                        temp_unified_reqs.unlink(missing_ok=True)
                        return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])

                    if pkg.lower() in target_std_libs:
                        continue

                    if self.run_pip_install(python_exe, ["-q", pkg]):
                        installed_any = True
                    else:
                        if self._is_cancelled:
                            temp_unified_reqs.unlink(missing_ok=True)
                            return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])
                        self.progress.emit(_("[WARN] Package '{pkg}' failed to install, skipping...", pkg=pkg))
                        failed_packages.append(pkg)
                
                if installed_any:
                    self.progress.emit(_("[INFO] Successfully installed compatible versions."))
                else:
                    self.progress.emit(_("[WARN] Some dependencies failed to install, build will proceed with risk..."))

            temp_unified_reqs.unlink(missing_ok=True)
            
            if self._is_cancelled:
                return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])

            has_playwright_pkg = any(re.match(r'^playwright([=><!~]|$)', pkg.lower()) for pkg in dedup_install_list)
            if has_playwright_pkg:
                self.progress.emit(_("[INFO] Playwright detected. Installing built-in browsers (PLAYWRIGHT_BROWSERS_PATH=0)..."))
                
                pw_mirrors = [
                    "https://npmmirror.com/mirrors/playwright/",
                    "https://cdn.npmmirror.com/binaries/playwright/",
                    "https://mirrors.huaweicloud.com/playwright/",
                    ""
                ] if (I18N.current_lang == 'zh_CN' or any(d in pip_idx for d in ['tsinghua', 'aliyun', 'tencent', 'huawei', 'ustc'])) else [""]

                success_pw = False
                for mirror in pw_mirrors:
                    if self._is_cancelled: break
                    if mirror:
                        os.environ["PLAYWRIGHT_DOWNLOAD_HOST"] = mirror
                        self.progress.emit(_("[INFO] Downloading Playwright browsers via mirror: {url}", url=mirror))
                    else:
                        os.environ.pop("PLAYWRIGHT_DOWNLOAD_HOST", None)
                        self.progress.emit(_("[INFO] Retrying Playwright browser download via official CDN..."))

                    if self.run_cmd([python_exe, "-m", "playwright", "install"], timeout=300, silent_error=True):
                        success_pw = True
                        break

                if not success_pw and not self._is_cancelled:
                    self.progress.emit(_("[WARN] Playwright browser installation failed across all sources, build will proceed with risk..."))

            if self._is_cancelled: 
                return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])

            self.progress.emit(_("[INFO] Starting {engine} engine to compile binary files...", engine=engine))
            
            if engine == "PyInstaller" and os.name == "nt":
                if 'multiprocessing' in {m.lower() for m in script_imports}:
                    self.progress.emit(_("[WARN] 'multiprocessing' module detected. Ensure 'multiprocessing.freeze_support()' is called under 'if __name__ == \"__main__\":' to prevent infinite process loops (fork bombs)."))

            if engine == "PyInstaller" and self.params['onefile']:
                try:
                    code_text = script_path.read_text(encoding='utf-8', errors='ignore')
                    if '__file__' in code_text and 'sys._MEIPASS' not in code_text:
                        self.progress.emit(_("[WARN] Usage of '__file__' detected. In PyInstaller One-File mode, use 'sys._MEIPASS' to reliably locate bundled resource files!"))
                except: pass

            cmd = []
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
                
                if self.params['onefile']: 
                    cmd.append("--onefile")
                else: 
                    cmd.append("--onedir")
                    contents_dir = (self.params.get('contents_dir') or '_internal').strip()
                    if contents_dir:
                        cmd.append(f"--contents-directory={contents_dir}")
                
                if self.params['noconsole']: 
                    cmd.append("--noconsole")
                else: 
                    cmd.append("--console")

                if icon_path: 
                    cmd.extend(["--icon", icon_path])
                    cmd.extend(["--add-data", f"{icon_path}{os.pathsep}."])
                    
                if self.params.get('version_file') and os.name == "nt": 
                    cmd.extend(["--version-file", self.params['version_file']])
                elif sys.platform == "darwin":
                    raw_comp = re.sub(r'[^a-zA-Z0-9]', '', self.params.get('ver_comp', 'mycompany')).lower() or 'anonymous'
                    raw_app = re.sub(r'[^a-zA-Z0-9]', '', app_name).lower() or 'app'
                    bundle_id = f"com.{raw_comp}.{raw_app}"
                    cmd.extend(["--osx-bundle-identifier", bundle_id])
                    
                if self.params.get('upx'):
                    upx_dir_custom = (self.params.get('upx_path') or '').strip()
                    if upx_dir_custom and Path(upx_dir_custom).exists():
                        cmd.append(f"--upx-dir={upx_dir_custom}")
                    else:
                        upx_dir_default = (Path.cwd() / "upx").resolve()
                        if upx_dir_default.exists(): cmd.append(f"--upx-dir={upx_dir_default.as_posix()}")
                    if os.name == "nt":
                        cmd.extend([
                            "--upx-exclude=python3.dll",
                            "--upx-exclude=vcruntime140.dll",
                            "--upx-exclude=vcruntime140_1.dll",
                        ])
                        try:
                            kw = {"capture_output": True, "text": True, "timeout": 3, "errors": "ignore"}
                            if os.name == 'nt': kw["creationflags"] = subprocess.CREATE_NO_WINDOW
                            res = subprocess.run([python_exe, "-c", 
                                "import sys; print(f'python{sys.version_info.major}{sys.version_info.minor}.dll')"], **kw)
                            if res.returncode == 0 and res.stdout.strip():
                                cmd.append(f"--upx-exclude={res.stdout.strip()}")
                        except:
                            for v in ("38", "39", "310", "311", "312", "313", "314"):
                                cmd.append(f"--upx-exclude=python{v}.dll")
                else:
                    cmd.append("--noupx")
                
                for imp in (self.params.get('hidden_imports') or '').split(','):
                    if imp.strip(): cmd.extend(["--hidden-import", imp.strip()])
                
                for r_type, src, dst in (self.params.get('add_data_list') or []):
                    cmd.extend(["--add-data", f"{src}{os.pathsep}{dst}"])
                
                for excl in (self.params.get('exclude_modules') or '').split(','):
                    if excl.strip(): cmd.extend(["--exclude-module", excl.strip()])
                
                imports_lower = {m.lower() for m in script_imports}
                hidden_list = [i.strip().lower() for i in (self.params.get('hidden_imports') or '').split(',') if i.strip()]
                all_imports_lower = imports_lower | set(hidden_list)

                if 'ttkbootstrap' in all_imports_lower: cmd.extend(["--collect-all", "ttkbootstrap"])
                if 'customtkinter' in all_imports_lower: cmd.extend(["--collect-all", "customtkinter"])
                if 'playwright' in all_imports_lower or has_playwright_pkg: cmd.extend(["--collect-all", "playwright"])
                if 'moviepy' in all_imports_lower: cmd.extend(["--collect-data", "moviepy"])
                if 'gradio' in all_imports_lower: cmd.extend(["--collect-all", "gradio"])
                if 'pydantic' in all_imports_lower: cmd.extend(["--collect-submodules", "pydantic"])
                if 'matplotlib' in all_imports_lower or 'seaborn' in all_imports_lower: 
                    cmd.extend(["--collect-data", "matplotlib"])

                if any(lib in all_imports_lower for lib in ('requests', 'httpx', 'urllib3', 'aiohttp')):
                    cmd.extend(["--collect-data", "certifi"])
                    self.progress.emit(_("[WARN] Detected 'requests' or 'httpx'. Auto-bundling 'certifi' certificates to prevent SSL errors."))
                
                for web_fw in ('fastapi', 'uvicorn', 'flask', 'streamlit', 'pywebio', 'dash'):
                    if web_fw in all_imports_lower:
                        cmd.extend(["--collect-all", web_fw])

            elif engine == "Nuitka":
                sandbox_mode = int(self.params.get('temp_sandbox_mode', 0) or 0)
                if sandbox_mode == 1:
                    self.temp_out_dir = Path(tempfile.mkdtemp(prefix="qpypack_nuitka_")).resolve()
                else:
                    self.temp_out_dir = (script_dir / ".qpypack_build").resolve()
                    self.temp_out_dir.mkdir(parents=True, exist_ok=True)
                
                cmd = [
                    python_exe, "-m", "nuitka", "--remove-output", "--assume-yes-for-downloads",
                    f"--output-dir={self.temp_out_dir.as_posix()}", 
                    f"--output-filename={app_name}{ext}"
                ]

                if self.params.get('auto_save_log'):
                    report_file = self.temp_out_dir / f"{app_name}_nuitka_report.xml"
                    cmd.append(f"--report={report_file.as_posix()}")
                
                if os.name == "nt":
                    has_msvc = shutil.which('cl.exe') is not None
                    if not has_msvc:
                        vswhere = Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")) / "Microsoft Visual Studio/Installer/vswhere.exe"
                        if vswhere.exists():
                            try:
                                res = subprocess.run([vswhere.as_posix(), "-latest", "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64"], capture_output=True, text=True, errors="ignore", creationflags=subprocess.CREATE_NO_WINDOW)
                                if res.stdout.strip(): has_msvc = True
                            except: pass

                    has_clang = (shutil.which('clang.exe') is not None) or (shutil.which('clang-cl.exe') is not None)
                    if not has_clang:
                        llvm_paths = [
                            Path(os.environ.get("ProgramFiles", "C:\\Program Files")) / "LLVM/bin/clang.exe",
                            Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")) / "LLVM/bin/clang.exe"
                        ]
                        if any(p.exists() for p in llvm_paths):
                            has_clang = True

                    py_ver_num = (3, 12)
                    try:
                        kw = {"capture_output": True, "text": True, "timeout": 2, "errors": "ignore"}
                        if os.name == 'nt': kw["creationflags"] = subprocess.CREATE_NO_WINDOW
                        check_ver = subprocess.run([python_exe, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"], **kw)
                        ver_str = check_ver.stdout.strip()
                        if ver_str:
                            parts = ver_str.split('.')
                            py_ver_num = (int(parts[0]), int(parts[1]))
                    except: pass

                    if has_msvc:
                        cmd.append("--msvc=latest")
                        self.progress.emit(_("[INFO] Found local MSVC environment, prioritizing native C++ compiler."))
                    elif has_clang:
                        cmd.append("--clang")
                        self.progress.emit(_("[INFO] Found local Clang environment, prioritizing LLVM Clang compiler."))
                    elif py_ver_num >= (3, 13):
                        cmd.append("--zig")
                        self.progress.emit(_("[INFO] Python 3.13+ detected: Using Zig compiler (--zig) as C backend."))
                    else:
                        cmd.append("--mingw64")
                        self.progress.emit(_("[INFO] Using MinGW64 compiler."))

                free_disk = get_free_disk_gb(script_dir.as_posix())
                if free_disk < 3.0:
                    self.progress.emit(_("[WARN] Low disk space detected on build target drive (Available: {free:.1f} GB, >= 5.0 GB recommended). Build process may interrupt due to disk exhaustion.", free=free_disk))

                cores = self.params.get('cpu_cores', os.cpu_count() or 2)
                free_ram = get_free_ram_gb()
                if free_ram < 4.0 and cores > 2:
                    safe_jobs = max(1, min(cores, int(free_ram / 1.5)))
                    self.progress.emit(_("[INFO] Evaluating system physical memory (Available: {ram:.1f} GB). Adaptive concurrency adjusted: {cores} -> {safe_jobs} ...", ram=free_ram, cores=cores, safe_jobs=safe_jobs))
                    cores = safe_jobs
                    cmd.append("--low-memory")
                cmd.append(f"--jobs={cores}")

                if self.params.get('upx'):
                    cmd.append("--enable-plugin=upx")
                    upx_dir_custom = (self.params.get('upx_path') or '').strip()
                    if upx_dir_custom and Path(upx_dir_custom).exists():
                        upx_exe = Path(upx_dir_custom) / ("upx.exe" if os.name == "nt" else "upx")
                        if upx_exe.exists():
                            cmd.append(f"--upx-binary={upx_exe.as_posix()}")
                        else:
                            cmd.append(f"--upx-binary={upx_dir_custom}")
                
                if self.params['noconsole']:
                    if os.name == "nt":
                        cmd.append("--windows-console-mode=disable")
                    if sys.platform == "darwin":
                        cmd.append("--macos-create-app-bundle")
                else:
                    if os.name == "nt": 
                        cmd.append("--windows-console-mode=force")

                if self.params['onefile']: 
                    cmd.append("--onefile")
                else: 
                    cmd.append("--standalone")

                if icon_path: 
                    if os.name == "nt": cmd.append(f"--windows-icon-from-ico={icon_path}")
                    if sys.platform == "darwin": cmd.append(f"--macos-app-icon={icon_path}")
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

                hidden_list = [i.strip().lower() for i in (self.params.get('hidden_imports') or '').split(',') if i.strip()]
                imports_lower = {m.lower() for m in script_imports} | set(hidden_list)

                if 'pyqt5' in imports_lower: cmd.append("--enable-plugin=pyqt5")
                elif 'pyqt6' in imports_lower: cmd.append("--enable-plugin=pyqt6")
                elif 'pyside2' in imports_lower: cmd.append("--enable-plugin=pyside2")
                elif 'pyside6' in imports_lower: cmd.append("--enable-plugin=pyside6")
                
                if 'matplotlib' in imports_lower: cmd.append("--enable-plugin=matplotlib")
                if any(tk in imports_lower for tk in ('tkinter', 'pysimplegui', 'customtkinter', 'turtle', 'easygui', 'ttkbootstrap')): 
                    cmd.append("--enable-plugin=tk-inter")
                if 'multiprocessing' in imports_lower:
                    cmd.append("--enable-plugin=multiprocessing")
                    if os.name == "nt":
                        self.progress.emit(_("[WARN] 'multiprocessing' module detected. Ensure 'multiprocessing.freeze_support()' is called under 'if __name__ == \"__main__\":' to prevent infinite process loops (fork bombs)."))          
                if 'ttkbootstrap' in imports_lower:
                    cmd.append("--include-package=ttkbootstrap")
                    cmd.append("--include-package-data=ttkbootstrap")
                if 'playwright' in imports_lower or has_playwright_pkg:
                    cmd.append("--include-package=playwright")
                    cmd.append("--include-package-data=playwright")

                if any(lib in imports_lower for lib in ('requests', 'httpx', 'urllib3', 'aiohttp')):
                    cmd.append("--include-package-data=certifi")
                    self.progress.emit(_("[WARN] Detected 'requests' or 'httpx'. Auto-bundling 'certifi' certificates to prevent SSL errors."))
                    
                for web_fw in ('fastapi', 'uvicorn', 'flask', 'streamlit', 'pywebio', 'dash'):
                    if web_fw in imports_lower:
                        cmd.append(f"--include-package={web_fw}")
                        cmd.append(f"--include-package-data={web_fw}")

                if 'numpy' in imports_lower: cmd.append("--enable-plugin=numpy")

                for imp in (self.params.get('hidden_imports') or '').split(','):
                    if imp.strip(): cmd.extend([f"--include-module={imp.strip()}"])
                
                for r_type, src, dst in (self.params.get('add_data_list') or []):
                    src_path = Path(src).resolve().as_posix()
                    if r_type == 'dir':
                        cmd.append(f"--include-data-dir={src_path}={dst}")
                    else:
                        filename = Path(src).name
                        if dst == ".": nuitka_dst = filename
                        else: nuitka_dst = os.path.normpath(os.path.join(dst, filename)).replace('\\', '/')
                        cmd.append(f"--include-data-files={src_path}={nuitka_dst}")

                for excl in (self.params.get('exclude_modules') or '').split(','):
                    if excl.strip(): cmd.append(f"--nofollow-import-to={excl.strip()}")

            if self.params.get('lite_mode'):
                self.progress.emit(_("[INFO] Lite mode enabled, applying bytecode optimization (-OO) and stripping dev modules..."))
                if not self.params.get('use_venv'):
                    self.progress.emit(_("[WARN] Strongly recommend checking [Virtual Environment] to maximize lite mode effect."))
                
                if engine == "PyInstaller":
                    cmd.append("--optimize=2")
                    safe_dev_excludes = ['unittest', 'doctest', 'pdb', 'pydoc', 'test', 'pytest', 'IPython', 'binder', 'tkinter.test']
                    for ex in safe_dev_excludes:
                        cmd.append(f"--exclude-module={ex}")
                elif engine == "Nuitka":
                    cmd.append("--python-flag=-OO")
                    cmd.append("--enable-plugin=anti-bloat")
                    nuitka_dev_excludes = ['unittest', 'doctest', 'pdb', 'pydoc', 'test', 'pytest', 'IPython', 'binder', 'tkinter.test', 'pip', 'setuptools', 'wheel']
                    for ex in nuitka_dev_excludes:
                        cmd.append(f"--nofollow-import-to={ex}")

            cmd.append(script_posix)
            
            if self._is_cancelled:
                return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])

            success = self.run_cmd(cmd, cwd=script_dir.as_posix(), timeout=3600)

            if not success and not self._is_cancelled:
                log_text = "\n".join(self.all_raw_logs)
                if any(kw in log_text for kw in ["NoSpaceLeft", "No space left on device", "[Errno 28]"]):
                    self.progress.emit(_("[ERROR] Build aborted: Insufficient disk space (NoSpaceLeft / Errno 28). Please clean up drive space (at least 5 GB free space recommended) and try again."))
                elif any(kw in log_text for kw in ["Allocation error", "not enough memory", "ZstdError", "out of memory"]):
                    self.progress.emit(_("[WARN] Memory allocation exception caught (ZstdError / OOM). Triggering memory protection fallback: Retrying in single-thread mode..."))
                    clean_cmd = [arg if not arg.startswith("--jobs=") else "--jobs=1" for arg in cmd]
                    if "--low-memory" not in clean_cmd:
                        clean_cmd.append("--low-memory")
                    self.all_raw_logs.clear()
                    success = self.run_cmd(clean_cmd, cwd=script_dir.as_posix())

            if not success and icon_path and not self._is_cancelled:
                log_text = "\n".join(self.all_raw_logs)
                icon_err_keywords = ["Failed to add resources", "error code 22", "UpdateResource", "Resource modification failed", "Failed to add"]
                if any(kw in log_text for kw in icon_err_keywords):
                    self.progress.emit(_("[WARN] Icon resource writing blocked (possibly locked by system/antivirus), triggering fallback protection..."))
                    self.progress.emit(_("[INFO] Stripping icon parameters and automatically rebuilding..."))
                    
                    clean_cmd = []
                    skip_next = False
                    for arg in cmd:
                        if skip_next:
                            skip_next = False
                            continue
                        if arg == "--icon":
                            skip_next = True
                            continue
                        if arg.startswith(("--windows-icon-from-ico=", "--macos-app-icon=")):
                            continue
                        if icon_path in arg and "--include-data-files=" in arg:
                            continue
                        clean_cmd.append(arg)
                    
                    self.all_raw_logs.clear()
                    success = self.run_cmd(clean_cmd, cwd=script_dir.as_posix())

            if self._is_cancelled:
                return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])

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

            out_mode = int(self.params.get('out_mode', 0) or 0)
            custom_out = (self.params.get('custom_out_dir') or '').strip()
            if out_mode == 1 and custom_out:
                try:
                    final_out_dir = Path(custom_out)
                    final_out_dir.mkdir(parents=True, exist_ok=True)
                except: final_out_dir = script_dir
            else:
                final_out_dir = script_dir
                
            if sys.platform == "darwin" and self.params['noconsole']:
                final_out = final_out_dir / f"{app_name}.app"
            elif self.params['onefile']:
                final_out = final_out_dir / f"{app_name}{ext}"
            else:
                final_out = final_out_dir / app_name

            if success and src_out and src_out.exists():
                self.progress.emit(_("[INFO] Compilation completed, archiving built files..."))
                try:
                    if src_out.resolve() != final_out.resolve():
                        if final_out.exists():
                            if final_out.is_dir(): 
                                robust_rmtree(final_out)
                            else: 
                                try:
                                    final_out.unlink()
                                except PermissionError:
                                    time.sleep(1)
                                    final_out.unlink(missing_ok=True)
                        shutil.move(src_out.as_posix(), final_out.as_posix())
                except PermissionError:
                    success = False
                    self.progress.emit(_("[ERROR] Target file is running or occupied. Please close the existing application and try again."))
                except Exception as e: 
                    success = False
                    self.progress.emit(_("[ERROR] Product transfer failed, file might be occupied by system process or lack permission: {error}", error=str(e)))
            else: 
                if not success and not self._is_cancelled:
                    self.progress.emit(_("[ERROR] Could not locate valid executable product in temporary build directory: {path}", path=str(src_out)))

            if success and final_out.exists(): 
                self.progress.emit(_("[INFO] Validating output files and generating final product..."))
                if self.params.get('auto_save_log') and self.all_raw_logs:
                    try:
                        log_file = final_out_dir / f"qpypack_build_{app_name}.log"
                        log_file.write_text('\n'.join(self.all_raw_logs), encoding='utf-8')
                        self.progress.emit(_("[INFO] Build log exported to: {path}", path=log_file.as_posix()))
                    except: pass
                
                if self.params['onefile'] and os.name == 'nt':
                    self.progress.emit(_("[INFO] Tip: Packaged executables might be falsely flagged by Windows Defender/Antivirus. Adding exclusions or code-signing is recommended."))
                self.build_finished.emit(True, _("[SUCCESS] Compilation completed, output path: {path}", path=final_out.resolve().as_posix()), failed_packages)
            else: 
                if self._is_cancelled:
                    return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])
                err_info = self.detect_python_syntax_errors()
                if err_info["is_code_error"]:
                    msg = _("[Syntax Error] Source code contains syntax errors, compilation aborted:\n  - File: {file}\n  - Type: {type}\n  - Line: Line {line}\n  - Detail: {desc}\n\nTip: Please ensure the source code runs locally before packaging.", 
                            file=err_info['file'], type=err_info['type'], line=err_info['line'], desc=err_info['desc'])
                else:
                    msg = _(
                        "[FAILED] Build interrupted exceptionally!\n\n"
                        "🔍 Common Troubleshooting:\n"
                        "1. Environment Mismatch (Most Common): The selected Python version is incompatible with your source code. Please go to [Build Settings] to switch to the Python version you normally use for this code.\n"
                        "2. Missing Dependencies: Click 'Detailed Mode' above to check for ModuleNotFoundError.\n"
                        "3. Antivirus Block: Ensure your security software is not blocking the build process.\n\n"
                        "(Note: This is usually caused by environment/code discrepancies rather than the packaging engine itself. Please check the detailed log for exact reasons.)"
                    )
                self.build_finished.emit(False, msg, failed_packages)

        except Exception as e:
            if self._is_cancelled:
                return self.build_finished.emit(False, _("[INFO] Build Cancelled."), [])
            self.build_finished.emit(False, f"[ERROR] {str(e)}", failed_packages)
        finally:
            if "PYTHONPATH" in os.environ and "_qpypack_temp_" in os.environ.get("PYTHONPATH", ""):
                parts = os.environ["PYTHONPATH"].split(os.pathsep)
                os.environ["PYTHONPATH"] = os.pathsep.join(p for p in parts if "_qpypack_temp_" not in p)
                if not os.environ["PYTHONPATH"]:
                    os.environ.pop("PYTHONPATH", None)
    
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
                for p in ["__pycache__", f"{app_name}.build", f"{app_name}.onefile-build"]:
                    robust_rmtree(script_dir / p)
                
                spec_file = script_dir / f"{app_name}.spec"
                if spec_file.exists():
                    try: spec_file.unlink()
                    except: pass

class PythonInstallMonitorThread(QThread):
    finished_signal = Signal(bool)

    def __init__(self, exe_path):
        super().__init__()
        self.exe_path = exe_path

    def run(self):
        try:
            cmd = [self.exe_path, "/passive", "PrependPath=1", "Include_pip=1", "SimpleInstall=1"]
            kwargs = {}
            if os.name == 'nt':
                kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
            
            res = subprocess.run(cmd, **kwargs)
            self.finished_signal.emit(res.returncode == 0)
        except Exception:
            self.finished_signal.emit(False)

class PythonInstallerDialog(QDialog):
    def __init__(self, parent=None, is_missing_mode=True):
        super().__init__(parent)
        self.parent_win = parent
        self.is_missing_mode = is_missing_mode
        self.selected_local_path = None
        self.is_selected_ver_local = False
        self.current_local_target_path = None

        self.setWindowTitle(_("Python Environment Required") if is_missing_mode else _("Python Environment Management"))
        self.setMinimumWidth(580)
        self.setMinimumHeight(440)
        self.setStyleSheet("QDialog { background-color: #ffffff; }")

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(22, 22, 22, 22)

        if is_missing_mode:
            header_html = _(
                "<b>Python Environment Required</b><br>"
                "<span style='color:#475569; font-size:12px; line-height:1.6;'>"
                "Application build depends on a Python interpreter.<br>"
                "Please select a version to automatically download, install, and configure environment variables."
                "</span>"
            )
        else:
            header_html = _(
                "<b>Python Environment Management</b><br>"
                "<span style='color:#475569; font-size:12px; line-height:1.6;'>"
                "Supports switching locally detected Python environments or downloading new versions."
                "</span>"
            )

        lbl_title = QLabel(header_html)
        lbl_title.setWordWrap(True)
        lbl_title.setStyleSheet("font-size: 13px; color: #1e293b;")
        layout.addWidget(lbl_title)

        if is_missing_mode:
            tip_card = QLabel(_(
                "💡 <b>Recommendation:</b> Python <b>3.11.9</b> is recommended for optimal build compatibility and engine support."
            ))
            tip_card.setWordWrap(True)
            tip_card.setStyleSheet("""
                QLabel {
                    background-color: #eff6ff;
                    border: 1px solid #bfdbfe;
                    border-radius: 6px;
                    padding: 10px 14px;
                    color: #1e40af;
                    font-size: 12px;
                    line-height: 1.5;
                }
            """)
            layout.addWidget(tip_card)

        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #e2e8f0; border-radius: 8px; background: #ffffff; }
            QTabBar::tab { background: #f8fafc; border: 1px solid #e2e8f0; padding: 8px 16px; font-weight: bold; font-size: 12px; color: #64748b; margin-right: 4px; border-top-left-radius: 6px; border-top-right-radius: 6px; }
            QTabBar::tab:selected { background: #ffffff; color: #2563eb; border-bottom-color: #ffffff; }
        """)

        self.tab_local = QWidget()
        lay_local = QVBoxLayout(self.tab_local)
        lay_local.setContentsMargins(12, 12, 12, 12)
        lay_local.setSpacing(8)

        self.local_list = QListWidget()
        self.local_list.setStyleSheet("""
            QListWidget { border: 1px solid #e2e8f0; border-radius: 6px; outline: none; background: #fafafa; }
            QListWidget::item { padding: 10px; border-bottom: 1px solid #f1f5f9; color: #1e293b; font-family: Consolas, monospace; font-size: 12px; }
            QListWidget::item:selected { background-color: #eff6ff; color: #2563eb; font-weight: bold; }
        """)
        lay_local.addWidget(self.local_list)

        self.btn_use_local = QPushButton(_("Use Selected Environment"))
        self.btn_use_local.setStyleSheet("QPushButton { background-color: #16a34a; color: white; border: none; border-radius: 6px; font-size: 13px; font-weight: bold; padding: 8px 16px; } QPushButton:hover { background-color: #15803d; }")
        self.btn_use_local.clicked.connect(self._on_use_local_clicked)
        lay_local.addWidget(self.btn_use_local)

        self.tab_widget.addTab(self.tab_local, _("Locally Detected Pythons"))

        self.tab_download = QWidget()
        lay_dl = QVBoxLayout(self.tab_download)
        lay_dl.setContentsMargins(12, 12, 12, 12)
        lay_dl.setSpacing(10)

        self.versions = [
            ("3.14.6", _("Python 3.14.6 (Experimental)")),
            ("3.13.0", _("Python 3.13.0")),
            ("3.12.4", _("Python 3.12.4")),
            ("3.11.9", _("Python 3.11.9 (Recommended)")),
            ("3.10.11", _("Python 3.10.11")),
            ("3.9.13", _("Python 3.9.13")),
            ("3.8.10", _("Python 3.8.10 (Win7 Support)")),
        ]

        self.dl_combo = QComboBox()
        setup_combo_white_theme(self.dl_combo)
        for ver, desc in self.versions:
            self.dl_combo.addItem(desc, ver)
        self.dl_combo.setCurrentIndex(3)

        lay_dl.addWidget(QLabel(_("Select Python Version to Download:")))
        lay_dl.addWidget(self.dl_combo)

        self.lbl_dl_hint = QLabel()
        self.lbl_dl_hint.setWordWrap(True)
        self.lbl_dl_hint.setStyleSheet("font-size: 12px; color: #64748b; line-height: 1.4;")
        lay_dl.addWidget(self.lbl_dl_hint)

        lay_dl.addStretch()

        self.btn_dl_install = QPushButton()
        self.btn_dl_install.clicked.connect(self._on_action_btn_clicked)
        lay_dl.addWidget(self.btn_dl_install)

        self.tab_widget.addTab(self.tab_download, _("Download New Version"))

        layout.addWidget(self.tab_widget)

        btn_lay = QHBoxLayout()
        self.btn_manual_config = QPushButton(_("Configure Manually"))
        self.btn_manual_config.setStyleSheet("QPushButton { background-color: #f8fafc; color: #2563eb; border: 1px solid #bfdbfe; border-radius: 6px; font-size: 12px; font-weight: bold; padding: 6px 14px; } QPushButton:hover { background-color: #eff6ff; }")
        self.btn_manual_config.clicked.connect(lambda: self.done(2))
        btn_lay.addWidget(self.btn_manual_config)

        btn_lay.addStretch()
        self.btn_cancel = QPushButton(_("Cancel"))
        self.btn_cancel.setStyleSheet("QPushButton { background-color: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 12px; font-weight: bold; padding: 6px 14px; } QPushButton:hover { background-color: #e2e8f0; }")
        self.btn_cancel.clicked.connect(self.reject)
        btn_lay.addWidget(self.btn_cancel)
        layout.addLayout(btn_lay)

        self.installed_map = self._scan_installed_map()
        self.dl_combo.currentIndexChanged.connect(self._on_download_ver_changed)
        self._load_local_environments()
        self._on_download_ver_changed()

        if is_missing_mode:
            self.tab_widget.setCurrentIndex(1)
        else:
            self.tab_widget.setCurrentIndex(0)

    def _scan_installed_map(self):
        installed = {}
        if self.parent_win and hasattr(self.parent_win, 'settings_panel'):
            combo = self.parent_win.settings_panel.python_path_combo
            for i in range(combo.count()):
                text = combo.itemText(i)
                path = combo.itemData(i) or text
                m = re.search(r'Python\s+(\d+\.\d+)', text, re.I)
                if m and path and os.path.exists(path):
                    installed[m.group(1)] = path

        if not installed:
            sys_py = find_system_python()
            if sys_py and os.path.exists(sys_py):
                installed["default"] = sys_py

        return installed

    def _on_download_ver_changed(self):
        ver_full = self.dl_combo.currentData()
        parts = ver_full.split('.')
        major_minor = f"{parts[0]}.{parts[1]}" if len(parts) >= 2 else ver_full

        local_path = self.installed_map.get(major_minor) or self.installed_map.get(ver_full)

        if local_path:
            self.is_selected_ver_local = True
            self.current_local_target_path = local_path
            self.lbl_dl_hint.setText(_(
                "<b><span style='color:#16a34a;'>✔ Detected locally:</span></b><br>"
                "<span style='color:#475569; font-family:Consolas;'>{path}</span><br>"
                "<span style='color:#16a34a; font-size:11px;'>Ready to switch directly without re-downloading.</span>",
                path=local_path
            ))
            self.btn_dl_install.setText(_("Use Installed Version Directly"))
            self.btn_dl_install.setStyleSheet("""
                QPushButton { background-color: #16a34a; color: white; border: none; border-radius: 6px; font-size: 13px; font-weight: bold; padding: 10px 16px; }
                QPushButton:hover { background-color: #15803d; }
            """)
        else:
            self.is_selected_ver_local = False
            self.current_local_target_path = None
            self.lbl_dl_hint.setText(_("Click to automatically download, install Python, and configure system environment variables."))
            self.btn_dl_install.setText(_("One-Click Download & Install"))
            self.btn_dl_install.setStyleSheet("""
                QPushButton { background-color: #1A73E8; color: white; border: none; border-radius: 6px; font-size: 13px; font-weight: bold; padding: 10px 16px; }
                QPushButton:hover { background-color: #1B66C9; }
            """)

    def _on_action_btn_clicked(self):
        if self.is_selected_ver_local and self.current_local_target_path:
            self.selected_local_path = self.current_local_target_path
            self.done(3)
        else:
            self.accept()

    def _load_local_environments(self):
        self.local_list.clear()
        found_any = False
        if self.parent_win and hasattr(self.parent_win, 'settings_panel'):
            combo = self.parent_win.settings_panel.python_path_combo
            for i in range(combo.count()):
                text = combo.itemText(i)
                path = combo.itemData(i) or text
                if path and os.path.exists(path):
                    item = QListWidgetItem(f"🐍  {text}")
                    item.setData(Qt.ItemDataRole.UserRole, path)
                    self.local_list.addItem(item)
                    found_any = True

        if not found_any:
            sys_py = find_system_python()
            if sys_py and os.path.exists(sys_py):
                item = QListWidgetItem(f"🐍  {sys_py}")
                item.setData(Qt.ItemDataRole.UserRole, sys_py)
                self.local_list.addItem(item)
                found_any = True

        if found_any:
            self.local_list.setCurrentRow(0)
        else:
            self.local_list.addItem(_("No local Python environments detected."))
            self.btn_use_local.setEnabled(False)

    def _on_use_local_clicked(self):
        item = self.local_list.currentItem()
        if item:
            path = item.data(Qt.ItemDataRole.UserRole)
            if path:
                self.selected_local_path = path
                self.done(3)

    def get_selected_version(self):
        return self.dl_combo.currentData()

    def get_selected_local_path(self):
        return getattr(self, 'selected_local_path', None)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.script_path = ""
        self.thread = None
        self.analysis_thread = None
        self.current_state = "idle" 
        
        load_config()
        
        self.init_style()
        self.init_ui()
        
        I18N.language_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def init_style(self):
        self.setWindowTitle(f"{__app_name__} {__version__}")
        self.setMinimumSize(560, 460)
        self.resize(760, 580)
        
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
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 16)

        self.drop_area = DropArea(self)
        self.drop_area.fileDropped.connect(self.on_script_selected)
        layout.addWidget(self.drop_area, stretch=1)

        self.log_container = QWidget()
        log_lay = QVBoxLayout(self.log_container)
        log_lay.setContentsMargins(0, 0, 0, 0)
        
        log_header = QHBoxLayout()
        log_header.setContentsMargins(5, 0, 5, 2)
        self.log_title = QLabel(_("Execution Log"))
        self.log_title.setStyleSheet("color: #5f6368; font-weight: bold; font-size: 13px;")
        
        self.btn_toggle_log_mode = QPushButton()
        self.btn_toggle_log_mode.setCheckable(True)
        self.btn_toggle_log_mode.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle_log_mode.setStyleSheet("""
            QPushButton { background-color: transparent; color: #1A73E8; border: none; font-size: 12px; font-weight: bold; }
            QPushButton:hover { color: #1B66C9; text-decoration: underline; }
        """)
        self.btn_toggle_log_mode.clicked.connect(self.on_log_mode_toggled)
        
        log_header.addWidget(self.log_title)
        log_header.addStretch(1)
        log_header.addWidget(self.btn_toggle_log_mode)
        
        self.log_stack_widget = QWidget()
        self.log_stack = QStackedLayout(self.log_stack_widget)
        self.log_stack.setContentsMargins(0, 0, 0, 0)
        
        self.log_concise = QTextEdit()
        self.log_detailed = QTextEdit()
        
        for text_edit in (self.log_concise, self.log_detailed):
            text_edit.setReadOnly(True)
            text_edit.setMinimumHeight(80)
            text_edit.setMaximumHeight(160)
            text_edit.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            text_edit.customContextMenuRequested.connect(self.show_log_context_menu)
            self.log_stack.addWidget(text_edit)
            
        log_lay.addLayout(log_header)
        log_lay.addWidget(self.log_stack_widget)
        self.log_container.hide()
        layout.addWidget(self.log_container)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        btn_layout.setContentsMargins(0, 0, 0, 0)

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
        
        is_concise = self.settings_panel.concise_log_check.isChecked()
        self.btn_toggle_log_mode.setChecked(not is_concise)
        self.btn_toggle_log_mode.setText(_("Detailed Mode") if is_concise else _("Concise Mode"))
        self.log_stack.setCurrentWidget(self.log_concise if is_concise else self.log_detailed)

        self.status_bar = self.statusBar()
        self.status_label = QLabel(_("Status: Ready"))
        self.status_bar.addWidget(self.status_label)

        current_year = time.localtime().tm_year
        year_str = f"2026-{current_year}" if current_year > 2026 else "2026"
        self.copyright_label = QLabel(f"Copyright © {year_str} {__author__}. ")

        self.copyright_label.setStyleSheet("color: #bdc1c6; font-size: 11px; font-weight: bold; background: transparent; padding-right: 5px;")
        self.status_bar.addPermanentWidget(self.copyright_label)

        self.update_ui_state("idle")

    def show_notification(self, msg, timeout=4000):
        msg = msg.replace('\n', ' ')
        self.statusBar().showMessage(msg, timeout)

    def _on_python_install_completed(self, success):
        if success:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(_("Install Complete"))
            msg_box.setText(_(
                "<b>Python Environment Installed Successfully!</b><br><br>"
                "System environment variables updated. Recommended to exit and restart the software to apply changes."
            ))
            msg_box.setIcon(QMessageBox.Icon.Information)

            btn_exit = msg_box.addButton(_("Exit Now"), QMessageBox.ButtonRole.AcceptRole)
            btn_later = msg_box.addButton(_("Later"), QMessageBox.ButtonRole.RejectRole)

            btn_exit.setStyleSheet("""
                QPushButton {
                    background-color: #1A73E8; color: #ffffff; border: none;
                    border-radius: 6px; font-size: 13px; font-weight: bold;
                    padding: 8px 16px; min-width: 80px;
                }
                QPushButton:hover { background-color: #1B66C9; }
                QPushButton:pressed { background-color: #174EA6; }
            """)

            btn_later.setStyleSheet("""
                QPushButton {
                    background-color: #f1f5f9; color: #475569; border: 1px solid #cbd5e1;
                    border-radius: 6px; font-size: 13px; font-weight: bold;
                    padding: 8px 16px; min-width: 80px;
                }
                QPushButton:hover { background-color: #e2e8f0; }
                QPushButton:pressed { background-color: #cbd5e1; }
            """)

            msg_box.exec()

            if msg_box.clickedButton() == btn_exit:
                QApplication.quit()
            else:
                self.show_notification(_("Python installed. Please restart QPyPack manually later."), 6000)
        else:
            self.show_error_log(_("[ERROR] Python installation failed or was cancelled."))

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

        if hasattr(self, 'log_title'):
            self.log_title.setText(_("Execution Log"))
        is_concise = self.settings_panel.concise_log_check.isChecked()
        self.btn_toggle_log_mode.setText(_("Detailed Mode") if is_concise else _("Concise Mode"))

        if self.current_state == "idle":
            self.set_status(_("Status: Ready"))
            self.drop_area.label.setText(_("Python Packaging, Reimagined."))
            self.drop_area.sub_label.setText(_("Drop Python source code to start"))
            
        elif self.current_state == "ready":
            mode_suffix = _(" [Console]") if not self.settings_panel.noconsole_check.isChecked() else _(" [No Console]")
            self.set_status(_("Status: Loaded {filename}{mode}", filename=Path(self.script_path).name, mode=mode_suffix))
            self.drop_area.label.setText(_("Loaded: {filename}", filename=Path(self.script_path).name))
            self.drop_area.sub_label.setText(_("Ready, waiting for build."))
            
        elif self.current_state == "building":
            self.set_status(_("Status: Packaging ({engine}) ...", engine=self.settings_panel.engine_combo.currentText()))
            
        elif self.current_state == "done":
            self.set_status(_("Status: Build Completed"))
            self.drop_area.label.setText(_("Build Successful"))
            self.drop_area.sub_label.setText(_("Open output directory or reset workspace."))
            
        elif self.current_state == "failed":
            self.set_status(_("Status: Build Failed"))
            self.drop_area.label.setText(_("Build Failed"))
            self.drop_area.sub_label.setText(_("Check log output below for troubleshooting."))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_status_bar()

    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            self.thread.cancel()
            self.thread.wait(2000)
            
        if self.analysis_thread and self.analysis_thread.isRunning():
            self.analysis_thread.requestInterruption()
            self.analysis_thread.wait(1000)
            
        if hasattr(self,'settings_panel') and hasattr(self.settings_panel, 'scanner_thread'):
            if self.settings_panel.scanner_thread and self.settings_panel.scanner_thread.isRunning():
                self.settings_panel.scanner_thread.requestInterruption()
                self.settings_panel.scanner_thread.wait(1000)
                
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
        if self.current_state in ("done", "failed"): 
            self.reset_to_ready()
        else: 
            self.toggle_log()

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
        if self.script_path and self.current_state in ("done", "failed"):
            self.reset_to_ready()

    def save_settings_and_return(self):
        self.settings_panel.save_to_config()
        self._animate_switch(self.main_panel)
        if self.script_path and self.current_state in ("done", "failed"):
            self.reset_to_ready()

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

    def _trigger_python_download_dialog(self, is_missing_mode=False):
        dialog = PythonInstallerDialog(self, is_missing_mode=is_missing_mode)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            selected_version = dialog.get_selected_version()
            self._auto_install_python(selected_version)
        elif result == 3:
            local_path = dialog.get_selected_local_path()
            if local_path and os.path.exists(local_path):
                self.settings_panel.python_path_combo.setCurrentText(local_path)
                self.show_notification(_("Switched to local Python environment: {path}", path=local_path))
        elif result == 2:
            self.show_settings()
            self.settings_panel.tabs.setCurrentIndex(0)
            self.settings_panel.sub_tabs.setCurrentIndex(0)
            self.settings_panel.python_path_combo.setFocus()
            self.show_notification(_("Switched to [Build Settings] -> [Engine], please set the Python path."), 6000)

    def _auto_install_python(self, version):
        import urllib.request
        from urllib.error import URLError
        from PySide6.QtWidgets import QProgressDialog
        
        url_hw = f"https://repo.huaweicloud.com/python/{version}/python-{version}-amd64.exe"
        url_off = f"https://www.python.org/ftp/python/{version}/python-{version}-amd64.exe"
        
        exe_path = Path(tempfile.gettempdir()) / f"python-{version}-amd64.exe"
        
        progress = QProgressDialog(_("Downloading Python {ver}... Please wait.", ver=version), _("Cancel"), 0, 100, self)
        progress.setWindowTitle(_("One-Click Install"))
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)
        
        def report(block_num, block_size, total_size):
            if total_size > 0:
                percent = int(block_num * block_size * 100 / total_size)
                progress.setValue(min(percent, 100))
                QApplication.processEvents()
            if progress.wasCanceled():
                raise Exception("Cancelled")
                
        try:
            target_url = url_hw if I18N.current_lang == "zh_CN" else url_off
            try:
                urllib.request.urlretrieve(target_url, exe_path.as_posix(), reporthook=report)
            except URLError:
                progress.setValue(0)
                urllib.request.urlretrieve(url_off, exe_path.as_posix(), reporthook=report)

            progress.setValue(100)
            self.show_notification(_("Download complete. Starting Python installation..."), 5000)
            
            self.install_monitor_thread = PythonInstallMonitorThread(exe_path.as_posix())
            self.install_monitor_thread.finished_signal.connect(self._on_python_install_completed)
            self.install_monitor_thread.start()

        except Exception as e:
            if str(e) != "Cancelled":
                self.show_error_log(f"[ERROR] Python download failed: {e}")

    def on_script_selected(self, path):
        path = Path(path).resolve().as_posix()
        if is_cloud_locked(path):
            self.show_error_log(_("[ERROR] Target file is locked or encrypted by cloud drive. Please decrypt and try again."))
            return

        if self.script_path != path:
            self.settings_panel.icon_edit.clear()
            self.settings_panel.hidden_edit.clear()
            self.settings_panel.exclude_edit.clear()
            self.settings_panel.add_data_list.clear()
            self.settings_panel.reqs_file_edit.clear()
            self.settings_panel.name_edit.clear()

        self.script_path = path
        self.drop_area.set_loading(Path(path).name)
        self.set_status(_("Status: Parsing {filename}...", filename=Path(path).name))
        
        if self.analysis_thread and self.analysis_thread.isRunning():
            self.analysis_thread.requestInterruption()
            self.analysis_thread.wait(1000)
            
        self.analysis_thread = ScriptAnalysisThread(self.script_path)
        self.analysis_thread.analysis_done.connect(self.on_analysis_finished)
        self.analysis_thread.start()

    def on_analysis_finished(self, app_name, version, author, desc, script_imports):
        path = self.script_path
        if not path: return

        if version: self.settings_panel.ver_ver.setText(version)
        else: self.settings_panel.ver_ver.setText("1.0.0")
            
        self.settings_panel.ver_comp.setText(_(author) if author == "My Studio" else author)
        self.settings_panel.ver_desc.setText(_(desc) if desc == "Python Executable" else desc)

        gui_libs = {
            'pyqt5', 'pyqt6', 'pyside2', 'pyside6', 'tkinter', 'wx', 'kivy', 'libavg', 
            'pysimplegui', 'customtkinter', 'turtle', 'easygui', 'pygame', 'arcade', 
            'dearpygui', 'flet', 'webview', 'remi'
        }

        has_gui = any(lib in {m.lower() for m in script_imports} for lib in gui_libs)
        self.settings_panel.noconsole_check.setChecked(has_gui)

        default_output_name = f"{app_name}_{version}" if version else app_name
        self.settings_panel.name_edit.setText(default_output_name)
        
        script_dir = Path(path).parent
        auto_icon = None
        
        if self.settings_panel.auto_icon_check.isChecked():
            ext_priority = [".ico", ".png", ".jpg", ".jpeg", ".svg"]
            if sys.platform == "darwin": 
                ext_priority = [".icns", ".png", ".svg", ".ico"]
            name_priority = ["logo", "icon", "app", "favicon", Path(path).stem]

            auto_icon = None
            found = False
            for ext in ext_priority:
                for name in name_priority:
                    for n_variant in [name, name.lower(), name.upper(), name.capitalize()]:
                        trial = script_dir / f"{n_variant}{ext}"
                        if trial.exists() and trial.is_file():
                            auto_icon = trial
                            found = True
                            break
                    if found: break
                if found: break

            if auto_icon:
                self.settings_panel.icon_edit.setText(auto_icon.resolve().as_posix())
                
        self.drop_area.set_success(Path(path).name, custom_icon_path=auto_icon)
        mode_suffix = _(" [Console]") if not has_gui else _(" [No Console]")
        self.set_status(_("Status: Loaded {filename}{mode}", filename=Path(path).name, mode=mode_suffix))
        
        self.log_concise.clear()
        self.log_detailed.clear()
        self.append_log(_("Loaded: {filename}", filename=path))
        self.btn_main.setEnabled(True)
        self.update_ui_state("ready")

    def cancel_pack(self):
        if self.thread and self.thread.isRunning():
            self.thread.cancel()
            self.thread.wait(1000)
            
        self.append_log(_("[INFO] Build Cancelled."))
        self.set_status(_("Status: Build Cancelled"))
        
        if self.script_path and Path(self.script_path).exists():
            self.reset_to_ready()
        else:
            self.reset_all()
            
        self.show_notification(_("Build Cancelled"))

    def start_pack(self):
        if self.current_state == "building":
            return
            
        if not self.script_path or not Path(self.script_path).exists():
            self.show_error_log(_("[ERROR] Please load a valid Python source file first!"))
            return

        sp = self.settings_panel
        
        raw_py = sp.python_path_combo.currentText().strip()
        if " (Python " in raw_py: 
            raw_py = raw_py.split(" (Python ")[0].strip()
        if not raw_py: 
            raw_py = get_python_executable()

        if raw_py:
            resolved_py = shutil.which(raw_py)
            if resolved_py:
                raw_py = Path(resolved_py).resolve().as_posix()

            
        is_valid_py = False
        if raw_py:
            try:
                clean_env = os.environ.copy()
                clean_env.pop("PYTHONHOME", None)
                clean_env.pop("PYTHONPATH", None)
                kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE, "text": True, "env": clean_env, "timeout": 3}
                if os.name == 'nt': kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
                
                proc = subprocess.run([raw_py, "-c", "import sys; print(sys.version_info.major)"], **kwargs)
                if proc.returncode == 0 and "3" in proc.stdout:
                    is_valid_py = True
            except Exception:
                pass

        if not is_valid_py:
            if os.name == 'nt':
                self._trigger_python_download_dialog(is_missing_mode=True)
            else:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle(_("Python Environment Required"))
                msg.setText(_("<b>Python is not detected on your system!</b><br><br>QPyPack requires a Python environment to compile your code.<br>If you haven't installed Python, please download and install it."))
                btn_down = msg.addButton(_("Download Python"), QMessageBox.ButtonRole.ActionRole)
                msg.addButton(_("Cancel"), QMessageBox.ButtonRole.RejectRole)
                msg.exec()
                if msg.clickedButton() == btn_down:
                    __import__('webbrowser').open("https://www.python.org/downloads/")
            return

        app_name = sp.name_edit.text().strip() or Path(self.script_path).stem
        engine = sp.engine_combo.currentText()

        version_file = None
        if engine == "PyInstaller" and os.name == "nt" and sp.ver_ver.text().strip():
            try:
                v_str = sp.ver_ver.text().strip()
                v_nums = re.findall(r'\d+', v_str)
                v_tuple = ",".join((v_nums + ['0', '0', '0', '0'])[:4])
                
                comp_escaped = sp.ver_comp.text().replace("\\", "\\\\").replace("'", "\\'")
                desc_escaped = sp.ver_desc.text().replace("\\", "\\\\").replace("'", "\\'")
                v_str_escaped = v_str.replace("\\", "\\\\").replace("'", "\\'")
                
                content = f'''VSVersionInfo(ffi=FixedFileInfo(filevers=({v_tuple}),prodvers=({v_tuple}),mask=0x3f,flags=0x0,OS=0x40004,fileType=0x1,subtype=0x0,date=(0,0)),kids=[StringFileInfo([StringTable('040904B0',[StringStruct('CompanyName','{comp_escaped}'),StringStruct('FileDescription','{desc_escaped}'),StringStruct('FileVersion','{v_str_escaped}'),StringStruct('ProductVersion','{v_str_escaped}'),StringStruct('OriginalFilename','{app_name}.exe')])]),VarFileInfo([VarStruct('Translation',[1033,1200])])])'''
                version_file = Path(tempfile.gettempdir()) / f"qpypack_{app_name}_version.txt"
                version_file.write_text(content, encoding='utf-8')
            except: pass

        icon_path_str = sp.icon_edit.text().strip()
        
        if icon_path_str and not Path(icon_path_str).exists():
            self.show_error_log(_("[ERROR] The specified icon file does not exist: {path}", path=icon_path_str))
            return
            
        temp_icon_file = None
        if icon_path_str:

            icon_path = Path(icon_path_str)
            needed_ext = "ico" if os.name == "nt" else ("icns" if sys.platform == "darwin" else "png")

            is_valid_native_icon = False
            if icon_path.suffix.lower() == f".{needed_ext}":
                try:
                    with open(icon_path, 'rb') as f:
                        header = f.read(4)
                        if needed_ext == "ico" and header == b'\x00\x00\x01\x00':
                            is_valid_native_icon = True
                        elif needed_ext == "icns" and header == b'icns':
                            is_valid_native_icon = True
                except:
                    is_valid_native_icon = False

            if is_valid_native_icon:
                icon_path_str = icon_path.as_posix()
            else:
                temp_ico = Path(tempfile.gettempdir()) / f"qpypack_sanitized_icon_{int(time.time())}.{needed_ext}"
                if convert_image_to_format(icon_path.as_posix(), temp_ico.as_posix(), needed_ext):
                    icon_path_str = temp_ico.as_posix()
                    temp_icon_file = temp_ico.as_posix()
                else:
                    if needed_ext == "icns":
                        icon_path_str = ""
                        self.show_notification(_("[WARN] Icon conversion to .icns failed, building without icon."))
                    else:
                        icon_path_str = icon_path.as_posix()

        add_data_items = [sp.add_data_list.item(i).data(Qt.ItemDataRole.UserRole) for i in range(sp.add_data_list.count())]
        main_pip = sp._get_url_from_combo(sp.pip_source_combo)
        backup_pip = sp._get_url_from_combo(sp.pip_backup_combo)

        mappings = DEFAULT_MAPPINGS.copy()
        for r in range(sp.mapping_table.rowCount()):
            k = sp.mapping_table.item(r, 0).text().strip()
            v = sp.mapping_table.item(r, 1).text().strip()
            if k and v: mappings[k] = v

        params = {
            'engine': engine,
            'python_exe': raw_py,
            'script_path': self.script_path,
            'app_name': app_name,
            'onefile': sp.rb_onefile.isChecked(),
            'contents_dir': sp.contents_dir_edit.text().strip() or '_internal',
            'noconsole': sp.noconsole_check.isChecked(),
            'icon': icon_path_str,
            'use_reqs': sp.reqs_check.isChecked(),
            'use_pipreqs': sp.pipreqs_check.isChecked(),
            'use_pipreqs_dir': sp.pipreqs_dir_check.isChecked(),
            'reqs_file': sp.reqs_file_edit.text().strip(),
            'hidden_imports': sp.hidden_edit.text(),
            'add_data_list': add_data_items,
            'upx': sp.upx_check.isChecked(),
            'upx_path': sp.upx_path_edit.text().strip(),
            'cpu_cores': sp.cores_spin.value(),
            'exclude_modules': sp.exclude_edit.text().strip(),
            'out_mode': sp.out_mode_combo.currentIndex(),
            'custom_out_dir': sp.out_dir_edit.text().strip(),
            'temp_sandbox_mode': sp.sandbox_mode_combo.currentIndex(), 
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
        }

        self.log_concise.clear()
        self.log_detailed.clear()
        if not self.log_container.isVisible(): self.toggle_log()
            
        self.thread = PackingThread(params)
        self.thread.progress.connect(self.append_log)
        self.thread.build_finished.connect(self.on_pack_finished)
        self.thread.start()
        
        self.set_status(_("Status: Packaging ({engine}) ...", engine=engine))
        self.update_ui_state("building")
        self.drop_area.start_build_anim()

    def on_pack_finished(self, success, msg, failed_pkgs=None):
        self.append_log("\n" + msg)
        self.drop_area.stop_build_anim()
        
        if self.thread and getattr(self.thread, '_is_cancelled', False):
            if self.script_path and Path(self.script_path).exists():
                self.reset_to_ready()
            else:
                self.drop_area.reset()
                self.update_ui_state("idle")
            self.set_status(_("Status: Build Cancelled"))
            return

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

        if failed_pkgs and not (self.thread and getattr(self.thread, '_is_cancelled', False)):
            warn_msg = _("Dependency Missing Warning: {pkgs} failed to install. Check log for details.", pkgs=", ".join(failed_pkgs))
            self.show_notification(warn_msg, 6000)
            err_log = _("[ERROR] Build completed, but the following dependencies failed to install:\n\n  - {pkgs}\n\nNote: The application might raise ModuleNotFoundError at runtime.", pkgs=", ".join(failed_pkgs))
            self.show_error_log(err_log)

    def open_dist(self):
        if self.settings_panel.out_mode_combo.currentIndex() == 1 and self.settings_panel.out_dir_edit.text().strip():
            target = Path(self.settings_panel.out_dir_edit.text().strip())
        else:
            target = Path(self.script_path).parent if self.script_path else Path.cwd()
            
        if target.exists():
            try:
                QDesktopServices.openUrl(QUrl.fromLocalFile(target.resolve().as_posix()))
            except: pass

    def reset_to_ready(self):
        if self.script_path and Path(self.script_path).exists():
            icon_path = self.settings_panel.icon_edit.text().strip()
            self.drop_area.set_success(Path(self.script_path).name, custom_icon_path=icon_path)
            self.update_ui_state("ready")
            self.set_status(_("Status: Ready"))
            self.show_notification(_("Script and settings retained. Ready to rebuild."))
        else:
            self.reset_all()

    def reset_all(self):
        self.script_path = ""
        self.settings_panel.name_edit.clear()
        self.settings_panel.icon_edit.clear()
        self.settings_panel.hidden_edit.clear()
        self.settings_panel.exclude_edit.clear()
        self.settings_panel.add_data_list.clear()
        self.settings_panel.reqs_file_edit.clear()
        self.settings_panel.out_dir_edit.clear()
        self.settings_panel.ver_ver.setText("1.0.0")
        self.settings_panel.ver_comp.setText(_("My Studio"))
        self.settings_panel.ver_desc.setText(_("Python Executable"))
        self.log_concise.clear()
        self.log_detailed.clear()
        
        if self.log_container.isVisible(): self.toggle_log()
        self.drop_area.reset()
        self.set_status(_("Status: Workspace Reset"))
        self.update_ui_state("idle")
    
    def on_log_mode_toggled(self, checked):
        is_concise = not checked
        self.settings_panel.concise_log_check.setChecked(is_concise)
        self.btn_toggle_log_mode.setText(_("Detailed Mode") if is_concise else _("Concise Mode"))
        self.log_stack.setCurrentWidget(self.log_concise if is_concise else self.log_detailed)

    def append_log(self, msg, is_error=False):
        concise_lines = []
        
        for line in msg.split('\n'):
            line_strip = line.strip()
            if not line_strip: continue
            
            if is_error:
                concise_lines.append(line)
                continue
                
            is_concise_kept = False
            valid_prefixes = (
                "[INFO]", "[WARN]", "[SUCCESS]", "[FAILED]", "[ERROR]", "[Syntax Error]",
                "•", "---", "━", "!"
            )
            
            is_critical_engine_log = any(kw in line for kw in (
                "FATAL:", "Disable Anti-Virus", "Failed to delete", "PermissionError", "Access is denied"
            ))

            if any(line_strip.startswith(p) for p in valid_prefixes) or is_critical_engine_log:
                concise_lines.append(line)
                is_concise_kept = True
            
            if self.current_state == "building":
                if any(k in line for k in ("Nuitka", "Scons", "PyInstaller", "Compiling", "Building", "Linking")):
                    clean_sub = re.sub(r'^(Nuitka-Scons:|Nuitka:|INFO:\s*PyInstaller:|\d+\s+INFO:\s*)', '', line).strip()
                    if clean_sub and len(clean_sub) > 3 and not clean_sub.startswith("Used command line"):
                        if len(clean_sub) > 60: clean_sub = clean_sub[:57] + "..."
                        self.drop_area.sub_label.setText(clean_sub)
                        
                        engine_name = self.settings_panel.engine_combo.currentText()
                        target_text = _("Status: Packaging ({engine}) ...", engine=engine_name).replace("Status: ", "").replace("状态: ", "")
                        if self.drop_area.label.text() != target_text:
                            self.drop_area.label.setText(target_text)
                            self.drop_area.label.setStyleSheet("QLabel { background: transparent; color: #1A73E8; font-size: 16px; font-weight: bold; border: none; }")
                        
                        if not is_concise_kept:
                            concise_lines.append(f"[BUILD] {clean_sub}")

                elif line_strip.startswith(("[INFO]", "[WARN]", "[SUCCESS]", "[FAILED]", "[ERROR]")):
                    clean_text = line_strip
                    for prefix in ("[INFO]", "[WARN]", "[SUCCESS]", "[FAILED]", "[ERROR]"):
                        if clean_text.startswith(prefix):
                            clean_text = clean_text[len(prefix):].strip()
                            break
                    if len(clean_text) > 40: clean_text = clean_text[:37] + "..."
                    self.drop_area.label.setText(clean_text)
                    self.drop_area.label.setStyleSheet("QLabel { background: transparent; color: #1A73E8; font-size: 16px; font-weight: bold; border: none; }")

        concise_msg = '\n'.join(concise_lines)

        if concise_msg:
            self._render_text_edit(self.log_concise, concise_msg, is_error)
            
        self._render_text_edit(self.log_detailed, msg, is_error)

    def _render_text_edit(self, text_edit, msg, is_error):
        if is_error:
            safe_msg = msg.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
            text_edit.append(f'<span style="color: #D93025; font-weight: bold;">{safe_msg}</span>')
        else:
            text_edit.append(msg)
        text_edit.ensureCursorVisible()

    def show_log_context_menu(self, pos):
        current_log = self.log_stack.currentWidget()
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #ffffff; color: #111827; border: 1px solid #d1d5db; border-radius: 8px; padding: 4px; }
            QMenu::item { padding: 6px 20px; border-radius: 4px; font-size: 12px; font-family: Consolas, "Segoe UI", sans-serif; }
            QMenu::item:selected { background-color: #eff6ff; color: #2563eb; font-weight: 600; }
            QMenu::separator { height: 1px; background-color: #e5e7eb; margin: 4px 2px; }
        """)
        
        act_copy = menu.addAction(_("Copy"))
        act_copy.setEnabled(current_log.textCursor().hasSelection())
        act_copy.triggered.connect(current_log.copy)

        act_select_all = menu.addAction(_("Select All"))
        act_select_all.triggered.connect(current_log.selectAll)

        menu.addSeparator()

        act_clear = menu.addAction(_("Clear Log"))
        act_clear.triggered.connect(self.log_concise.clear)
        act_clear.triggered.connect(self.log_detailed.clear)

        act_save = menu.addAction(_("Export Log..."))
        act_save.triggered.connect(self.save_log_file)

        menu.exec(current_log.mapToGlobal(pos))

    def save_log_file(self):
        current_log = self.log_stack.currentWidget()
        content = current_log.toPlainText()
        
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