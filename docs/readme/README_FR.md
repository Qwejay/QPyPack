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
  <strong>Outil GUI moderne et prêt à l'emploi pour empaqueter des applications Python multiplateformes</strong><br>
  <sub>Propulsé par PyInstaller et Nuitka, offrant configuration visuelle, analyse statique des dépendances et flux de compilation automatisé.</sub>
</p>

## 📌 Présentation du projet (Overview)

**QPyPack** est un outil graphique multiplateforme conçu pour les développeurs Python. En intégrant de manière transparente les deux moteurs majeurs **PyInstaller** (empaquetage de bytecode) et **Nuitka** (compilation C/C++ native), QPyPack abstrait les chaînes d'outils complexes, l'analyse des dépendances implicites, l'isolation d'environnements et la collecte de ressources dans une interface de bureau intuitive.

Qu'il s'agisse de distribuer de simples scripts d'automatisation ou des applications complexes (avec PySide6/PyQt, Playwright, CustomTkinter, FastAPI, etc.), QPyPack garantit une expérience de compilation fiable, reproductible et à haut taux de succès.

---

## 📸 Captures d'écran (Screenshots)

<p align="center">
  <img width="32%" alt="Interface principale (Anglais)" src="https://github.com/user-attachments/assets/9d16c68e-d283-4020-86c1-9d4791756c29" />
  <img width="32%" alt="Interface principale (Chinois)" src="https://github.com/user-attachments/assets/0147460d-1e9e-4612-9b52-9d347d81b7c5" />
  <img width="32%" alt="Moteur et Environnement" src="https://github.com/user-attachments/assets/0ad4db6d-b008-4018-bd69-40a369a10b7d" />
  <br />
  <img width="32%" alt="Gestion des dépendances" src="https://github.com/user-attachments/assets/c7fd1218-d079-4898-a97c-aa980c4d1375" />
  <img width="32%" alt="Optimisation et Signature" src="https://github.com/user-attachments/assets/e5b7500e-2a0d-4c6d-b20b-7d8d2d3bac8d" />
  <img width="32%" alt="À propos et Diagnostics" src="https://github.com/user-attachments/assets/e652b222-49f5-44cd-ad3f-d93369ede26b" />
</p>

---

## 🛠️ Architecture & Fonctionnalités clés

### 1. Double moteur de compilation & Optimisation binaire
* **Basculement transparent entre les moteurs** :
  * **PyInstaller** : Compilation rapide, sans dépendance de compilateur C, excellente compatibilité.
  * **Nuitka** : Traduit le code Python en binaires C/C++ natifs pour des performances accrues, une forte protection contre la rétro-ingénierie et une taille d'exécutable réduite.
* **Optimisation LTO & Élagage de sous-modules** : Support de l'optimisation à l'édition des liens (`--lto=yes`) en mode Lite. Détection et exclusion automatique des sous-modules Qt lourds non utilisés (WebEngine, 3D, Quick, etc.) pour éviter l'alourdissement du binaire.
* **Formats de distribution flexibles** : Prise en charge des modes **Fichier unique (`--onefile`)** et **Dossier (`--onedir`)**, avec personnalisation du dossier interne des ressources (`--contents-directory`).

### 2. Analyse statique & Protection des dépendances
* **Scan AST récursif natif** : Analyseur statique d'arbre syntaxique abstrait (AST) en pur Python, découvrant les dépendances explicites et implicites sans exécuter le code.
* **Système de mappage intelligent** : Table de correspondance intégrée entre noms d'import et paquets PyPI (ex. `cv2` $\to$ `opencv-python`, `PIL` $\to$ `pillow`, `win32com` $\to$ `pywin32`), entièrement personnalisable.
* **Isolation dynamique des bibliothèques obsolètes (Backport Isolation)** : Détecte et neutralise automatiquement les bibliothèques de rétrocompatibilité en conflit avec la bibliothèque standard moderne (ex. `pathlib` ou `typing` sous Python 3.10+).

### 3. Gestion automatisée des environnements & Auto-récupération
* **Provisionnement automatique des compilateurs C/C++** : Détecte automatiquement MSVC, Clang (LLVM) et GCC. En l'absence de compilateur local, Nuitka télécharge et gère automatiquement une chaîne d'outils MinGW-w64.
* **Gestion du cycle de vie des environnements virtuels** : Prise en charge des bacs à sable isolés et des environnements virtuels partagés, avec outil de nettoyage intégré.
* **Gestion adaptative des ressources & Résilience** :
  * Évalue la mémoire vive et l'espace disque avant la compilation pour ajuster automatiquement le nombre de cœurs CPU (Adaptive Concurrency).
  * Récupère automatiquement les erreurs de mémoire saturée (`ZstdError` / OOM) en relançant la compilation en mode basse mémoire mono-thread.
  * Contourne les verrouillages temporaires de fichiers causés par les antivirus ou les services de synchronisation cloud.

### 4. Signature de code & Préréglages de projet
* **Signature numérique intelligente** : Applique automatiquement les signatures numériques Authenticode aux binaires Windows (compatible Signtool et PowerShell avec horodatage RFC 3161) et signature runtime `codesign` sous macOS.
* **Suite de certificats** : Outil intégré de génération de certificats auto-signés (`.pfx`) et prise en charge des certificats commerciaux.
* **Exportation / Importation de préréglages** : Sauvegarde tous les paramètres de compilation, listes de ressources et règles dans des fichiers portables `.qpypack`.

### 5. Expérience utilisateur moderne & i18n
* **Glisser-déposer intuitif** : Déposer un script Python analyse automatiquement les métadonnées (`__version__`, `__author__`, nom de l'application), déduit le point d'entrée et associe l'icône correspondante.
* **Interface vectorielle avec support HiDPI** : Entièrement conçue avec les icônes vectorielles Google Material SVG pour un rendu net sur écrans 4K/Haute résolution. Traduite en 17 langues (français, anglais, chinois, japonais, coréen, allemand, espagnol, etc.).

---

## 📊 Comparatif des moteurs (PyInstaller vs. Nuitka)

| Critère | PyInstaller | Nuitka |
| :--- | :--- | :--- |
| **Principe** | Bündle l'interpréteur Python + bytecode (`.pyc`) | Compile le code Python en binaires C/C++ natifs |
| **Vitesse de compilation** | Très rapide (généralement 10 – 60 s) | Plus lente (génération de code C++ et optimisations) |
| **Compilateur C/C++** | Non requis | Requis (MSVC / GCC / Clang / MinGW-w64 géré) |
| **Protection du code** | Basique (décompilation possible) | Très élevée (code machine compilé, résistant à l'ingénierie inverse) |
| **Performances d'exécution** | Vitesse standard de Python | Démarrage plus rapide, boucles et calculs intensifs optimisés |
| **Recommandé pour** | Prototypage rapide, outils internes, projets à imports dynamiques | Logiciels commerciaux, protection d'algorithmes, optimisation de taille |

---

## ⚡ Démarrage rapide (Quick Start)

> 💡 **Première utilisation ?** Consultez notre [**📖 Guide de démarrage rapide (QUICKSTART.md)**](../../QUICKSTART.md) pour un pas-à-pas détaillé et les configurations recommandées.

### Méthode 1 : Installation via pip / pipx (Recommandée)

Nécessite Python >= 3.8 :

```bash
# Installer via pip
pip install qpypack

# Lancer l'application
qpypack
```

*Avec les gestionnaires de paquets modernes :*
```bash
# Exécuter de manière isolée avec pipx
pipx run qpypack

# Lancement ultra-rapide avec uv
uvx qpypack
```

### Méthode 2 : Version binaire autonome précompilée

Sans configuration préalable de Python, téléchargez directement les exécutables précompilés pour votre système :

👉 [**Télécharger la version précompilée (GitHub Releases)**](https://github.com/Qwejay/QPyPack/releases)

---

## 📋 Résolution des chemins de ressources (`sys._MEIPASS`)

En mode fichier unique (`--onefile`), les fichiers statiques (images, configurations, modèles) sont extraits à l'exécution dans un dossier temporaire isolé. Utilisez le modèle standard suivant pour résoudre les chemins :

```python
import sys
import os
from pathlib import Path

def get_asset_path(relative_path: str) -> Path:
    """Résout le chemin absolu des ressources empaquetées."""
    if hasattr(sys, "_MEIPASS"):
        # Répertoire d'extraction temporaire PyInstaller
        base_path = Path(sys._MEIPASS)
    elif "__compiled__" in globals():
        # Répertoire d'exécution binaire Nuitka
        base_path = Path(sys.argv[0]).resolve().parent
    else:
        # Environnement de développement local
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path
```

---

## 📅 Historique des versions (Changelog)

Pour consulter les notes de version détaillées et les corrections de bugs, référez-vous à [CHANGELOG.md](../../CHANGELOG.md).

---

## 💖 Contribution & Sponsoring

QPyPack est un projet open-source développé sur mon temps personnel. Si cet outil vous est utile, vous pouvez soutenir sa maintenance continue :

- 🌟 **Étoile GitHub** : Donnez une étoile au projet sur [GitHub](https://github.com/Qwejay/QPyPack).
- 🐛 **Retours & Suggestions** : Soumettez vos rapports de bugs sur [GitHub Issues](https://github.com/Qwejay/QPyPack/issues).
- ⚡ **Soutien financier** : Contribuez via [Afdian (爱发电)](https://www.ifdian.net/a/qwejay) (WeChat Pay / Alipay).

---

## 📄 Licence (License)

Ce projet est distribué sous licence [GNU General Public License v3.0 (GPL-3.0)](../../LICENSE).

> [!IMPORTANT]
> **Propriété des binaires générés** :
> Les droits de propriété intellectuelle et les licences des applications créées avec QPyPack **appartiennent intégralement à l'utilisateur**. La licence GPL-3.0 de QPyPack n'impose aucune contrainte sur vos binaires finaux.

<p align="right">Copyright (C) 2026 QwejayHuang.</p>
