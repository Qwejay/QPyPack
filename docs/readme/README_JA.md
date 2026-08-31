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
  <strong>モダンで使いやすいクロスプラットフォーム対応 Python アプリケーションパッケージング GUI ツール</strong><br>
  <sub>PyInstaller と Nuitka のデュアルエンジンを搭載し、視覚的な設定、静的依存関係解析、自動ビルドパイプラインを提供</sub>
</p>

## 📌 プロジェクト概要 (Overview)

**QPyPack** は、Python 開発者のために設計されたクロスプラットフォームのグラフィカルパッケージングツールです。**PyInstaller**（インタープリタおよびバイトコード同梱）と **Nuitka**（C/C++ ネイティブコンパイル）の 2 大コアエンジンを高度に統合し、複雑な低レイヤコンパイル引数、暗黙の依存関係解析、環境分離、リソース収集プロセスを直感的な GUI に集約しました。

シンプルな自動化スクリプトの配布から、大規模な依存関係（PySide6 / PyQt、Playwright、CustomTkinter、FastAPI など）を持つデスクトップやサーバーサイドアプリまで、QPyPack は安定した高い成功率と再現性のあるビルド体験を提供します。

---

## 📸 スクリーンショット (Screenshots)

<p align="center">
  <img width="32%" alt="メイン画面（英語）" src="https://github.com/user-attachments/assets/9d16c68e-d283-4020-86c1-9d4791756c29" />
  <img width="32%" alt="メイン画面（中国語）" src="https://github.com/user-attachments/assets/0147460d-1e9e-4612-9b52-9d347d81b7c5" />
  <img width="32%" alt="エンジンと環境設定" src="https://github.com/user-attachments/assets/0ad4db6d-b008-4018-bd69-40a369a10b7d" />
  <br />
  <img width="32%" alt="依存関係管理とスキャン" src="https://github.com/user-attachments/assets/c7fd1218-d079-4898-a97c-aa980c4d1375" />
  <img width="32%" alt="最適化・署名・セキュリティ" src="https://github.com/user-attachments/assets/e5b7500e-2a0d-4c6d-b20b-7d8d2d3bac8d" />
  <img width="32%" alt="バージョン情報と診断" src="https://github.com/user-attachments/assets/e652b222-49f5-44cd-ad3f-d93369ede26b" />
</p>

---

## 🛠️ コアアーキテクチャと機能 (Key Features)

### 1. デュアルビルドエンジンとバイナリ最適化
* **シームレスなデュアルエンジン切替**：
  * **PyInstaller**：高速なビルド速度、外部 C コンパイラ不要、優れた互換性とエコシステムサポート。
  * **Nuitka**：Python ソースコードを直接ネイティブ C/C++ バイナリにトランスパイルし、実行パフォーマンス向上、高い難読化/耐リバースエンジニアリング性能、コンパクトなファイルサイズを実現。
* **LTO リンク時最適化とサブモジュール削除**：軽量モード（Lite Mode）で `--lto=yes` リンク時最適化をサポート。PySide/PyQt において参照されていない重いサブモジュール（WebEngine、3D、Quick など）を自動検出して除外し、バイナリ肥大化を防止。
* **柔軟な出力形式**：**単一ファイル形式 (`--onefile`)** と **ディレクトリ形式 (`--onedir`)** をサポートし、内部依存関係ディレクトリの指定 (`--contents-directory`) にも対応。

### 2. 静的解析と依存関係トポロジー保護
* **ネイティブ AST 再帰スキャン**：純粋な Python 実装の抽象構文木（AST）静的解析エンジンを内蔵。コードを実行せずにソースコードとプロジェクトディレクトリ内のインポート関係を再帰的に解析。
* **インテリジェントなパッケージ名マッピング**：一般的なサードパーティ製ライブラリのインポート名と PyPI パッケージ名のマッピングテーブルを内蔵（例: `cv2` $\to$ `opencv-python`、`PIL` $\to$ `pillow`、`win32com` $\to$ `pywin32`）。ユーザーによるカスタム拡張も可能。
* **古い互換パッケージの動的隔離 (Backport Isolation)**：ターゲット Python バージョンの標準ライブラリと競合する古い Backport パッケージを自動検知して除外（例: Python 3.10+ における `pathlib` や `typing` の自動隔離）。

### 3. 環境の自動管理と自己修復フォールバック
* **C/C++ コンパイラの自動プロビジョニング**：ローカルの MSVC、Clang (LLVM)、GCC 環境を自動検出。コンパイラが存在しない場合、Nuitka エンジンが互換性のある MinGW-w64 ツールチェーンを自動ダウンロードおよび管理。
* **仮想環境ライフサイクル管理**：完全隔離の仮想環境サンドボックスおよび共有仮想環境モードをサポート。過去の無効な仮想環境の一括スキャンとクリーンアップユーティリティを搭載。
* **適応型リソース管理とエラー自動復旧**：
  * ビルド前にディスク容量と物理メモリを評価し、メモリ不足時には並行スレッド数（Adaptive Concurrency）を自動調整。
  * メモリ割り当てオーバーフロー（OOM / ZstdError）を検知し、シングルスレッド低メモリモードで自動再試行。
  * Windows アンチウイルスソフトウェアによる中間アイコンや一時ファイルの排他ロックを自動回避。

### 4. コード署名とデリバリー保証
* **スマートデジタル署名管理**：Windows ビルド生成後に Authenticode デジタル署名を自動適用（Signtool および PowerShell エンジンに対応、RFC 3161 タイムスタンプサービス統合）。macOS のワンクリック `codesign` ランタイム署名に対応。
* **自己署名証明書スイート**：Windows 自己署名コード署名証明書（`.pfx`）生成ツールを内蔵し、商用秘密鍵証明書とパスワード設定をサポート。
* **プロジェクト設定プリセットのインポート/エクスポート**：すべてのビルド引数、リソース一覧、マッピングルールを共有可能な `.qpypack` プリセットファイルとしてエクスポート可能。

### 5. クロスプラットフォーム UX
* **ドラッグ＆ドロップ対応**：Python スクリプトをドロップするだけで、モジュールのメタデータ（バージョン、作者、アプリ名）の解析、エントリーポイントの推論、アプリアイコンのマッピングを自動完了。
* **ベクターレンダリングと多言語 i18n**：Google Material SVG ベクターアイコンを採用し、4K/高 DPI ディスプレイのスケーリングに完全対応。日本語、英語、簡体字/繁体字中国語、韓国語、ドイツ語、フランス語など 17 言語の即時切り替えをサポート。

---

## 📊 エンジン選定の比較 (PyInstaller vs. Nuitka)

| 比較項目 | PyInstaller | Nuitka |
| :--- | :--- | :--- |
| **パッケージング原理** | Python インタープリタとバイトコード (`.pyc`) を同梱 | Python コードをネイティブ C/C++ バイナリにコンパイル |
| **ビルド時間** | 非常に高速（通常 10 〜 60 秒） | 比較的低速（C++ コード生成とコンパイラ最適化を伴う） |
| **C/C++ コンパイラ依存** | 不要 | 必要（MSVC / GCC / Clang / MinGW-w64 自動ダウンロード対応） |
| **コード保護レベル** | 基本（デコンパイラでソース復元可能） | 極めて高い（機械語バイナリ化、強固な耐解析性） |
| **実行パフォーマンス** | 標準的な Python 実行速度 | 起動が高速、ループや計算負荷の高い処理で優位 |
| **推奨ユースケース** | 迅速なプロトタイプ検証、社内ツール、動的インポートが多いプロジェクト | 商用配布ソフトウェア、コアアルゴリズム保護、サイズ・起動速度重視 |

---

## ⚡ クイックスタート (Quick Start)

> 💡 **初めてのご利用ですか？** 詳細な手順と推奨設定については、[**📖 クイックスタートガイド (QUICKSTART.md)**](../../QUICKSTART.md) をご参照ください。

### 方法 1：pip / pipx によるインストール（推奨）

Python >= 3.8 の環境で以下を実行します：

```bash
# pip によるインストール
pip install qpypack

# GUI アプリケーションの起動
qpypack
```

*モダンなパッケージマネージャーを使用する場合（推奨）：*
```bash
# pipx による隔離実行
pipx run qpypack

# uv による高速起動
uvx qpypack
```

### 方法 2：スタンドアロンビルド済みバイナリ版

Python 環境の事前構築を行わず、GitHub Releases ページから OS に適した実行ファイルを直接ダウンロードして利用できます：

👉 [**ビルド済みバイナリのダウンロード (GitHub Releases)**](https://github.com/Qwejay/QPyPack/releases)

---

## 📋 ベストプラクティス：リソース解決パス (`sys._MEIPASS`)

単一ファイルモード（`--onefile`）では、同梱された静的アセット（画像、設定ファイル、モデルデータなど）は実行時にサンドボックス一時ディレクトリへ展開されます。ソースコード内では以下の標準パターンを用いて安全にパスを解決してください：

```python
import sys
import os
from pathlib import Path

def get_asset_path(relative_path: str) -> Path:
    """パッケージング後のリソース絶対パスを取得"""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller 単一ファイルの展開ディレクトリ
        base_path = Path(sys._MEIPASS)
    elif "__compiled__" in globals():
        # Nuitka ネイティブバイナリの実行ディレクトリ
        base_path = Path(sys.argv[0]).resolve().parent
    else:
        # ローカル開発・デバッグ環境ディレクトリ
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path
```

---

## 📅 更新履歴 (Changelog)

詳細なバージョン履歴、新機能、バグ修正内容については [CHANGELOG.md](../../CHANGELOG.md) をご覧ください。

---

## 💖 貢献とスポンサーシップ (Contributing & Sponsorship)

QPyPack はオープンソースの理念に基づいて開発・メンテナンスされています。日々の開発や業務でお役に立ちましたら、継続的な改善のためご支援をいただけますと幸いです：

- 🌟 **Star を付ける**：[GitHub](https://github.com/Qwejay/QPyPack) リポジトリにスターをお願いします。
- 🐛 **フィードバックと提案**：[Issue](https://github.com/Qwejay/QPyPack/issues) からバグ報告や改善要望をお寄せください。
- ⚡ **スポンサー**：[Afdian (爱发电)](https://www.ifdian.net/a/qwejay) より無償の寄付を受け付けています（WeChat Pay / Alipay 対応）。

> *注：スポンサーシップはオープンソースコミュニティへの自発的な支援であり、商用サポートや特定機能開発の義務を伴うものではありません。*

---

## 📄 ライセンス (License)

本プロジェクトは [GNU General Public License v3.0 (GPL-3.0)](../../LICENSE) に基づいてオープンソースとして公開されています。

> [!IMPORTANT]
> **ビルド成果物の著作権について**：
> QPyPack を使用して生成された最終バイナリおよびアプリケーションの**知的財産権とライセンス形態は、完全にユーザー自身に帰属します**。QPyPack の GPL-3.0 ライセンスがビルド成果物に対して伝播することはありません。

<p align="right">Copyright (C) 2026 QwejayHuang.</p>
