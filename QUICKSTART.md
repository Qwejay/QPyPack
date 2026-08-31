# ⚡ QPyPack 快速入门指南 | Quick Start Guide

<p align="center">
  <a href="#-简体中文">简体中文</a> | <a href="#-english">English</a>
</p>

---

## 🇨🇳 简体中文

欢迎使用 **QPyPack**！本指南将带你在 3 分钟内掌握 QPyPack 的核心功能与打包流程，轻松将 Python 脚本或复杂工程项目转换为独立运行的原生可执行程序 (`.exe` / macOS `.app` / Linux 二进制)。

---

### 📥 第一步：安装与启动

你可以根据使用习惯选择以下任意一种方式获取并运行 QPyPack：

#### 方式 A：通过包管理器安装（推荐开发者）

在已配置 Python (>= 3.8) 的终端中执行：

```bash
# 1. 在线安装
pip install qpypack

# 启动 GUI 界面
qpypack
```

*若使用现代包管理器（免全局安装，隔离运行）：*
```bash
# 使用 pipx 隔离运行
pipx run qpypack

# 或使用 uv 极速启动
uvx qpypack
```

*离线安装（使用 Releases 提供的 Wheel 包）：*
```bash
pip install qpypack-2.8.0-py3-none-any.whl
```

#### 方式 B：下载 GitHub Releases 预编译包（适合无 Python 环境用户）

前往 [GitHub Releases 页面](https://github.com/Qwejay/QPyPack/releases) 直接下载对应系统的预编译发布包（以下以QPyPack-2.8.0为例）：

| 操作系统 / 架构 | 发布包文件名 | 版本说明 |
| :--- | :--- | :--- |
| **Windows (x64)** | `QPyPack-2.8.0-windows-x64-Standalone.zip` | **单文件独立版**（解压即为一个干净的单个 `.exe` 文件） |
| **Windows (x64)** | `QPyPack-2.8.0-windows-x64-Portable.zip` | **便携目录版**（包含完整依赖目录，秒级启动，无临时解压延迟） |
| **Linux (x64)** | `QPyPack-2.8.0-linux-x64-Standalone.tar.gz` | **单文件独立版**（解压即用单可执行文件） |
| **Linux (x64)** | `QPyPack-2.8.0-linux-x64-Portable.tar.gz` | **便携目录版**（包含完整运行库目录） |
| **macOS (Apple Silicon)** | `QPyPack-2.8.0-macos-arm64.dmg` | **原生 DMG 镜像**（原生适配 Apple Silicon M1/M2/M3/M4 系列芯片） |
| **全平台 Python** | `qpypack-2.8.0-py3-none-any.whl` | **离线 Wheel 包**（适用于内网或离线环境 `pip install`） |

---

### 🎯 第二步：标准打包 5 步流程

```
 [1. 载入文件/工程] ➔ [2. 引擎与模式] ➔ [3. 附加数据文件] ➔ [4. 依赖与环境] ➔ [5. 构建与产物]
```

#### 1. 载入脚本文件或项目工程文件夹
* **单脚本打包**：将主入口脚本（如 `main.py` 或 `app.pyw`）**直接拖入**主界面的虚线区域。
* **多层级复杂工程打包**：直接将**整个项目总文件夹**拖入主界面，QPyPack 会自动锁定工作区根目录、识别根目录 `requirements.txt`，并自动匹配主入口脚本（若有多个候选入口会弹出点选框）。

#### 2. 选择构建引擎与模式
进入 **「构建设置」** 面板：
* **构建引擎 (Engine)**：
  * **PyInstaller**：构建速度快（通常 10~60 秒），零外部 C 编译器依赖，生态兼容性好。
  * **Nuitka**：将 Python 直接编译为 C/C++ 原生二进制，体积更小、启动更快，具备极强的代码防反编译保护（未检测到本地 C 编译器时，QPyPack 会自动下载托管 MinGW-w64）。
* **打包模式 (Packaging Mode)**：
  * **单文件 (`--onefile`)**：生成单个独立的 `.exe` / 可执行文件，便携干净。
  * **文件夹 (`--onedir`)**：生成包含主程序与 `_internal` 依赖文件夹的目录，适合包含大量静态资源的复杂应用。
* **精简模式 (Lite Mode)**：自动剔除未引用的重型模块并开启 LTO 链接优化，大幅压缩体积（若特殊动态导入报错，切回「兼容模式」即可）。

#### 3. 配置附加资源（静态文件 / 资产）
如果你的程序需要读取额外的外部数据（图片、网页静态资源、配置文件、解密密钥等）：
* 切换到 **【构建设置】 $\rightarrow$ 【附加资源】**；
* 点击「添加文件」或「添加目录」，也可直接把资源文件夹（如 `assets/`、`static/`）拖入列表；
* 支持双击修改打包后的相对存放路径。

#### 4. 依赖管理与环境隔离
* **Python 解释器**：自动检测系统 Python；若未安装，点击「查看 Python」可一键自动下载安装。
* **虚拟环境沙盒 (推荐)**：勾选「使用虚拟环境」可隔离环境污染；勾选「保留虚拟环境」可在重复构建时复用 `.qpypack_venv` 缓存，大幅提速后续打包。
* **智能依赖分析 (AST)**：勾选「分析依赖 (原生 AST)」，系统会自动穿透扫描源码中的隐式依赖，并自动处理包名映射（如 `Crypto` $\to$ `pycryptodome`、`cv2` $\to$ `opencv-python`），同时智能排除本地工程模块，防止 pip 误装报错。

#### 5. 开始构建与获取产物
* 点击主界面底部的 **「开始构建」** 按钮；
* 展开下方的 **「执行日志」** 可实时查看编译输出；
* 构建成功后，点击 **「打开目录」** 即可直接定位到生成的成品程序。

---

### 💡 典型应用场景配置推荐

| 场景需求 | 推荐引擎 | 推荐形态 | 关键设置与建议 |
| :--- | :--- | :--- | :--- |
| **日常小工具 / 自动化脚本** | PyInstaller | 单文件 (`--onefile`) | 自动提取图标 + 勾选「精简模式」 |
| **Web 服务 (FastAPI / Flask)** | PyInstaller / Nuitka | 文件夹 (`--onedir`) | 拖入项目总文件夹 + 附加资源添加 `static/`、`templates/` |
| **商业软件 / 核心算法保护** | Nuitka | 单文件 (`--onefile`) | 勾选「使用虚拟环境」+ 开启数字签名 |
| **大型桌面 GUI (PySide6 / PyQt)** | PyInstaller / Nuitka | 文件夹 (`--onedir`) | 勾选「分析依赖 (原生 AST)」+ 开启「精简模式」剔除未使用子模块 |
| **加解密 / 复杂底层 C 扩展** | PyInstaller | 文件夹 (`--onedir`) | 保持「兼容模式」确保 C 扩展 `.pyd` 完整收录 |

---

### 📋 开发者最佳实践：资源文件路径寻址规范

在单文件模式（`--onefile`）下，打包后的数据文件会在运行时临时解压至特定沙盒目录。请在源码中统一采用以下标准函数获取资源绝对路径，避免路径报错：

```python
import os
import sys
from pathlib import Path

def get_asset_path(relative_path: str) -> Path:
    """获取程序运行时资源的绝对路径（兼容本地开发、PyInstaller 与 Nuitka）"""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller 单文件临时解压目录
        base_path = Path(sys._MEIPASS)
    elif "__compiled__" in globals():
        # Nuitka 二进制执行目录
        base_path = Path(sys.argv[0]).resolve().parent
    else:
        # 本地开发调试目录
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path

# 使用示例：
# logo_path = get_asset_path("assets/logo.png")
# config_path = get_asset_path("config/settings.json")
```

---

### ❓ 常见问题排查 (FAQ)

#### Q1: 打包后运行报错 `ModuleNotFoundError: No module named 'xxx'`？
* **原因**：程序中使用了动态反射导入（如 `importlib`）或某些包的子模块未被静态检测到。
* **解决办法**：在【构建设置】 $\rightarrow$ 【依赖管理】中的「隐式导入 (hidden-imports)」填入缺失的包名（逗号分隔）；或在【附加资源】中将该本地源码包目录添加进去。

#### Q2: 静态资源（图片/配置文件）在单文件打包后读不到？
* **原因**：源码中使用了 `open("assets/config.json")` 相对当前工作目录寻址，而单文件解压到了临时路径。
* **解决办法**：参考上方 [资源文件路径寻址规范](#-开发者最佳实践资源文件路径寻址规范)，使用 `sys._MEIPASS` 兼容代码。对于大型 Web/数据项目，优先推荐使用 **文件夹模式 (`--onedir`)**。

#### Q3: Windows 下运行打包出的程序，瞬间弹出几百个窗口死机？
* **原因**：项目中使用了 `multiprocessing` 多进程，但在 Windows 上未加保护。
* **解决办法**：在主入口文件的 `if __name__ == '__main__':` 块内第一行调用 `multiprocessing.freeze_support()`。

#### Q4: Nuitka 提示缺少 C/C++ 编译器？
* **解决办法**：完全无需手动配置环境变量！QPyPack 内置编译器自动托管机制。未检测到 MSVC 或 GCC 时，Nuitka 会自动下载并配置 MinGW-w64 编译器。

---

## 🇬🇧 English

Welcome to **QPyPack**! This guide helps you master the core features and packaging workflow of QPyPack in 3 minutes, transforming Python scripts and complex projects into standalone native executables (`.exe` / macOS `.app` / Linux binaries).

---

### 📥 Step 1: Installation & Launch

Choose any of the following methods to obtain and launch QPyPack:

#### Method A: Install via Package Manager (Recommended for Developers)

Run in a terminal with Python (>= 3.8):

```bash
# 1. Install via pip
pip install qpypack

# Launch the GUI directly from command line
qpypack
```

*Run in an isolated environment via modern package managers (Zero global install):*
```bash
# Using pipx
pipx run qpypack

# Or using uv for ultra-fast startup
uvx qpypack
```

*Offline installation (using the Release Wheel):*
```bash
pip install qpypack-2.8.0-py3-none-any.whl
```

#### Method B: Standalone Pre-built Releases (For Users without Python)

Download the release asset for your platform from the [GitHub Releases page](https://github.com/Qwejay/QPyPack/releases):

| OS / Architecture | Release Asset | Description |
| :--- | :--- | :--- |
| **Windows (x64)** | `QPyPack-2.8.0-windows-x64-Standalone.zip` | **Standalone Single-File** (Extracts to a single standalone `.exe`) |
| **Windows (x64)** | `QPyPack-2.8.0-windows-x64-Portable.zip` | **Portable Directory** (Full runtime directory, fast launch, zero extraction overhead) |
| **Linux (x64)** | `QPyPack-2.8.0-linux-x64-Standalone.tar.gz` | **Standalone Single-File** (Single executable binary) |
| **Linux (x64)** | `QPyPack-2.8.0-linux-x64-Portable.tar.gz` | **Portable Directory** (Extracted folder with full runtime libraries) |
| **macOS (Apple Silicon)** | `QPyPack-2.8.0-macos-arm64.dmg` | **Native DMG Image** (Native installer for Apple Silicon M1/M2/M3/M4 Macs) |
| **Universal Python** | `qpypack-2.8.0-py3-none-any.whl` | **Offline Wheel** (For offline environments via `pip install`) |

---

### 🎯 Step 2: Standard 5-Step Packaging Workflow

```
 [1. Load Script/Project] ➔ [2. Engine & Mode] ➔ [3. Data Files] ➔ [4. Dependencies] ➔ [5. Build & Output]
```

#### 1. Load Python Script or Project Directory
* **Single Script**: Drag and drop your main entry file (e.g., `main.py` or `app.pyw`) **directly into the drop zone**.
* **Multi-directory Projects**: Drag and drop the **entire project root folder** into the drop zone. QPyPack will automatically lock the workspace root, link the root `requirements.txt`, and match the entry point (prompting an entry selection dialog if multiple candidates exist).

#### 2. Choose Packaging Engine & Mode
Navigate to the **"Build Settings"** panel:
* **Build Engine**:
  * **PyInstaller**: Fast compilation (typically 10–60 seconds), zero compiler dependencies, and extensive ecosystem compatibility.
  * **Nuitka**: Compiles Python directly into native C/C++ binaries, offering smaller output size, faster startup, and deep anti-decompilation protection (MinGW-w64 toolchain is automatically provisioned if no C compiler is detected).
* **Packaging Mode**:
  * **Single-File (`--onefile`)**: Bundles everything into a single standalone executable file.
  * **Directory Mode (`--onedir`)**: Generates an application folder containing the executable and `_internal` dependency tree, ideal for media/web apps with heavy assets.
* **Lite Mode**: Automatically excludes redundant testing/development modules and enables Link-Time Optimization (`--lto=yes`) to reduce binary footprint.

#### 3. Configure Additional Resources (Static Assets)
If your application requires external data files (images, web templates, configs, encryption keys, etc.):
* Switch to **"Build Settings" $\rightarrow$ "Resources"**;
* Click "Add File" or "Add Dir", or drag resource directories (e.g., `assets/`, `static/`) directly into the list;
* Double-click any item to customize its relative bundle target path.

#### 4. Dependency Management & Environment Isolation
* **Python Interpreter**: Automatically detects system Python. Click "View Python" to download and configure one if none is found.
* **Virtual Environment Sandbox (Recommended)**: Check "Use Virtual Environment" to prevent global package pollution. Check "Keep Local Venv" to reuse `.qpypack_venv` cache across builds.
* **AST Dependency Analysis**: Check "Analyze Dependencies (AST)". QPyPack recursively parses Abstract Syntax Trees to detect hidden imports, applies package name mappings (e.g., `Crypto` $\to$ `pycryptodome`, `cv2` $\to$ `opencv-python`), and isolates local modules from triggering redundant pip downloads.

#### 5. Build and Obtain Binaries
* Click the **"Start Build"** button at the bottom;
* Expand the **"Execution Log"** to inspect real-time compiler outputs (switchable between Concise and Detailed modes);
* Upon completion, click **"Open Directory"** to navigate directly to your generated executable.

---

### 💡 Recommended Configurations by Project Type

| Scenario | Recommended Engine | Packaging Mode | Key Settings & Tips |
| :--- | :--- | :--- | :--- |
| **CLI Tools / Quick Scripts** | PyInstaller | Single-File (`--onefile`) | Auto Extract Icon + Enable Lite Mode |
| **Web Services (FastAPI / Flask)** | PyInstaller / Nuitka | Directory (`--onedir`) | Drag project root folder + Add `static/` & `templates/` to Resources |
| **Commercial Software / IP Protection** | Nuitka | Single-File (`--onefile`) | Use Virtual Environment + Enable Smart Code Signing |
| **Desktop GUI (PySide6 / PyQt)** | PyInstaller / Nuitka | Directory (`--onedir`) | Enable AST Analysis + Lite Mode to prune unused submodules |
| **C-Extensions / Cryptography** | PyInstaller | Directory (`--onedir`) | Use Compatibility Mode to ensure all binary `.pyd` files are retained |

---

### 📋 Developer Best Practices: Runtime Asset Path Resolution

In Single-File mode (`--onefile`), bundled data files are extracted to a temporary sandbox directory at runtime. Use the following standard helper function to resolve asset paths across development, PyInstaller, and Nuitka:

```python
import os
import sys
from pathlib import Path

def get_asset_path(relative_path: str) -> Path:
    """Resolve absolute asset path across Dev, PyInstaller, and Nuitka."""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller temporary extraction directory
        base_path = Path(sys._MEIPASS)
    elif "__compiled__" in globals():
        # Nuitka native binary directory
        base_path = Path(sys.argv[0]).resolve().parent
    else:
        # Local development directory
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path

# Usage Example:
# logo_path = get_asset_path("assets/logo.png")
# config_path = get_asset_path("config/settings.json")
```

---

### ❓ Troubleshooting & FAQ

#### Q1: Runtime error `ModuleNotFoundError: No module named 'xxx'` after building?
* **Cause**: Dynamic reflection imports (e.g., `importlib`) or submodules were missed during static analysis.
* **Solution**: In "Build Settings" $\rightarrow$ "Dependencies", add the missing package names to "Hidden Imports", or add the local package directory to "Additional Resources".

#### Q2: Static asset files (images/configs) cannot be found in `--onefile` mode?
* **Cause**: The code uses relative paths like `open("assets/config.json")`, which evaluates relative to `os.getcwd()` rather than the extracted bundle directory.
* **Solution**: Follow the [Runtime Asset Path Resolution](#-developer-best-practices-runtime-asset-path-resolution) pattern using `sys._MEIPASS`. For complex web/data apps, prefer **Directory Mode (`--onedir`)**.

#### Q3: Windows executable spawns hundreds of subprocess windows until crashing?
* **Cause**: The application uses `multiprocessing` without freeze protection on Windows.
* **Solution**: Call `multiprocessing.freeze_support()` as the very first line inside `if __name__ == '__main__':` in your entry script.

#### Q4: Nuitka reports missing C/C++ compiler?
* **Solution**: No manual environment variable setup is required! QPyPack features automated compiler provisioning. If MSVC or GCC is absent, Nuitka will automatically download and manage a compatible MinGW-w64 toolchain.

---

<p align="center">
  📖 <b>Need more advanced optimizations and configuration details?</b><br>
  Please consult the comprehensive <a href="README.md">README.md</a> or visit our <a href="https://github.com/Qwejay/QPyPack">GitHub Repository</a>.
</p>
