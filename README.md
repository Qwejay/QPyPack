# QPyPack

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
<img width="1023" height="977" alt="image" src="https://github.com/user-attachments/assets/5201ce6f-e908-443b-b6aa-733cf4d4c4ad" />
<img width="1023" height="977" alt="image" src="https://github.com/user-attachments/assets/cfa93356-1def-4b39-9cc9-5cb6914c783e" />
</p>

---

## 🚀 核心特性 (Key Features)

为了降低传统命令行构建的配置成本，解决多平台下环境与依赖冲突问题，QPyPack 深度整合了以下工程化辅助功能：

### 1. 直观的可视化交互体验
* 📥 **拖放式载入 (Drag & Drop)**：无需手动拷贝路径，直接将 `.py` 或 `.pyw` 源代码文件拖放至软件窗口，系统将全自动解析并载入工作区。
* 🎨 **图标智能检索与自适应**：源程序导入后，系统会自动检索同级目录下的常用图像资产（如 `icon.ico` / `logo.ico` / `icon.svg` / `logo.svg`）进行自适应格式转换、自动绑定与高清预览。

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

您可以通过以下两种方式之使用 QPyPack：

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
### [2.5.4] - 2026-07-18

* **新增精简模式**：自动剔除 `pip`、`unittest` 等冗余库并启用 Nuitka `-OO` 优化，大幅缩减产物体积；配套深度源码静态扫描（至多检索 500 个本地依赖），保障极致精简下的运行稳定性。
* **修复 UPX 假性报错问题**：当未勾选 UPX 时，显式向引擎传递 `--noupx` 指令，阻断 PyInstaller 静默调用系统 UPX 造成的兼容性报错与日志干扰。
* **修复日志中文乱码问题**：对底层命令行调用 (`subprocess`) 全面强制追加 `encoding="utf-8"` 参数，彻底解决 Windows 默认编码 (GBK) 解析字节流时引发的控制台乱码。。

### [2.5.3] - 2026-07-17

* **引擎版本锁定**：支持在高级设置中自定义 Nuitka/PyInstaller/pipreqs 的版本，杜绝上游更新导致的打包失败。
* **动态进度 UI**：主界面大字标题实时同步并轮播当前构建步骤，告别卡顿感与等待焦虑。
* **解决编译崩溃**：全局强制注入 UTF-8 环境，修复 Windows 中文系统下 Nuitka 解析 PyTorch 等库时因 GBK 编码导致的致命报错。
* **高分屏渲染修复**：解决非整数缩放（如 125%）下的字体发虚问题，清理冗余代码消除 DPI 权限报错。
* **依赖扫描自适应**：修复非 UTF-8 编码源码导致 `pipreqs` 分析崩溃的问题，支持自动回退本地编码。
* **智能解释器检索**：合并 `.EXE/.exe` 重复路径，默认选中当前环境，并剥离 `\\?\` 路径前缀以防子进程调用异常。
* **绝对无痕清理**：增加对 `nuitka-crash-report.xml` 与临时 `__pycache__` 的强制回收，绝不污染用户目录。
* **修复图标未更新问题**：修复添加新的打包会导致图标未能更新的问题。
* **综合细节提升**：重构设置面板排版以消除滚动条；移除高版本 API 完美向下兼容 Python 3.7；Nuitka 插件匹配忽略大小写。

<details>
<summary><b>展开查看历史版本更新记录</b></summary>

### [2.5.2] - 2026-07-15
* **重构编译后端指令集**：将 PyInstaller 与 Nuitka 的底层打包参数生成逻辑重构为两套**完全独立、互不干扰的构建分支**。这在架构上彻底消除了历史版本中因共享部分参数生成逻辑而导致的参数污染隐患，确保各自在运行中均符合官方最新的标准规范。
* **优化 Nuitka 附加资源兼容性**：针对 Nuitka 编译器在处理单个附加数据文件时，若目标相对路径为 `.` 会导致编译崩溃（*contains illegal suffix*）的问题进行了自适应修复（`os.path.normpath` 路径标准化）。
* **修正 Nuitka 排除模块指令**：将 Nuitka 引擎下排除特定模块的参数由原先不规范的 `--exclude-module` 修正为 Nuitka 官方标准的 `--nofollow-import-to`，提升了打包时对冗余依赖库进行剪裁的安全性和有效性。
* **完善 Windows 二进制属性映射**：修正并补充了 Nuitka 编译分支下 Windows PE 元数据的字段映射。将应用描述正确映射至 `--file-description`（此前误映射为产品名称）、应用名称映射至 `--product-name`，并同步补充了 `--product-version` 参数，使输出的可执行文件属性信息更趋完整。

### [2.5.1] - 2026-07-15
* **多平台自动编译**：利用 GitHub Actions，工作流将会在 windows-latest、macos-latest 和 ubuntu-latest 三种原生系统容器中并发运行，并自动将各自生成的原生可执行产物打包归档，最后统一上传至该 Tag 对应的 GitHub Release 附件中。
* **扁平风格**：清除 Emoji 表情，全面换装扁平化 Google 风格矢量图标。
* **修改版权信息显示**：删除标题栏作者信息，增加状态栏右侧常驻版权声明（自适应隐藏）。

### [2.5.0]
* **安全去耦与跨平台稳定性优化**：完全隔离 Windows 的 `winreg` 注册表静态调用，基于动态占位保障 macOS 与 Linux 等非 Windows 环境下的静态加载安全性。
* **自适应图像格式转换引擎**：引入全新的 `convert_image_to_format` 弹性图形转译机制。可将 SVG、PNG、JPG 等格式自动适配转换为 Windows `.ico` 与 macOS `.icns`，内置“macOS sips -> Qt QImage -> Pillow”三重安全降级备份。
* **应用元数据精准转译与写入**：在 Windows 系统下自动动态写入 `VSVersionInfo` 元数据，而在 macOS 平台下自动映射生成规范的 Bundle ID（如 `com.company.appname`），为后续的代码签名与公证提供标准数据格式。
* **多维异构构建产物精准提炼**：重构底层产物移动（Move）与重置逻辑，精准捕获并转移不同编译模式下产生的文件实体或目录包（如 Windows 的 `.exe`，macOS 拥有独立目录结构的 `.app`，以及 UNIX 无后缀二进制），杜绝旧版本跨系统提取失败的问题。
* **依赖声明与打包规范优化**：更新 `pyproject.toml`，补充标准 PyPI 分类器（Classifiers）及扩展项目链接（URLs），显式声明 `setuptools` 范围防止打包杂质，并将 Pillow 加入核心运行时依赖保障跨平台图标转译。

### [2.4.6]
* **跨平台兼容性适配**：修复了底层进程调用中 Windows 平台专有的 `creationflags` 导致非 Windows 系统执行崩溃的致命异常；重构 UNIX 环境（macOS/Linux）下的 Python 解释器静态探测与虚拟沙盒环境分析器；过滤及剔成了平台特异性编译参数（如 `version-file` 等）。
* **UI 现代化重构与 UX 体验升级**：废弃传统密集型排版，采用卡片式容器布局（Card-based Layout）。为复杂的构建参数面板引入“胶囊式子导航（Pill-Tabs）”，在功能丰富度与视觉克制力之间取得平衡；全面解决因低分辨率缩放引发的组件挤压、文本截断等视觉缺陷。
* **多版本内核独立编译沙盒**：支持全局指定或浏览任意版本的 Python 解释器（例如兼容极旧的 Python 3.5 内核），程序将在对应的专属内核沙盒中完成代码解析、依赖对齐与独立编译分发，彻底与主控宿主环境解耦。
* **关于界面视觉重构**：引入原生交互式动作行（Action Row）替代传统低质感排版，支持无缝调用系统浏览器跳转开源仓库；修复了部分 ICO 图标渲染时的抗锯齿失真问题，保证界面资产高清锐利。

### [2.4.5]
* **源码解析安全修复**：移除了在进行依赖扫描（AST 语法树解析）和控制台防闪退代码注入时对源码换行符（CRLF 强转 LF）的干预操作，修复了由此导致的潜在多行字符串解析错误及文件破坏问题。

### [2.4.4]
* **附加资源可视化管理**：废弃了易输错的单行文本框输入，引入列表化管理组件。支持通过图形化对话框分别添加“文件”和“文件夹”，并支持双击列表条目直接修改打包后的相对释放路径。
* **路径解析引擎升级**：配合新的可视化资源管理，重写了底层存储与引擎构建指令（`--add-data`）的拼接逻辑，解决了旧版本中绝对路径被错误切割的解析隐患。

### [2.4.3]
* **自定义依赖清单支持**：新增指定依赖文件路径配置。当多个 Python 脚本放置在同一文件夹管理时，可直接为各个脚本绑定不同的依赖清单（例如 `requirements1.txt`），无需再频繁手动重命名。
* **修复控制台模式下导入及资源读取异常**：调整了控制台防闪退代码注入逻辑，将生成的临时入口文件限制在源脚本同级目录下，规避了原版本在系统临时文件夹编译导致本地相对导入（Import）及相对路径资源失效的错误。
* **重构后台分析线程控制逻辑**：废弃了不安全的后台线程强制终止方式（`QThread.terminate()`），采用解绑信号的处理机制，降低了在快速拖拽或频繁切换脚本时程序偶发的界面卡死、闪退或死锁概率。
* **提升 Nuitka Standalone 打包兼容性**：重构了 Nuitka 自动匹配逻辑，改用动态扫描匹配 `.dist` 产物文件夹，避免因打包入口临时重命名而引发“未定位到有效产物”的构建异常。
* **优化 SVG 图标转换容错**：针对 Windows 平台下 PyInstaller 对图标格式的限制，在宿主环境缺少特定图片格式插件时，新增优雅降级与日志提示机制，预防编译器因传入不支持的格式而引发崩溃。

### [2.4.2]
* **编译语法异常诊断**：编译失败时，系统将自动扫描并重排完整的构建日志，精准识别源码中的 `IndentationError`、`SyntaxError` 和 `TabError` 语法错误。
* **精准定位错误源**：解析并高亮展示发生语法错误的源文件名、行号及错误描述，区分“源码逻辑异常”与“打包工具故障”，避免混淆。

### [2.4.1]
* **模块化配置重构**：全面重构设置面板，将参数解耦并分类为“版本信息与元数据”、“编译控制”、“资源与沙盒”、“软件设置”四大模块。
* **自定义归档目录**：支持将编译产物输出至全局指定的自定义输出目录，并支持对缺失的多级父目录进行全自动递归创建。
* **并发编译限制**：支持手动限制打包引擎并发编译时所能占用的最大 CPU 核心数，避免由于硬件满载引发设备死机。
* **编译提示音效**：引入系统级轻量化音频通知，在打包成功或发生异常中断时给予不同的声音提示。
* **编译日志自动保存**：任务结束后支持在目标输出路径自动保存运行日志（.log 格式），极大提升异常分析排查的便利性。
  
### [2.4.0]
* **控制台防闪退机制**：在非 GUI 模式打包时，工具会自动在临时脚本尾部注入防闪退控制代码（针对 Windows 平台下双击运行的非交互式程序），提升用户体验。
* **提升文件删除的鲁棒性**：重构了临时目录清理机制，引入带重试延时与只读属性解除的 `robust_rmtree` 回收机制，减少因防病毒软件或进程占用导致清理失败的情况。
* **云盘锁状态前置拦截**：针对处于云盘同步锁定状态的文件，提供前置 I/O 异常检测，避免打包过程意外被系统挂起。
* **完善引擎参数映射**：优化 Nuitka 的插件自动加载逻辑（自适应 PyQt/PySide 家族、numpy, matplotlib, tkinter 等常见重型库），使其配置更加贴合实际运行环境。
* **持续集成与自动发布**：新增 GitHub Actions 工作流，推送版本标签自动触发 PyPI 发布，并同步编译运行包上传至 GitHub Release。

</details>

---

## 🤝 参与贡献 (Contributing)

我们非常欢迎您的参与！如果您在测试或使用过程中发现任何异常，或者有更好的优化建议，可以通过以下方式参与贡献：

1. **提交反馈**：在项目主页提交 [GitHub Issues](https://github.com/Qwejay/QPyPack/issues)，并附带异常日志。
2. **提交代码**：欢迎提交 Pull Requests，请在提交前确保您的代码符合标准规范并完成了多平台本地测试。

---

## 📄 开源协议 (License)

本项目基于 **GPL-3.0** 开源许可协议。在遵守该开源许可协议的前提下，您可以自由分发、修改和二次开发。

---

## 📈 Star History

<a href="https://www.star-history.com/?repos=Qwejay%2FQPyPack&type=date&legend=bottom-right">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=Qwejay/QPyPack&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=Qwejay/QPyPack&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=Qwejay/QPyPack&type=date&legend=top-left" />
 </picture>
</a>
