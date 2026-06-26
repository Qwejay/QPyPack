# QPyPack

QPyPack 是一个为 Python 开发者设计的图形化打包配置工具。它将复杂的命令行打包流程转化为直观、简易的 GUI 界面操作，无需记忆繁琐的终端命令，即可快速生成可执行文件。

<p align="center">
<img width="904" height="887" alt="image" src="https://github.com/user-attachments/assets/0f7831a2-68fc-460c-a5a2-75b39e36a7af" />
<img width="904" height="887" alt="image" src="https://github.com/user-attachments/assets/ce50d3a0-95df-4773-bd56-763701bfd16a" />
</p>

---
## 核心设计：让打包变简单

为了解决传统命令行打包参数多、依赖易冲突、配置繁琐的问题，QPyPack 围绕“易用性”与“官方最佳实践”进行了深度设计：

### 1. 极简的交互流程
* **拖拽即装载**：无需手动输入路径，直接将您的 `.py` 或 `.pyw` 源代码文件拖入软件窗口，即可自动识别并准备构建。
* **智能图标匹配**：脚本载入后，程序会自动检索同目录下的常用图标文件（如 `icon.ico` / `logo.ico` / `icon.svg` / `logo.svg`）并自动填充和预览。
* **一键直达结果**：打包完成后，点击“打开输出目录”按钮即可自动弹出资源管理器并定位到生成的程序。

### 2. 自动化的依赖与环境处理
* **智能沙盒隔离 (Venv)**：支持一键开启虚拟环境。工具会在临时目录下自动创建干净的沙盒环境，仅安装打包所需的库，有效减小最终生成的可执行文件的体积。
* **多维度依赖扫描**：
  * 自动检测并优先读取项目目录下的 `requirements.txt`。
  * 提供辅助的 AST（静态语法树）扫描选项，自动分析代码中导入的第三方模块，帮助您查漏补缺隐式依赖。
* **内置国内加速源**：预设清华大学等国内 PIP 镜像源，在沙盒中拉取打包工具或依赖库时自动加速。

### 3. 可视化高级参数配置
* **双引擎无缝切换**：在下拉菜单中即可在 PyInstaller 和 Nuitka 之间灵活切换，相关的参数输入框与高级选项会根据所选引擎特性自动启用或隐藏。
* **可视化版本属性**：无需编写复杂的版本配置文件，直接在界面文本框中输入版本号、公司名和产品描述，工具会自动将其写入生成的可执行文件元数据中，提升系统识别度。
* **直观的资源添加**：通过交互式对话框选择需要打包的图片、数据文件夹，引擎会自动进行跨平台兼容的路径映射与资源封装。

---
### Changelog
**2.3.6**
* **新增 SVG 格式图标支持**：现在能够自动加载 `icon.svg` / `logo.svg`为程序图标。
* **增加 `.pyw` 格式脚本支持**：全面支持无控制台窗口的 Python 脚本格式，优化拖拽校验与文件选择过滤器。
* **修复 Windows 绝对路径分割 BUG**：重构附加资源解析器，避免绝对路径中的盘符冒号（如 `C:`）被错误截断，确保跨引擎数据装载安全。
* **优化 AST 本地依赖过滤**：安装前主动检索当前目录结构，自动过滤本地辅助模块或文件夹，防止向 PyPI 发起不必要的安装请求。
* **强化元数据清理机制**：将临时版本配置文件的生命周期管理提升至最高级别，确保即使在未启用“一键清理”时，构建结束也会无条件收回临时文件。

**2.3.5**
* **防漏包机制**：彻底废弃极易误判的短路判定，重构依赖拉取架构为“三重绝对安全网”（Requirements -> Pipreqs -> AST源码强扫）。即使前置分析工具漏报，最终的 AST 保底扫描也会强行抓取 `PySide6` 等核心隐式库并塞入沙盒，终结漏包闪退问题。
* **工作区“零污染”改造**：贯彻绝对纯净的构建理念。将 `QPyPack.ini` 配置文件平滑迁移至全局系统路径（`~/.qpypack/config.ini`），并将所有 AST 缓存、依赖清单等中间产物全部转移至操作系统 `Temp` 目录，确保不留任何垃圾文件污染用户的工程代码区。
* **构建日志工程化规范**：全面重构控制台与 UI 日志的输出文案，引入规范化的 CI/CD 生命周期状态标签（如 `[Init]`, `[Env]`, `[Deps]`, `[Build]`, `[Pack]`），大幅提升状态诊断的清晰度与专业性。
* **虚拟环境沙盒智能自愈**：在分配独立隔离的 venv 打包沙盒后，首个初始化动作变更为静默自动升级 `pip`，清除因老旧模块引发的大段黄色警告乱码。
* **核心 BUG 修复**：精准修复了因底层 `configparser` 映射字典降级读取失败，导致抛出 `'dict' object has no attribute 'lower'` 的系统崩溃问题。
* **优化日志表述**：调整了日志输出文字的语言表述，使之更具工程专业度。

**2.3.0**
* **UI框架重构**：由 PyQt5 升级至 PySide6。优化了现代高分屏（High-DPI）下的文字与图标缩放表现。
* **精简架构**：移除 `cx_Freeze` 打包引擎，专注打磨更现代、更高效的 PyInstaller 与 Nuitka 双核心引擎。
* **Nuitka 官方最佳实践深度集成**：
  * 单文件 (`--onefile`) 模式下，强制启用 `zstandard` 核心压缩环境，大幅优化产物体积与解压启动性能。
  * 全局引入 `anti-bloat` 防膨胀插件，智能拦截并避免 `pytest`、`IPython` 等无用巨大依赖被误打包。
  * 新增对 `tkinter` 官方探针 of 自动识别与插件激活。
  * 重构附加资源打包逻辑，引擎将自动探测目标类型，严格区分并适配单文件 (`--include-data-files`) 与文件夹 (`--include-data-dir`) 打包规范。
* **PyInstaller 深度优化**：
  * 移除过时的强制 PyQt 隐藏导入逻辑，交由现代 Hook 自动处理。
  * 彻底修复附加资源在跨平台构建时的路径分隔符 (`os.pathsep`) 匹配与切割异常问题。

**2.2.0**
* 更名为 QPyPack，规范目录结构 for PyPI，优化内部沙盒与临时文件命名规范。
* 超时守护 (Watchdog)：引入看门狗机制，为关键打包步骤设置超时限制，防止因网络问题导致构建无限期挂起。
* 依赖推推导优化：pipreqs 原生支持国内镜像站重定向加速，并增加 15 秒超时自愈，失败时自动降级为本地纯静态 AST 解析。
* 智能命名输出：自动解析脚本版本，预设输出文件名为 `{Name}_{Version}` 格式（例如：QPyPack_2.2.0.exe）。
* 编译兼容扩展：Nuitka 编译模式新增对 PyQt6、PySide、NumPy、Matplotlib 等常用插件的自适应识别。
* 细节打磨：改进日志高频刷新滚动体验，优化版本信息元数据抓取退级逻辑。

**2.1.0**
* Nuitka 单文件打包解压路径修改为 `%LOCALAPPDATA%`。
* 增加构建失败的 UI 动画反馈。
* 尝试修复打包后容易被 Windows 安全中心误报拦截的问题。

**2.0.1**
* 修正 Nuitka 参数传递方式：将 `cmd.extend(["--include-data-files", "src=dest"])` 修改为更符合 Nuitka 规范的单参数追加形式：`cmd.append(f"--include-data-files={src}={dest}")`。
* 加入平台感知后缀：动态识别操作系统（Windows 使用 `.exe` 后缀，而 macOS/Linux 不使用），避免跨平台定位产物失败。
* 安全过滤平台专有参数：对于 Windows 特有的元数据写入（如公司名称、描述、文件版本、ICO 图标），只有当 `os.name == "nt"` 时才追加对应指令。

---

## 快速上手

只需三步，即可完成打包：

1. **拖入脚本**：将您的 Python 脚本（`.py` 或 `.pyw`）拖拽至主界面。
2. **选择引擎**：点击右下角设置，在“基础打包”中选择您想使用的引擎（推荐默认的 PyInstaller 进行快速验证）。
3. **开始构建**：返回主界面点击“开始构建”，并在下方展开的控制台中实时查看打包进度。

---
### 启动应用
在 Python >=3.8 环境中执行以下命令启动程序：

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
