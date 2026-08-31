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
  <strong>현대적이고 즉시 사용 가능한 크로스 플랫폼 Python 애플리케이션 패키징 GUI 도구</strong><br>
  <sub>PyInstaller 및 Nuitka 듀얼 엔진을 탑재하여 시각적 구성, 정적 의존성 분석 및 자동화된 빌드 워크플로 제공</sub>
</p>

## 📌 프로젝트 개요 (Overview)

**QPyPack**은 Python 개발자를 위해 설계된 크로스 플랫폼 그래픽 패키징 도구입니다. **PyInstaller**(인터프리터 및 바이트코드 번들링)와 **Nuitka**(C/C++ 네이티브 컴파일) 듀얼 코어 엔진을 깊이 통합하여 복잡한 컴파일 파라미터, 암시적 의존성 분석, 가상 환경 격리, 리소스 수집 프로세스를 직관적인 GUI 인터페이스로 단순화했습니다.

경량 자동화 스크립트 배포부터 대규모 의존성(PySide6 / PyQt, Playwright, CustomTkinter, FastAPI 등)을 포함하는 데스크톱 및 서버 애플리케이션까지, QPyPack은 높은 성공률과 재현 가능한 빌드 경험을 제공합니다.

---

## 📸 스크린샷 (Screenshots)

<p align="center">
  <img width="32%" alt="메인 화면 (영어)" src="https://github.com/user-attachments/assets/9d16c68e-d283-4020-86c1-9d4791756c29" />
  <img width="32%" alt="메인 화면 (중국어)" src="https://github.com/user-attachments/assets/0147460d-1e9e-4612-9b52-9d347d81b7c5" />
  <img width="32%" alt="빌드 엔진 및 환경" src="https://github.com/user-attachments/assets/0ad4db6d-b008-4018-bd69-40a369a10b7d" />
  <br />
  <img width="32%" alt="의존성 관리 및 스캔" src="https://github.com/user-attachments/assets/c7fd1218-d079-4898-a97c-aa980c4d1375" />
  <img width="32%" alt="최적화, 서명 및 보안" src="https://github.com/user-attachments/assets/e5b7500e-2a0d-4c6d-b20b-7d8d2d3bac8d" />
  <img width="32%" alt="정보 및 진단" src="https://github.com/user-attachments/assets/e652b222-49f5-44cd-ad3f-d93369ede26b" />
</p>

---

## 🛠️ 핵심 아키텍처 및 주요 기능 (Key Features)

### 1. 듀얼 빌드 엔진 및 바이너리 최적화
* **원활한 듀얼 엔진 전환**:
  * **PyInstaller**: 빠른 빌드 속도, 외부 C 컴파일러 불필요, 광범위한 생태계 호환성 지원.
  * **Nuitka**: Python 코드를 C/C++ 바이너리로 직접 변환하여 실행 속도 향상, 강력한 역공학 방지, 컴팩트한 용량 제공.
* **LTO 링크 최적화 및 모듈 가지치기**: 경량 모드(Lite Mode)에서 `--lto=yes` 링크 타임 최적화 지원. PySide/PyQt 사용 시 참조되지 않은 무거운 하위 모듈(WebEngine, 3D, Quick 등)을 자동 식별 및 제거하여 바이너리 용량 낭비 방지.
* **유연한 배포 형태**: **단일 파일 모드 (`--onefile`)** 및 **디렉터리 모드 (`--onedir`)** 지원, 내부 리소스 저장 디렉터리 경로 지정 (`--contents-directory`) 지원.

### 2. 정적 분석 및 의존성 토폴로지 보호
* **순수 AST 재귀 스캔**: 순수 Python 기반의 추상 구문 트리(AST) 정적 분석기를 내장하여 코드를 실행하지 않고도 소스 코드와 프로젝트 폴더의 명시적/암시적 임포트를 재귀적으로 분석.
* **스마트 패키지 이름 매핑 시스템**: 일반적인 서드파티 라이브러리 임포트 이름과 PyPI 패키지 이름 매핑 테이블 내장(예: `cv2` $\to$ `opencv-python`, `PIL` $\to$ `pillow`, `win32com` $\to$ `pywin32`), 사용자 정의 확장 지원.
* **레거시 호환 패키지 동적 격리 (Backport Isolation)**: 대상 Python 버전의 표준 라이브러리와 충돌하는 구형 Backport 패키지(예: Python 3.10+ 환경의 `pathlib`, `typing` 등)를 자동 감지 및 차단.

### 3. 환경 자동화 관리 및 자체 복구 메커니즘
* **C/C++ 컴파일러 자동 프로비저닝**: 로컬 MSVC, Clang (LLVM), GCC 환경 자동 감지. 네이티브 컴파일러가 없을 경우 Nuitka 엔진이 호환 가능한 MinGW-w64 툴체인을 자동 다운로드 및 관리.
* **가상 환경 라이프사이클 관리**: 독립 격리 가상 환경 및 공유 가상 환경 모드 지원. 이전 프로젝트의 비활성 가상 환경 원클릭 스캔 및 정리 유틸리티 제공.
* **리소스 인식형 동시성 및 오류 자가 치유**:
  * 빌드 전 디스크 용량과 물리 메모리를 평가하여 저메모리 상태에서 CPU 동시 작업 스레드 수(Adaptive Concurrency) 자동 조절.
  * 메모리 할당 오버플로(OOM / ZstdError)를 감지하고 단일 스레드 저메모리 모드로 자동 재시도.
  * Windows 백신 프로그램의 중간 아이콘/임시 파일 잠금 충돌 자동 우회.

### 4. 코드 서명 및 릴리스 보증
* **스마트 디지털 서명 관리**: Windows 바이너리 빌드 완료 후 Authenticode 디지털 서명 자동 적용(Signtool 및 PowerShell 엔진 지원, RFC 3161 타임스탬프 서비스 통합). macOS의 원클릭 `codesign` 런타임 서명 지원.
* **자체 서명 인증서 도구**: Windows 자체 서명 코드 서명 인증서(`.pfx`) 생성 도구 내장 및 상용 개인 키 인증서/비밀번호 구성 지원.
* **프로젝트 설정 프리셋 가져오기/내보내기**: 모든 빌드 매개변수, 리소스 매핑 및 제외 규칙을 공유 가능한 `.qpypack` 프리셋 파일로 내보내어 팀 협업 및 CI/CD 워크플로 지원.

### 5. 크로스 플랫폼 사용자 경험
* **드래그 앤 드롭 지원**: Python 스크립트를 드롭하면 모듈 메타데이터(버전, 작성자, 앱 이름) 파싱, 진입점 유추, 소스 디렉터리의 앱 아이콘 매핑 자동 수행.
* **벡터 렌더링 및 글로벌 i18n**: Google Material SVG 벡터 아이콘을 적용하여 4K/고해상도 DPI 스케일링 완벽 지원. 한국어, 영어, 중국어(간체/번체), 일본어, 독일어, 프랑스어 등 17개 언어 실시간 다국어 지원.

---

## 📊 엔진 비교 (PyInstaller vs. Nuitka)

| 평가 지표 | PyInstaller | Nuitka |
| :--- | :--- | :--- |
| **패키징 방식** | Python 인터프리터 + 바이트코드 (`.pyc`) 번들링 | Python 코드를 네이티브 C/C++ 바이너리로 컴파일 |
| **빌드 속도** | 매우 빠름 (보통 10 ~ 60초) | 상대적으로 느림 (C++ 코드 생성 및 최적화 수반) |
| **C/C++ 컴파일러** | 불필요 | 필요 (MSVC / GCC / Clang / MinGW-w64 자동 관리) |
| **코드 보호 수준** | 기본 (디컴파일러를 통한 소스 복원 가능) | 매우 높음 (기계어 바이너리, 강력한 역공학 방지) |
| **실행 성능** | 표준 Python 실행 속도 | 빠른 시작 속도, 루프 및 연산 집약적 작업 최적화 |
| **권장 사용 시나리오** | 빠른 프로토타입 검증, 내부 도구, 동적 임포트 프로젝트 | 상용 배포 소프트웨어, 핵심 알고리즘 보호, 용량/속도 최적화 |

---

## ⚡ 빠른 시작 (Quick Start)

> 💡 **QPyPack을 처음 사용하시나요?** 자세한 사용 가이드와 모범 사례는 [**📖 빠른 시작 가이드 (QUICKSTART.md)**](../../QUICKSTART.md)를 참조하세요.

### 방법 1: pip / pipx를 통한 설치 (권장)

Python >= 3.8 환경에서 실행:

```bash
# pip를 통한 설치
pip install qpypack

# GUI 애플리케이션 실행
qpypack
```

*최신 패키지 관리자 사용 시 (권장):*
```bash
# pipx를 통한 격리 실행
pipx run qpypack

# uv를 통한 초고속 실행
uvx qpypack
```

### 방법 2: 독립형 빌드 바이너리 버전

사전에 Python 환경을 구축할 필요 없이 GitHub Releases 페이지에서 해당 운영체제에 맞는 실행 파일을 직접 다운로드할 수 있습니다:

👉 [**사전 빌드 바이너리 다운로드 (GitHub Releases)**](https://github.com/Qwejay/QPyPack/releases)

---

## 📋 권장 설정: 리소스 해제 경로 (`sys._MEIPASS`)

단일 파일 모드(`--onefile`)에서는 포함된 정적 리소스(이미지, 설정 파일, 모델 등)가 실행 시 임시 샌드박스 디렉터리에 압축 해제됩니다. 소스 코드 내에서 다음과 같은 표준 방식으로 경로를 참조하십시오:

```python
import sys
import os
from pathlib import Path

def get_asset_path(relative_path: str) -> Path:
    """패키징 후 리소스의 절대 경로를 안전하게 반환"""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller 단일 파일 압축 해제 임시 디렉터리
        base_path = Path(sys._MEIPASS)
    elif "__compiled__" in globals():
        # Nuitka 네이티브 바이너리 실행 디렉터리
        base_path = Path(sys.argv[0]).resolve().parent
    else:
        # 로컬 개발 및 디버깅 디렉터리
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path
```

---

## 📅 변경 이력 (Changelog)

자세한 릴리스 정보, 신규 기능 및 버그 수정 내역은 [CHANGELOG.md](../../CHANGELOG.md)를 참조하세요.

---

## 💖 기여 및 후원 (Sponsorship & Contributing)

QPyPack은 오픈 소스 철학에 따라 유지 관리되는 프로젝트입니다. 본 프로젝트가 개발 효율 향상에 도움이 되었다면 지속적인 유지 관리를 위해 후원해 주실 수 있습니다:

- 🌟 **Star 지원**: [GitHub](https://github.com/Qwejay/QPyPack)에서 Star를 눌러주세요.
- 🐛 **피드백 및 제안**: [GitHub Issues](https://github.com/Qwejay/QPyPack/issues)를 통해 버그를 보고하거나 개선 사항을 제안해 주세요.
- ⚡ **프로젝트 후원**: [Afdian (爱发电)](https://www.ifdian.net/a/qwejay) 플랫폼을 통해 자발적 후원이 가능합니다 (WeChat Pay / Alipay 지원).

> *참고: 후원은 오픈 소스 프로젝트에 대한 자발적인 응원이며 상업적 서비스 약정을 포함하지 않습니다. 오픈 소스 생태계를 지원해 주시는 모든 분께 감사드립니다!*

---

## 📄 라이선스 (License)

본 프로젝트는 [GNU General Public License v3.0 (GPL-3.0)](../../LICENSE)에 따라 오픈 소스로 배포됩니다.

> [!IMPORTANT]
> **빌드 결과물의 저작권 안내**:
> QPyPack을 통해 빌드된 최종 애플리케이션 및 바이너리의 **지식재산권과 라이선스 형태는 전적으로 사용자에게 귀속됩니다**. QPyPack의 GPL-3.0 라이선스는 사용자가 패키징한 결과물에 전염되지 않습니다.

<p align="right">Copyright (C) 2026 QwejayHuang.</p>
