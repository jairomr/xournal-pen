#!/usr/bin/env python3
"""
Teste de imports sem interface gráfica
Verifica se todos os módulos importam corretamente
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Python version:", sys.version)
print()
print("Testando imports...")
print("=" * 60)

# Teste 1: Versão
try:
    from _version import __version__
    print(f"✓ _version: {__version__}")
except Exception as e:
    print(f"✗ _version: {e}")
    sys.exit(1)

# Teste 2: XournalController (não precisa de GUI)
try:
    # Temporariamente mockar pyautogui para teste
    import unittest.mock as mock
    sys.modules['pyautogui'] = mock.MagicMock()

    from xournal_controller import XournalController
    controller = XournalController()

    # Verificar mapeamentos
    assert len(controller.tool_shortcuts) == 16, f"Esperado 16 ferramentas, encontrado {len(controller.tool_shortcuts)}"
    assert len(controller.color_shortcuts) == 16, f"Esperado 16 cores, encontrado {len(controller.color_shortcuts)}"

    print(f"✓ xournal_controller: {len(controller.tool_shortcuts)} ferramentas, {len(controller.color_shortcuts)} cores")
except Exception as e:
    print(f"✗ xournal_controller: {e}")
    sys.exit(1)

# Teste 3: Sintaxe do radial_menu (sem instanciar)
try:
    with open('src/radial_menu.py', 'r') as f:
        code = f.read()
    compile(code, 'radial_menu.py', 'exec')
    print("✓ radial_menu.py: Sintaxe OK")
except Exception as e:
    print(f"✗ radial_menu.py: {e}")
    sys.exit(1)

# Teste 4: Sintaxe do stylus_handler
try:
    with open('src/stylus_handler.py', 'r') as f:
        code = f.read()
    compile(code, 'stylus_handler.py', 'exec')
    print("✓ stylus_handler.py: Sintaxe OK")
except Exception as e:
    print(f"✗ stylus_handler.py: {e}")
    sys.exit(1)

# Teste 5: Sintaxe do main
try:
    with open('src/main.py', 'r') as f:
        code = f.read()
    compile(code, 'main.py', 'exec')
    print("✓ main.py: Sintaxe OK")
except Exception as e:
    print(f"✗ main.py: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("✅ Todos os testes passaram!")
print()
print("Observação: Testes de GUI requerem X server (não disponível aqui)")
print("Para testar GUI, execute no Windows/Linux com interface gráfica:")
print("  python run.py")
