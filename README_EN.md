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
  <strong>A Modern Cross-Platform Python Application Packaging & Compilation Suite Powered by PyInstaller and Nuitka</strong>
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

QPyPack is a visual GUI tool designed to simplify Python application packaging workflows. It deeply integrates two major compilation engines—**PyInstaller** and **Nuitka**—converting tedious CLI arguments into an intuitive graphical interface, helping developers generate cross-platform native executables efficiently and reliably.

---

## 📷 Screenshots

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

## 🚀 Key Features

QPyPack addresses configuration complexity, missing implicit dependencies, cross-platform glitches, and high compilation failure rates in traditional CLI workflows:

### 1. Modern UI & Intuitive UX
* 📥 **Drag & Drop Workspace**: Simply drop `.py` or `.pyw` source files into the window; QPyPack will automatically parse and initialize the workspace.
* 🎨 **Pure Vector Icon Stack (Material Design SVG)**：Cleaned up emoji icons in favor of Google Material SVG vector icons, completely eliminating font fallback issues and alignment glitches across Linux and older Windows systems.
* 🌐 **Native i18n Support**: Multilingual UI support out-of-the-box (English, Simplified/Traditional Chinese, German, French, Japanese, Korean, etc.) with auto-detection and live switching.
* 📊 **Dual-Mode Live Log Viewer**: Toggle between "Concise" and "Detailed" log panels with real-time build status tracking, error highlighting, and log export.

### 2. Dual Compilation Backends & Compiler Sniffing
* ⚙️ **PyInstaller & Nuitka Integration**: Seamlessly switch engines via GUI, with dynamic UI controls that adapt based on the selected backend.
* 🔍 **Smart Compiler Auto-Detection**: Automatically sniffs and prioritizes system C/C++ compilers for Nuitka, including **MSVC**, **Clang** (LLVM), and **Zig** (optimized for Python 3.13+ C backends).
* 💻 **Platform Compatibility Matrix**: Real-time status cards displaying OS support (Windows 7/8/10/11, macOS, Linux) for selected Python interpreters with official download shortcuts.

### 3. Robust Dependency Resolution & Zero-Config Presets
* 🛡️ **Isolated Virtualenv Sandbox**: Create pristine temporary build sandboxes with one click, eliminating global package pollution and minimizing output binary sizes.
* 🔍 **Triple-Layer Dependency Protection**: Reads `requirements.txt`, runs deep native **AST (Abstract Syntax Tree)** static analysis, and executes `pipreqs` to automatically catch hidden imports.
* 📦 **Zero-Config Third-Party Presets**: Built-in automated handling for error-prone libraries like `ttkbootstrap`, `customtkinter`, `playwright`, `moviepy`, and more.
* ⚡ **Multi-Mirror PIP Management**: Integrated PyPI mirror presets with automatic fallback to secondary index sources on network timeout.

### 4. Build Resilience & Self-Healing Fallbacks
* 📏 **Pre-flight Resource Evaluation**: Assesses available RAM and disk space before build, dynamically adjusting CPU concurrency.
* 🛡️ **OOM Fallback Recovery**: Automatically triggers single-thread retry mode (`--jobs=1`) when catching `ZstdError` / Out-Of-Memory exceptions.
* 🛡️ **Antivirus/Icon Lock Resilience**: Automatically strips icon parameters and retries build if icon resource writing is blocked by security software or system locks.
* ☁️ **Cloud Storage Lock Alerts**: Detects file synchronization locks caused by OneDrive, Dropbox, or other cloud drives and provides clear diagnostic tips.

### 5. Data File Management & Metadata Injection
* 📝 **PE / Plist Metadata Injection**: Configure version strings, company names, and application descriptions via GUI; automatically writes Windows PE VersionInfo or macOS `Info.plist` bundles.
* 📂 **Visual Data Files Management**: Manage supplementary files and directories in a structured list with inline double-click editing for relative output destination paths.

---

## ⚡ Quick Start

### Method 1: Install via pip

Ensure you are using Python >= 3.8:

```bash
# Install QPyPack
pip install qpypack

# Launch
qpypack
```

### Method 2: Download Standalone Binaries

Download pre-compiled standalone executables directly from GitHub Releases:
👉 [GitHub Releases](https://github.com/Qwejay/QPyPack/releases)

---

## 📅 Changelog

For detailed update history and release notes, please refer to [CHANGELOG.md](CHANGELOG.md) or [GitHub Releases](https://github.com/Qwejay/QPyPack/releases).

---

## 💖 Sponsorship

QPyPack is an open-source project developed and maintained by the author in their free time. If QPyPack has improved your efficiency or solved packaging challenges, consider supporting the project with a voluntary donation:

- ⚡ **Buy the Author a Coffee**: [Sponsor QPyPack](https://www.ifdian.net/a/qwejay)

> **Note**: Sponsorship is completely voluntary and represents unconditional encouragement to open-source development, involving no commercial commitments or specific feature promises. Thank you for your support!

---

## 📄 License

Open-sourced under the [GNU General Public License v3.0](LICENSE).

> [!NOTE]
> **Regarding Binary Product Licensing**:
> Binaries and applications built using QPyPack are **entirely owned by the user**. QPyPack's GPL-3.0 license does not restrict or apply to your compiled output binaries.

Copyright (C) 2026 QwejayHuang.
