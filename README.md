# Xournal++ Menu

Menu simples para Xournal++ usando PyQt6.

## Instalação Windows

```powershell
# Se o projeto está no OneDrive, usar:
$env:UV_LINK_MODE="copy"
uv run python src/main.py

# OU mover projeto para fora do OneDrive (C:\projetos)
```

## Instalação Linux/Mac

```bash
uv run python src/main.py
```

## Uso

Pressione **Alt+R** para abrir o menu.

## Estrutura

- `src/menu.py` - Menu com widgets padrão PyQt6
- `src/main.py` - Aplicação principal

100% widgets padrão. Sem customizações.
