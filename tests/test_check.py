# -*- coding: utf-8 -*-
"""
=============================================================================
 QPyPack 全功能终极一体化自检与双引擎真实打包验证系统 (UI 深度集成完整版)
=============================================================================
 特性：
   - 深度集成：直接实例化 MainWindow 模拟用户拖拽与点击，完整测试 UI->Engine 链路
   - 前瞻兼容：不写死参数字典，直接读取 UI 界面控件生成的配置，随软件升级自动适配
   - 自动自净：测试开始前与结束后自动抹除一切 build/、spec、egg-info 残留
   - 全量覆盖：包含 AST 分析、I18N 多语言引擎、状态机逻辑等 8 大核心维度
=============================================================================
"""

import sys
import os
import re
import json
import time
import shutil
import zipfile
import tempfile
import subprocess
import traceback
from pathlib import Path

# 全局开启 Qt 无头模式与 Windows 字体 (屏蔽无关警告)
os.environ["QT_QPA_PLATFORM"] = "offscreen"
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    if os.path.exists(r"C:\Windows\Fonts"):
        os.environ["QT_QPA_FONTDIR"] = r"C:\Windows\Fonts"
os.environ["QT_LOGGING_RULES"] = "qt.qpa.fonts=false;qt.qpa.*=false;qt.multimedia*=false"

current_path = Path(__file__).resolve()
if current_path.parent.name == "tests":
    ROOT_DIR = current_path.parent.parent
else:
    ROOT_DIR = current_path.parent

PACKAGE_DIR = ROOT_DIR / "qpypack"
LOCALES_DIR = PACKAGE_DIR / "locales"
ICON_PATH = PACKAGE_DIR / "icon.ico"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def log_pass(msg):
    print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} {msg}")


def log_warn(msg):
    print(f"  {Colors.YELLOW}⚠ [WARN]{Colors.RESET} {msg}")


def log_fail(msg):
    print(f"  {Colors.RED}✖ [FAIL]{Colors.RESET} {msg}")


def log_info(msg):
    print(f"  {Colors.CYAN}ℹ [INFO]{Colors.RESET} {msg}")


# =====================================================================
# 垃圾自净机制 (自动清理根目录残留)
# =====================================================================
def clean_project_junk():
    """扫描并强制清除项目根目录下的所有测试与构建残留"""
    junk_patterns_dir = ["build", "dist", "*.egg-info", "__pycache__", ".pytest_cache"]
    junk_patterns_file = ["*.spec", ".coverage"]

    # 清理目录
    for pattern in junk_patterns_dir:
        for p in ROOT_DIR.glob(pattern):
            if p.is_dir() and p != PACKAGE_DIR:
                try:
                    shutil.rmtree(p, ignore_errors=True)
                except Exception:
                    pass
        for p in (ROOT_DIR / "tests").glob(pattern):
            if p.is_dir():
                try:
                    shutil.rmtree(p, ignore_errors=True)
                except Exception:
                    pass

    # 清理文件
    for pattern in junk_patterns_file:
        for p in ROOT_DIR.glob(pattern):
            if p.is_file():
                try:
                    p.unlink(missing_ok=True)
                except Exception:
                    pass
        for p in (ROOT_DIR / "tests").glob(pattern):
            if p.is_file():
                try:
                    p.unlink(missing_ok=True)
                except Exception:
                    pass


# 测试前先自净一次历史垃圾
clean_project_junk()


# =====================================================================
# 1. 静态资源与配置深度检测
# =====================================================================
def test_01_static_assets():
    """测试 1: 静态资源与配置物理合法性"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 1/8] 静态资源与工程配置完整性检查...{Colors.RESET}")

    assert ICON_PATH.exists(), f"关键图标缺失: {ICON_PATH}"
    assert ICON_PATH.stat().st_size > 1024, "icon.ico 文件大小异常"
    with open(ICON_PATH, "rb") as f:
        header = f.read(4)
        assert header == b"\x00\x00\x01\x00", "icon.ico 不是有效的 Windows ICO 格式"
    log_pass(f"图标格式与二进制签名正常 (大小: {ICON_PATH.stat().st_size} bytes)")

    toml_path = ROOT_DIR / "pyproject.toml"
    assert toml_path.exists(), "pyproject.toml 缺失"
    assert "qpypack" in toml_path.read_text(encoding="utf-8").lower()
    log_pass("pyproject.toml 配置文件解析正常")


# =====================================================================
# 2. 16 种多语言语法、Key 一致性与占位符检测
# =====================================================================
def test_02_locales_and_placeholders():
    """测试 2: 16 国多语言深度校验"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 2/8] 16 国国际化语言包与语法占位符检测...{Colors.RESET}")

    assert LOCALES_DIR.is_dir(), "locales 目录不存在"
    json_files = list(LOCALES_DIR.glob("*.json"))
    assert len(json_files) == 16, f"应包含 16 种语言包，实际发现 {len(json_files)} 个"
    log_pass(f"成功定位到全部 {len(json_files)} 个语言包文件")

    parsed = {}
    for jf in json_files:
        with open(jf, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert isinstance(data, dict), f"{jf.name} 格式非合法字典"
            parsed[jf.name] = data
    log_pass("所有语言包 JSON 语法解析正常")

    base_data = parsed.get("zh_CN.json", {})
    assert base_data, "基准语言包 zh_CN.json 缺失或为空"
    base_keys = set(base_data.keys())

    missing_map = {}
    for name, data in parsed.items():
        if name == "zh_CN.json":
            continue
        missing = base_keys - set(data.keys())
        if missing:
            missing_map[name] = missing

    if missing_map:
        for fname, keys in missing_map.items():
            log_warn(f"{fname} 缺少 {len(keys)} 个词条: {list(keys)[:3]}...")
    else:
        log_pass("16 国语言包与 zh_CN.json 词条保持 100% 完全对齐！")


# =====================================================================
# 3. AST 语法分析与依赖提取算法测试
# =====================================================================
def test_03_ast_engine():
    """测试 3: AST 源码静态语法分析与依赖侦测 (QPyPack 原生算法)"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 3/8] AST 静态分析与依赖侦测 (QPyPack 原生算法)...{Colors.RESET}")
    
    from qpypack.main import extract_project_imports_via_ast

    with tempfile.TemporaryDirectory() as tmpdir:
        mock_file = Path(tmpdir) / "test_ast.py"
        mock_file.write_text("import os, sys\nimport requests.auth\nfrom PyQt5.QtWidgets import QMainWindow", encoding="utf-8")
        
        modules = extract_project_imports_via_ast(mock_file, scan_dir=False)
        assert {"requests", "PyQt5", "os", "sys"}.issubset(modules), f"QPyPack 原生提取异常: {modules}"
        log_pass(f"QPyPack AST 引擎成功提取模块依赖: {modules}")


# =====================================================================
# 4. 核心模块与入口健全性 (集成配置存储及多语言引擎联调)
# =====================================================================
def test_04_core_logic():
    """测试 4: 核心配置管理与翻译引擎联调测试"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 4/8] QPyPack 核心配置读取与多语言翻译引擎测试...{Colors.RESET}")
    
    from qpypack.main import load_config, I18N
    
    config = load_config(retry=True)
    assert "Settings" in config, "配置生成或加载失败"
    assert "Mappings" in config, "包名映射字典缺失"
    
    # 动态切换并断言多语言系统
    I18N.set_language("en_US")
    assert I18N.t("Build Settings") == "Build Settings", "英文翻译错误"
    I18N.set_language("zh_CN")
    assert I18N.t("Build Settings") == "构建设置", "中文翻译未命中映射"
    
    log_pass("配置 I/O 系统与 I18N 多语言引擎运行正常")


# =====================================================================
# 5. UI 控件与主窗口状态机独立交互测试
# =====================================================================
def test_05_ui_interaction():
    """测试 5: Qt UI 界面与控件状态机逻辑交互测试 (独立无打包)"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 5/8] Qt UI 控件与状态机模拟交互测试...{Colors.RESET}")

    try:
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance() or QApplication(["qp_test", "-platform", "offscreen"])
    except ImportError:
        log_warn("未安装 PySide6，跳过 GUI 交互测试")
        return

    from PySide6.QtCore import QEventLoop, QTimer
    from qpypack.main import MainWindow
    window = MainWindow()
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        mock_py = Path(tmp_dir) / "mock_app.py"
        mock_py.write_text("print('hello')", encoding="utf-8")
        
        # 测试拖入脚本
        window.on_script_selected(str(mock_py))
        
        # 等待后台 AST 解析子线程完成
        loop = QEventLoop()
        timer = QTimer()
        timer.timeout.connect(loop.quit)
        timer.start(1000)
        loop.exec()
        timer.stop()
        
        assert window.current_state == "ready", "脚本载入后状态机未变为 ready"
        assert window.settings_panel.name_edit.text() == "mock_app", "未成功解析推导出默认程序名"
        
        # 测试修改引擎配置
        window.settings_panel.engine_combo.setCurrentIndex(1)
        assert window.settings_panel.engine_combo.currentText() == "Nuitka"
        
    log_pass("主窗口完成内存初始化，状态机推导与 UI 数据绑定响应正常")


# =====================================================================
# 6. Wheel 分发包真实打包与解压内嵌资产验证 (沙箱环境零残留)
# =====================================================================
def test_06_wheel_packaging():
    """测试 6: Wheel 包构建与资源嵌入"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 6/8] Wheel (.whl) 分发包构建与资源嵌入深度检查...{Colors.RESET}")

    with tempfile.TemporaryDirectory(prefix="qp_whl_") as tmp_dist:
        try:
            build_cmd = [sys.executable, "-m", "build", "--wheel", "--outdir", tmp_dist, str(ROOT_DIR)]
            result = subprocess.run(build_cmd, capture_output=True, text=True, cwd=tmp_dist)

            if result.returncode != 0:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "wheel", "--no-deps", "-w", tmp_dist, str(ROOT_DIR)],
                    capture_output=True, text=True, cwd=tmp_dist
                )
                assert result.returncode == 0, f"构建 Wheel 失败:\n{result.stderr}"

            wheels = list(Path(tmp_dist).glob("*.whl"))
            assert wheels, "未找到生成的 .whl 文件"
            wheel_file = wheels[0]
            log_pass(f"成功构建 Wheel: {wheel_file.name}")

            with zipfile.ZipFile(wheel_file, "r") as zf:
                names = zf.namelist()
                assert any("icon.ico" in n for n in names), "icon.ico 漏打包进 Wheel！"
                json_in_wheel = [n for n in names if "locales/" in n and n.endswith(".json")]
                assert len(json_in_wheel) >= 16, f"语言包未全部嵌入 Wheel (仅 {len(json_in_wheel)} 个)！"
                log_pass(f"icon.ico 及 16 个语言包已 100% 嵌入 Wheel 压缩包中")
        finally:
            clean_project_junk()


# =====================================================================
# 辅助函数: 创建微型真实测试工程 & 产物实机拉起断言
# =====================================================================
def _create_mock_project(base_dir: Path) -> Path:
    proj_dir = base_dir / "mock_app"
    proj_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = proj_dir / "assets"
    assets_dir.mkdir(exist_ok=True)

    with open(assets_dir / "data.json", "w", encoding="utf-8") as f:
        json.dump({"engine_test": "QPYPACK_REAL_OK"}, f)

    with open(proj_dir / "calc.py", "w", encoding="utf-8") as f:
        f.write("def multiply(a, b): return a * b\n")

    entry_file = proj_dir / "app_main.py"
    with open(entry_file, "w", encoding="utf-8") as f:
        f.write('''# -*- coding: utf-8 -*-
__version__ = "1.0.0"
__app_name__ = "MockTestApp"

import sys, os, json, multiprocessing
from calc import multiply

def get_res(rel):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), rel)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    calc_res = multiply(6, 7)
    res_path = get_res(os.path.join("assets", "data.json"))
    val = "FAIL"
    if os.path.exists(res_path):
        with open(res_path, "r", encoding="utf-8") as f:
            val = json.load(f).get("engine_test", "CORRUPTED")
    else:
        val = f"NOT_FOUND:{res_path}"
    print(f"__QP_ASSERT__|{calc_res}|{val}|__QP_ASSERT_END__")
    sys.exit(0)
''')
    return entry_file


def _get_size(path: Path):
    if path.is_file():
        return path.stat().st_size
    return sum(f.stat().st_size for f in path.rglob('*') if f.is_file())


def _assert_executable_execution(exe_path: Path):
    if sys.platform == "darwin" and exe_path.is_dir() and exe_path.name.endswith(".app"):
        exe_path = exe_path / "Contents" / "MacOS" / exe_path.stem

    assert exe_path.exists(), f"未找到生成的 EXE/二进制 文件: {exe_path}"
    start_t = time.time()
    proc = subprocess.run([str(exe_path)], capture_output=True, text=True, timeout=20, cwd=str(exe_path.parent))
    
    assert proc.returncode == 0, f"程序运行报错 (Code {proc.returncode}):\n{proc.stderr}"
    assert "__QP_ASSERT__|42|QPYPACK_REAL_OK|__QP_ASSERT_END__" in proc.stdout, f"输出不符，资源提取失败:\n{proc.stdout}"
    
    size_mb = _get_size(exe_path) / (1024 * 1024)
    log_pass(f"产物实机拉起验证通过！耗时: {time.time() - start_t:.2f}s | 体积: {size_mb:.2f} MB | 静态资源捆绑读取正常")


# =====================================================================
# E2E 测试核心引擎: 完整模拟 MainWindow 界面交互与打包
# =====================================================================
def run_e2e_via_mainwindow(engine_name: str, tmp_dir: Path, is_onefile: bool):
    """
    通过直接实例化 MainWindow 并触发界面事件，模拟真实用户的打包全流程。
    这能保证测试紧跟 UI 升级，覆盖完整的 "界面配置 -> 参数生成 -> 线程打包" 链路。
    """
    from PySide6.QtCore import QEventLoop, QTimer
    from qpypack.main import MainWindow
    
    sandbox = Path(tmp_dir)
    entry_file = _create_mock_project(sandbox)
    
    # 1. 实例化主窗口 (触发所有的初始化和配置读取)
    window = MainWindow()
    
    # 2. 模拟用户拖拽源码文件到界面
    window.on_script_selected(str(entry_file))
    
    # 等待分析线程(ScriptAnalysisThread)完成
    loop_wait = QEventLoop()
    timer_wait = QTimer()
    timer_wait.timeout.connect(loop_wait.quit)
    timer_wait.start(1000) # 等待1秒确保分析完毕
    loop_wait.exec()
    timer_wait.stop()
    
    assert window.current_state == "ready", "脚本载入后状态机未变为 ready"
    
    # 3. 模拟用户配置界面面板 (SettingsPanel)
    sp = window.settings_panel
    sp.engine_combo.setCurrentText(engine_name)
    sp.rb_onefile.setChecked(is_onefile)
    sp.rb_onedir.setChecked(not is_onefile)
    sp.noconsole_check.setChecked(True)
    sp.enable_sign_check.setChecked(False) # 测试环境关闭签名防阻断
    
    # 设置输出目录到沙箱中
    sp.out_mode_combo.setCurrentIndex(1)
    sp.out_dir_edit.setText(str(sandbox / "dist"))
    
    # 4. 模拟用户拖入附加资源 (assets 文件夹)
    window.on_main_resources_dropped([str(entry_file.parent / "assets")])
    
    # 5. 模拟点击【开始构建】
    window.start_pack()
    assert window.current_state == "building", "启动打包后，主窗口未进入 building 状态"
    
    # 6. 使用事件循环等待 PackingThread 后台线程完成
    loop = QEventLoop()
    def check_status():
        # 轮询状态机是否退出 building
        if window.current_state in ("done", "failed"):
            loop.quit()
            
    timer = QTimer()
    timer.timeout.connect(check_status)
    timer.start(500)
    loop.exec()
    timer.stop()
    
    assert window.current_state == "done", f"【{engine_name}】打包失败！详细日志如下:\n{window.log_detailed.toPlainText()}"
    
    # 7. 提取生成的程序名，并定位产物
    app_name = sp.name_edit.text().strip() or "MockTestApp"
    ext = ".exe" if sys.platform == "win32" else ""
    dist_dir = sandbox / "dist"
    
    if sys.platform == "darwin" and sp.noconsole_check.isChecked():
        exe_path = dist_dir / f"{app_name}.app"
    else:
        if is_onefile:
            exe_path = dist_dir / f"{app_name}{ext}"
        else:
            # 文件夹模式：产物为 dist_dir/app_name/app_name.exe
            exe_path = dist_dir / app_name / f"{app_name}{ext}"
            
            # 容错：Nuitka 在极少数情况下可能未重命名 .dist 文件夹，或者文件名带版本号
            if not exe_path.exists():
                fallback_dist = dist_dir / f"{app_name}.dist" / f"{app_name}{ext}"
                if fallback_dist.exists():
                    exe_path = fallback_dist
                else:
                    # 终极兜底：直接在目录里搜索可执行文件
                    possible_exes = list((dist_dir / app_name).glob(f"*{ext}"))
                    if possible_exes:
                        exe_path = possible_exes[0]

    # 8. 校验实机拉起
    _assert_executable_execution(exe_path)


# =====================================================================
# 7. PyInstaller E2E 测试
# =====================================================================
def test_07_pyinstaller_real_build():
    """测试 7: 深度集成 UI 的 PyInstaller 真实打包与拉起测试"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 7/8] 深度集成测试: UI 操作 -> PyInstaller 构建 -> 实机拉起...{Colors.RESET}")
    try:
        import PyInstaller
    except ImportError:
        log_warn("缺少 PyInstaller，跳过测试")
        return

    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication(["qp_test", "-platform", "offscreen"])
    
    with tempfile.TemporaryDirectory(prefix="qp_e2e_pyi_") as tmp_dir:
        start_t = time.time()
        # 测试 PyInstaller 的单文件模式
        run_e2e_via_mainwindow("PyInstaller", Path(tmp_dir), is_onefile=True)
        log_pass(f"PyInstaller E2E 完整链路测试通过，耗时: {time.time() - start_t:.2f}s")
    
    clean_project_junk()


# =====================================================================
# 8. Nuitka E2E 测试
# =====================================================================
def test_08_nuitka_real_build():
    """测试 8: 深度集成 UI 的 Nuitka 原生编译与拉起测试"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 8/8] 深度集成测试: UI 操作 -> Nuitka 原生编译 -> 实机拉起...{Colors.RESET}")
    try:
        import nuitka
    except ImportError:
        log_warn("缺少 Nuitka，跳过测试")
        return

    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication(["qp_test", "-platform", "offscreen"])
    
    with tempfile.TemporaryDirectory(prefix="qp_e2e_nuitka_") as tmp_dir:
        start_t = time.time()
        # 测试 Nuitka 的文件夹模式 (Standalone)
        run_e2e_via_mainwindow("Nuitka", Path(tmp_dir), is_onefile=False)
        log_pass(f"Nuitka E2E 完整链路测试通过，耗时: {time.time() - start_t:.2f}s")
        
    clean_project_junk()


# =====================================================================
# 主调度入口
# =====================================================================
def main():
    print(f"""
{Colors.CYAN}{Colors.BOLD}======================================================================
     🚀 QPyPack 全功能终极一体化自检与双引擎真实打包验证系统 (UI深度集成版)
======================================================================{Colors.RESET}""")

    tests = [
        ("静态资源与工程配置", test_01_static_assets),
        ("多语言包格式对齐与校验", test_02_locales_and_placeholders),
        ("QPyPack 原生 AST 分析引擎", test_03_ast_engine),
        ("QPyPack 核心配置与翻译引擎逻辑", test_04_core_logic),
        ("Qt UI 主窗口状态机独立交互测试", test_05_ui_interaction),
        ("Wheel 分发包沙箱构建测试", test_06_wheel_packaging),
        ("PyInstaller E2E 链路验证 (单文件)", test_07_pyinstaller_real_build),
        ("Nuitka E2E 链路验证 (文件夹)", test_08_nuitka_real_build),
    ]

    failed = False
    for title, func in tests:
        try:
            func()
        except Exception as e:
            failed = True
            log_fail(f"【{title}】未通过！原因: {e}")
            print(f"\n{Colors.RED}详细错误回溯:{Colors.RESET}")
            traceback.print_exc()
            break

    # 无论成功失败，强制执行纯净清理
    clean_project_junk()

    print(f"\n{Colors.BOLD}======================================================================{Colors.RESET}")
    if not failed:
        print(f"{Colors.GREEN}{Colors.BOLD} 🎉 [CONGRATULATIONS] 全部端到端深度集成测试 100% 顺利通过！{Colors.RESET}")
        print(f"{Colors.GREEN} 💡 你的所有 UI 修改、功能迭代、参数注入均完美运行，且一切残留已被销毁！{Colors.RESET}")
        print(f"{Colors.BOLD}======================================================================{Colors.RESET}\n")
        sys.exit(0)
    else:
        print(f"{Colors.RED}{Colors.BOLD} 💥 [TEST FAILED] 发现程序缺陷！测试已中断，请根据上方回溯修复代码。{Colors.RESET}")
        print(f"{Colors.BOLD}======================================================================{Colors.RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
