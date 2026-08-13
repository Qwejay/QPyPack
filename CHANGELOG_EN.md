# Changelog

All notable changes to the **QPyPack** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**English** | [中文版](./CHANGELOG.md)

---

# Changelog

---
## [2.7.10] - 2026-08-13

### Added
- **Shared Virtual Environment Mode**: Introduced an Isolated/Shared toggle for virtual environments. Shared mode allows specifying a unified directory, enabling dependency reuse across different scripts and saving disk space.
- **Pre-flight Health Checks**: Added automatic validation of available RAM, disk space, and Python interpreter status before the build process starts, blocking inadequate environments early with clear warnings.
- **Pre-build Configuration Validation**: The packager now verifies the validity of script paths, icon paths, additional resources, and output directory write permissions upfront, preventing mid-build failures caused by invalid configurations.
- **System Constants Extraction**: Moved hardcoded thresholds (e.g., timeouts, memory/disk limits, retry limits) into global constants for better project maintainability.

### Changed
- **Enhanced Build Interruption**: Improved the "Stop Build" logic to gracefully terminate background compilation processes first, falling back to a force-kill only on timeout. This prevents orphaned background processes.
- **Optimized Cache Cleanup**: Strengthened the temporary file cleanup process after builds. It now retries when files are locked by the system or antivirus, and summarizes any uncleared residual files in the log.
- **Improved Execution Stability**: Refined the error handling for background command execution. Added strict timeout controls and better detection for missing commands, preventing silent failures and UI freezes.
- **Refined Log Leveling**: The internal logging system now more accurately categorizes message levels (info, warning, error), providing better structure for troubleshooting.

### Fixed
- **Health Check Crash**: Fixed an issue where the pre-flight health check would crash the application due to an uninitialized variable.
- **Resource Validation Error**: Fixed a crash caused by attempting to process invalid or empty data in the additional resources list during configuration validation.
- **Redundant Validation Logic**: Removed dead code that performed duplicate checks on the script path during the build startup phase.
- **Duplicate Permission Testing**: Fixed a redundant double write-permission test when setting up a shared virtual environment directory.
- **Missing Translations**: Added missing Chinese/English translations for shared directory warnings, disk space alerts, and health check error messages.

---

## [2.7.9] - 2026-08-12

#### Added
- **Build Diagnostics & Stack Tracing**: Added build environment diagnostics header and fatal traceback capturing, with a new `[DETAILED_ONLY]` log routing tag to keep concise logs clean.
- **Venv Fault-Tolerance**: Automatically renames invalid virtual environments as backups when cleanup fails, providing clear manual instructions if backup fails.
- **Adaptive Memory Concurrency**: Dynamically adjusts Nuitka `--jobs` concurrency based on free physical memory and automatically enables `--low-memory` flag under memory pressure.

#### Fixed
- **Config Load Bug**: Fixed an issue where the "Keep Local Venv" (`keep_venv`) setting was mistakenly reset to `False` when loading configurations.
- **Missing Nuitka Flags**: Restored the missing `--jobs` multi-core compilation parameter in Nuitka build commands.
- **Product Name Truncation**: Improved string suffix matching when stripping version tags from app names to prevent accidental truncation or slicing errors.

---

## [2.7.8] - 2026-08-11

#### Added
- **Asynchronous Background Venv Cleanup**: Introduced a background worker thread to offload scanning and deletion of local virtual environments from the UI thread, preventing interface freezing during large folder cleanups while accurately calculating and displaying freed disk space.
- **Automatic Pip Permission Fallback & Retry**: Automatically retries dependency installation using `--user` mode if the system Python environment lacks write permissions, further improving build success rates.
- **Updated AI Translation Tool**: Added support for auto-patching missing translation dictionaries back into the main application, and standardized English bracketed tags for all log prefixes.

#### Fixed
- **Thorough Temporary Directory Cleanup**: Fixed an issue where custom temp paths were not fully deleted in non-sandbox mode. Optimized with robust recursive cleanup to completely free residual build caches.
- **UI State Synchronization Fix**: Fixed an issue where the "Keep Local Venv" checkbox was not properly reset when dragging in a new script or resetting the workspace.

---

## [2.7.7] - 2026-08-09

#### Added
- **Configuration Write Protection**: Introduced an atomic save mechanism to completely prevent configuration loss or corruption caused by power outages, system crashes, or full disks.
- **Enhanced Encoding Compatibility**: Upgraded the reading logic for source code and dependencies to intelligently support various complex encodings (such as GBK and UTF-8 with BOM), eliminating crashes and garbled text.
- **Antivirus Interception Resistance**: Added a smart retry mechanism to the build output stage, effectively resolving "Permission Denied" errors caused by security software temporarily locking files during generation.
- **Stability Enhancements**: Added global exception logging and isolated environment variables during engine compilation to avoid interfering with main program operations.

#### Fixed
- Fixed a crash caused by path resolution issues resulting in `[WinError 1]` when packaging under certain RamDisk environments.
- Fixed a bug where the "Temporary Directory" option in the settings panel did not fully apply to virtual environments and the PyInstaller cache.

---

## [2.7.6] - 2026-08-08

#### Added
- **Smart Project Sandbox Sensing**: Generates unique sandbox identifiers based on script path hashes and Python version/architecture. Automatically detects and reuses existing virtual environments upon loading project scripts.
- **One-Click Virtual Environment Cleanup**: Added a project virtual environment cleanup feature in the Settings panel, automatically scanning associated virtual environments and providing one-click cleanup to free up disk space.
- **AI Translation Tool**: Introduced `update_locales_ai.py`, a modern GUI translation management studio that automatically completes and updates application translations with one click using LLM APIs.
- **Window Size Memory**: Automatically remembers and restores window size adjustments, ensuring custom dimensions are preserved across application restarts.

#### Improved
- **Self-Healing Environment & Fallback**: Refactored virtual environment validation logic. Automatically falls back to a temporary sandbox if environment corruption or purge failure is detected, ensuring zero-interruption builds.
- **Thorough Cross-Platform Process Reclamation**: Optimized build cancellation logic by introducing independent process session group termination on Linux / macOS, completely eliminating leftover background processes upon canceling builds.
- **Environment Detection & Fallback Alerts**: Optimized timeout handling for Python interpreter version and architecture (x64/x86) detection, adding robust exception handling and fallback log alerts.
- **UI Copy Refinement**: Refactored dependency and virtual environment checkbox labels, unifying cleanup confirmation dialog button styles and risk warnings.

#### Fixed
- **i18n String Synchronization**: Completed and synchronized Simplified Chinese mappings for new UI strings, including environment cleanup, timestamp signing logs, and fallback warnings.

---

## [2.7.5] - 2026-08-06

#### Added
- **Code Signing & Timestamping**: Added automatic digital signing for Windows / macOS build artifacts, supporting `.pfx` self-signed certificate generation and commercial certificate configuration; integrated timestamp server (TSA) stamping for Windows signatures with support for authoritative providers like Microsoft, DigiCert, and Sectigo.
- **macOS DMG Building**: CI/CD build workflows now support automatically generating `.dmg` installer images for macOS.

#### Improved
- **macOS Default Signing**: Enabled Ad-hoc signing by default on macOS, resolving the "App is damaged and can't be opened" error when running unsigned binaries on M-series Apple Silicon chips.
- **Cross-Platform Packaging**: Refactored CI/CD automated build workflows, optimizing PySide6 plugin dependency bundling and stability on Linux.
- **OS Support Matrix**: Adjusted interpreter detection logic to dynamically evaluate and display compatibility requirements across operating systems and architectures.
- **UI & Copywriting Enhancements**: Unified cross-platform file dialog rendering mechanics; updated default author to "Independent Developer" and app description to "Desktop Application".

#### Fixed
- **Localization & i18n Sync**: Completed and synchronized signature log entries and text box context menu translations across 8+ languages (Simplified/Traditional Chinese, Japanese, Korean, German, French, Spanish, Portuguese, Russian, etc.).
- **Process Resource Cleanup**: Optimized process pipe and handle cleanup logic when packaging tasks terminate abnormally.

---

## [2.7.4] - 2026-08-05

#### Added
- **Packaging Mode Selection**: Supports switching between "Compatibility Mode" and "Lite Mode". Compatibility Mode minimizes build errors, while Lite Mode produces smaller output sizes and provides automated retry tips upon build failures.
- **Keep Virtual Environment**: Supports generating and reusing local virtual environments per project without recreating them every time, significantly accelerating rebuilds.

#### Improved
- **Nuitka Strategy Optimization**: Dynamically optimizes packaging parameters for frameworks like `playwright` and `ttkbootstrap` in Lite Mode to further shrink output size.
- **Context Menu Enhancement**: Dynamically loads Qt system translation packages for improved multilingual native context menus and dialogs, and fixed a bug where the context menu background rendered in black (took an entire afternoon to fix==!).
- **UI & Visual Consistency**: Explicitly configured the Fusion light theme Palette, unified global context menu styling, and optimized preset button layouts and page margins.
- **AST Dependency Scanning**: Scanning paths now automatically exclude virtual packaging directories, and package name comparisons are standardized to lowercase.
- **Bug Fixes & Tweaks**: Fixed audio alert toggle logic; added support for independent subprocess environment variables; strengthened null-pointer checks in tables; updated translations and fixed multiple minor bugs.

## [2.7.3] - 2026-08-04

#### Added
* **Python Environment Manager**: Added a new management dialog that supports intelligent detection and switching of local Python installations, as well as one-click download/installation via official or mirror sources.
* **Folder Mode (`--onedir`)**: Added Folder Mode to execution settings, along with support for customizable internal contents directory names (`--contents-directory`).
* **Native AST Dependency Analysis**: Refactored the dependency scanner using native AST parsing instead of `pipreqs`, significantly improving speed and accuracy for implicit dependency detection.
* **Playwright Mirror Acceleration**: Added mirror source downloads for Playwright browser binaries with automatic fallback to official CDNs.

#### Improved
* **Dynamic UPX Exclusion**: Upgraded UPX compression rules to automatically detect and exclude core Python DLLs and `vcruntime140_1.dll` to prevent runtime errors.
* **Thread & Interruption Control**: Strengthened build cancellation and cleanup logic to prevent lingering threads and locked temporary files.
* **Platform Compatibility & Timeouts**: Optimized macOS Bundle Identifier generation and introduced command execution timeout protection.
* **UI Polish**: Refactored execution mode radio buttons, streamlined About tab layout and spacing, and updated copyright notices.
* **i18n Updates**: Refined wording and updated translations across various UI text and logs.

---

## [2.7.2] - 2026-08-03

### Key Improvements
* **Compiler Selection Strategy Refactored**: Removed hardcoded Zig compiler forcing for Python 3.13+. Prioritizes local MSVC / Clang / GCC(MinGW64) environments; falls back to Nuitka auto-detection and toolchain download if none are found.
* **Updated Compatibility Matrix**: Refined interpreter status cards to accurately reflect Nuitka's adaptive C compiler detection capabilities.
* **Enhanced Build Prompts**: Displays MinGW-w64 auto-download notices when no local compiler is found; adds explicit detection feedback for local compilers.
* **UI Polish**: Updated resource list tooltips to recommend saving via "Export Preset"; simplified temporary directory selection labels.
* **Restored Default Dependency Directory**: Reverted PyInstaller's one-dir dependency folder name back to the official default (`_internal`), allowing packaged apps to share runtime libraries and reduce disk footprint.
* **State Persistence Optimized**: The custom output directory setting is no longer cleared when loading a new script or resetting the workspace, improving the workflow for continuous packaging.

---

## [2.7.1] - 2026-08-02

### Added
* **Lock-Prevention Temp Directory Option**: Added a "Temp Directory" location setting on the Settings page, allowing Nuitka's intermediate compilation sandbox to be switched to the system Temp directory. This resolves build interruption issues caused by OneDrive or antivirus software locking files.

### Improved
* **Seamless Multi-Version Rebuilding**: After packaging is completed, switching Python interpreters or saving and returning from configuration changes now automatically retains the loaded script state. Icons, version metadata, implicit imports, and additional resources are 100% preserved, eliminating the tedious workflow of repeatedly dragging files or reloading presets.

---

## [2.7.0] - 2026-08-01

### Added
* **Automated Compiler Sniffing & Invocation**: Added auto-detection and invocation for `Clang` (LLVM) and `Zig` (optimized for Python 3.13+ C backend) compilers in Nuitka, prioritizing MSVC (`--msvc=latest`) or Clang when available.
* **Zero-Config Package Presets**: PyInstaller engine now includes automated `--collect-all` and `--collect-data` handling for frequently problematic packages like `ttkbootstrap`, `customtkinter`, `playwright`, and `moviepy`.
* **Dual-Mode Real-Time Log Viewer**: Introduced a dual-mode log viewer with "Concise Mode" and "Detailed Mode" stacked views, supporting real-time seamless switching, clearing, and exporting above the log panel.
* **Smart Python Platform Compatibility Matrix**: Added a dynamic HTML platform support matrix to the Python interpreter selector in Settings, displaying real-time compatibility status for Windows 7/8/10/11, macOS, and Linux along with official download links.
* **Build Fault Tolerance & Fallback Protection**: Added pre-compilation system RAM and disk space evaluation; automatically triggers single-thread (`--jobs=1`) fallback retries on `ZstdError` (OOM) and strips icon flags if antivirus software locks icon resources.

### Fixed
* **Source Encoding & BOM Compatibility**: Fixed an issue where the AST module could throw decoding exceptions on source code containing BOM (`utf-8-sig`) or non-standard system fallback encodings.
* **Cloud Drive Sync Warning**: Fixed unexpected build interruptions caused by OneDrive/Dropbox file synchronization locks by introducing early lock detection and warnings.
* **Console Runtime Crash**: Fixed crashes caused by console "pause on exit (`input`)" scoping conflicts by refactoring the injection logic to register strictly via `atexit.register`.

### Changed
* **Native In-Process AST Parsing**: Refactored implicit dependency scanning from spawning subprocesses to native same-process AST parsing, drastically reducing system overhead and multiplying scan speed.
* **Asynchronous Parallel Environment Detection**: Introduced multi-threaded concurrent detection for candidate Python environments, eliminating startup I/O blocking.
* **Pure Vector UI & Emoji Cleanup**: Stripped emojis from sidebars, tab headers, and language selectors in favor of Google Material SVG vector icons, eliminating font fallback glitches and layout jumps on Linux and older Windows systems.
* **Granular Build Progress Feedback**: Main drop cards and status bars now capture and stream live compilation progress text from backend engines (Nuitka / Scons / PyInstaller), eliminating waiting anxiety.
* **Redesigned About Page & Sponsorship Integration**: Overhauled the About tab layout with interactive action buttons for GitHub, PyPI, and Issues, introducing a voluntary sponsorship encouragement section.
* **Atomic Dependency Resolution & Fallback**: Unified dependency build logic into an atomic manifest; automatically strips strict version constraints (`==`) and retries if specific version installs fail.
* **Native Byte-Stream Icon Generation**: Removed reliance on macOS `sips` CLI tool, refactoring pure Python byte-stream assembly for cross-platform `.ico` and `.icns` generation.
* **Expanded Package Mapping Library**: Expanded the built-in package mapping library to cover common third-party packages such as `pyside6_addons`, `pyside6_essentials`, `attrs`, `psycopg2-binary`, etc.

---

## [2.6.2] - 2026-07-27

* **UI Slide Transition Animations**: Refactored page switching logic with dual-layer smooth slide animations, eliminating visual flickering and icon displacement when returning to the main dashboard.
* **Non-Intrusive Notification System**: Fully replaced invasive `QMessageBox` popups with lightweight status bar Toast notifications to maintain smooth packaging workflows.
* **Error Log Red Highlighting**: Automatically expands the log panel and highlights fatal exceptions, locked files, or missing dependencies in bright red HTML font for fast troubleshooting.
* **GNU gettext Engine Refactor**: Introduced `TranslationEngine`, refactoring hardcoded Chinese strings into English Base Keys; built-in `zh_CN` fallback dictionary ensures zero external dependency execution.
* **Global Multilingual Support**: Added translation packages for Japanese (`ja_JP`), Korean (`ko_KR`), French (`fr_FR`), German (`de_DE`), Spanish (`es_ES`), Russian (`ru_RU`), Portuguese (`pt_BR`), and Traditional Chinese (`zh_TW`).
* **Smart Language Selector**: Added language selector dropdown in Settings displaying native language names (e.g., Deutsch, Français) with automatic OS locale detection.
* **Scope Variable Collision Fix**: Fixed a critical issue where `QFileDialog` unpacking (`fp, _`) accidentally shadowed global translation function `_()`, causing local scope crashes.
* **Qt Animation Engine Warning**: Fixed low-level geometry animation warnings (`starting an animation without end value`) when applied to `QStackedLayout`.
* **PyPI Static Asset Packaging**: Updated `pyproject.toml` to include `locales/*.json` resources, ensuring i18n support works seamlessly after `pip install`.

---

## [2.6.1] - 2026-07-25

* **Dependency Contamination Elimination**: Fixed a bug in "Lite Mode" where AST incorrectly traversed parent directories, preventing unrelated packages from leaking into the output bundle.
* **Build Sandbox Isolation**: Isolated target scripts in dedicated sandboxes during parsing to prevent interference from adjacent files; added an option to "Allow scanning all files in directory".
* **MSVC Smart Detection**: Added C++ compilation environment sniffing. If MSVC is installed, Nuitka automatically applies `--msvc=latest`, prioritizing native compilers and skipping MinGW downloads.
* **UPX Warning Suppression**: Automatically recognizes and ignores UPX compression errors on system core DLLs, slightly boosting build speed.

---

## [2.6.0] - 2026-07-24

### 🎨 UI & UX Refactoring
* **Tab Navigation Refactor**: Reorganized TAB layouts for improved aesthetics and usability.
* **Typography & Layout Refinement**: Compacted engine description boxes; introduced cross-platform safe font stacks with graceful fallbacks.
* **High-DPI Rendering**: Prioritized extracting 256px HD icon layers combined with floating-point precision rendering, eliminating icon blurriness on 125%~200% DPI scales.

### 🛠️ Engine & Stability Fixes
* **Package Name Fallback**: Built-in C-extension hardcoded mapping dictionary to prevent "module not found" errors.
* **False Mirror Timeout Suppression**: Smartly identifies pip package name typos to prevent false "Mirror Connection Timeout" alerts when network connections are normal.
* **Read-Only Directory Protection**: Console anti-crash scripts are now written to system temp directories to prevent build interruptions in read-only source folders.

---

## [2.5.7] - 2026-07-23

* **Log Context Menu**: Added "Clear Log" and "Export Log" options.
* **Dropdown & Styling Fixes**: Fixed text overlapping bugs in non-editable combo boxes.
* **Button & Layout Standardization**: Unified sizes for action buttons like "Browse" and "AST Scan".
* **UX Enhancements**: Enabled auto-wrapping for drag-and-drop region titles to prevent UI clipping on long file paths.

---

## [2.5.6] - 2026-07-23

* **PIP Dual-Source Backup**: Added backup PyPI mirror configuration and auto-retry fallback mechanisms, pre-loaded with major Chinese PyPI mirrors.
* **UI Visual Overhaul**: Refactored `QComboBox` drop-down popups to unify minimal white themes and scrolling experiences; centered Tab bar labels and set minimum window width (710px).
* **Packaging Stability**: Full-lifecycle control over dependency installations with auto-fallback mirror switching; populated Windows binary metadata `VarFileInfo` translation headers; optimized exclusion strategies in Lite Mode.

---

## [2.5.5] - 2026-07-22

* **Accidental Deletion Prevention**: Optimized `build/dist` smart cleanup to protect desktop and workspace directories.
* **Full Sandbox Compilation**: Isolated build outputs in system temp directories, resolving cross-drive and path separator issues.
* **Path Mapping & UX Fixes**: Redirected `cwd` to source script directories during builds to resolve relative path references; fixed `open_dist` folder opening behavior.
* **pipreqs Crash Fix**: Resolved encoding crashes during automated dependency scanning.

---

## [2.5.4] - 2026-07-18

* **Lite Mode Introduced**: Automatically strips redundant modules like `pip` and `unittest` and enables Nuitka `-OO` optimization to drastically reduce output size; paired with deep source scanning (up to 500 local dependencies) to maintain runtime stability.
* **False UPX Error Fix**: Explicitly passes `--noupx` when UPX is unchecked, blocking PyInstaller from quietly invoking system UPX tools and generating log noise.
* **Log Encoding Fix**: Enforced `encoding="utf-8"` across all underlying process calls (`subprocess`), solving console encoding garbles on Windows systems with GBK defaults.

---

## [2.5.3] - 2026-07-17

* **Engine Version Locking**: Allows custom version pin settings for Nuitka, PyInstaller, and pipreqs in Advanced Settings to prevent upstream breakage.
* **Dynamic Progress UI**: Main dashboard titles now update and cycle build steps in real-time to eliminate perceived hanging.
* **Compilation Crash Fix**: Enforced global UTF-8 environments, resolving fatal GBK encoding errors when Nuitka parses libraries like PyTorch on Chinese Windows systems.
* **High-DPI Rendering Fix**: Resolved font blurriness on fractional scale factors (e.g., 125%) and cleaned up DPI permission errors.
* **Adaptive Dependency Scanning**: Fixed `pipreqs` crashes on non-UTF-8 source files by adding automatic fallback to local encodings.
* **Smart Interpreter Search**: Merged duplicate `.EXE` paths, default-selected current active environment, and stripped `\\?\` path prefixes to prevent subprocess invocation errors.
* **Absolute Clean Recycles**: Added forced cleanup for `nuitka-crash-report.xml` and temporary `__pycache__` folders to keep user directories clean.
* **Icon Update Fix**: Fixed an issue where icons failed to update when initiating new packaging tasks.

---

## [2.5.2] - 2026-07-15

* **Refactored Compiler Command Generators**: Completely separated PyInstaller and Nuitka instruction generation into independent pipelines to eliminate cross-engine flag pollution.
* **Nuitka Asset Path Fix**: Fixed Nuitka compilation crashes when relative target paths for data files were set to `.` via `os.path.normpath` path normalization.
* **Nuitka Module Exclusion Fix**: Standardized module exclusion parameters to Nuitka's official `--nofollow-import-to`.
* **Windows Metadata Mapping**: Correctly mapped application description to `--file-description`, application name to `--product-name`, and added support for `--product-version`.

---

## [2.5.1] - 2026-07-15

* **Multi-Platform CI/CD**: Utilized GitHub Actions to run concurrently across `windows-latest`, `macos-latest`, and `ubuntu-latest`, automatically attaching builds to Tag Releases.
* **Flat Icon Style**: Removed Emoji icons and updated UI to flat Google-style vector icons.
* **Copyright Notice Update**: Removed author name from the window title bar and added a subtle persistent copyright notice on the right side of the status bar.

---

## [2.5.0] - 2026-07-15

* **Cross-Platform Safety & Decoupling**: Fully isolated Windows `winreg` registry calls to ensure safe static module loading on macOS and Linux.
* **Adaptive Image Format Engine**: Introduced `convert_image_to_format` graphics converter supporting SVG, PNG, and JPG conversion into `.ico` and `.icns`.
* **Metadata Translation**: Automatically writes `VSVersionInfo` metadata on Windows and maps standard Bundle IDs (e.g., `com.company.appname`) on macOS.
* **Artifact Extraction**: Refactored output file moving and resetting logic to accurately capture Windows `.exe`, macOS `.app`, and UNIX extensionless binaries.

---

## [2.4.6] - 2026-07-12

* **Cross-Platform Compatibility**: Fixed crashes on non-Windows platforms caused by Windows-specific `creationflags` in subprocess calls; refactored UNIX Python interpreter detectors.
* **Modernized UI & UX**: Adopted card-based layouts and pill-tabs, resolving component overlap issues on low-resolution displays.
* **Multi-Version Kernel Sandboxing**: Supports selecting or browsing any local Python interpreter for code analysis and isolated compilation.
* **About Page Overhaul**: Introduced interactive action rows with seamless links to open-source repositories; fixed ICO anti-aliasing distortion.

---

## [2.4.5] - 2026-07-06

* **Source Parsing Security**: Removed line-ending manipulation (CRLF to LF) during dependency scans and anti-crash injections, preventing multiline string corruption.

---

## [2.4.4] - 2026-07-06

* **Visual Asset Manager**: Added a visual list component supporting file and directory additions via dialogs, with double-click support to modify target release paths.
* **Path Parsing Upgrade**: Rewrote underlying storage and `--add-data` flag construction to prevent absolute paths from being improperly truncated.

---

## [2.4.3] - 2026-07-01

* **Custom Dependency List Support**: Added support for configuring custom `requirements.txt` paths per script.
* **Console Import Fixes**: Adjusted anti-crash injection to write temporary entry scripts in the source directory, preserving relative imports.
* **Background Thread Control**: Replaced unsafe `QThread.terminate()` calls with signal disconnection to eliminate UI freezes and deadlocks.
* **Nuitka Standalone Compatibility**: Switched to dynamic matching for `.dist` output folders, preventing build failures caused by entry point renaming.

---

## [2.4.2] - 2026-06-28

* **Syntax Error Diagnostics**: Automatically scans build logs upon failure to pinpoint `IndentationError`, `SyntaxError`, and `TabError` in source files.
* **Precise Error Localization**: Highlights file names, line numbers, and error messages to distinguish between source code bugs and packaging engine failures.

---

## [2.4.1] - 2026-06-25

* **Modular Settings Refactor**: Reorganized settings into "App Metadata", "Build Control", "Resources & Sandbox", and "Software Settings".
* **Custom Output Directory**: Supports exporting build artifacts to custom global directories with auto-creation of missing parent folders.
* **Compilation Concurrency Limits**: Added options to cap max CPU core usage during parallel compilation.
* **Build Sounds & Auto-Logging**: Introduced system audio notifications upon build completion and options to automatically save `.log` files to the output directory.

---

## [2.4.0] - 2026-06-22

* **Console Anti-Crash Mechanism**: Automatically injects pause logic at the end of scripts when building non-GUI applications.
* **Robust File Deletion**: Refactored temp folder cleanup using `robust_rmtree` with delayed retries and read-only attribute stripping.
* **Cloud Storage Lock Pre-Check**: Added I/O pre-checks to catch OneDrive/Dropbox sync file locks before compilation starts.
* **CI/CD Automation**: Added GitHub Actions workflows to auto-publish releases to PyPI and GitHub Release attachments on Tag pushes.

---

## [2.3.5] - 2026-06-17

* **Triple-Layer Dependency Safety Net**: Refactored dependency resolution into a 3-layer net (`Requirements -> Pipreqs -> AST Scan`), eliminating missing package runtime crashes.
* **Zero Workspace Pollution**: Moved configuration files to global path `~/.qpypack/config.ini` and shifted intermediate build files to system temp folders.
* **Standardized Build Logs**: Introduced CI/CD lifecycle status tags (`[Init]`, `[Env]`, `[Deps]`, `[Build]`, `[Pack]`).
* **Virtual Environment Self-Healing**: Automatically upgrades pip upon isolated venv creation, eliminating verbose legacy module warnings.

---

## [2.3.0] - 2026-06-15

* **GUI Framework Upgrade**: Upgraded from PyQt5 to PySide6 for superior High-DPI scaling support.
* **Streamlined Engines**: Removed cx_Freeze to focus on refining PyInstaller and Nuitka double-engine cores.
* **Nuitka Best Practices**: Enforced `zstandard` compression in single-file mode; enabled `anti-bloat` plugins; added automatic `tkinter` probe detection.

---

## [2.2.0] - 2026-06-14

* **Rebranding**: Officially rebranded to **QPyPack**, standardizing internal sandbox and temp file naming conventions.
* **Watchdog Timeouts**: Added timeout watchdog mechanisms to critical build steps to prevent hanging builds.
* **Smart Output Naming**: Automatically parses script versions to default output names as `{Name}_{Version}`.

---

## [1.0.1] - 2026-05-31

* **Custom PIP Mirror Support**: Added PIP mirror configuration defaulting to Tsinghua University mirrors, with immediate UI application and `QSettings` persistence.
* **Unified Build Logic**: Virtual environment initialization and dependency resolution now strictly adhere to user-configured PIP mirrors.

---

## 📄 License

Copyright (C) 2026 QwejayHuang.  
Licensed under the [GNU General Public License v3.0](LICENSE).