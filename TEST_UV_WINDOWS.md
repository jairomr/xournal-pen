# Teste com UV no Windows

Este documento descreve como testar o Xournal Radial Menu usando `uv` no Windows.

## O que é UV?

`uv` é um gerenciador de pacotes Python extremamente rápido escrito em Rust. É uma alternativa moderna ao `pip`.

Documentação: https://github.com/astral-sh/uv

## Instalação do UV

### Windows (PowerShell)

```powershell
# Método 1: Via PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Método 2: Via Scoop
scoop install uv

# Método 3: Via Chocolatey
choco install uv
```

### Verificar instalação

```cmd
uv --version
```

## Teste Completo com UV

### 1. Clone o Repositório

```cmd
git clone https://github.com/jairomr/xournal-pen.git
cd xournal-pen
```

### 2. Instalar Dependências com UV

```cmd
uv pip install -r requirements.txt
```

**Observação:** `uv` é MUITO mais rápido que pip (10-100x)!

**⚠️ Importante:** Use sempre `requirements.txt` com UV! Não instale pacotes individuais.

### 3. Testar Imports (sem GUI)

```cmd
python test_imports.py
```

**Saída esperada:**
```
Python version: 3.x.x
Testando imports...
============================================================
✓ _version: 2.1.0
✓ xournal_controller: 16 ferramentas, 16 cores
✓ radial_menu.py: Sintaxe OK
✓ stylus_handler.py: Sintaxe OK
✓ main.py: Sintaxe OK
============================================================
✅ Todos os testes passaram!
```

### 4. Executar Aplicação

```cmd
python run.py
```

**Saída esperada:**
```
============================================================
Xournal++ Radial Menu v2.1.0 - Python/PyQt5 Edition
============================================================

✓ Aplicação iniciada
  - Pressione botão lateral da stylus ou Alt+R para abrir menu
  - ESC para fechar menu
  - Ctrl+Q para sair da aplicação
```

## Compatibilidade com Python 3.13

O projeto é totalmente compatível com Python 3.13.x!

Testado com:
- ✅ Python 3.9
- ✅ Python 3.10
- ✅ Python 3.11
- ✅ Python 3.12
- ✅ Python 3.13

## Resolução de Problemas

### ❌ "No solution found when resolving dependencies"

**Problema:** Tentou instalar com `uv run python` ou `pyproject.toml` com extras `[dev]`

**Solução:** Use instalação direta:
```cmd
uv pip install PyQt5 pynput pyautogui pyyaml
python run.py
```

### ❌ UV não reconhecido

**Solução:** Adicione UV ao PATH ou use path completo:
```cmd
C:\Users\SeuUsuario\.cargo\bin\uv pip install ...
```

### ❌ PyQt5 demora muito para instalar

**Solução:** Use `uv` em vez de `pip` - é 10-100x mais rápido!
```cmd
# pip (lento)
pip install PyQt5  # ~2-5 minutos

# uv (rápido)
uv pip install PyQt5  # ~10-30 segundos
```

## Comparação UV vs PIP

| Comando | pip | uv | Speedup |
|---------|-----|-----|---------|
| `install PyQt5` | 2-5 min | 10-30s | ~10x |
| `install -r requirements.txt` | 1-3 min | 5-15s | ~10x |
| `resolve dependencies` | 30-60s | 1-3s | ~20x |

## Vantagens do UV

1. **Velocidade:** 10-100x mais rápido que pip
2. **Cache inteligente:** Reutiliza downloads entre projetos
3. **Resolução de dependências:** Muito mais rápida
4. **Compatível com pip:** Mesma sintaxe

## Comandos Úteis

```cmd
# Instalar dependências (recomendado)
uv pip install -r requirements.txt

# Listar pacotes instalados
uv pip list

# Desinstalar pacote
uv pip uninstall PyQt5

# Atualizar pacote
uv pip install --upgrade PyQt5

# Instalar de requirements.txt
uv pip install -r requirements.txt

# Sincronizar dependências (instala apenas o necessário)
uv pip sync requirements.txt
```

## Build com UV

Para criar executável com PyInstaller usando UV:

```cmd
# Instalar PyInstaller
uv pip install pyinstaller

# Build
pyinstaller --onefile ^
  --name xournal-radial-menu-windows ^
  --noconsole ^
  --hidden-import=radial_menu ^
  --hidden-import=stylus_handler ^
  --hidden-import=xournal_controller ^
  --hidden-import=_version ^
  --paths=src ^
  src\main.py

# Executável em: dist\xournal-radial-menu-windows.exe
```

## Suporte

**Issues:** https://github.com/jairomr/xournal-pen/issues
**UV Docs:** https://github.com/astral-sh/uv

---

**Testado com:**
- Windows 10/11
- Python 3.9 - 3.13
- UV 0.5.x
- PyQt5 5.15.x
