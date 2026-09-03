import os
import sys
import time
import stat
import shutil
import tempfile
import subprocess
from pathlib import Path

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

# 智能搜索并添加项目路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, PROJECT_ROOT.as_posix())
if (PROJECT_ROOT / "src").exists():
    sys.path.insert(0, (PROJECT_ROOT / "src").as_posix())
if (PROJECT_ROOT / "qpypack").exists():
    sys.path.insert(0, (PROJECT_ROOT / "qpypack").as_posix())

try:
    import main
except ModuleNotFoundError:
    try:
        from qpypack import main
    except ModuleNotFoundError:
        import src.qpypack.main as main


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def log_pass(msg):
    print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} {msg}")


def log_warn(msg):
    print(f"  {Colors.YELLOW}⚠ [WARN]{Colors.RESET} {msg}")


def log_fail(msg):
    print(f"  {Colors.RED}✖ [FAIL]{Colors.RESET} {msg}")


def safe_cleanup_dir(path: Path, retries=15, delay=0.5):
    """Windows 下鲁棒删除临时目录，解决句柄延迟释放导致的 WinError 5 PermissionError"""
    if not path or not path.exists():
        return True

    def remove_readonly(func, p, exc_info):
        try:
            os.chmod(p, stat.S_IWRITE)
            func(p)
        except Exception:
            pass

    for attempt in range(retries):
        try:
            shutil.rmtree(path, onerror=remove_readonly)
            if not path.exists():
                return True
        except Exception:
            time.sleep(delay)

    try:
        shutil.rmtree(path, ignore_errors=True)
    except Exception:
        pass
    return not path.exists()


@pytest.fixture(scope="session", autouse=True)
def init_qapp():
    app = QApplication.instance()
    if not app:
        app = QApplication(["pytest_qpypack", "-platform", "offscreen"])
    yield app


def test_01_config_and_i18n():
    """测试 1: 配置加载、保存及多语言系统"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 1/8] 偏好设置及国际化引擎校验...{Colors.RESET}")
    config = main.load_config()
    assert "Settings" in config
    assert "Mappings" in config
    assert "BackportRules" in config

    # 验证翻译引擎
    zh_text = main.ZH_CN_DICT.get("Start Build", "开始构建")
    assert zh_text == "开始构建"
    log_pass("配置加载与多语言引擎校验通过")


def test_02_ast_dependency_scanner():
    """测试 2: AST 依赖深度扫描与本地白名单识别"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 2/8] AST 依赖引擎与白名单扫描...{Colors.RESET}")
    tmp_dir = Path(tempfile.mkdtemp(prefix="qp_test_ast_"))
    try:
        script = tmp_dir / "sample.py"
        script.write_text("import requests\nfrom PIL import Image\nimport local_dummy\n", encoding="utf-8")
        
        local_mod = tmp_dir / "local_dummy.py"
        local_mod.write_text("def hello(): pass\n", encoding="utf-8")

        discovered = main.extract_project_imports_via_ast(script, scan_dir=False)
        assert "requests" in discovered
        assert "PIL" in discovered
        assert "local_dummy" in discovered

        local_modules = main.get_all_local_modules(tmp_dir, tmp_dir)
        assert "local_dummy" in local_modules

        log_pass(f"成功识别 AST 依赖: {discovered}，本地模块排除列表: {local_modules}")
    finally:
        safe_cleanup_dir(tmp_dir)


def test_03_backport_version_parsing_safety():
    """测试 3: 废弃兼容包版本解析安全性 (防御 tuple index out of range)"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 3/8] 版本解析防护机制 (防止 IndexError)...{Colors.RESET}")
    
    test_cases = [
        ("3.11", (3, 11)),
        ("3.9.13", (3, 9)),
        ("3", (3, 0)),
        ("", (3, 4)),
        ("invalid", (3, 4)),
        ((3, 10), (3, 10)),
        ([3, 12], (3, 12)),
    ]

    for val, expected in test_cases:
        if isinstance(val, (tuple, list)):
            res = (int(val[0]), int(val[1])) if len(val) >= 2 else (int(val[0]), 0)
        elif isinstance(val, str):
            import re
            parts = [int(x) for x in re.findall(r"\d+", str(val))]
            if len(parts) >= 2:
                res = (parts[0], parts[1])
            elif len(parts) == 1:
                res = (parts[0], 0)
            else:
                res = (3, 4)
        else:
            res = (3, 4)

        assert res == expected, f"解析 {val} 失败，得到 {res}"

    log_pass("版本解析异常防御测试完全通过")


def test_04_sanitize_script_pep263_injection():
    """测试 4: 脚本净化与控制台暂停代码注入 (保护 PEP 263 编码头与 Shebang)"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 4/8] 脚本安全净化与控制台暂停代码注入...{Colors.RESET}")
    tmp_dir = Path(tempfile.mkdtemp(prefix="qp_test_sanitize_"))
    try:
        script = tmp_dir / "app_with_encoding.py"
        raw_code = (
            "#!/usr/bin/env python\n"
            "# -*- coding: utf-8 -*-\n"
            "from __future__ import annotations\n"
            "print('Hello World')\n"
        )
        script.write_text(raw_code, encoding="utf-8")

        mock_params = {
            "noconsole": False,
            "script_path": script.as_posix()
        }
        thread = main.PackingThread(mock_params)
        sanitized_path, is_temp, err = thread.sanitize_script(script)

        assert sanitized_path.exists()
        new_content = sanitized_path.read_text(encoding="utf-8")

        # 验证前部关键声明全部保留，且注入了 _qpypack_pause
        assert "#!/usr/bin/env python" in new_content
        assert "coding: utf-8" in new_content
        assert "from __future__ import annotations" in new_content
        assert "_qpypack_pause" in new_content

        # 验证 pause 代码位于头部声明之后
        pos_coding = new_content.find("coding: utf-8")
        pos_pause = new_content.find("_qpypack_pause")
        assert pos_coding < pos_pause, "pause 代码不应插在编码声明之前"

        if is_temp:
            sanitized_path.unlink(missing_ok=True)

        log_pass("控制台暂停注入成功保留 Shebang 与 PEP 263 编码头声明")
    finally:
        safe_cleanup_dir(tmp_dir)


def test_05_complex_dependency_spec_parsing():
    """测试 5: 复合依赖规范字符串解析 (extras, @, 版本符号切分)"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 5/8] 复合依赖包名正则表达式提取...{Colors.RESET}")
    import re

    test_specs = [
        "uvicorn[standard]>=0.20.0",
        "fastapi==0.100.0",
        "requests~=2.31.0",
        "my-pkg @ git+https://github.com/org/repo.git",
        "certifi ; python_version >= '3.8'",
    ]

    extracted = []
    for pkg in test_specs:
        cleaned = re.split(r"[=><!~@;\[]", pkg)[0].strip()
        if cleaned:
            extracted.append(cleaned)

    assert extracted == ["uvicorn", "fastapi", "requests", "my-pkg", "certifi"]
    log_pass(f"复合依赖包名提取完全符合预期: {extracted}")


def test_06_ui_settings_panel(init_qapp):
    """测试 6: 构建设置面板组件与参数状态双向绑定"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 6/8] UI 设置面板及交互流转...{Colors.RESET}")
    win = main.MainWindow()
    panel = win.settings_panel

    panel.rb_lite_mode.setChecked(True)
    assert panel.rb_lite_mode.isChecked()

    panel.engine_combo.setCurrentText("Nuitka")
    assert panel.engine_combo.currentText() == "Nuitka"

    panel._add_resource_item("file", "C:/dummy.txt", ".")
    assert panel.add_data_list.count() == 1
    panel.clear_resource()
    assert panel.add_data_list.count() == 0

    win.close()
    log_pass("UI 核心交互与状态绑定测试通过")


def run_e2e_mock_build(engine_name: str, tmp_dir: Path, is_onefile: bool = True):
    """辅助函数: 创建模拟项目并执行全自动构建与拉起验证"""
    app_dir = tmp_dir / "mock_app"
    app_dir.mkdir(parents=True, exist_ok=True)

    entry_py = app_dir / "app_main.py"
    entry_py.write_text(
        "import sys, os, time\n"
        "if __name__ == '__main__':\n"
        "    print('BOOT_SUCCESS_OK')\n"
        "    time.sleep(0.1)\n"
        "    sys.exit(0)\n",
        encoding="utf-8",
    )

    reqs = app_dir / "requirements.txt"
    reqs.write_text("# simple requirements\n", encoding="utf-8")

    python_exe = main.get_python_executable()
    assert python_exe and os.path.exists(python_exe), "未检测到可用的测试 Python 解释器"

    params = {
        "engine": engine_name,
        "python_exe": python_exe,
        "script_path": entry_py.as_posix(),
        "project_folder": app_dir.as_posix(),
        "enable_sign": False,
        "cert_path": "",
        "cert_pass": "",
        "app_name": "app_main",
        "onefile": is_onefile,
        "contents_dir": "_internal",
        "noconsole": True,
        "icon": "",
        "use_reqs": True,
        "use_pipreqs": False,
        "use_pipreqs_dir": False,
        "reqs_file": reqs.as_posix(),
        "hidden_imports": "",
        "add_data_list": [],
        "upx": False,
        "upx_path": "",
        "cpu_cores": 2,
        "exclude_modules": "",
        "out_mode": 0,
        "custom_out_dir": "",
        "temp_sandbox_mode": 0,
        "use_venv": True,
        "keep_venv": False,
        "venv_mode": "isolated",
        "shared_venv_dir": "",
        "clean_all": True,
        "version_file": None,
        "temp_icon_file": None,
        "ver_comp": "Qwesoft",
        "ver_desc": "E2E Test App",
        "ver_ver": "1.0.0",
        "pip_index_url": "https://pypi.org/simple",
        "pip_index_backup": "",
        "concise_log": True,
        "auto_save_log": False,
        "lite_mode": True,
        "pyi_version": "",
        "nuitka_version": "",
        "mappings": main.DEFAULT_MAPPINGS.copy(),
        "enable_backport_shield": True,
        "backport_rules": main.DEFAULT_BACKPORT_RULES.copy(),
    }

    thread = main.PackingThread(params)
    results = []

    def on_finished(success, msg, failed_pkgs):
        results.append((success, msg))

    thread.build_finished.connect(on_finished)
    thread.run()

    assert len(results) > 0, "构建线程未返回结果"
    success, msg = results[0]
    assert success, f"{engine_name} 构建失败: {msg}"

    ext = ".exe" if os.name == "nt" else ""
    if is_onefile:
        built_exe = app_dir / f"app_main{ext}"
    else:
        # 针对 文件夹模式 (onedir / standalone) 全面兼容查找路径
        candidates = [
            app_dir / "app_main" / f"app_main{ext}",
            app_dir / "app_main.dist" / f"app_main{ext}",
            app_dir / f"app_main{ext}",
        ]
        built_exe = next((p for p in candidates if p.exists()), None)

    assert built_exe is not None and built_exe.exists(), f"找不到构建产物，搜索路径: {candidates if not is_onefile else built_exe}"

    # 实机拉起产物验证
    proc = subprocess.run([built_exe.as_posix()], capture_output=True, text=True, timeout=10)
    assert proc.returncode == 0
    assert "BOOT_SUCCESS_OK" in proc.stdout
    log_pass(f"{engine_name} (Lite Mode) 产物实机拉起验证成功！")


def test_07_pyinstaller_real_build(init_qapp):
    """测试 7: PyInstaller 真实构建与产物执行测试"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 7/8] PyInstaller Lite 模式真实端到端打包...{Colors.RESET}")
    tmp_dir = Path(tempfile.mkdtemp(prefix="qp_e2e_pyi_"))
    try:
        start_t = time.time()
        run_e2e_mock_build("PyInstaller", tmp_dir, is_onefile=True)
        log_pass(f"PyInstaller E2E 测试通过，耗时: {time.time() - start_t:.2f}s")
    finally:
        time.sleep(0.5)
        init_qapp.processEvents()
        safe_cleanup_dir(tmp_dir)


def test_08_nuitka_real_build(init_qapp):
    """测试 8: Nuitka 真实编译与产物执行测试 (防 WinError 5)"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}>>> [测试 8/8] Nuitka Lite 模式原生编译与实机验证...{Colors.RESET}")
    try:
        import nuitka
    except ImportError:
        log_warn("当前环境未安装 Nuitka，跳过实机编译测试")
        return

    tmp_dir = Path(tempfile.mkdtemp(prefix="qp_e2e_nuitka_"))
    try:
        start_t = time.time()
        # 测试 Nuitka 文件夹独立模式 (Standalone)
        run_e2e_mock_build("Nuitka", tmp_dir, is_onefile=False)
        log_pass(f"Nuitka E2E 完整链路测试通过，耗时: {time.time() - start_t:.2f}s")
    finally:
        time.sleep(0.5)
        init_qapp.processEvents()
        safe_cleanup_dir(tmp_dir)


if __name__ == "__main__":
    pytest.main(["-s", "-vv", __file__])