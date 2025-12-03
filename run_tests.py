#!/usr/bin/env python3
"""
Script para executar todos os testes
"""
import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("="*60)
print("EXECUTANDO TESTES DO XOURNAL RADIAL MENU")
print("="*60)
print()

failed_tests = []
passed_tests = []

# Lista de testes
tests = [
    ("Versão", "tests.test_version"),
    ("XournalController", "tests.test_xournal_controller"),
    ("RadialMenu Lógica", "tests.test_radial_menu_logic"),
]

for test_name, test_module in tests:
    print(f"Executando: {test_name}...")
    try:
        module = __import__(test_module, fromlist=[''])

        # Executar todos os test_* functions
        test_functions = [name for name in dir(module) if name.startswith('test_')]

        for func_name in test_functions:
            func = getattr(module, func_name)
            try:
                func()
                passed_tests.append(f"{test_name}::{func_name}")
            except AssertionError as e:
                failed_tests.append((f"{test_name}::{func_name}", str(e)))
                print(f"  ✗ {func_name}: {e}")
            except Exception as e:
                failed_tests.append((f"{test_name}::{func_name}", str(e)))
                print(f"  ✗ {func_name}: {e}")

        if not failed_tests:
            print(f"  ✓ {test_name} - {len(test_functions)} testes passaram")
    except Exception as e:
        print(f"  ✗ Erro ao importar/executar {test_name}: {e}")
        failed_tests.append((test_name, str(e)))
    print()

# Resumo
print("="*60)
print("RESUMO DOS TESTES")
print("="*60)
print(f"Passaram: {len(passed_tests)}")
print(f"Falharam: {len(failed_tests)}")
print()

if failed_tests:
    print("TESTES QUE FALHARAM:")
    for test_name, error in failed_tests:
        print(f"  ✗ {test_name}")
        print(f"    {error}")
    print()
    sys.exit(1)
else:
    print("🎉 TODOS OS TESTES PASSARAM!")
    sys.exit(0)
