# QPyPack

<p align="center">
  <a href="../../README.md">简体中文</a> |
  <a href="../../README_EN.md">English</a> |
  <a href="README_TW.md">繁體中文</a> |
  <a href="README_JA.md">日本語</a> |
  <a href="README_KO.md">한국어</a> |
  <a href="README_FR.md">Français</a> |
  <a href="README_DE.md">Deutsch</a> |
  <a href="README_ES.md">Español</a> |
  <a href="README_RU.md">Русский</a> |
  <a href="README_PT.md">Português</a>
</p>

<p align="center">
  <strong>基於 PyInstaller 與 Nuitka 的跨平台 Python 應用圖形化打包建置工具</strong>
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

QPyPack 是一款致力於簡化 Python 應用打包流程的圖形化工具。它深度整合了 PyInstaller 與 Nuitka 兩大主流編譯引擎，將繁瑣的命令列引數轉化為直觀、便利的圖形介面互動，幫助開發者更高效地產生跨平台原生可執行程式。

---

## 📷 介面預覽 (Screenshots)

<p align="center">
<img width="1143" height="1067" alt="image" src="https://github.com/user-attachments/assets/8658aaef-5867-470d-ba4d-07892309ab1a" />
<img width="1142" height="1067" alt="image" src="https://github.com/user-attachments/assets/b64d9b89-8bfd-4bf8-8fec-9c75f61305dd" />
</p>

---

## 🚀 核心特性 (Key Features)

### 1. 直觀的圖形化互動體驗
* 📥 **拖放式載入 (Drag & Drop)**：直接將 `.py` 或 `.pyw` 原始碼檔案拖放至視窗即可自動解析。
* 🎨 **圖示智慧偵測與自適應**：自動檢索同級目錄下的圖示資產 (`icon.ico` / `logo.svg` 等) 並進行格式轉換與預覽。

### 2. 依賴解析與虛擬環境沙盒
* 🛡️ **虛擬環境隔離 (Virtualenv Sandbox)**：一鍵建立隔離的虛擬環境，僅安裝最小依賴項以縮減執行檔體積。
* 🔍 **多維度依賴解析**：自動讀取 `requirements.txt` 並透過 AST 靜態掃描補全隱式匯入 (Hidden Imports)。

### 3. 進階編譯參數精準控制
* ⚙️ **雙引擎自適應切換**：支援 PyInstaller 與 Nuitka 的無縫切換。
* 📝 **應用元資料寫入 (Metadata)**：直觀輸入版本號、公司名和描述，自動寫入 PE 屬性或 macOS Info.plist。
* 📂 **附加資源視覺化管理**：清單化管理檔案與資料夾，支援雙擊修改釋放路徑。

---

## ⚡ 快速上手 (Quick Start)

### 通過 pip 安裝並執行

```bash
# 安裝 QPyPack
pip install qpypack

# 啟動程式
qpypack
```

亦可直接在 [GitHub Releases 頁面](https://github.com/Qwejay/QPyPack/releases) 下載預編譯的可執行檔。

---

## 📅 更新記錄 (Changelog)

完整的版本更新歷史與 Release 說明請參閱 [CHANGELOG.md](CHANGELOG.md) 或 [GitHub Releases 頁面](https://github.com/Qwejay/QPyPack/releases)。

---

## 📄 開源協議 (License)

基於 [GNU General Public License v3.0](LICENSE) 協議開源。

Copyright (C) 2026 QwejayHuang.