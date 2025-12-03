#!/usr/bin/env python3
"""
Teste do XournalController
Verifica se todas as ferramentas e cores estão mapeadas corretamente
"""

import sys
sys.path.insert(0, 'src')

from xournal_controller import XournalController


def test_tools():
    """Testa todas as ferramentas do menu radial"""
    print("="*60)
    print("TESTE DE FERRAMENTAS")
    print("="*60)
    print()

    controller = XournalController()

    # Ferramentas do menu radial (nível 3)
    tools = [
        "pen_fine",
        "pen_medium",
        "pen_thick",
        "highlighter",
        "eraser",
        "select",
        "hand",
        "zoom_in",
        "zoom_out",
        "undo",
        "redo",
        "page_prev",
        "page_next",
        "text",
        "image",
        "ruler",
    ]

    missing = []
    for tool in tools:
        if tool in controller.tool_shortcuts:
            shortcuts = controller.tool_shortcuts[tool]
            print(f"✓ {tool:15s} → {shortcuts}")
        else:
            print(f"✗ {tool:15s} → NÃO MAPEADO")
            missing.append(tool)

    print()
    if missing:
        print(f"❌ {len(missing)} ferramenta(s) faltando: {missing}")
        return False
    else:
        print(f"✅ Todas as {len(tools)} ferramentas estão mapeadas!")
        return True


def test_colors():
    """Testa todas as cores do menu radial"""
    print()
    print("="*60)
    print("TESTE DE CORES")
    print("="*60)
    print()

    controller = XournalController()

    # Cores do menu radial (nível 2)
    colors = [
        "Preto",
        "Cinza Escuro",
        "Cinza",
        "Cinza Claro",
        "Branco",
        "Vermelho",
        "Laranja",
        "Amarelo",
        "Verde Lima",
        "Verde",
        "Ciano",
        "Azul Claro",
        "Azul",
        "Roxo",
        "Magenta",
        "Rosa",
    ]

    missing = []
    for color in colors:
        if color in controller.color_shortcuts:
            shortcut = controller.color_shortcuts[color]
            print(f"✓ {color:15s} → Tecla {shortcut}")
        else:
            print(f"✗ {color:15s} → NÃO MAPEADO")
            missing.append(color)

    print()
    if missing:
        print(f"❌ {len(missing)} cor(es) faltando: {missing}")
        return False
    else:
        print(f"✅ Todas as {len(colors)} cores estão mapeadas!")
        return True


def test_execute_action():
    """Testa o método execute_action"""
    print()
    print("="*60)
    print("TESTE DE EXECUÇÃO DE AÇÕES")
    print("="*60)
    print()

    controller = XournalController()

    print("Testando execução de ferramenta...")
    try:
        controller.execute_action("tool", {"action": "pen_fine"})
        print("✓ Ferramenta executada com sucesso")
        tool_ok = True
    except Exception as e:
        print(f"✗ Erro ao executar ferramenta: {e}")
        tool_ok = False

    print()
    print("Testando execução de cor...")
    try:
        controller.execute_action("color", {"name": "Vermelho"})
        print("✓ Cor executada com sucesso")
        color_ok = True
    except Exception as e:
        print(f"✗ Erro ao executar cor: {e}")
        color_ok = False

    print()
    print("Testando execução de cor customizada (HSV picker)...")
    try:
        # Simular QColor
        class MockQColor:
            def red(self): return 128
            def green(self): return 64
            def blue(self): return 200

        controller.execute_action("color", {
            "name": "Custom",
            "color": MockQColor()
        })
        print("✓ Cor customizada executada com sucesso")
        custom_ok = True
    except Exception as e:
        print(f"✗ Erro ao executar cor customizada: {e}")
        custom_ok = False

    print()
    if tool_ok and color_ok and custom_ok:
        print("✅ Todos os testes de execução passaram!")
        return True
    else:
        print("❌ Alguns testes de execução falharam")
        return False


def main():
    """Executa todos os testes"""
    print()
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "TESTE DO XOURNAL CONTROLLER" + " "*15 + "║")
    print("╚" + "="*58 + "╝")
    print()

    results = []
    results.append(("Ferramentas", test_tools()))
    results.append(("Cores", test_colors()))
    results.append(("Execução", test_execute_action()))

    print()
    print("="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    print()

    for name, passed in results:
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{name:20s} {status}")

    print()

    all_passed = all(r[1] for r in results)
    if all_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print()
        print("O controller está pronto para uso!")
        return 0
    else:
        print("⚠️  ALGUNS TESTES FALHARAM")
        print()
        print("Revise os erros acima antes de usar.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
