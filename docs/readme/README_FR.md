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
  <strong>Un outil GUI multiplateforme pour empaqueter des applications Python basé sur PyInstaller & Nuitka</strong>
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

QPyPack est un outil graphique conçu pour simplifier le processus d'empaquetage des applications Python. Il intègre de manière transparente deux moteurs de compilation majeurs—PyInstaller et Nuitka—convertissant les arguments complexes en ligne de commande en une interface visuelle intuitive.

---

## 📷 Captures d'écran (Screenshots)

<p align="center">
<img width="1143" height="1067" alt="image" src="https://github.com/user-attachments/assets/8658aaef-5867-470d-ba4d-07892309ab1a" />
<img width="1142" height="1067" alt="image" src="https://github.com/user-attachments/assets/b64d9b89-8bfd-4bf8-8fec-9c75f61305dd" />
</p>

---

## 🚀 Fonctionnalités principales

* 📥 **Glisser-déposer intuitif** : Glissez simplement vos fichiers `.py` ou `.pyw` dans l'application.
* 🎨 **Détection d'icône automatique** : Conversion et aperçu automatique des icônes présentes dans le dossier source.
* 🛡️ **Bac à sable d'environnement virtuel** : Crée un environnement virtuel isolé pour réduire la taille de l'exécutable final.
* 🔍 **Analyse des dépendances** : Détection de `requirements.txt` et analyse statique du code (AST) pour inclure les dépendances implicites.
* ⚙️ **Commutation de moteur double** : Basculez facilement entre PyInstaller et Nuitka.
* 📝 **Injection de métadonnées** : Configurez la version, l'auteur et la description directement depuis l'interface (Windows PE & macOS Info.plist).

---

## ⚡ Démarrage rapide

```bash
# Installer via pip
pip install qpypack

# Lancer l'application
qpypack
```

Ou téléchargez les exécutables autonomes directement sur la page des [GitHub Releases](https://github.com/Qwejay/QPyPack/releases).

---

## 📅 Notes de version (Changelog)

Pour consulter l'historique complet des mises à jour, veuillez vous référer à [CHANGELOG.md](CHANGELOG.md) ou à la page des [GitHub Releases](https://github.com/Qwejay/QPyPack/releases).

---

## 📄 Licence

Distribué sous la licence [GNU General Public License v3.0](LICENSE).

Copyright (C) 2026 QwejayHuang.