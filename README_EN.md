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

<p align="center">
  <strong>A Modern, Cross-Platform Python Packaging GUI</strong><br>
  <sub>Powered by PyInstaller and Nuitka, featuring visual configuration, static dependency analysis, and automated build workflows.</sub>
</p>

## 📌 Overview

**QPyPack** is a cross-platform graphical packaging tool designed for Python developers. By integrating both **PyInstaller** (bytecode bundling) and **Nuitka** (C/C++ native compilation) core engines, QPyPack abstracts low-level compiler toolchains, complex dependency tracking, sandbox isolation, and resource collection into an intuitive, reliable desktop interface.

Whether you are distributing simple automation scripts or complex enterprise applications (built with PySide6/PyQt, Playwright, CustomTkinter, FastAPI, etc.), QPyPack delivers a reproducible, high-success build experience across Windows, macOS, and Linux.

---

## 📸 Screenshots

<p align="center">
  <img width="32%" alt="Main Interface (English)" src="https://github.com/user-attachments/assets/9d16c68e-d283-4020-86c1-9d4791756c29" />
  <img width="32%" alt="Main Interface (Chinese)" src="https://github.com/user-attachments/assets/0147460d-1e9e-4612-9b52-9d347d81b7c5" />
  <img width="32%" alt="Engine & Environment" src="https://github.com/user-attachments/assets/0ad4db6d-b008-4018-bd69-40a369a10b7d" />
  <br />
  <img width="32%" alt="Dependency Management" src="https://github.com/user-attachments/assets/c7fd1218-d079-4898-a97c-aa980c4d1375" />
  <img width="32%" alt="Optimization & Signing" src="https://github.com/user-attachments/assets/e5b7500e-2a0d-4c6d-b20b-7d8d2d3bac8d" />
  <img width="32%" alt="About & Diagnostics" src="https://github.com/user-attachments/assets/e652b222-49f5-44cd-ad3f-d93369ede26b" />
</p>

---

## 🛠️ Architecture & Key Features

### 1. Dual-Engine Compilation & Binary Optimization
* **Dual Packaging Engines**:
  * **PyInstaller**: Fast compilation, zero compiler dependencies, and extensive ecosystem hook compatibility.
  * **Nuitka**: Translates Python code into native C/C++ binaries, providing performance acceleration, compact size, and deep IP/reverse-engineering protection.
* **LTO & Submodule Pruning**: Lite Mode integrates `--lto=yes` (Link-Time Optimization) and automatically identifies and excludes unused heavy Qt submodules (e.g., `QtWebEngineCore`, `Qt3DCore`, `QtQuick`, `QtLocation`), preventing binary size bloat.
* **Flexible Binary Distribution**: Supports **Single-File (`--onefile`)** and **Directory (`--onedir`)** modes, with customizable internal asset directory paths (`--contents-directory`).

### 2. Static Dependency Analysis & Safety Net
* **Native AST Static Scanner**: Recursively parses Abstract Syntax Trees (AST) across source files and folders to discover explicit and hidden imports without executing the code.
* **Package Distribution Mapper**: Maps common import namespaces to their canonical PyPI distribution names (e.g., `cv2` $\to$ `opencv-python`, `PIL` $\to$ `pillow`, `win32com` $\to$ `pywin32`), with full user customization.
* **Obsolete Backport Isolation**: Automatically detects and shields legacy backport modules that conflict with modern standard libraries (e.g., isolating redundant `pathlib` or `typing` packages on Python 3.10+).

### 3. Toolchain Provisioning & Runtime Self-Healing
* **Automated Compiler Provisioning**: Detects local MSVC, Clang (LLVM), or GCC compilers. If no native C compiler is found, Nuitka automatically provisions a managed MinGW-w64 toolchain.
* **Virtual Environment Management**: Supports isolated sandboxes as well as reusable shared virtual environments, complete with a built-in clean-up utility for legacy project environments.
* **Resource-Aware Concurrency**:
  * Evaluates system RAM and disk space prior to compilation, adaptively adjusting thread concurrency to prevent out-of-memory errors.
  * Recovers from memory allocation failures (`ZstdError` / OOM) by automatically retrying in single-threaded low-memory mode.
  * Mitigates file-locking collisions caused by antivirus software or cloud sync drives during output assembly.

### 4. Code Signing & Project Presets
* **Smart Code Signing**: Automatically applies digital signatures to Windows binaries (supporting Signtool and PowerShell Authenticode engines with RFC 3161 timestamping) and handles macOS `codesign` runtime signing.
* **Certificate Suite**: Includes an integrated self-signed `.pfx` certificate generator and supports custom commercial certificate injection.
* **Preset Import / Export**: Saves complete build parameters, asset mappings, and exclusions into shareable `.qpypack` preset files for CI/CD and team workflows.

### 5. UI/UX & Global Localization
* **Drag-and-Drop Workflow**: Dropping a `.py`/`.pyw` script auto-parses metadata (`__version__`, `__author__`, `__title__`), initializes the workspace, and maps corresponding application icons.
* **Vector UI with HiDPI Support**: Built entirely with Google Material SVG vector icons with native multi-monitor DPI scaling.
* **Full Localization (i18n)**: Out-of-the-box support for 17 languages, including English, Simplified/Traditional Chinese, Japanese, Korean, German, French, Spanish, and Russian.

---

## 📊 Engine Comparison (PyInstaller vs. Nuitka)

| Metric | PyInstaller | Nuitka |
| :--- | :--- | :--- |
| **Mechanism** | Bundles Python interpreter + bytecode (`.pyc`) | Compiles Python code to native C/C++ binaries |
| **Build Time** | Fast (typically 10 – 60 seconds) | Slower (requires C++ code generation & optimization) |
| **C/C++ Compiler** | Not required | Required (MSVC / GCC / Clang / MinGW-w64) |
| **Source Protection** | Basic (can be unpacked via decompilers) | High (compiled machine code; resistant to reverse engineering) |
| **Execution Performance** | Standard Python runtime speed | Fast startup; improved loop and compute efficiency |
| **Ideal For** | Rapid prototyping, internal tools, dynamic import scripts | Commercial distribution, proprietary algorithms, optimized size |

---

## ⚡ Quick Start

> 💡 **First time using QPyPack?** Check out the [**📖 Quickstart Guide (QUICKSTART.md)**](QUICKSTART.md) for step-by-step instructions and recommended project configurations.

### Method 1: Install via pip / pipx (Recommended)

Requires Python >= 3.8:

```bash
# Install QPyPack
pip install qpypack

# Launch the application
qpypack
```

*Or run directly in an isolated environment via modern package managers:*
```bash
# Using pipx
pipx run qpypack

# Using uv
uvx qpypack
```

### Method 2: Standalone Executable

If you prefer not to install Python locally, download pre-built binary releases for Windows, macOS, or Linux:

👉 [**Download Standalone Release (GitHub Releases)**](https://github.com/Qwejay/QPyPack/releases)

---

## 📋 Best Practices: Asset Resolution (`sys._MEIPASS`)

In Single-File mode (`--onefile`), bundled static assets (images, configuration files, model weights) are extracted to a temporary runtime sandbox directory. Use the following helper pattern to reliably resolve paths across development and production:

```python
import sys
import os
from pathlib import Path

def get_asset_path(relative_path: str) -> Path:
    """Resolve asset paths across development, PyInstaller, and Nuitka."""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller temporary extraction directory
        base_path = Path(sys._MEIPASS)
    elif "__compiled__" in globals():
        # Nuitka native binary execution directory
        base_path = Path(sys.argv[0]).resolve().parent
    else:
        # Local development environment
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path
```

---

## 📅 Changelog

For detailed release notes, new features, and bug fixes, please consult [CHANGELOG.md](CHANGELOG.md).

---

## 💖 Contributing & Sponsorship

QPyPack is an open-source project maintained during personal time. If QPyPack has helped streamline your deployment workflow, voluntary sponsorships are warmly welcomed to support continuous development:

- 🌟 **Star the Project**: Give us a star on [GitHub](https://github.com/Qwejay/QPyPack).
- 🐛 **Feedback & Issues**: Submit bug reports and feature requests via [GitHub Issues](https://github.com/Qwejay/QPyPack/issues).
- ⚡ **Sponsor**: Support the author via [Afdian (爱发电)](https://www.ifdian.net/a/qwejay) (WeChat Pay / Alipay).

> *Note: Sponsorship is voluntary and serves as encouragement for open-source maintenance without commercial service commitments. Thank you for your support!*

---

## 📄 License

This project is licensed under the [GNU General Public License v3.0 (GPL-3.0)](LICENSE).

> [!IMPORTANT]
> **Copyright of Compiled Binaries**:
> The ownership, licensing, and distribution rights of applications compiled using QPyPack **belong entirely to the user**. QPyPack's GPL-3.0 license does not apply copyleft restrictions to the software you package.

<p align="right">Copyright (C) 2026 QwejayHuang.</p>