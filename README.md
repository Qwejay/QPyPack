# QPyPack

QPyPack 是一个为 Python 开发者设计的图形化打包配置工具。它将命令行打包流程转换为直观、简易的 GUI 界面操作，无需记忆繁琐的终端命令，即可辅助生成可执行文件。

<p align="center">
<img width="904" height="887" alt="image" src="https://github.com/user-attachments/assets/0f7831a2-68fc-460c-a5a2-75b39e36a7af" />
<img width="904" height="887" alt="image" src="https://github.com/user-attachments/assets/ce50d3a0-95df-4773-bd56-763701bfd16a" />
</p>

---
## 核心设计：简化打包流程

为了降低传统命令行打包的配置成本，解决依赖易冲突等问题，QPyPack 整合了以下辅助功能：

### 1. 简易的交互流程
* **拖拽即装载**：无需手动输入路径，直接将您的 `.py` 或 `.pyw` 源代码文件拖入软件窗口，即可自动识别并准备构建。
* **智能图标匹配**：脚本载入后，程序会自动检索同目录下的常用图标文件（如 `icon.ico` / `logo.ico` / `icon.svg` / `logo.svg`）并进行自动填充和预览。
* **一键直达结果**：打包完成后，点击“打开输出目录”按钮即可自动打开资源管理器并定位到生成的程序。

### 2. 自动化的依赖与环境处理
* **独立打包环境 (Venv)**：支持一键开启虚拟环境。工具会在临时目录下自动创建干净的沙盒环境，仅安装打包所需的库，有助于控制最终生成的可执行文件的体积。
* **多维度依赖扫描**：
  * 自动检测并优先读取项目目录下的 `requirements.txt`。
  * 提供辅助的 AST（静态语法树）扫描选项，分析代码中导入的第三方模块，帮助查漏补缺隐式依赖。
* **内置国内加速源**：预设清华大学等国内 PIP 镜像源，在沙盒中拉取打包工具或依赖库时提供加速通道。

### 3. 可视化参数配置
* **双引擎切换**：在下拉菜单中即可在 PyInstaller 和 Nuitka 之间灵活切换，相关的参数输入框与高级选项会根据所选引擎特性自动启用或隐藏。
* **可视化版本属性**：无需编写复杂的版本配置文件，直接在界面文本框中输入版本号、公司名和产品描述，工具会自动将其写入生成的可执行文件元数据中。
* **直观的资源添加**：通过交互式对话框选择需要打包的图片、数据文件夹，引擎会自动进行路径映射与资源封装。

---
### 更新日志 (Changelog)
**2.4.2**
语法错误提示：打包失败时，自动扫描完整构建日志，识别 Python 源码中的 IndentationError、SyntaxError 和 TabError。
显示错误位置：解析出出错文件名、行号及错误描述，帮助用户快速定位代码缺陷，程序区分“用户代码错误”与“打包工具故障”，避免混淆。

**2.4.1**
* **重构设置TAB**：全面重构设置面板，将参数分类为“应用元数据”、“编译控制”、“资源与沙盒”、“软件设置”四大模块。
* **保存路径配置**：支持将 EXE 输出至全局指定的自定输出目录，并支持对缺失的多级父目录进行全自动递归创建。
* **并发编译限制**：支持手动限制打包引擎并发编译时所能占用的最大 CPU 核心数，避免由于硬件满载引发设备死机。
* **编译完成声音反馈**：引入非外部重度依赖的系统级音频通知，在打包成功或异常中断时给予不同的声音提示。
* **自动持久化打包日志**：任务结束后支持在目标输出路径自动保存运行日志（.log 格式），极大提升异常分析排查的便利性。
  
**2.4.0**
* **控制台防闪退机制**：在非 GUI 模式打包时，工具会自动在临时脚本尾部注入防闪退控制代码（针对 Windows 平台下双击运行的非交互式程序），提升用户体验。
* **提升文件删除的鲁棒性**：重构了临时目录清理机制，引入带重试延时与只读属性解除的 `robust_rmtree` 回收机制，减少因防病毒软件或进程占用导致清理失败的情况。
* **新增云同步锁检测**：对于处于 OneDrive 等云同步盘锁定状态的文件，提供前置 I/O 异常检测，避免打包过程意外被系统挂起。
* **完善引擎参数映射**：优化 Nuitka 的插件自动加载逻辑（自适应 PyQt/PySide 家族、numpy, matplotlib, tkinter 等常见重型库），使其配置更加贴合实际运行环境。
* **新增 CI/CD 工作流**：推送版本标签自动触发 PyPI 发布，并同步编译 Windows 运行包（`.exe`）上传至 GitHub Release 附件。
* **版本自动同步**：构建时自动对齐 `pyproject.toml` 与入口脚本中的版本号，降低手动维护出错率。

**2.3.6**
* **新增 SVG 格式图标支持**：支持加载 `icon.svg` / `logo.svg` 作为程序图标。
* **增加 `.pyw` 格式脚本支持**：全面支持无控制台窗口的 Python 脚本格式，优化拖拽校验与文件选择过滤器。
* **修复 Windows 绝对路径分割问题**：重构附加资源解析器，避免绝对路径中的盘符冒号（如 `C:`）被错误截断，确保跨引擎数据装载安全。
* **优化 AST 本地依赖过滤**：安装前主动检索当前目录结构，自动过滤本地辅助模块或文件夹，防止向 PyPI 发起不必要的安装请求。
* **强化元数据清理机制**：将临时版本配置文件的生命周期管理提升至最高级别，确保即使在未启用“一键清理”时，构建结束也会无条件收回临时文件。

**2.3.5**
* **重构依赖拉取架构**：采用三重安全检测（Requirements -> Pipreqs -> AST 源码扫描），即使前置分析工具漏报，最终的 AST 扫描也会尝试抓取核心隐式库。
* **工作区优化**：将 `QPyPack.ini` 配置文件平滑迁移至全局系统路径（`~/.qpypack/config.ini`），并将所有 AST 缓存、依赖清单等中间产物全部转移至操作系统 `Temp` 目录，避免对用户的工程代码区造成额外文件占用。
* **构建日志标准化**：重构控制台与 UI 日志的输出，引入规范化的生命周期状态标签（如 `[Init]`, `[Env]`, `[Deps]`, `[Build]`, `[Pack]`），提升状态诊断的清晰度。
* **虚拟环境静默优化**：分配独立隔离的 venv 打包沙盒后，首个动作变更为自动升级 `pip`，减少因旧版本引起的警告提示。
* **核心 BUG 修复**：修复了因底层 `configparser` 映射字典读取异常，导致抛出 `'dict' object has no attribute 'lower'` 的问题。

**2.3.0**
* **UI 框架升级**：由 PyQt5 升级至 PySide6。优化了高分屏（High-DPI）下的文字与图标缩放表现。
* **精简架构**：移除 `cx_Freeze` 打包引擎，专注打磨更实用的 PyInstaller 与 Nuitka 双核心引擎。
* **Nuitka 最佳实践集成**：
  * 单文件 (`--onefile`) 模式下，自适应启用 `zstandard` 核心压缩环境，优化产物体积。
  * 全局引入 `anti-bloat` 防膨胀插件，避免 `pytest`、`IPython` 等无用依赖被误打包。
  * 新增对 `tkinter` 官方探针的自动识别与插件激活。
  * 重构附加资源打包逻辑，自适应单文件 (`--include-data-files`) 与文件夹 (`--include-data-dir`) 打包规范。
* **PyInstaller 深度优化**：
  * 移除过时的强制 PyQt 隐藏导入逻辑，交由现代 Hook 自动处理。
  * 修复附加资源在跨平台构建时的路径分隔符 (`os.pathsep`) 匹配问题。

**2.2.0**
* 规范目录结构，优化内部沙盒与临时文件命名规范。
* **超时守护 (Watchdog)**：为关键打包步骤设置超时限制，防止打包过程因网络等外界干扰无限制挂起。
* **依赖推导优化**：pipreqs 增加 15 秒超时保护，失败时自动降级为本地纯静态 AST 解析。
* **智能命名输出**：自动解析脚本版本，预设输出文件名为 `{Name}_{Version}` 格式。
* **编译兼容扩展**：Nuitka 编译模式新增对 PyQt6、PySide、NumPy、Matplotlib 等常用插件的自适应识别。

**2.1.0**
* 将 Nuitka 单文件打包解压路径调整为 `%LOCALAPPDATA%`。
* 增加构建失败的 UI 动画反馈。
* 改善打包程序防杀毒软件误报拦截的兼容表现。

**2.0.1**
* 修正 Nuitka 参数传递方式：采用更符合 Nuitka 规范的单参数追加形式：`cmd.append(f"--include-data-files={src}={dest}")`。
* 加入平台感知后缀：动态识别操作系统（Windows 使用 `.exe` 后缀，而 macOS/Linux 不使用后缀），避免跨平台定位产物失败。
* 安全过滤平台专有参数：针对 Windows 特有的元数据写入，只有当 `os.name == "nt"` 时才追加对应指令。

---

## 快速上手

只需三步，即可完成打包：

1. **拖入脚本**：将您的 Python 脚本（`.py` 或 `.pyw`）拖拽至主界面。
2. **选择引擎**：点击右下角设置，在“基础打包”中选择您想使用的引擎（默认推荐 PyInstaller 进行快速验证）。
3. **开始构建**：返回主界面点击“开始构建”，并在下方展开的控制台中实时查看打包进度。

---
### 启动应用
在 Python >= 3.8 环境中执行以下命令安装并启动程序：

```bash
pip install qpypack
qpypack
```

### 预编译版本下载
若不想配置 Python 环境，可直接下载打包好的独立可执行文件：
[GitHub Releases 下载链接](https://github.com/Qwejay/PyPack/releases)

## Star History

<a href="https://www.star-history.com/?repos=Qwejay%2FQPyPack&type=date&legend=bottom-right">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=Qwejay/QPyPack&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=Qwejay/QPyPack&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=Qwejay/QPyPack&type=date&legend=top-left" />
 </picture>
</a>
