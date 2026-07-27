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

QPyPack 是一款致力于简化 Python 应用打包流程的可视化工具。它深度整合了 PyInstaller 与 Nuitka 两大主流编译引擎，将繁琐的终端命令行参数转化为直观、便捷的图形界面交互，帮助开发者更高效、高成功率地生成跨平台原生可执行程序。

---

## 📷 界面预览 (Screenshots)

<p align="center">
<img width="1173" height="1067" alt="image" src="https://github.com/user-attachments/assets/6cf1e937-d35f-4e71-b4e7-7fd86f771d20" />
<img width="1173" height="1067" alt="image" src="https://github.com/user-attachments/assets/b4f563fb-328b-4615-8522-e4f9e490f759" />
<img width="1173" height="1067" alt="image" src="https://github.com/user-attachments/assets/522d7a3b-9a01-4387-8e81-def4cabcbfff" />
<img width="1173" height="1067" alt="image" src="https://github.com/user-attachments/assets/c8a89212-bf48-40d0-8125-98595f6052bd" />
<img width="1173" height="1067" alt="image" src="https://github.com/user-attachments/assets/3f5b803a-3c96-493c-b56b-e11f50bd9139" />
</p>

---

## 🚀 核心特性 (Key Features)

为了降低传统命令行构建的配置成本，解决多平台下环境与依赖冲突问题，QPyPack 深度整合了以下工程化辅助功能：

### 1. 直观的可视化交互体验
* 📥 **拖放式载入 (Drag & Drop)**：无需手动拷贝路径，直接将 `.py` 或 `.pyw` 源代码文件拖放至软件窗口，系统将全自动解析并载入工作区。
* 🎨 **图标智能检索与自适应**：源程序导入后，系统会自动检索同级目录下的常用图像资产（如 `icon.ico` / `logo.ico` / `icon.svg` / `logo.svg`）进行自适应格式转换、自动绑定与高清预览。
* 🌐 **多语言支持 (i18n)**：原生支持简体中文、英文等多语言界面自由切换，为全球开发者提供零门槛、无障碍的使用体验。

### 2. 依赖解析与虚拟环境沙盒
* 🛡️ **虚拟环境隔离 (Virtualenv Sandbox)**：支持一键在系统临时目录下创建隔离的虚拟沙盒，仅安装应用运行所需的最小依赖项，从而有效精简最终可执行产物的体积。
* 🔍 **多维度依赖解析**：
  * **配置同步**：自动检索并优先读取项目目录下的 `requirements.txt` 依赖声明。
  * **AST 静态扫描**：提供辅助的 AST（静态语法树）深度分析，自动提取代码中导入的非标准库模块，精准补齐隐式导入依赖（Hidden Imports）。
* ⚡ **内置 PyPI 加速源**：预设主流镜像加速通道，大幅提升沙盒中拉取构建引擎与依赖库的速度。

### 3. 高级编译参数精准控制
* ⚙️ **双引擎自适应切换**：在图形界面上实现 PyInstaller 与 Nuitka 的无缝切换，参数面板与优化选项将根据所选引擎的特性进行自适应调整。
* 📝 **应用元数据注入 (Metadata)**：无需编写繁琐的规格文件，直接在界面输入版本号、公司名和产品描述，工具会自动将元数据注入二进制程序属性中（支持 Windows PE 结构和 macOS Info.plist 写入）。
* 📂 **附加资源可视化管理 (Data Files)**：支持通过列表交互分别导入文件或文件夹，并支持双击列表条目直接修改打包后的相对释放路径（自适应释放路径映射）。

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

### 方法二：下载二进制文件

如果您不想配置本地 Python 环境，可直接在 Release 页面下载对应系统的预编译打包版本：
👉 [下载页面](https://github.com/Qwejay/QPyPack/releases)

---

## 📅 更新日志 (Changelog)

完整的版本更新历史与 Release 说明请参阅 [CHANGELOG.md](CHANGELOG.md) 或 [GitHub Releases 页面](https://github.com/Qwejay/QPyPack/releases)。

---

## 💖 赞助支持 (Sponsorship)

QPyPack 是一个完全开源且免费的项目，由个人利用业余时间开发与维护。如果本项目帮助您提高了开发效率或解决了打包难题，欢迎通过以下方式对项目进行**自愿赞助**。您的支持将是本项目持续更新与维护的重要动力：

- ⚡ **请作者喝咖啡**：[赞助支持 QPyPack](https://www.ifdian.net/a/qwejay)（支持微信 / 支付宝）

> **赞助说明**：赞助完全出于自愿，属于对开源项目的无偿鼓励，不包含任何商业服务绑定或特定功能开发承诺。非常感谢每一位支持开源创作的朋友！

---

## 📄 开源协议 (License)

本项目基于 [GNU General Public License v3.0](LICENSE) 开源，允许在遵循协议条款的前提下自由分发、修改和二次开发。

> [!NOTE]
> **关于打包产物的版权**：
> 使用 QPyPack 构建生成的二进制文件/应用程序，其版权和开源许可**完全由使用者自行决定**，QPyPack 的 GPL-3.0 协议不会影响用户打包后的程序。

Copyright (C) 2026 QwejayHuang.
