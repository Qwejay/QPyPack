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
    <img src="https://img.shields.io/github/stars/Qwejay/QPyPack.svg?logo=github&color=gold" alt="GitHub stars" />
  </a>
</p>

---

<h2 align="center">
  🚀 <i>“只需拖入 Python 代码，剩下的交给 QPyPack！”</i>
</h2>
<p align="center">
  <sub><strong>Drag, drop, and build — QPyPack takes care of the rest!</strong></sub>
</p>

## 💡 QPyPack 是什么？

QPyPack 是一款现代化的跨平台 Python 打包工具。它深度整合 **PyInstaller** 与 **Nuitka** 双核心打包引擎，将极其繁琐复杂的终端命令行参数与环境配置，转化为极简、直观、高成功的图形界面体验。

无论你是打包简单的脚本工具，还是包含复杂依赖（如 PySide/PyQt, Playwright, CustomTkinter, MoviePy 等）的项目，QPyPack 都能助你轻松生成纯净、高效的跨平台原生可执行文件。

---

## 🌟 为什么选择 QPyPack？

* **告别噩梦般的命令行**：无需再记忆繁琐的 `--hidden-import`、`--add-data` 路径分隔符和参数格式。
* **零门槛 C/C++ 编译器集成**：自动嗅探本地 MSVC、Clang 或 GCC 环境；缺失时免交互自动托管下载 MinGW-w64 工具链，无需手动配置环境变量。
* **告别运行时 `ModuleNotFoundError`**：首创“三重依赖安全网”（Requirements + 原生 AST 语法树扫描 + pipreqs），精准补全隐式依赖。
* **告别打包崩溃与中间死锁**：自动评估物理内存，自带内存溢出（OOM）自愈重试、杀软图标锁定剥离重构建及 Temp 防锁沙盒。

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

- ✨ **极简拖拽，即刻启程**：拖入 `.py` 或 `.pyw` 源代码，全自动完成应用元数据解析、工作区初始化与图标匹配。
- ⚙️ **双打包引擎自由切换**：
  - **PyInstaller**：打包速度快，兼容性极佳，零 C 编译器依赖。
  - **Nuitka**：将源码编译为原生 C/C++ 二进制，体积更小、运行更快、代码深度抗反编译。
- 🔍 **C/C++ 编译器智能托管**：优先调用本地 MSVC、Clang (LLVM) 或 GCC；未检测到本地编译器时，由 Nuitka 自动托管下载兼容的 MinGW-w64 编译器。
- 🛡️ **三重依赖防护网**：融合 `requirements.txt`、原生 **AST 静态语法树** 扫描与 `pipreqs`，智能捕获所有隐式导入（Hidden Imports）。
- 📦 **复杂第三方库零配置预设**：内置对 `ttkbootstrap`、`customtkinter`、`playwright`、`moviepy` 等高频报错/遗漏资源库的自动 Hooks 拦截与资源收集。
- 🛡️ **防锁沙盒与自愈机制**：构建前物理资源评估，捕获内存溢出（OOM/ZstdError）自动降低并发重试，支持 Temp 目录防锁隔离，解决 OneDrive/杀软锁文件导致的构建中断。
- 🎨 **纯矢量 UI & 多语言支持**：全界面基于 Google Material SVG 矢量图标，完美适配高分屏缩放；原生支持中、英、日、韩、德、法等全球多语言无缝切换。

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
