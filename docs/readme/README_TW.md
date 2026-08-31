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
    <img src="https://img.shields.io/github/stars/Qwejay/QPyPack.svg?logo=github&color=gold" alt="GitHub 星星數" />
  </a>
</p>

---

<p align="center">
  <strong>現代化、開箱即用的跨平台 Python 應用程式打包 GUI 工具</strong><br>
  <sub>基於 PyInstaller 與 Nuitka 雙引擎驅動，提供視覺化配置、靜態相依性分析與自動化建置工作流程</sub>
</p>

## 📌 專案概述

**QPyPack** 是一款專為 Python 開發者打造的跨平台圖形化打包工具。透過深度整合 **PyInstaller**（直譯器與位元組碼打包）與 **Nuitka**（C/C++ 原生編譯）雙核心引擎，將繁瑣的底層編譯參數、隱式相依性分析、環境隔離與資源收集等流程轉化為直觀的可視化介面。

無論是用於打包輕量命令列指令碼，還是包含大型複雜相依性（如 PySide6 / PyQt、Playwright、CustomTkinter、FastAPI 等）的桌面或伺服端應用，QPyPack 均可提供穩定、高成功率且可重現的建置體驗。

---

## 📸 介面預覽 (Screenshots)

<p align="center">
  <img width="32%" alt="主介面（英文）" src="https://github.com/user-attachments/assets/9d16c68e-d283-4020-86c1-9d4791756c29" />
  <img width="32%" alt="主介面（中文）" src="https://github.com/user-attachments/assets/0147460d-1e9e-4612-9b52-9d347d81b7c5" />
  <img width="32%" alt="建置引擎與環境" src="https://github.com/user-attachments/assets/0ad4db6d-b008-4018-bd69-40a369a10b7d" />
  <br />
  <img width="32%" alt="相依性管理與掃描" src="https://github.com/user-attachments/assets/c7fd1218-d079-4898-a97c-aa980c4d1375" />
  <img width="32%" alt="最佳化、簽名與安全" src="https://github.com/user-attachments/assets/e5b7500e-2a0d-4c6d-b20b-7d8d2d3bac8d" />
  <img width="32%" alt="關於與系統資訊" src="https://github.com/user-attachments/assets/e652b222-49f5-44cd-ad3f-d93369ede26b" />
</p>

---

## 🛠️ 核心架構與特性

### 1. 雙建置引擎與精簡最佳化
* **雙引擎無縫切換**：
  * **PyInstaller**：建置速度快，零 C 編譯器相依，兼具優異的相容性與生態支援。
  * **Nuitka**：將 Python 原始碼直接轉譯為 C/C++ 二進位檔，具備執行速度快、抗反編譯能力強、產物體積小等特點。
* **LTO 連結最佳化與模組修剪**：在精簡模式（Lite Mode）下支援開啟 `--lto=yes` 連結時間最佳化；針對 PySide/PyQt 自動識別並剔除未引用的重型子模組（如 WebEngine、3D、Quick 等），有效防止產物體積冗餘。
* **靈活產物形態**：支援 **單檔案 (`--onefile`)** 與 **目錄模式 (`--onedir`)**，支援自訂相依性內部存放目錄 (`--contents-directory`)。

### 2. 靜態分析與相依性拓撲防護
* **原生 AST 遞迴掃描**：內建純 Python 實現的抽象語法樹（AST）靜態分析器，無需執行程式碼即可遞迴分析原始碼及專案目錄中的相依性匯入。
* **智慧套件名稱對應系統**：內建主流第三方函式庫匯入名稱與 PyPI 套件名稱對應表（如 `cv2` $\to$ `opencv-python`、`PIL` $\to$ `pillow`、`win32com` $\to$ `pywin32`），支援使用者自訂擴充。
* **廢棄相容套件動態隔離 (Backport Isolation)**：自動識別並屏蔽與目標 Python 版本內建模組衝突的過時 Backport 函式庫（如在 Python 3.10+ 下自動隔離 `pathlib`、`typing` 等），防止執行期引發不可預測的命名空間覆蓋。

### 3. 環境自動化管理與容錯機制
* **C/C++ 編譯器自動託管**：自動偵測本機 MSVC、Clang (LLVM) 與 GCC 環境；在缺失本機編譯器時，Nuitka 引擎將自動下載並託管相容的 MinGW-w64 工具鏈。
* **環境生命週期管理**：支援獨立隔離虛擬環境與共享虛擬環境模式；支援對歷史失效虛擬環境的一鍵掃描與空間清理。
* **自適應資源與錯誤自癒**：
  * 建置前自動評估磁碟與實體記憶體，低記憶體狀態下自適應下調並行數（Adaptive Concurrency）。
  * 自動攔截記憶體配置溢位（OOM / ZstdError）並自動降級為單執行緒低記憶體模式重試。
  * 自動規避 Windows 防毒軟體對中繼圖示/暫存檔案的獨占鎖定。

### 4. 程式碼簽名與交付保障
* **智慧數位簽名託管**：支援在 Windows 產物輸出後自動套用 Authenticode 數位簽名（相容 Signtool 與 PowerShell 引擎，整合 RFC 3161 時間戳記服務）；支援 macOS 下的一鍵 `codesign` 程式碼簽名。
* **自簽名憑證套件**：內建 Windows 自簽名程式碼簽名憑證（`.pfx`）產生工具，支援商業私密金鑰憑證與密碼配置。
* **專案配置預設匯入/匯出**：支援將所有建置參數、資源清單與對應規則匯出為獨立的 `.qpypack` 專案工程預設檔案，便於團隊共享與持續整合。

### 5. 跨平台互動體驗
* **拖放即用**：直接拖入 Python 原始碼即可自動解析模組元資料（版本、作者、應用程式名稱）、推導進入點並匹配同層資源圖示。
* **向量渲染與全球化 i18n**：全介面基於 Google Material SVG 向量圖示繪製，完美適配 4K/高解析度螢幕 DPI 縮放；內建涵蓋簡繁中文、英語、日語、韓語、德語、法語等 17 種語言的即時國際化系統。

---

## 📊 引擎選型對比 (PyInstaller vs. Nuitka)

| 評估維度 | PyInstaller | Nuitka |
| :--- | :--- | :--- |
| **打包原理** | 打包 Python 直譯器與位元組碼檔案 (`.pyc`) | 將 Python 程式碼編譯為原生 C/C++ 二進位檔案 |
| **建置速度** | 極快（通常 10 ~ 60 秒） | 較慢（涉及 C++ 程式碼產生與編譯器最佳化） |
| **C/C++ 編譯器相依** | 無需任何外部編譯器 | 相依 MSVC / GCC / Clang（支援自動託管下載） |
| **程式碼保護等級** | 基礎（可透過反編譯工具還原原始碼邏輯） | 極高（原生機器碼，深層抗逆向分析） |
| **產物執行效能** | 接近原生 Python 執行速度 | 啟動速度快，部分迴圈與計算密集型邏輯更優 |
| **推薦適用場景** | 快速反覆運算測試、內部工具、複雜動態匯入專案 | 商業交付軟體、核心演算法保護、追求體積與啟動速度 |

---

## ⚡ 快速開始 (Quick Start)

> 💡 **首次使用？** 建議查閱 3 分鐘 [**📖 快速入門指南 (QUICKSTART.md)**](../../QUICKSTART.md) 了解詳細的使用教學與典型情境配置指南。

### 安裝方式 1：透過 pip / pipx 安裝（推薦）

在 Python >= 3.8 的環境中執行：

```bash
# 透過 pip 安裝
pip install qpypack

# 啟動圖形介面
qpypack
```

*若使用現代套件管理器（推薦）：*
```bash
# 使用 pipx 隔離執行
pipx run qpypack

# 或使用 uv 極速啟動
uvx qpypack
```

### 安裝方式 2：使用獨立預編譯免安裝版

無需預先安裝 Python 環境，可直接在 GitHub Release 頁面下載適用於您作業系統的可執行檔：

👉 [**下載預編譯版本 (GitHub Releases)**](https://github.com/Qwejay/QPyPack/releases)

---

## 📋 常用配置說明

### 相依性與資源釋放路徑 (`sys._MEIPASS`)
在單檔案打包模式下，附加的資料檔案（圖片、配置、模型等）會在執行期暫時解壓縮至特定沙盒目錄。請確保在原始碼中按如下標準方式解析路徑：

```python
import sys
import os
from pathlib import Path

def get_asset_path(relative_path: str) -> Path:
    """取得打包後資源的絕對路徑"""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller 單檔案解壓縮目錄
        base_path = Path(sys._MEIPASS)
    elif "__compiled__" in globals():
        # Nuitka 二進位執行目錄
        base_path = Path(sys.argv[0]).resolve().parent
    else:
        # 開發偵錯環境目錄
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path
```

---

## 📅 版本更新歷史 (Changelog)

詳細的版本演進路線、功能新增與缺陷修復說明請參閱 [CHANGELOG.md](../../CHANGELOG.md)。

---

## 💖 參與貢獻與贊助 (Sponsorship & Contributing)

QPyPack 是一個遵循開源理念的專案。如果您在日常開發或工作中受益於本專案，歡迎透過以下方式支援本專案的長期維護與反覆運算：

- 🌟 **Star 支援**：在 [GitHub](https://github.com/Qwejay/QPyPack) 上為專案點亮 Star。
- 🐛 **反饋與建議**：提交 [Issue](https://github.com/Qwejay/QPyPack/issues) 反饋缺陷或提出改進需求。
- ⚡ **贊助專案**：透過 [愛發電平台](https://www.ifdian.net/a/qwejay) 進行無償資助（支援微信 / 支付寶）。

> *註：贊助屬於對開源社群專案的無償鼓勵，不涉及任何商業承諾或客製化開發服務。感謝所有支援開源社群建設的開發者！*

---

## 📄 開源許可 (License)

本專案基於 [GNU General Public License v3.0 (GPL-3.0)](../../LICENSE) 協議開源。

> [!IMPORTANT]
> **關於建置產物的版權說明**：
> 使用 QPyPack 建置產生的最終應用程式與二進位產物，其**智慧財產權與開源授權完全由使用者自行決定**，QPyPack 的 GPL-3.0 許可協議不會對您的編譯產物施加傳染性約束。

<p align="right">Copyright (C) 2026 QwejayHuang.</p>
