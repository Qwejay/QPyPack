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
  <strong>Uma ferramenta GUI multiplataforma para empacotar aplicações Python baseada no PyInstaller & Nuitka</strong>
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

O QPyPack é uma ferramenta gráfica projetada para simplificar o empacotamento de aplicações Python. Ele integra perfeitamente os motores PyInstaller e Nuitka, convertendo argumentos complexos de linha de comando em uma interface intuitiva.

---

## 📷 Capturas de Tela (Screenshots)

<p align="center">
<img width="1143" height="1067" alt="image" src="https://github.com/user-attachments/assets/8658aaef-5867-470d-ba4d-07892309ab1a" />
<img width="1142" height="1067" alt="image" src="https://github.com/user-attachments/assets/b64d9b89-8bfd-4bf8-8fec-9c75f61305dd" />
</p>

---

## 🚀 Principais Recursos

* 📥 **Arrastar e Soltar** : Arraste arquivos `.py` ou `.pyw` diretamente para a janela.
* 🎨 **Detecção Automática de Ícone** : Converte e pré-visualiza ícones da pasta fonte.
* 🛡️ **Ambiente Virtual Isolado** : Cria um ambiente virtual automaticamente para reduzir o tamanho do executável.
* 🔍 **Análise de Dependências** : Leitura de `requirements.txt` e análise estática de código AST para importações ocultas.
* ⚙️ **Troca de Motor Duplo** : Alterne facilmente entre PyInstaller e Nuitka.
* 📝 **Injeção de Metadados** : Configure versão, autor e descrição diretamente na interface gráfica.

---

## ⚡ Início Rápido

```bash
# Instalar via pip
pip install qpypack

# Iniciar aplicação
qpypack
```

Ou baixe executáveis pré-compilados diretamente na página de [Releases do GitHub](https://github.com/Qwejay/QPyPack/releases).

---

## 📅 Registro de Alterações (Changelog)

Para ver o histórico completo de atualizações, consulte [CHANGELOG.md](CHANGELOG.md) ou a página de [Releases do GitHub](https://github.com/Qwejay/QPyPack/releases).

---

## 📄 Licença

Distribuído sob a licença [GNU General Public License v3.0](LICENSE).

Copyright (C) 2026 QwejayHuang.