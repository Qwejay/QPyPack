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
  <strong>Современный кроссплатформенный GUI-инструмент для упаковки Python-приложений</strong><br>
  <sub>На базе PyInstaller и Nuitka, с визуальной конфигурацией, статическим анализом зависимостей и автоматизацией сборки.</sub>
</p>

## 📌 Обзор проекта (Overview)

**QPyPack** — это графический кроссплатформенный инструмент для упаковки Python-приложений. Благодаря глубокой интеграции двух компиляторов — **PyInstaller** (бандлинг байт-кода) и **Nuitka** (нативная компиляция в C/C++) — сложные параметры командной строки, отслеживание неявных зависимостей, изоляция сред и сбор ресурсов объединены в удобном интерфейсе.

От простых скриптов автоматизации до сложных приложений (с PySide6/PyQt, Playwright, CustomTkinter, FastAPI и др.) — QPyPack гарантирует стабильную сборку с высоким процентом успеха на Windows, macOS и Linux.

---

## 📸 Скриншоты (Screenshots)

<p align="center">
  <img width="32%" alt="Главное окно (Английский)" src="https://github.com/user-attachments/assets/9d16c68e-d283-4020-86c1-9d4791756c29" />
  <img width="32%" alt="Главное окно (Китайский)" src="https://github.com/user-attachments/assets/0147460d-1e9e-4612-9b52-9d347d81b7c5" />
  <img width="32%" alt="Движок и окружение" src="https://github.com/user-attachments/assets/0ad4db6d-b008-4018-bd69-40a369a10b7d" />
  <br />
  <img width="32%" alt="Управление зависимостями" src="https://github.com/user-attachments/assets/c7fd1218-d079-4898-a97c-aa980c4d1375" />
  <img width="32%" alt="Оптимизация и подпись" src="https://github.com/user-attachments/assets/e5b7500e-2a0d-4c6d-b20b-7d8d2d3bac8d" />
  <img width="32%" alt="О программе и диагностика" src="https://github.com/user-attachments/assets/e652b222-49f5-44cd-ad3f-d93369ede26b" />
</p>

---

## 🛠️ Архитектура и ключевые возможности

### 1. Двойной движок сборки и оптимизация бинарных файлов
* **Плавное переключение движков**:
  * **PyInstaller**: Высокая скорость сборки, отсутствие потребности в C-компиляторе, отличная совместимость.
  * **Nuitka**: Транслирует Python-код напрямую в C/C++ бинарники, обеспечивая высокую скорость выполнения, стойкость к декомпиляции и компактный размер.
* **LTO-оптимизация и обрезка модулей**: Поддержка оптимизации на этапе компоновки (`--lto=yes`) в режиме Lite. Автоматическое исключение неиспользуемых тяжелых субмодулей Qt (WebEngine, 3D, Quick и др.).
* **Гибкие форматы сборки**: Поддержка режимов **одного файла (`--onefile`)** и **директории (`--onedir`)**, а также настройка внутреннего каталога зависимостей (`--contents-directory`).

### 2. Статический анализ и защита зависимостей
* **Рекурсивный AST-анализ**: Встроенный анализатор абстрактного синтаксического дерева (AST) на чистом Python, определяющий явные и неявные импорты без запуска кода.
* **Интеллектуальное сопоставление пакетов**: Встроенная таблица соответствия имён импорта и пакетов PyPI (например, `cv2` $\to$ `opencv-python`, `PIL` $\to$ `pillow`, `win32com` $\to$ `pywin32`) с возможностью расширения.
* **Динамическая изоляция устаревших бэкпортов**: Автоматически блокирует устаревшие backport-модули, конфликтующие со стандартной библиотекой (например, изоляция `pathlib` или `typing` в Python 3.10+).

### 3. Автоматизация окружения и отказоустойчивость
* **Автоматическое управление компиляторами C/C++**: Определяет установленные MSVC, Clang (LLVM) и GCC. При отсутствии компилятора Nuitka автоматически загружает MinGW-w64.
* **Управление виртуальными окружениями**: Поддержка изолированных и общих виртуальных сред, а также встроенная утилита очистки старых сред.
* **Адаптивный контроль ресурсов и самовосстановление**:
  * Оценивает ОЗУ и диск перед сборкой, автоматически снижая параллелизм потоков при нехватке памяти.
  * Перехватывает ошибки нехватки памяти (`ZstdError` / OOM) и автоматически перезапускает сборку в однопоточном режиме.
  * Обходит временные блокировки файлов антивирусами и облачными дисками.

### 4. Подпись кода и пресеты проектов
* **Умная цифровая подпись**: Автоматически подписывает исполняемые файлы Windows через Authenticode (Signtool/PowerShell с меткой времени RFC 3161) и выполняет `codesign` в macOS.
* **Генератор сертификатов**: Встроенный инструмент создания самоподписанных сертификатов (`.pfx`) и поддержка коммерческих ключей.
* **Импорт/экспорт пресетов**: Сохраняет все параметры сборки и списки ресурсов в файлы `.qpypack`.

### 5. Кроссплатформенный интерфейс и локализация
* **Удобный Drag & Drop**: При перетаскивании скрипта автоматически извлекаются метаданные (`__version__`, `__author__`), определяется точка входа и подбирается иконка.
* **Векторная графика и поддержка HiDPI**: Построен на векторных иконках Google Material SVG, отлично масштабируется на экранах 4K. Переведён на 17 языков (русский, английский, китайский, японский, корейский, немецкий, французский, испанский и др.).

---

## 📊 Сравнение движков (PyInstaller vs. Nuitka)

| Критерий | PyInstaller | Nuitka |
| :--- | :--- | :--- |
| **Принцип работы** | Упаковывает интерпретатор Python + байт-код (`.pyc`) | Компилирует Python в нативные C/C++ бинарники |
| **Скорость сборки** | Очень высокая (10 – 60 сек) | Более медленная (генерация C++ и компиляция) |
| **Компилятор C/C++** | Не требуется | Требуется (MSVC / GCC / Clang / MinGW-w64) |
| **Защита кода** | Базовая (исходники можно извлечь декомпилятором) | Максимальная (машинный код, защита от реверс-инжиниринга) |
| **Производительность** | Стандартная скорость Python | Быстрый запуск, ускорение циклов и вычислений |
| **Рекомендуется для** | Быстрого тестирования, внутренних утилит, динамических скриптов | Коммерческого ПО, защиты интеллектуальной собственности, оптимизации |

---

## ⚡ Быстрый старт (Quick Start)

> 💡 **Впервые используете QPyPack?** Ознакомьтесь с [**📖 Руководством по быстрому старту (QUICKSTART.md)**](../../QUICKSTART.md).

### Способ 1: Установка через pip / pipx (Рекомендуется)

Требуется Python >= 3.8:

```bash
# Установка через pip
pip install qpypack

# Запуск приложения
qpypack
```

*С современными пакетными менеджерами:*
```bash
# Изолированный запуск через pipx
pipx run qpypack

# Быстрый запуск через uv
uvx qpypack
```

### Способ 2: Готовые скомпилированные версии

Без предварительной настройки Python скачайте готовые исполняемые файлы со страницы релизов:

👉 [**Скачать релизы (GitHub Releases)**](https://github.com/Qwejay/QPyPack/releases)

---

## 📋 Разрешение путей к ресурсам (`sys._MEIPASS`)

В режиме одного файла (`--onefile`) статические ресурсы (изображения, конфигурации, модели) распаковываются во временный каталог. Используйте следующий шаблон:

```python
import sys
import os
from pathlib import Path

def get_asset_path(relative_path: str) -> Path:
    """Получение абсолютного пути к упакованным ресурсам."""
    if hasattr(sys, "_MEIPASS"):
        # Временная папка распаковки PyInstaller
        base_path = Path(sys._MEIPASS)
    elif "__compiled__" in globals():
        # Директория запуска бинарника Nuitka
        base_path = Path(sys.argv[0]).resolve().parent
    else:
        # Локальное окружение разработки
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path
```

---

## 📅 История изменений (Changelog)

Подробный список изменений версий доступен в [CHANGELOG.md](../../CHANGELOG.md).

---

## 💖 Участие и поддержка проекта

QPyPack — это проект с открытым исходным кодом. Если инструмент помог вам в разработке, вы можете поддержать автора:

- 🌟 **Поставьте Star**: Отметьте репозиторий звездой на [GitHub](https://github.com/Qwejay/QPyPack).
- 🐛 **Обратная связь**: Создавайте тикеты на [GitHub Issues](https://github.com/Qwejay/QPyPack/issues).
- ⚡ **Спонсорство**: Поддержите автора через [Afdian (爱发电)](https://www.ifdian.net/a/qwejay) (WeChat Pay / Alipay).

---

## 📄 Лицензия (License)

Проект распространяется под лицензией [GNU General Public License v3.0 (GPL-3.0)](../../LICENSE).

> [!IMPORTANT]
> **Авторские права на собранные приложения**:
> Права интеллектуальной собственности и лицензия на созданные вами приложения **полностью принадлежат вам**. Лицензия GPL-3.0 проекта QPyPack не накладывает ограничений на созданные вами программы.

<p align="right">Copyright (C) 2026 QwejayHuang.</p>
