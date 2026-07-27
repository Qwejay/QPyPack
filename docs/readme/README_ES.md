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
  <strong>Herramienta GUI multiplataforma para empaquetar aplicaciones Python basada en PyInstaller y Nuitka</strong>
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

QPyPack es una herramienta gráfica diseñada para simplificar el empaquetado de aplicaciones Python. Integra los motores PyInstaller y Nuitka, transformando comandos de consola en una interfaz intuitiva.

---

## 📷 Capturas de pantalla (Screenshots)

<p align="center">
<img width="1143" height="1067" alt="image" src="https://github.com/user-attachments/assets/8658aaef-5867-470d-ba4d-07892309ab1a" />
<img width="1142" height="1067" alt="image" src="https://github.com/user-attachments/assets/b64d9b89-8bfd-4bf8-8fec-9c75f61305dd" />
</p>

---

## 🚀 Características principales

* 📥 **Arrastrar y Soltar** : Arrastre archivos `.py` o `.pyw` directamente a la ventana.
* 🎨 **Detección de icono automática** : Convierte y previsualiza iconos del directorio fuente.
* 🛡️ **Aislamiento en entorno virtual** : Crea entornos virtuales automáticamente para reducir el tamaño final.
* 🔍 **Análisis de dependencias** : Lectura de `requirements.txt` y análisis estático de código AST para importaciones ocultas.
* ⚙️ **Conmutación de motor doble** : Cambie libremente entre PyInstaller y Nuitka.
* 📝 **Inyección de metadatos** : Configure la versión, autor y descripción directamente desde la interfaz.

---

## ⚡ Inicio rápido

```bash
# Instalar a través de pip
pip install qpypack

# Iniciar la aplicación
qpypack
```

Descargue ejecutables precompilados directamente en la página de [Releases de GitHub](https://github.com/Qwejay/QPyPack/releases).

---

## 📅 Historial de cambios (Changelog)

Para ver las notas de versión completas, consulte [CHANGELOG.md](CHANGELOG.md) o la página de [Releases de GitHub](https://github.com/Qwejay/QPyPack/releases).

---

## 📄 Licencia

Licenciado bajo la [GNU General Public License v3.0](LICENSE).

Copyright (C) 2026 QwejayHuang.