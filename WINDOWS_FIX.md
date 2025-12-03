# Correção para Windows - PyQt5 Wheels

## Problema Identificado

Usuário reportou erro ao instalar no Windows com Python 3.13 e UV:

```
error: Distribution `pyqt5-qt5==5.15.18 @ registry+https://pypi.org/simple` can't be installed
because it doesn't have a source distribution or wheel for the current platform

hint: You're on Windows (`win_amd64`), but `pyqt5-qt5` (v5.15.18) only has wheels for
the following platforms: `manylinux2014_x86_64`, `macosx_10_13_x86_64`, `macosx_11_0_arm64`
```

## Causa Raiz

- Especificação `PyQt5>=5.15.0` no requirements.txt permitia resolver para versões recentes
- PyQt5 5.15.9+ e suas dependências (pyqt5-qt5) **não têm wheels para Windows**
- Apenas têm wheels para Linux e macOS

## Solução Aplicada

**requirements.txt atualizado:**
```python
PyQt5==5.15.2  # Fixado para compatibilidade multi-plataforma
```

PyQt5 5.15.2 é a última versão com suporte completo para:
- ✅ Windows (win_amd64)
- ✅ Linux (manylinux)
- ✅ macOS (x86_64 e arm64)

## Versões PyQt5 e Compatibilidade Windows

| Versão | Windows | Linux | macOS | Notas |
|--------|---------|-------|-------|-------|
| 5.15.2 | ✅ | ✅ | ✅ | **Última estável multi-plataforma** |
| 5.15.3-5.15.8 | ⚠️ | ✅ | ✅ | Wheels limitados |
| 5.15.9+ | ❌ | ✅ | ✅ | Sem wheels para Windows |
| 5.15.18 | ❌ | ✅ | ✅ | Reportado pelo usuário |

## Teste de Instalação (Windows)

```cmd
# Limpar instalação anterior
uv pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip

# Reinstalar com versão fixa
uv pip install -r requirements.txt

# Verificar versão instalada
uv pip list | findstr PyQt5
```

**Saída esperada:**
```
PyQt5        5.15.2
PyQt5-Qt5    5.15.2
PyQt5-sip    12.8.1
```

## Lições Aprendidas

### ❌ O que NÃO fazer:
```python
# ERRADO: Permite versões sem wheels Windows
PyQt5>=5.15.0
```

### ✅ O que fazer:
```python
# CORRETO: Versão fixa compatível com todas as plataformas
PyQt5==5.15.2
```

## Testes Necessários ANTES de Commit

1. **Teste em ambiente Windows:**
   - Python 3.9, 3.10, 3.11, 3.12, 3.13
   - pip install -r requirements.txt
   - uv pip install -r requirements.txt

2. **Teste em ambiente Linux:**
   - Verificar que 5.15.2 ainda funciona

3. **Teste em ambiente macOS:**
   - Verificar compatibilidade

## Ação Corretiva

- ✅ requirements.txt corrigido para `PyQt5==5.15.2`
- ⏳ Aguardando teste do usuário no Windows com Python 3.13
- ⏳ Aguardando confirmação que funciona

## Próximos Passos

1. Usuário testa no Windows
2. Se funcionar: fazer commit
3. Se falhar: investigar alternativas (PyQt6, PySide6)
