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
  <strong>A Cross-Platform GUI Packaging & Compilation Suite based on PyInstaller and Nuitka</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/qpypack/">
    <img src="https://img.shields.io/pypi/v/qpypack.svg?color=blue" alt="PyPI version" />
  </a>
  <a href="https://pypi.org/project/qpypack/">
    <img src="https://img.shields.io/pypi/pyversions/qpypack.svg" alt="Python versions" />
  </a>
  <a href="https://github.com/Qwejay/QPyPack/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Qwejay/QPyPack.svg" alt="License" />
  </a>
  <a href="https://github.com/Qwejay/QPyPack/stargazers">
    <img src="https://img.shields.io/github/stars/Qwejay/QPyPack.svg" alt="GitHub stars" />
  </a>
</p>

QPyPack is a visual GUI tool designed to simplify Python application packaging workflows. It deeply integrates two major compilation engines—PyInstaller and Nuitka—converting tedious CLI arguments into an intuitive graphical interface, helping developers generate cross-platform native executables efficiently.

---

## 📷 Screenshots

<p align="center">
<img width="1173" height="1067" alt="image" src="https://github.com/user-attachments/assets/3895da6b-b872-4862-a4ad-34aa439e7e3f" />
<img width="1173" height="1067" alt="image" src="https://github.com/user-attachments/assets/a83026ab-e553-41e4-9a25-b69cc4aefc47" />
<img width="1173" height="1067" alt="image" src="https://github.com/user-attachments/assets/ce992be7-9d06-493b-afd9-a89721a53fdc" />
<img width="1173" height="1067" alt="image" src="https://github.com/user-attachments/assets/8a490923-fc7b-4977-94dc-9c5c91e7a184" />
<img width="1173" height="1067" alt="image" src="https://github.com/user-attachments/assets/44520551-56d5-4283-834d-3dab7705e520" />

</p>

---

## 🚀 Key Features

To reduce configuration overhead in traditional CLI builds and resolve cross-platform environment/dependency conflicts, QPyPack provides the following integrated engineering features:

### 1. Intuitive Visual Interaction
* 📥 **Drag & Drop Loading**: Simply drag `.py` or `.pyw` source files into the app window; QPyPack will automatically parse and load them into the workspace.
* 🎨 **Smart Icon Search & Adaptation**: Automatically searches for common icon assets in the source directory (`icon.ico`, `logo.ico`, `icon.svg`, `logo.svg`), performs format conversion, binds them, and provides high-res previews.
* 🌐 **Internationalization (i18n) Support**: Native multi-language interface support (English, Simplified Chinese, etc.) with real-time switching, providing a seamless, obstacle-free experience for global developers.

### 2. Dependency Resolution & Sandbox Isolation
* 🛡️ **Virtualenv Sandbox**: One-click creation of isolated temporary virtual environments to install only minimal required dependencies, significantly reducing output binary size.
* 🔍 **Multi-dimensional Dependency Scanning**:
  * **Config Sync**: Automatically detects and prioritizes `requirements.txt` in the project directory.
  * **AST Static Analysis**: Provides deep Abstract Syntax Tree (AST) scanning to extract non-standard modules and automatically complete hidden imports.
* ⚡ **Built-in PyPI Acceleration Mirrors**: Presets mainstream PyPI mirror channels to drastically speed up package downloading in the sandbox.

### 3. Advanced Compilation Control
* ⚙️ **Dual-Engine Adaptive Switch**: Seamlessly switch between PyInstaller and Nuitka. Parameter panels dynamically adapt based on the selected engine.
* 📝 **Application Metadata Injection**: Write version numbers, company names, and descriptions directly in the UI without editing spec/version files (Supports Windows PE metadata & macOS Info.plist).
* 📂 **Visual Data Files Management**: Add files or folders via GUI lists with double-click editing support for output relative destination paths.
---

## ⚡ Quick Start

### Method 1: Install via pip

```bash
# Install QPyPack
pip install qpypack

# Launch
qpypack
```

### Method 2: Download Standalone Binaries

Download pre-compiled binaries directly from the [GitHub Releases](https://github.com/Qwejay/QPyPack/releases) page.

---

## 📅 Changelog

For detailed release notes and update history, please refer to [CHANGELOG.md](CHANGELOG.md) or [GitHub Releases](https://github.com/Qwejay/QPyPack/releases).

---

## 🤝 Contributing

Issues and Pull Requests are welcome on [GitHub Issues](https://github.com/Qwejay/QPyPack/issues)!

---

## 📄 License

Open-sourced under [GNU General Public License v3.0](LICENSE).

Copyright (C) 2026 QwejayHuang.
