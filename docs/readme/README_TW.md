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
  <strong>基於 PyInstaller 與 Nuitka 的跨平台 Python 應用程式視覺化打包建置工具</strong>
</p>

<p align="center">
  <!-- PyPI Version -->
  <a href="https://pypi.org/project/qpypack/">
    <img src="https://img.shields.io/pypi/v/qpypack.svg?color=blue&logo=pypi&logoColor=white" alt="PyPI 版本" />
  </a>
  <!-- Python Versions -->
  <a href="https://pypi.org/project/qpypack/">
    <img src="https://img.shields.io/pypi/pyversions/qpypack.svg?logo=python&logoColor=white" alt="Python 版本" />
  </a>
  <!-- PyPI Downloads -->
  <a href="https://pypistats.org/packages/qpypack">
    <img src="https://img.shields.io/pypi/dm/qpypack?color=orange&logo=pypi&logoColor=white" alt="PyPI 下載量" />
  </a>
  <!-- Supported Platforms -->
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-informational" alt="支援平台" />
  <br>
  <!-- Release Date -->
  <a href="https://github.com/Qwejay/QPyPack/releases">
    <img src="https://img.shields.io/github/release-date/Qwejay/QPyPack?color=brightgreen&logo=github" alt="釋出日期" />
  </a>
  <!-- Last Commit -->
  <a href="https://github.com/Qwejay/QPyPack/commits/main">
    <img src="https://img.shields.io/github/last-commit/Qwejay/QPyPack" alt="最新提交" />
  </a>
  <!-- GitHub License -->
  <a href="https://github.com/Qwejay/QPyPack/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Qwejay/QPyPack.svg" alt="開源條款" />
  </a>
  <!-- GitHub Stars -->
  <a href="https://github.com/Qwejay/QPyPack/stargazers">
    <img src="https://img.shields.io/github/stars/Qwejay/QPyPack.svg?logo=github" alt="GitHub 星星數" />
  </a>
</p>

QPyPack 是一款致力於簡化 Python 應用程式打包流程的視覺化工具。它深度整合了 **PyInstaller** 與 **Nuitka** 兩大主流編譯引擎，將繁瑣的終端機命令列參數轉化為直觀、極簡的圖形介面互動，協助開發者高效、高成功率地產生跨平台原生可執行程式。

---

## 📷 介面預覽 (Screenshots)

<p align="center">
<img width="1173" height="1067" alt="主介面預覽" src="https://github.com/user-attachments/assets/6cf1e937-d35f-4e71-b4e7-7fd86f771d20" />
<img width="1173" height="1067" alt="設定面板預覽" src="https://github.com/user-attachments/assets/b4f563fb-328b-4615-8522-e4f9e490f759" />
<img width="1173" height="1067" alt="相依性管理預覽" src="https://github.com/user-attachments/assets/522d7a3b-9a01-4387-8e81-def4cabcbfff" />
<img width="1173" height="1067" alt="進階優化預覽" src="https://github.com/user-attachments/assets/c8a89212-bf48-40d0-8125-98595f6052bd" />
<img width="1173" height="1067" alt="關於頁面預覽" src="https://github.com/user-attachments/assets/3f5b803a-3c96-493c-b56b-e11f50bd9139" />
</p>

---

## 🚀 核心特性 (Key Features)

QPyPack 旨在解決傳統命令列打包設定繁瑣、相依性遺漏、跨平台相容性差以及編譯失敗率高的問題：

### 1. 現代化 UI 與直觀互動體驗
* 📥 **拖放式載入 (Drag & Drop)**：只需將 `.py` 或 `.pyw` 原始程式碼檔案拖入視窗，系統全自動完成剖析與工作區初始化。
* 🎨 **純向量圖示棧 (Material Design SVG)**：全介面採用 Google Material 向量圖示，全面清理 Emoji 表情，徹底杜絕跨平台系統下字型遞補導致的排版亂碼與跳動。
* 🌐 **智慧多語言 (i18n)**：原生支援簡體中文、繁體中文、英文、德語、法語、日語、韓語等全球主流語言，自動辨識系統偏好語言並支援無縫切換。
* 📊 **雙模式即時日誌檢視器**：引入「精簡模式 (Concise)」與「詳細模式 (Detailed)」雙檢視日誌面板，支援即時擷取編譯引擎極細粒度的編譯進度、一鍵匯出與高亮提示。

### 2. 雙編譯後端與智慧環境偵測
* ⚙️ **PyInstaller & Nuitka 架構**：圖形化介面一鍵切換引擎，根據所選引擎自適應提供針對性的優化選項與參數控制。
* 🔍 **C/C++ 編譯器智慧偵測**：Nuitka 引擎下自動偵測系統內已安裝的 **MSVC**、**Clang** (LLVM) 及 **Zig**（專為 Python 3.13+ C 後端優化）編譯器並優先呼叫，免除繁瑣的環境變數設定。
* 💻 **Python 平台相容性卡片**：動態顯示當前選中 Python 解譯器對 Windows 7/8/10/11、macOS 及 Linux 的支援狀態，並提供官方下載引導。

### 3. 三重安全相依性網與零設定預設
* 🛡️ **隔離虛擬沙盒 (Virtualenv Sandbox)**：一鍵在系統暫存目錄建立純淨建置沙盒，避免全域環境污染，極大精簡產物體積。
* 🔍 **多維相依性自動補全**：優先讀取 `requirements.txt`；搭配深度原生 **AST（靜態語法樹）** 掃描引擎與 `pipreqs`，精準補齊隱式匯入（Hidden Imports）。
* 📦 **免設定第三方套件打包預設**：內建對 `ttkbootstrap`、`customtkinter`、`playwright`、`moviepy` 等高頻缺失/報錯套件的自動化打包處理，實現零設定一鍵產生。
* ⚡ **多源 PIP 鏡像與備用切源**：內建主流鏡像加速源，支援主源逾時自動平滑切換至備用源。

### 4. 強健的建置容錯與自癒降級
* 📏 **編譯前實體資源評估**：自動評估實體記憶體與磁碟可用空間，智慧調整併發 CPU 核心數。
* 🛡️ **OOM 記憶體溢出自癒**：建置過程中遭遇 `ZstdError`（記憶體溢出）時，自動觸發單執行緒 (`--jobs=1`) 降級重試。
* 🛡️ **圖示鎖定抗性**：遭遇防毒軟體或系統鎖定圖示檔案時，自動觸發剝離圖示參數自癒建置，保障二進位產物順利產生。
* ☁️ **雲端硬碟鎖定預警**：前置感知識別 OneDrive / Dropbox 等雲端硬碟對檔案的鎖定同步狀態並提供明確排查提示。

### 5. 資源管理與應用程式元資料
* 📝 **PE / Plist 元資料注入**：直接在介面設定版本號、公司名稱、產品描述，全自動寫入 Windows PE VersionInfo 或 macOS `Info.plist` 結構。
* 📂 **視覺化附加資源管理**：提供列表化介面管理附加檔案與資料夾，支援雙擊直接編輯打包後的相對釋放路徑（自適應路徑對映）。

---

## ⚡ 快速上手 (Quick Start)

### 方法一：透過 pip 安裝並執行

在 Python >= 3.8 的環境中，執行以下命令進行安裝與啟動：

```bash
# 安裝 QPyPack
pip install qpypack

# 啟動程式
qpypack
```

### 方法二：下載獨立二進位免安裝版

如果您不想設定本地 Python 環境，可直接在 GitHub Release 頁面下載對應系統的預編譯打包版本：
👉 [下載預編譯版本 (GitHub Releases)](https://github.com/Qwejay/QPyPack/releases)

---

## 📅 更新日誌 (Changelog)

完整的版本更新歷史與 Release 說明請參閱 [CHANGELOG.md](../../CHANGELOG.md) 或 [GitHub Releases 頁面](https://github.com/Qwejay/QPyPack/releases)。

---

## 💖 贊助支援 (Sponsorship)

QPyPack 是一款完全開源且免費的專案，由作者利用業餘時間開發與維護。如果本專案協助您提高了開發效率或解決了打包難題，歡迎透過以下方式對專案進行**自願贊助**。您的支援將是本專案持續更新的重要動力：

- ⚡ **請作者喝咖啡**：[贊助支援 QPyPack](https://www.ifdian.net/a/qwejay)（支援微信 / 支付寶）

> **贊助說明**：贊助完全出於自願，屬於對開源專案的無償鼓勵，不包含任何商業服務繫結或特定功能開發承諾。非常感謝每一位支援開源創作的朋友！

---

## 📄 開源條款 (License)

本專案基於 [GNU General Public License v3.0](LICENSE) 開源，允許在遵循條款的前提下自由分發、修改和二次開發。

> [!NOTE]
> **關於打包產物的版權**：
> 使用 QPyPack 建置產生的二進位檔案/應用程式，其版權和開源許可**完全由使用者自行決定**，QPyPack 的 GPL-3.0 協議不會約束或影響使用者打包後的程式。

Copyright (C) 2026 QwejayHuang.