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
  <strong>Ferramenta GUI moderna e pronta para uso para empacotar aplicações Python multiplataforma</strong><br>
  <sub>Alimentada pelos motores PyInstaller e Nuitka, com configuração visual, análise estática de dependências e fluxo de compilação automatizado.</sub>
</p>

## 📌 Visão Geral do Projeto (Overview)

O **QPyPack** é uma ferramenta gráfica multiplataforma desenvolvida para simplificar o empacotamento de aplicações Python. Ao integrar perfeitamente os motores **PyInstaller** (agrupamento de bytecode) e **Nuitka** (compilação nativa C/C++), transforma cadeias de ferramentas complexas, análise de dependências implícitas, isolamento de ambientes e coleta de recursos em uma interface de usuário intuitiva.

Seja para distribuir scripts de automação simples ou aplicações complexas com dependências pesadas (como PySide6/PyQt, Playwright, CustomTkinter, FastAPI, etc.), o QPyPack oferece uma experiência de compilação estável, reproduzível e com alta taxa de sucesso no Windows, macOS e Linux.

---

## 📸 Capturas de Tela (Screenshots)

<p align="center">
  <img width="32%" alt="Interface Principal (Inglês)" src="https://github.com/user-attachments/assets/9d16c68e-d283-4020-86c1-9d4791756c29" />
  <img width="32%" alt="Interface Principal (Chinês)" src="https://github.com/user-attachments/assets/0147460d-1e9e-4612-9b52-9d347d81b7c5" />
  <img width="32%" alt="Motor e Ambiente" src="https://github.com/user-attachments/assets/0ad4db6d-b008-4018-bd69-40a369a10b7d" />
  <br />
  <img width="32%" alt="Gerenciamento de Dependências" src="https://github.com/user-attachments/assets/c7fd1218-d079-4898-a97c-aa980c4d1375" />
  <img width="32%" alt="Otimização e Assinatura" src="https://github.com/user-attachments/assets/e5b7500e-2a0d-4c6d-b20b-7d8d2d3bac8d" />
  <img width="32%" alt="Sobre e Diagnósticos" src="https://github.com/user-attachments/assets/e652b222-49f5-44cd-ad3f-d93369ede26b" />
</p>

---

## 🛠️ Arquitetura e Principais Recursos

### 1. Compilação por Motor Duplo e Otimização Binária
* **Alternância fluida entre motores**:
  * **PyInstaller**: Compilação rápida, sem dependência de compiladores C externos, excelente compatibilidade.
  * **Nuitka**: Traduz código Python diretamente para binários C/C++ nativos para alto desempenho, forte proteção contra engenharia reversa e tamanho compacto.
* **Otimização LTO e poda de submódulos**: Suporte a LTO (`--lto=yes`) no modo Lite. Identificação e exclusão automática de submódulos Qt pesados não utilizados (WebEngine, 3D, Quick, etc.) para evitar inchaço binário.
* **Formatos de distribuição flexíveis**: Compatível com modo de **Arquivo único (`--onefile`)** e modo **Diretório (`--onedir`)**, com personalização do diretório interno de dependências (`--contents-directory`).

### 2. Análise Estática e Proteção de Dependências
* **Varredura AST recursiva nativa**: Analisador estático de árvore de sintaxe abstrata (AST) em Python puro que descobre importações explícitas e implícitas sem executar o código.
* **Mapeamento inteligente de pacotes**: Tabela de correspondência integrada entre nomes de importação e pacotes PyPI (ex: `cv2` $\to$ `opencv-python`, `PIL` $\to$ `pillow`, `win32com` $\to$ `pywin32`), modular e extensível.
* **Isolamento dinâmico de bibliotecas obsoletas (Backport Isolation)**: Detecta e bloqueia pacotes de retrocompatibilidade obsoletos que entram em conflito com a biblioteca padrão moderna (ex: isolando `pathlib` ou `typing` no Python 3.10+).

### 3. Gerenciamento Automatizado de Ambiente e Autorrecuperação
* **Provisionamento automático de compiladores C/C++**: Detecta MSVC, Clang (LLVM) e GCC locais. Caso nenhum compilador seja encontrado, o Nuitka baixa e gerencia automaticamente a toolchain MinGW-w64.
* **Gerenciamento do ciclo de vida de ambientes virtuais**: Suporte para sandboxes isoladas e ambientes compartilhados com utilitário de limpeza integrado.
* **Gerenciamento adaptativo de recursos e autorrecuperação**:
  * Avalia RAM e espaço em disco antes da compilação, ajustando a concorrência de threads (Adaptive Concurrency).
  * Captura falhas de memória saturada (`ZstdError` / OOM) e reinicia a compilação no modo mono-thread de baixo consumo.
  * Evita bloqueios exclusivos de arquivos causados por antivírus ou serviços de sincronização em nuvem.

### 4. Assinatura de Código e Predefinições de Projeto
* **Assinatura digital inteligente**: Aplica assinaturas digitais Authenticode em binários Windows (compatível com Signtool e PowerShell com carimbo de data/hora RFC 3161) e assinatura runtime `codesign` no macOS.
* **Suite de certificados**: Gerador integrado de certificados autoassinados (`.pfx`) e suporte para certificados comerciais.
* **Importação/Exportação de predefinições**: Salva todos os parâmetros de compilação, listas de recursos e regras em arquivos `.qpypack`.

### 5. Experiência de Usuário e Internacionalização (i18n)
* **Arrastar e soltar intuitivo**: Ao soltar um script Python, extrai metadados (`__version__`, `__author__`), deduz o ponto de entrada e mapeia o ícone da aplicação.
* **Interface vetorial com suporte HiDPI**: Construída com ícones vetoriais Google Material SVG, com dimensionamento perfeito em monitores 4K. Traduzida para 17 idiomas (português, inglês, chinês, japonês, coreano, alemão, francês, espanhol, etc.).

---

## 📊 Comparativo de Motores (PyInstaller vs. Nuitka)

| Critério | PyInstaller | Nuitka |
| :--- | :--- | :--- |
| **Princípio** | Empacota interpretador Python + bytecode (`.pyc`) | Compila código Python para binários C/C++ nativos |
| **Velocidade de compilação** | Muito rápida (geralmente 10 – 60 s) | Mais lenta (requer geração de código C++ e otimizações) |
| **Compilador C/C++** | Não necessário | Necessário (gestão automática de MSVC / GCC / Clang / MinGW-w64) |
| **Nível de proteção** | Básico (código recuperável via descompiladores) | Extremamente alto (código de máquina nativo, alta proteção) |
| **Desempenho de execução**| Velocidade padrão do Python | Inicialização mais rápida, laços e computação otimizados |
| **Recomendado para** | Prototipagem rápida, ferramentas internas, projetos dinâmicos | Software comercial, proteção de algoritmos, otimização de tamanho |

---

## ⚡ Início Rápido (Quick Start)

> 💡 **Primeira vez usando o QPyPack?** Consulte nosso [**📖 Guia de Início Rápido (QUICKSTART.md)**](../../QUICKSTART.md) para um tutorial passo a passo e configurações recomendadas.

### Método 1: Instalação via pip / pipx (Recomendado)

Requer Python >= 3.8:

```bash
# Instalar via pip
pip install qpypack

# Iniciar a aplicação gráfica
qpypack
```

*Com gerenciadores de pacotes modernos:*
```bash
# Executar isolado via pipx
pipx run qpypack

# Inicialização ultrarrápida via uv
uvx qpypack
```

### Método 2: Versão binária pré-compilada independente

Sem necessidade de configurar o Python localmente, baixe os executáveis pré-compilados diretamente na página de lançamentos:

👉 [**Baixar versões pré-compiladas (GitHub Releases)**](https://github.com/Qwejay/QPyPack/releases)

---

## 📋 Resolução de Caminhos de Recursos (`sys._MEIPASS`)

No modo de arquivo único (`--onefile`), os recursos estáticos (imagens, arquivos de configuração, modelos) são extraídos temporariamente durante a execução. Utilize o seguinte padrão padrão para resolver caminhos:

```python
import sys
import os
from pathlib import Path

def get_asset_path(relative_path: str) -> Path:
    """Obtém o caminho absoluto para recursos empacotados."""
    if hasattr(sys, "_MEIPASS"):
        # Diretório de extração temporária do PyInstaller
        base_path = Path(sys._MEIPASS)
    elif "__compiled__" in globals():
        # Diretório de execução do binário Nuitka
        base_path = Path(sys.argv[0]).resolve().parent
    else:
        # Ambiente de desenvolvimento local
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path
```

---

## 📅 Registro de Alterações (Changelog)

Para notas de versão detalhadas e correções de bugs, consulte o arquivo [CHANGELOG.md](../../CHANGELOG.md).

---

## 💖 Contribuição e Patrocínio

O QPyPack é um projeto de código aberto mantido no meu tempo livre. Se esta ferramenta foi útil para você, agradecemos seu apoio voluntário:

- 🌟 **Estrela no GitHub**: Deixe uma estrela no repositório no [GitHub](https://github.com/Qwejay/QPyPack).
- 🐛 **Feedback e Sugestões**: Envie relatórios de bugs e melhorias no [GitHub Issues](https://github.com/Qwejay/QPyPack/issues).
- ⚡ **Patrocínio**: Apoie o autor através do [Afdian (爱发电)](https://www.ifdian.net/a/qwejay) (compatível com WeChat Pay / Alipay).

---

## 📄 Licença (License)

Este projeto está licenciado sob a [GNU General Public License v3.0 (GPL-3.0)](../../LICENSE).

> [!IMPORTANT]
> **Direitos autorais sobre binários gerados**:
> Os direitos de propriedade intelectual e termos de licença das aplicações criadas com o QPyPack **pertencem integralmente ao usuário**. A licença GPL-3.0 do QPyPack não impõe restrições ao seu software compilado.

<p align="right">Copyright (C) 2026 QwejayHuang.</p>
