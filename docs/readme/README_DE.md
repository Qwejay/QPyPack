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
  <strong>Ein plattformübergreifendes GUI-Tool zur Paketierung von Python-Anwendungen basierend auf PyInstaller & Nuitka</strong>
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

QPyPack ist ein visuelles GUI-Tool zur Vereinfachung des Build-Prozesses von Python-Anwendungen. Es integriert PyInstaller und Nuitka nahtlos und wandelt komplexe Befehlszeilenparameter in eine intuitive grafische Benutzeroberfläche um.

---

## 📷 Screenshots

<p align="center">
<img width="1143" height="1067" alt="image" src="https://github.com/user-attachments/assets/8658aaef-5867-470d-ba4d-07892309ab1a" />
<img width="1142" height="1067" alt="image" src="https://github.com/user-attachments/assets/b64d9b89-8bfd-4bf8-8fec-9c75f61305dd" />
</p>

---

## 🚀 Hauptfunktionen

* 📥 **Drag & Drop** : Ziehen Sie `.py`- oder `.pyw`-Skripte direkt in das Anwendungsfenster.
* 🎨 **Automatische Icon-Erkennung** : Erkennt automatisch Bilddateien im Quellordner und wandelt diese um.
* 🛡️ **Virtuelle Umgebung (Sandbox)** : Erstellt automatisch eine isolierte Umgebung zur Minimierung der Ausgabegröße.
* 🔍 **Abhängigkeitsanalyse** : Erkennt `requirements.txt` und führt statische AST-Code-Analysen für verdeckte Importe durch.
* ⚙️ **Dual-Engine-Unterstützung** : Wechseln Sie nahtlos zwischen PyInstaller und Nuitka.
* 📝 **App-Metadaten-Injektion** : Fügen Sie Versionsnummern und Beschreibungen direkt in die Binärdatei ein.

---

## ⚡ Schnellstart

```bash
# Über pip installieren
pip install qpypack

# Anwendung starten
qpypack
```

Alternativ können Sie vorkompilierte Dateien von der [GitHub Release-Seite](https://github.com/Qwejay/QPyPack/releases) herunterladen.

---

## 📅 Änderungsprotokoll (Changelog)

Die vollständige Versionshistorie finden Sie in [CHANGELOG.md](CHANGELOG.md) oder auf der [GitHub Releases-Seite](https://github.com/Qwejay/QPyPack/releases).

---

## 📄 Lizenz

Lizenziert unter der [GNU General Public License v3.0](LICENSE).

Copyright (C) 2026 QwejayHuang.