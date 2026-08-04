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
  🚀 <i>“Drag, drop, and build — QPyPack takes care of the rest!”</i>
</h2>
<p align="center">
  <sub><strong>只需拖入 Python 代码，剩下的交给 QPyPack！</strong></sub>
</p>

## 💡 What is QPyPack?

QPyPack is a modern cross-platform Python packaging GUI tool. It deeply integrates **PyInstaller** and **Nuitka** core compilation engines, transforming tedious CLI flags and compiler environment setups into an intuitive, high-success graphical interface experience.

Whether you are bundling lightweight scripts or complex applications (e.g., PySide/PyQt, Playwright, CustomTkinter, MoviePy), QPyPack helps you build standalone, efficient, native cross-platform binaries effortlessly.

---

## 🌟 Why Choose QPyPack?

* **Say Goodbye to CLI Nightmares**: No need to memorize `--hidden-import`, `--add-data` syntax, or path separator variations across OSes.
* **Zero C/C++ Compiler Friction**: Automatically detects local MSVC, Clang, or GCC environments; downloads and manages MinGW-w64 toolchains seamlessly when none are present.
* **Eliminate Runtime `ModuleNotFoundError`**: Powered by a "Triple-Layer Safety Net" (`requirements.txt` + Native AST Static Analysis + `pipreqs`) to ensure missing implicit dependencies are automatically resolved.
* **Resilient Build Execution**: Includes pre-flight memory evaluations, OOM (out-of-memory) fallback retries, antivirus/icon lock recovery, and temp directory sandboxing.

---

## 📷 Screenshots

<p align="center">
  <img width="32%" alt="Main UI" src="https://github.com/user-attachments/assets/c7c8ce04-b572-4d79-845b-101ba9598837" />
  <img width="32%" alt="Build Settings" src="https://github.com/user-attachments/assets/bd4f35c8-d260-4b95-bb63-31fbbe1b17e7" />
  <img width="32%" alt="Dependencies" src="https://github.com/user-attachments/assets/30999990-be5a-47fe-b03d-f7bf8ae2e30b" />
</p>

---

## 🚀 Key Features

- ✨ **Drag, Drop & Go**: Simply drop `.py` / `.pyw` files; QPyPack auto-parses metadata, matches application icons, and initializes the workspace.
- 🐍 **Smart Python Environment Manager**: Built-in environment dialog supporting intelligent local Python detection/switching, as well as one-click automatic downloading & installation via official or mirror sources.
- ⚙️ **Dual Engines & Flexible Execution Modes**:
  - **PyInstaller**: Rapid build speeds, high compatibility, zero compiler setup.
  - **Nuitka**: Compiles Python source directly to native C/C++ binaries for smaller sizes, faster runtime, and anti-decompilation protection.
  - Supports both **One-File (`--onefile`)** and **Folder Mode (`--onedir`)**, with customizable internal dependencies directory names (`--contents-directory`).
- 🔍 **Seamless C/C++ Compiler Integration**: Auto-detects local MSVC, Clang, or GCC environments, and silently manages MinGW-w64 downloads without manual environment variable setups.
- 🛡️ **Triple-Layer Dependency Protection**: Combines `requirements.txt` parsing, native **AST static analysis**, and environment package mapping to capture all implicit imports.
- 📦 **Zero-Config Presets**: Automated hooks and resource collection for troublesome packages (`ttkbootstrap`, `customtkinter`, `playwright` with mirror acceleration support, `moviepy`, etc.).
- 🛡️ **Resilient Sandboxing & Fallbacks**: Runs pre-flight RAM/disk checks, retries in single-thread concurrency on OOM/ZstdError, and isolates builds in Temp directories to bypass OneDrive sync locks.
- 🎨 **Pure Vector UI & i18n**: Rendered with Google Material SVG vector icons with native multi-language support (English, Chinese, Japanese, Korean, German, French, etc.).

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
