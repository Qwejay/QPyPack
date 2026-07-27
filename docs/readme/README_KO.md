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
  <strong>PyInstaller 및 Nuitka 기반의 크로스 플랫폼 Python 애플리케이션 패키징 GUI 도구</strong>
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

QPyPack은 Python 애플리케이션 패키징 프로세스를 단순화하도록 설계된 GUI 도구입니다. PyInstaller와 Nuitka를 깊이 통합하여 복잡한 CLI 명령을 직관적인 그래픽 인터페이스로 변환합니다.

---

## 📷 스크린샷 (Screenshots)

<p align="center">
<img width="1143" height="1067" alt="image" src="https://github.com/user-attachments/assets/8658aaef-5867-470d-ba4d-07892309ab1a" />
<img width="1142" height="1067" alt="image" src="https://github.com/user-attachments/assets/b64d9b89-8bfd-4bf8-8fec-9c75f61305dd" />
</p>

---

## 🚀 주요 기능 (Key Features)

* 📥 **드래그 앤 드롭 지원**: 소스 파일(.py / .pyw)을 창으로 끌어다 놓아 빠르게 로드.
* 🎨 **아이콘 자동 추출**: 디렉터리 내 아이콘 자산(`icon.ico`, `logo.svg` 등) 자동 탐지 및 포맷 변환.
* 🛡️ **가상 환경 샌드박스**: 독립된 가상 환경을 생성하여 최소 의존성만 설치, 실행 파일 용량 최적화.
* 🔍 **의존성 자동 분석**: `requirements.txt` 파싱 및 AST 정적 스캔을 통한 암시적 임포트(Hidden Imports) 추출.
* ⚙️ **듀얼 엔진 스위칭**: PyInstaller와 Nuitka 간의 손쉬운 전환.
* 📝 **메타데이터 주입**: 버전 정보, 작성자, 설명을 UI에서 직접 실행 파일 속성에 주입.

---

## ⚡ 빠른 시작 (Quick Start)

```bash
# pip를 통한 설치
pip install qpypack

# 실행
qpypack
```

또는 [GitHub Releases 페이지](https://github.com/Qwejay/QPyPack/releases)에서 사전 빌드된 실행 파일을 다운로드하세요.

---

## 📅 변경 사항 (Changelog)

자세한 릴리스 노트 및 업데이트 기록은 [CHANGELOG.md](CHANGELOG.md) 또는 [GitHub Releases 페이지](https://github.com/Qwejay/QPyPack/releases)를 참조하세요.

---

## 📄 라이선스 (License)

[GNU General Public License v3.0](LICENSE)에 따라 오픈 소스로 제공됩니다.

Copyright (C) 2026 QwejayHuang.