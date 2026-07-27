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
  <strong>PyInstaller と Nuitka をベースにしたクロスプラットフォーム Python パッケージング GUI ツール</strong>
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

QPyPack は、Python アプリケーションのパッケージング手順を簡素化するために設計された GUI ツールです。PyInstaller と Nuitka の 2 大コンパイルエンジンを高度に統合し、複雑な CLI コマンドライン引数を直感的な GUI 操作に変換します。

---

## 📷 スクリーンショット (Screenshots)

<p align="center">
<img width="1143" height="1067" alt="image" src="https://github.com/user-attachments/assets/8658aaef-5867-470d-ba4d-07892309ab1a" />
<img width="1142" height="1067" alt="image" src="https://github.com/user-attachments/assets/b64d9b89-8bfd-4bf8-8fec-9c75f61305dd" />
</p>

---

## 🚀 主な機能 (Key Features)

* 📥 **ドラッグ＆ドロップ対応**: `.py` / `.pyw` ソースファイルをウィンドウに直接ドラッグして読み込み。
* 🎨 **アイコン自動検出**: ソースディレクトリ内の画像資産 (`icon.ico` / `logo.svg` 等) を自動検出しフォーマット変換。
* 🛡️ **仮想環境サンドボックス**: 独立した仮想環境を自動生成し、最小限の依存関係でバイナリサイズを削減。
* 🔍 **依存関係の自動解析**: `requirements.txt` 解析および AST 静的解析による暗黙のインポート (Hidden Imports) 補完。
* ⚙️ **デュアルエンジン切替**: PyInstaller と Nuitka をワンクリックで切り替え。
* 📝 **メタデータ注入**: バージョン情報や作者情報を実行ファイルプロパティに自動書き込み。

---

## ⚡ クイックスタート (Quick Start)

```bash
# pip によるインストール
pip install qpypack

# アプリケーションの起動
qpypack
```

または [GitHub Releases ページ](https://github.com/Qwejay/QPyPack/releases) からビルド済みバイナリを直接ダウンロードできます。

---

## 📅 更新履歴 (Changelog)

詳細なリリースノートおよび更新履歴については、[CHANGELOG.md](CHANGELOG.md) または [GitHub Releases ページ](https://github.com/Qwejay/QPyPack/releases) を参照してください。

---

## 📄 ライセンス (License)

[GNU General Public License v3.0](LICENSE) のもとでオープンソース化されています。

Copyright (C) 2026 QwejayHuang.