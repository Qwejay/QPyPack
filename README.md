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
  <strong>现代化、开箱即用的跨平台 Python 应用打包 GUI 工具</strong><br>
  <sub>基于 PyInstaller 与 Nuitka 双引擎驱动，提供可视化配置、静态依赖分析与自动化构建流</sub>
</p>

## 📌 项目概述

**QPyPack** 是一款专为 Python 开发者打造的跨平台图形化打包工具。通过深度整合 **PyInstaller**（解释器与字节码打包）与 **Nuitka**（C/C++ 原生编译）双核心引擎，将繁琐的底层编译参数、隐式依赖分析、环境隔离与资源收集等流程抽象为直观的可视化界面。

无论用于打包轻量命令行脚本，还是包含大型复杂依赖（如 PySide6 / PyQt、Playwright、CustomTkinter、FastAPI 等）的桌面或服务端应用，QPyPack 均可提供稳定、高成功率且可重现的构建体验。

---

## 📸 界面预览 (Screenshots)

<p align="center">
  <img width="32%" alt="主界面（英文）" src="https://github.com/user-attachments/assets/9d16c68e-d283-4020-86c1-9d4791756c29" />
  <img width="32%" alt="主界面（中文）" src="https://github.com/user-attachments/assets/0147460d-1e9e-4612-9b52-9d347d81b7c5" />
  <img width="32%" alt="构建引擎与环境" src="https://github.com/user-attachments/assets/0ad4db6d-b008-4018-bd69-40a369a10b7d" />
  <br />
  <img width="32%" alt="依赖管理与扫描" src="https://github.com/user-attachments/assets/c7fd1218-d079-4898-a97c-aa980c4d1375" />
  <img width="32%" alt="优化、签名与安全" src="https://github.com/user-attachments/assets/e5b7500e-2a0d-4c6d-b20b-7d8d2d3bac8d" />
  <img width="32%" alt="关于与系统信息" src="https://github.com/user-attachments/assets/e652b222-49f5-44cd-ad3f-d93369ede26b" />
</p>

---

## 🛠️ 核心架构与特性

### 1. 双构建引擎与精简优化
* **双引擎无缝切换**：
  * **PyInstaller**：构建速度快，零 C 编译器依赖，兼具优异的兼容性与生态支持。
  * **Nuitka**：将 Python 源码直接转译为 C/C++ 二进制，具备执行速度快、抗反编译能力强、产物体积小等特点。
* **LTO 链接优化与模块剪枝**：在精简模式（Lite Mode）下支持开启 `--lto=yes` 链接时间优化；针对 PySide/PyQt 自动识别并剔除未引用的重型子模块（如 WebEngine、3D、Quick 等），有效防止产物体积冗余。
* **灵活产物形态**：支持 **单文件 (`--onefile`)** 与 **目录模式 (`--onedir`)**，支持自定义依赖内部存放目录 (`--contents-directory`)。

### 2. 静态分析与依赖拓扑防护
* **原生 AST 递归扫描**：内置纯 Python 实现的抽象语法树（AST）静态分析器，无需执行代码即可递归分析源码及项目目录中的依赖导入。
* **智能包名映射系统**：内置主流第三方库导入名与 PyPI 包名映射表（如 `cv2` $\to$ `opencv-python`、`PIL` $\to$ `pillow`、`win32com` $\to$ `pywin32`），支持用户自定义扩展。
* **废弃兼容包动态隔离 (Backport Isolation)**：自动识别并屏蔽与目标 Python 版本内置模块冲突的过时 Backport 库（如在 Python 3.10+ 下自动隔离 `pathlib`、`typing` 等），防止运行时引发不可预测的命名空间覆盖。

### 3. 环境自动化管理与容错机制
* **C/C++ 编译器自动托管**：自动检测本地 MSVC、Clang (LLVM) 与 GCC 环境；在缺失本地编译器时，Nuitka 引擎将自动下载并托管兼容的 MinGW-w64 工具链。
* **环境生命周期管理**：支持独立隔离虚拟环境与共享虚拟环境模式；支持对历史失效虚拟环境的一键扫描与空间清理。
* **自适应资源与错误自愈**：
  * 构建前自动评估磁盘与物理内存，低内存状态下自适应下调并发数（Adaptive Concurrency）。
  * 自动拦截内存分配溢出（OOM / ZstdError）并自动降级为单线程低内存模式重试。
  * 自动规避 Windows 杀毒软件对中间图标/临时文件的独占锁定。

### 4. 代码签名与交付保障
* **智能数字签名托管**：支持在 Windows 产物输出后自动应用 Authenticode 数字签名（兼容 Signtool 与 PowerShell 引擎，集成 RFC 3161 时间戳服务）；支持 macOS 下的一键 `codesign` 代码签名。
* **自签名证书套件**：内置 Windows 自签名代码签名证书（`.pfx`）生成工具，支持商业私钥证书与密码配置。
* **项目配置预设导入/导出**：支持将所有构建参数、资源清单与映射规则导出为独立的 `.qpypack` 项目工程预设文件，便于团队共享与持续集成。

### 5. 跨平台交互体验
* **拖拽即用**：直接拖入 Python 源码即可自动解析模块元数据（版本、作者、应用名）、推导入口点并匹配同级资源图标。
* **矢量渲染与全球化 i18n**：全界面基于 Google Material SVG 矢量图标绘制，完美适配 4K/高分屏 DPI 缩放；内置涵盖简繁中文、英语、日语、韩语、德语、法语等 17 种语言的即时国际化系统。

---

## 📊 引擎选型对比 (PyInstaller vs. Nuitka)

| 评估维度 | PyInstaller | Nuitka |
| :--- | :--- | :--- |
| **打包原理** | 打包 Python 解释器与字节码文件 (`.pyc`) | 将 Python 代码编译为原生 C/C++ 二进制文件 |
| **构建速度** | 极快（通常 10 ~ 60 秒） | 较慢（涉及 C++ 代码生成与编译器优化） |
| **C/C++ 编译器依赖** | 无需任何外部编译器 | 依赖 MSVC / GCC / Clang（支持自动托管下载） |
| **代码保护等级** | 基础（可通过反编译工具还原源码逻辑） | 极高（原生机器码，深层抗逆向分析） |
| **产物运行性能** | 接近原生 Python 运行速度 | 启动速度快，部分循环与计算密集型逻辑更优 |
| **推荐适用场景** | 快速迭代测试、内部工具、复杂动态导入项目 | 商业交付软件、核心算法保护、追求体积与启动速度 |

---

## ⚡ 快速开始 (Quick Start)

> 💡 **首次使用？** 建议查阅 3 分钟 [**📖 快速入门指南 (QUICKSTART.md)**](QUICKSTART.md) 了解详细的使用教程与典型场景配置指南。

### 安装方式 1：通过 pip / pipx 安装（推荐）

在 Python >= 3.8 的环境中执行：

```bash
# 通过 pip 安装
pip install qpypack

# 启动图形界面
qpypack
```

*若使用现代包管理器（推荐）：*
```bash
# 使用 pipx 隔离运行
pipx run qpypack

# 或使用 uv 极速启动
uvx qpypack
```

### 安装方式 2：使用独立预编译免安装版

无需预先安装 Python 环境，可直接在 GitHub Release 页面下载适用于您操作系统的可执行文件：

👉 [**下载预编译版本 (GitHub Releases)**](https://github.com/Qwejay/QPyPack/releases)

---

## 📋 常用配置说明

### 依赖与资源释放路径 (`sys._MEIPASS`)
在单文件打包模式下，附加的数据文件（图片、配置、模型等）会在运行时临时解压至特定沙盒目录。请确保在源码中按如下标准方式解析路径：

```python
import sys
import os
from pathlib import Path

def get_asset_path(relative_path: str) -> Path:
    """获取打包后资源的绝对路径"""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller 单文件解压目录
        base_path = Path(sys._MEIPASS)
    elif "__compiled__" in globals():
        # Nuitka 二进制运行目录
        base_path = Path(sys.argv[0]).resolve().parent
    else:
        # 开发调试环境目录
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path
```

---

## 📅 版本更新历史 (Changelog)

详细的版本演进路线、功能新增与缺陷修复说明请参阅 [CHANGELOG.md](CHANGELOG.md)。

---

## 💖 参与贡献与赞助 (Sponsorship & Contributing)

QPyPack 是一个遵循开源理念的项目。如果您在日常开发或工作中受益于本项目，欢迎通过以下方式支持本项目的长期维护与迭代：

- 🌟 **Star 支持**：在 [GitHub](https://github.com/Qwejay/QPyPack) 上为项目点亮 Star。
- 🐛 **反馈与建议**：提交 [Issue](https://github.com/Qwejay/QPyPack/issues) 反馈缺陷或提出改进需求。
- ⚡ **赞助项目**：通过 [爱发电平台](https://www.ifdian.net/a/qwejay) 进行无偿资助（支持微信 / 支付宝）。

> *注：赞助属于对开源社区项目的无偿鼓励，不涉及任何商业承诺或定制开发服务。感谢所有支持开源社区建设的开发者！*

---

## 📄 开源许可 (License)

本项目基于 [GNU General Public License v3.0 (GPL-3.0)](LICENSE) 协议开源。

> [!IMPORTANT]
> **关于构建产物的版权说明**：
> 使用 QPyPack 构建生成的最终应用程序与二进制产物，其**知识产权与开源授权完全由使用者自行决定**，QPyPack 的 GPL-3.0 许可协议不会对您的编译产物施加传染性约束。

<p align="right">Copyright (C) 2026 QwejayHuang.</p>