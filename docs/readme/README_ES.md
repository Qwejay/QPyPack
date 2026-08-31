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
  <strong>Herramienta GUI moderna y lista para usar para empaquetar aplicaciones Python multiplataforma</strong><br>
  <sub>Impulsada por los motores PyInstaller y Nuitka, con configuración visual, análisis estático de dependencias y flujo de compilación automatizado.</sub>
</p>

## 📌 Visión general del proyecto (Overview)

**QPyPack** es una herramienta gráfica multiplataforma diseñada para desarrolladores de Python. Al integrar de manera nativa los motores **PyInstaller** (empaquetado de bytecode) y **Nuitka** (compilación nativa C/C++), simplifica las cadenas de compilación complejas, el análisis de dependencias implícitas, el aislamiento de entornos y la recolección de recursos en una interfaz intuitiva.

Ya sea para distribuir scripts ligeros de automatización o aplicaciones de escritorio y servidor con dependencias complejas (como PySide6/PyQt, Playwright, CustomTkinter, FastAPI, etc.), QPyPack ofrece una experiencia de compilación estable, reproducible y con alta tasa de éxito en Windows, macOS y Linux.

---

## 📸 Capturas de pantalla (Screenshots)

<p align="center">
  <img width="32%" alt="Interfaz principal (Inglés)" src="https://github.com/user-attachments/assets/9d16c68e-d283-4020-86c1-9d4791756c29" />
  <img width="32%" alt="Interfaz principal (Chino)" src="https://github.com/user-attachments/assets/0147460d-1e9e-4612-9b52-9d347d81b7c5" />
  <img width="32%" alt="Motor y Entorno" src="https://github.com/user-attachments/assets/0ad4db6d-b008-4018-bd69-40a369a10b7d" />
  <br />
  <img width="32%" alt="Gestión de dependencias" src="https://github.com/user-attachments/assets/c7fd1218-d079-4898-a97c-aa980c4d1375" />
  <img width="32%" alt="Optimización y Firma" src="https://github.com/user-attachments/assets/e5b7500e-2a0d-4c6d-b20b-7d8d2d3bac8d" />
  <img width="32%" alt="Acerca de y Diagnósticos" src="https://github.com/user-attachments/assets/e652b222-49f5-44cd-ad3f-d93369ede26b" />
</p>

---

## 🛠️ Arquitectura y características principales

### 1. Motor dual de compilación y optimización binaria
* **Conmutación fluida entre motores**:
  * **PyInstaller**: Compilación rápida, sin dependencias de compilador C, excelente compatibilidad con el ecosistema.
  * **Nuitka**: Traduce código Python a binarios C/C++ nativos para un rendimiento superior, máxima protección contra ingeniería inversa y tamaño reducido.
* **Optimización LTO y poda de submódulos**: Soporte para optimización en tiempo de enlace (`--lto=yes`) en modo Lite. Detección y exclusión automática de submódulos Qt pesados no utilizados (WebEngine, 3D, Quick, etc.) para evitar el sobrepeso binario.
* **Formatos de distribución flexibles**: Compatible con modo de **Archivo único (`--onefile`)** y modo **Directorio (`--onedir`)**, con personalización del directorio interno de dependencias (`--contents-directory`).

### 2. Análisis estático y protección de dependencias
* **Escaneo AST recursivo nativo**: Analizador estático de árbol de sintaxis abstracta (AST) en Python puro que descubre importaciones explícitas e implícitas sin ejecutar el código.
* **Mapeo inteligente de paquetes**: Tabla de correspondencia integrada entre nombres de importación y paquetes PyPI (ej. `cv2` $\to$ `opencv-python`, `PIL` $\to$ `pillow`, `win32com` $\to$ `pywin32`), modular y extensible.
* **Aislamiento dinámico de bibliotecas obsoletas (Backport Isolation)**: Detecta y bloquea paquetes de retrocompatibilidad que entren en conflicto con la biblioteca estándar moderna (ej. aislando `pathlib` o `typing` en Python 3.10+).

### 3. Gestión automatizada del entorno y autorreparación
* **Aprovisionamiento automático de compiladores C/C++**: Detecta entornos locales MSVC, Clang (LLVM) y GCC. Si no hay compilador nativo, Nuitka descarga y gestiona automáticamente una cadena MinGW-w64.
* **Gestión del ciclo de vida de entornos virtuales**: Admite sandboxes aislados y entornos virtuales compartidos, con utilidad de limpieza integrada.
* **Gestión adaptativa de recursos y autorrecuperación**:
  * Evalúa RAM y espacio en disco antes de compilar, ajustando la concurrencia de hilos (Adaptive Concurrency).
  * Captura errores de memoria saturada (`ZstdError` / OOM) y reintenta automáticamente en modo monohilo de bajo consumo.
  * Evita bloqueos exclusivos de archivos temporales causados por antivirus o servicios de sincronización en la nube.

### 4. Firma de código y preajustes de proyecto
* **Firma digital inteligente**: Aplica firmas digitales Authenticode automáticamente a binarios de Windows (compatible con Signtool y PowerShell con sellado de tiempo RFC 3161) y firma en tiempo de ejecución `codesign` en macOS.
* **Suite de certificados**: Generador integrado de certificados autofirmados (`.pfx`) y soporte para certificados comerciales.
* **Importación/Exportación de preajustes**: Guarda todos los parámetros de compilación, recursos y reglas en archivos `.qpypack` compartibles.

### 5. Experiencia de usuario e internacionalización (i18n)
* **Arrastrar y soltar fluido**: Al soltar un script Python, extrae automáticamente los metadatos (`__version__`, `__author__`, nombre de la app), deduce el punto de entrada y mapea el icono de la aplicación.
* **Interfaz vectorial con soporte HiDPI**: Construida con iconos vectoriales Google Material SVG, con escalado perfecto en pantallas 4K. Traducida a 17 idiomas (español, inglés, chino, japonés, coreano, alemán, francés, etc.).

---

## 📊 Comparativa de motores (PyInstaller vs. Nuitka)

| Criterio | PyInstaller | Nuitka |
| :--- | :--- | :--- |
| **Principio** | Empaqueta intérprete de Python + bytecode (`.pyc`) | Compila código Python a binarios C/C++ nativos |
| **Velocidad de compilación** | Muy rápida (típicamente 10 – 60 s) | Más lenta (requiere generación de código C++ y optimización) |
| **Compilador C/C++** | No requerido | Requerido (gestión automática de MSVC / GCC / Clang / MinGW-w64) |
| **Nivel de protección** | Básico (código recuperable mediante descompiladores) | Extremadamente alto (código máquina, alta resistencia a ingeniería inversa) |
| **Rendimiento de ejecución**| Velocidad estándar de Python | Inicio más rápido, bucles y computación optimizados |
| **Recomendado para** | Prototipado rápido, herramientas internas, proyectos dinámicos | Software comercial, protección de algoritmos, optimización de tamaño |

---

## ⚡ Inicio rápido (Quick Start)

> 💡 **¿Primera vez usando QPyPack?** Consulte nuestra [**📖 Guía de inicio rápido (QUICKSTART.md)**](../../QUICKSTART.md) para un tutorial detallado y configuraciones recomendadas.

### Método 1: Instalación mediante pip / pipx (Recomendado)

Requiere Python >= 3.8:

```bash
# Instalar a través de pip
pip install qpypack

# Iniciar la interfaz gráfica
qpypack
```

*Con gestores de paquetes modernos:*
```bash
# Ejecutar aislado con pipx
pipx run qpypack

# Inicio ultrarrápido con uv
uvx qpypack
```

### Método 2: Versión binaria precompilada independiente

Sin necesidad de configurar Python localmente, descargue los ejecutables compilados directamente para su sistema operativo:

👉 [**Descargar versiones precompiladas (GitHub Releases)**](https://github.com/Qwejay/QPyPack/releases)

---

## 📋 Resolución de rutas de recursos (`sys._MEIPASS`)

En modo de archivo único (`--onefile`), los recursos estáticos (imágenes, configuraciones, modelos) se extraen temporalmente al ejecutarse. Utilice el siguiente patrón estándar para resolver rutas:

```python
import sys
import os
from pathlib import Path

def get_asset_path(relative_path: str) -> Path:
    """Obtiene la ruta absoluta a recursos empaquetados."""
    if hasattr(sys, "_MEIPASS"):
        # Directorio de extracción temporal de PyInstaller
        base_path = Path(sys._MEIPASS)
    elif "__compiled__" in globals():
        # Directorio de ejecución binaria de Nuitka
        base_path = Path(sys.argv[0]).resolve().parent
    else:
        # Entorno de desarrollo local
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path
```

---

## 📅 Historial de cambios (Changelog)

Consulte [CHANGELOG.md](../../CHANGELOG.md) para notas de versión detalladas y corrección de errores.

---

## 💖 Contribuciones y patrocinio

QPyPack es un proyecto de código abierto mantenido en mi tiempo libre. Si le ha sido de utilidad, agradecemos su apoyo voluntario:

- 🌟 **Estrella en GitHub**: Dele una estrella al repositorio en [GitHub](https://github.com/Qwejay/QPyPack).
- 🐛 **Reportes y sugerencias**: Envíe incidencias a través de [GitHub Issues](https://github.com/Qwejay/QPyPack/issues).
- ⚡ **Patrocinar**: Apoye al autor a través de [Afdian (爱发电)](https://www.ifdian.net/a/qwejay) (WeChat Pay / Alipay).

---

## 📄 Licencia (License)

Este proyecto está licenciado bajo la [GNU General Public License v3.0 (GPL-3.0)](../../LICENSE).

> [!IMPORTANT]
> **Derechos de autor sobre los binarios generados**:
> La propiedad intelectual y los términos de licencia de las aplicaciones creadas con QPyPack **pertenecen en su totalidad al usuario**. La licencia GPL-3.0 de QPyPack no impone restricciones sobre su software compilado.

<p align="right">Copyright (C) 2026 QwejayHuang.</p>
