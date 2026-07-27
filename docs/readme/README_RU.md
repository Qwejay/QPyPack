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
  <strong>Кроссплатформенный GUI-инструмент упаковки Python-приложений на базе PyInstaller и Nuitka</strong>
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

QPyPack — это визуальный инструмент, предназначенный для упрощения процесса сборки приложений Python. Он объединяет два основных компилятора — PyInstaller и Nuitka, преобразуя сложные консольные команды в интуитивный графический интерфейс.

---

## 📷 Скриншоты (Screenshots)

<p align="center">
<img width="1143" height="1067" alt="image" src="https://github.com/user-attachments/assets/8658aaef-5867-470d-ba4d-07892309ab1a" />
<img width="1142" height="1067" alt="image" src="https://github.com/user-attachments/assets/b64d9b89-8bfd-4bf8-8fec-9c75f61305dd" />
</p>

---

## 🚀 Основные возможности

* 📥 **Drag & Drop** : Перетаскивайте файлы `.py` или `.pyw` прямо в окно программы.
* 🎨 **Автоопределение иконки** : Автоматически находит иконки в папке исходников и конвертирует их.
* 🛡️ **Виртуальное окружение (Sandbox)** : Создает изолированное окружение для минимизации размера итогового файла.
* 🔍 **Анализ зависимостей** : Считывание `requirements.txt` и статический AST-анализ кода для скрытых импортов.
* ⚙️ **Два движка сборки** : Быстрое переключение между PyInstaller и Nuitka.
* 📝 **Внедрение метаданных** : Указывайте версию, автора и описание приложения прямо в интерфейсе.

---

## ⚡ Быстрый старт

```bash
# Установка через pip
pip install qpypack

# Запуск
qpypack
```

Или скачайте готовые исполняемые файлы на странице [GitHub Releases](https://github.com/Qwejay/QPyPack/releases).

---

## 📅 История изменений (Changelog)

Полную историю версий и примечания к релизу см. в [CHANGELOG.md](CHANGELOG.md) или на странице [GitHub Releases](https://github.com/Qwejay/QPyPack/releases).

---

## 📄 Лицензия

Распространяется под лицензией [GNU General Public License v3.0](LICENSE).

Copyright (C) 2026 QwejayHuang.