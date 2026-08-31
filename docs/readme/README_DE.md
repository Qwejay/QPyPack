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
  <strong>Modernes, einsatzbereites plattformübergreifendes GUI-Tool zur Paketierung von Python-Anwendungen</strong><br>
  <sub>Angetrieben von PyInstaller und Nuitka, mit visueller Konfiguration, statischer Abhängigkeitsanalyse und automatisiertem Build-Workflow.</sub>
</p>

## 📌 Projektübersicht (Overview)

**QPyPack** ist ein plattformübergreifendes grafisches Paketierungstool für Python-Entwickler. Durch die nahtlose Integration der beiden Haupt-Engines **PyInstaller** (Bytecode-Bündelung) und **Nuitka** (native C/C++-Kompilierung) werden komplexe Compiler-Toolchains, implizite Abhängigkeitsanalysen, Sandbox-Isolation und Ressourcenextraktion in einer intuitiven Benutzeroberfläche abstrahiert.

Egal ob Sie einfache Automatisierungsskripte oder komplexe Desktop- und Serveranwendungen (mit PySide6/PyQt, Playwright, CustomTkinter, FastAPI etc.) verteilen möchten: QPyPack bietet einen stabilen, hochgradig reproduzierbaren Build-Prozess unter Windows, macOS und Linux.

---

## 📸 Screenshots

<p align="center">
  <img width="32%" alt="Hauptfenster (Englisch)" src="https://github.com/user-attachments/assets/9d16c68e-d283-4020-86c1-9d4791756c29" />
  <img width="32%" alt="Hauptfenster (Chinesisch)" src="https://github.com/user-attachments/assets/0147460d-1e9e-4612-9b52-9d347d81b7c5" />
  <img width="32%" alt="Engine & Umgebung" src="https://github.com/user-attachments/assets/0ad4db6d-b008-4018-bd69-40a369a10b7d" />
  <br />
  <img width="32%" alt="Abhängigkeitsverwaltung" src="https://github.com/user-attachments/assets/c7fd1218-d079-4898-a97c-aa980c4d1375" />
  <img width="32%" alt="Optimierung & Signierung" src="https://github.com/user-attachments/assets/e5b7500e-2a0d-4c6d-b20b-7d8d2d3bac8d" />
  <img width="32%" alt="Über & Diagnose" src="https://github.com/user-attachments/assets/e652b222-49f5-44cd-ad3f-d93369ede26b" />
</p>

---

## 🛠️ Hauptfunktionen & Architektur

### 1. Dual-Engine-Kompilierung & Binäroptimierung
* **Nahtloser Wechsel zwischen zwei Engines**:
  * **PyInstaller**: Schnelle Build-Zeiten, keine C-Compiler-Abhängigkeit, hervorragende Kompatibilität.
  * **Nuitka**: Übersetzt Python-Code direkt in native C/C++-Binärdateien für hohe Ausführungsgeschwindigkeit, starken Schutz gegen Reverse-Engineering und kompakte Ausgabegröße.
* **LTO-Linkzeitoptimierung & Modulbereinigung**: Unterstützt `--lto=yes` im Lite-Modus; ungenutzte schwere Qt-Submodule (z. B. `WebEngine`, `3D`, `Quick`) werden automatisch erkannt und entfernt, um Dateigrößen-Overhead zu vermeiden.
* **Flexible Ausgabeformate**: Unterstützt **Einzeldatei- (`--onefile`)** und **Verzeichnis-Modus (`--onedir`)** sowie benutzerdefinierte interne Ressourcenpfade (`--contents-directory`).

### 2. Statische Codeanalyse & Topologieschutz
* **Natives rekursives AST-Scanning**: Analysiert abstrakte Syntaxbäume (AST) direkt in Python, um explizite und implizite Importe (Hidden Imports) ohne Programmausführung zu erfassen.
* **Intelligentes Paket-Mapping**: Enthält Zuordnungstabellen für gängige Import- und PyPI-Paketnamen (z. B. `cv2` $\to$ `opencv-python`, `PIL` $\to$ `pillow`, `win32com` $\to$ `pywin32`), modular erweiterbar.
* **Automatische Backport-Isolation**: Erkennt und blockiert veraltete Backport-Bibliotheken, die mit modernen Standardbibliotheken kollidieren (z. B. `pathlib` oder `typing` unter Python 3.10+).

### 3. Automatisiertes Umgebungsmanagement & Selbstheilung
* **Automatische C/C++-Compiler-Verwaltung**: Erkennt lokale MSVC-, Clang- (LLVM) und GCC-Installationen. Falls kein nativer Compiler vorhanden ist, lädt Nuitka automatisch eine MinGW-w64-Toolchain herunter.
* **Lebenszyklus virtueller Umgebungen**: Unterstützt isolierte Sandkästen sowie wiederverwendbare geteilte virtuelle Umgebungen mit Bereinigungsfunktion.
* **Ressourcenüberwachung & Fehlerselbstheilung**:
  * Bewertet vor dem Build RAM und Festplattenspeicher und passt die Thread-Parallelität (Adaptive Concurrency) an.
  * Fängt Speicherengpässe (`ZstdError` / OOM) ab und wiederholt den Build im Single-Thread-Modus.
  * Umgeht Dateisperren durch Antivirenprogramme oder Cloud-Synchronisationsdienste.

### 4. Codesignatur & Projekt-Voreinstellungen
* **Intelligente digitale Signatur**: Signiert Windows-Binärdateien automatisch via Authenticode (unterstützt Signtool und PowerShell mit RFC 3161 Zeitstempeln) sowie macOS `codesign`.
* **Zertifikat-Suite**: Integrierter Generator für selbstsignierte `.pfx`-Zertifikate und Unterstützung für kommerzielle Zertifikate.
* **Projekt-Presets (Import/Export)**: Speichert alle Build-Parameter, Ressourcenlisten und Mappings in portable `.qpypack`-Dateien.

### 5. Benutzererlebnis & Lokalisierung
* **Intuitive Drag & Drop-Bedienung**: Automatisches Auslesen von Modul-Metadaten (`__version__`, `__author__`, App-Titel) und Zuweisung von Programmsymbolen.
* **Google Material Vektor-UI**: Skaliert verlustfrei auf High-DPI/4K-Monitoren. Enthält Übersetzungen für 17 Sprachen (Deutsch, Englisch, Chinesisch, Japanisch, Koreanisch, Französisch, Spanisch etc.).

---

## 📊 Engine-Vergleich (PyInstaller vs. Nuitka)

| Kriterium | PyInstaller | Nuitka |
| :--- | :--- | :--- |
| **Funktionsweise** | Bündelt Python-Interpreter + Bytecode (`.pyc`) | Kompiliert Python-Code zu nativen C/C++-Binärdateien |
| **Build-Geschwindigkeit** | Sehr schnell (typisch 10 – 60 s) | Moderat bis langsam (erfordert C++-Kompilierung) |
| **Compiler-Bedarf** | Keiner | Erforderlich (MSVC / GCC / Clang / MinGW-w64) |
| **Code-Schutz** | Basis (über Dekompilierer einsehbar) | Extrem hoch (Maschinencode, hoher Reverse-Engineering-Schutz) |
| **Ausführungsleistung** | Standard Python-Geschwindigkeit | Sehr schneller Start, optimierte Schleifen/Berechnungen |
| **Empfohlen für** | Schnelles Prototyping, interne Tools, dynamische Skripte | Kommerzielle Distribution, Schutz geistigen Eigentums, kompakte Größe |

---

## ⚡ Schnellstart (Quick Start)

> 💡 **Erste Schritte?** Konsultieren Sie unsere [**📖 Kurzanleitung (QUICKSTART.md)**](../../QUICKSTART.md) für Schritt-für-Schritt-Anweisungen und empfohlene Konfigurationen.

### Methode 1: Installation über pip / pipx (Empfohlen)

Voraussetzung: Python >= 3.8

```bash
# Installation via pip
pip install qpypack

# Anwendung starten
qpypack
```

*Mit modernen Paketmanagern:*
```bash
# Isoliert über pipx
pipx run qpypack

# Ultraschnell über uv
uvx qpypack
```

### Methode 2: Vorkompilierte Binärdateien

Ohne lokale Python-Installation können Sie direkt kompilierte Binärdateien für Windows, macOS oder Linux herunterladen:

👉 [**Vorkompilierte Versionen herunterladen (GitHub Releases)**](https://github.com/Qwejay/QPyPack/releases)

---

## 📋 Pfadauflösung für Ressourcen (`sys._MEIPASS`)

Im Einzeldatei-Modus (`--onefile`) werden statische Dateien (Bilder, Konfigurationen, Modelle) zur Laufzeit temporär entpackt. Verwenden Sie folgendes Standardmuster zur Pfadauflösung:

```python
import sys
import os
from pathlib import Path

def get_asset_path(relative_path: str) -> Path:
    """Ermittelt den absoluten Pfad zu gepackten Ressourcen."""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller temporäres Extraktionsverzeichnis
        base_path = Path(sys._MEIPASS)
    elif "__compiled__" in globals():
        # Nuitka natives Binärverzeichnis
        base_path = Path(sys.argv[0]).resolve().parent
    else:
        # Lokale Entwicklungsumgebung
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path
```

---

## 📅 Änderungsprotokoll (Changelog)

Ausführliche Versionshinweise und behobene Fehler finden Sie in [CHANGELOG.md](../../CHANGELOG.md).

---

## 💖 Mitwirken & Sponsoring

QPyPack ist ein Open-Source-Projekt. Wenn Ihnen das Tool bei Ihrer Arbeit geholfen hat, freuen wir uns über Ihre Unterstützung:

- 🌟 **Star vergeben**: Schenken Sie uns einen Stern auf [GitHub](https://github.com/Qwejay/QPyPack).
- 🐛 **Feedback & Fehlerberichte**: Erstellen Sie ein [Issue auf GitHub](https://github.com/Qwejay/QPyPack/issues).
- ⚡ **Sponsoring**: Unterstützen Sie das Projekt auf [Afdian (爱发电)](https://www.ifdian.net/a/qwejay) (WeChat / Alipay).

---

## 📄 Lizenz (License)

Lizenziert unter der [GNU General Public License v3.0 (GPL-3.0)](../../LICENSE).

> [!IMPORTANT]
> **Urheberrecht an kompilierten Binärdateien**:
> Die Rechte an Ihren mit QPyPack erstellten Anwendungen **verbleiben vollständig bei Ihnen**. Die GPL-3.0-Lizenz von QPyPack überträgt sich nicht auf Ihre kompilierten Programme.

<p align="right">Copyright (C) 2026 QwejayHuang.</p>
