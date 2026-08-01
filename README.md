# QPyPack

<p align="center">
  <a href="README.md">简体中文</a> |
  <a href="README_EN.md">English</a> |
  <a href="docs/readme/README_TW.md">繁體中文</a> |
  <a href="docs/readme/README_JA.md">日本語</a> |
  <a href="docs/readme/README_KO.md">한국어</a> |
  <a href="docs/readme/README_FR.md">Français</a> |
  <a href="docs/readme/README_DE.md">Deutsch</a> |
  <a href="docs/readme/README_ES.md">Español</a> |
  <a href="docs/readme/README_RU.md">Русский</a> |
  <a href="docs/readme/README_PT.md">Português</a>
</p>

<p align="center">
  <strong>基于 PyInstaller 与 Nuitka 的跨平台 Python 应用可视化打包构建工具</strong>
</p>

<p align="center">
  <!-- PyPI Version -->
  <a href="https://pypi.org/project/qpypack/">
    <img src="https://img.shields.io/pypi/v/qpypack.svg?color=blue&logo=pypi&logoColor=white" alt="PyPI version" />
  </a>
  <!-- Python Versions -->
  <a href="https://pypi.org/project/qpypack/">
    <img src="https://img.shields.io/pypi/pyversions/qpypack.svg?logo=python&logoColor=white" alt="Python versions" />
  </a>
  <!-- PyPI Downloads -->
  <a href="https://pypistats.org/packages/qpypack">
    <img src="https://img.shields.io/pypi/dm/qpypack?color=orange&logo=pypi&logoColor=white" alt="PyPI Downloads" />
  </a>
  <!-- Supported Platforms -->
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-informational" alt="Platform Support" />
  <br>
  <!-- Release Date -->
  <a href="https://github.com/Qwejay/QPyPack/releases">
    <img src="https://img.shields.io/github/release-date/Qwejay/QPyPack?color=brightgreen&logo=github" alt="Release Date" />
  </a>
  <!-- Last Commit -->
  <a href="https://github.com/Qwejay/QPyPack/commits/main">
    <img src="https://img.shields.io/github/last-commit/Qwejay/QPyPack" alt="Last Commit" />
  </a>
  <!-- GitHub License -->
  <a href="https://github.com/Qwejay/QPyPack/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Qwejay/QPyPack.svg" alt="License" />
  </a>
  <!-- GitHub Stars -->
  <a href="https://github.com/Qwejay/QPyPack/stargazers">
    <img src="https://img.shields.io/github/stars/Qwejay/QPyPack.svg?logo=github" alt="GitHub stars" />
  </a>
</p>

QPyPack 是一款致力于简化 Python 应用打包流程的可视化工具。它深度整合了 **PyInstaller** 与 **Nuitka** 两大主流编译引擎，将繁琐的终端命令行参数转化为直观、极简的图形界面交互，帮助开发者高效、高成功率地生成跨平台原生可执行程序。

---

## 📷 界面预览 (Screenshots)

<p align="center">
  <img width="32%" alt="主界面英文预览" src="https://github.com/user-attachments/assets/9d16c68e-d283-4020-86c1-9d4791756c29" />
  <img width="32%" alt="主界面中文预览" src="https://github.com/user-attachments/assets/0147460d-1e9e-4612-9b52-9d347d81b7c5" />
  <img width="32%" alt="设置面板预览" src="https://github.com/user-attachments/assets/0ad4db6d-b008-4018-bd69-40a369a10b7d" />
  <br />
  <img width="32%" alt="依赖管理预览" src="https://github.com/user-attachments/assets/c7fd1218-d079-4898-a97c-aa980c4d1375" />
  <img width="32%" alt="高级优化预览" src="https://github.com/user-attachments/assets/e5b7500e-2a0d-4c6d-b20b-7d8d2d3bac8d" />
  <img width="32%" alt="关于页面预览" src="https://github.com/user-attachments/assets/e652b222-49f5-44cd-ad3f-d93369ede26b" />
</p>

---

## 🚀 核心特性 (Key Features)

QPyPack 旨在解决传统命令行打包配置繁琐、依赖遗漏、跨平台兼容性差以及编译失败率高的问题：

### 1. 现代化 UI 与直观交互体验
* 📥 **拖放式载入 (Drag & Drop)**：只需将 `.py` 或 `.pyw` 源代码文件拖入窗口，系统全自动完成解析与工作区初始化。
* 🎨 **纯矢量图标栈 (Material Design SVG)**：全界面采用 Google Material 矢量图标，全面清理 Emoji 表情，彻底杜绝跨平台系统下字体回退导致的排版乱码与跳动。
* 🌐 **智能多语言 (i18n)**：原生支持简体中文、繁体中文、英文、德语、法语、日语、韩语等全球主流语言，自动识别系统首选语言并支持无缝切换。
* 📊 **双模式实时日志查看器**：引入“精简模式 (Concise)”与“详细模式 (Detailed)”双视图日志面板，支持实时捕获编译引擎极细粒度的编译进度、一键导出与高亮提示。

### 2. 双编译后端与智能环境嗅探
* ⚙️ **PyInstaller & Nuitka 架构**：图形化界面一键切换引擎，根据所选引擎自适应提供针对性的优化选项与参数控制。
* 🔍 **C/C++ 编译器智能嗅探**：Nuitka 引擎下自动探测系统内已安装的 **MSVC**、**Clang** (LLVM) 及 **Zig**（专为 Python 3.13+ C 后端优化）编译器并优先调用，免除繁琐的环境变量设置。
* 💻 **Python 平台兼容性卡片**：动态显示当前选中 Python 解释器对 Windows 7/8/10/11、macOS 及 Linux 的支持状态，并提供官方下载引导。

### 3. 三重安全依赖网与零配置预设
* 🛡️ **隔离虚拟沙盒 (Virtualenv Sandbox)**：一键在系统临时目录创建纯净构建沙盒，避免全局环境污染，极大精简产物体积。
* 🔍 **多维依赖自动补全**：优先读取 `requirements.txt`；搭配深度原生 **AST（静态语法树）** 扫描引擎与 `pipreqs`，精准补齐隐式导入（Hidden Imports）。
* 📦 **免配置第三方库打包预设**：内置对 `ttkbootstrap`、`customtkinter`、`playwright`、`moviepy` 等高频缺失/报错库的自动化打包处理，实现零配置一键生成。
* ⚡ **多源 PIP 镜像与备用切源**：内置主流镜像加速源，支持主源超时自动平滑切换至备用源。

### 4. 强健的构建容错与自愈降级
* 📏 **编译前物理资源评估**：自动评估物理内存与磁盘可用空间，智能调整并发 CPU 核心数。
* 🛡️ **OOM 溢出自愈**：构建过程中遭遇 `ZstdError`（内存溢出）时，自动触发单线程 (`--jobs=1`) 降级重试。
* 🛡️ **图标锁定抗性**：遭遇杀毒软件或系统锁定图标文件时，自动触发剥离图标参数自愈构建，保障二进制产物顺利生成。
* ☁️ **云盘锁定预警**：前置感知识别 OneDrive / Dropbox 等云盘对文件的锁定同步状态并提供明确排查提示。

### 5. 资源管理与应用元数据
* 📝 **PE / Plist 元数据注入**：直接在界面设定版本号、公司名、产品描述，全自动写入 Windows PE VersionInfo 或 macOS `Info.plist` 结构。
* 📂 **可视化附加资源管理**：提供列表化界面管理附加文件与文件夹，支持双击直接编辑打包后的相对释放路径（自适应路径映射）。

---

## ⚡ 快速上手 (Quick Start)

### 方法一：通过 pip 安装并运行

在 Python >= 3.8 的环境中，执行以下命令进行安装与启动：

```bash
# 安装 QPyPack
pip install qpypack

# 启动程序
qpypack
```

### 方法二：下载独立二进制免安装版

如果您不想配置本地 Python 环境，可直接在 GitHub Release 页面下载对应系统的预编译打包版本：
👉 [下载预编译版本 (GitHub Releases)](https://github.com/Qwejay/QPyPack/releases)

---

## 📅 更新日志 (Changelog)

完整的版本更新历史与 Release 说明请参阅 [CHANGELOG.md](CHANGELOG.md) 或 [GitHub Releases 页面](https://github.com/Qwejay/QPyPack/releases)。

---

## 💖 赞助支持 (Sponsorship)

QPyPack 是一款完全开源且免费的项目，由作者利用业余时间开发与维护。如果本项目帮助您提高了开发效率或解决了打包难题，欢迎通过以下方式对项目进行**自愿赞助**。您的支持将是本项目持续更新的重要动力：

- ⚡ **请作者喝咖啡**：[赞助支持 QPyPack](https://www.ifdian.net/a/qwejay)（支持微信 / 支付宝）

> **赞助说明**：赞助完全出于自愿，属于对开源项目的无偿鼓励，不包含任何商业服务绑定或特定功能开发承诺。非常感谢每一位支持开源创作的朋友！

---

## 📄 开源协议 (License)

本项目基于 [GNU General Public License v3.0](LICENSE) 开源，允许在遵循协议条款的前提下自由分发、修改和二次开发。

> [!NOTE]
> **关于打包产物的版权**：
> 使用 QPyPack 构建生成的二进制文件/应用程序，其版权和开源许可**完全由使用者自行决定**，QPyPack 的 GPL-3.0 协议不会约束或影响用户打包后的程序。

Copyright (C) 2026 QwejayHuang.
