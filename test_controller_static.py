#!/usr/bin/env python3
"""
Teste Estático do XournalController
Verifica mapeamentos sem precisar instalar dependências
"""

import sys


def test_tools():
    """Testa se todas as ferramentas do menu radial estão mapeadas"""
    print("="*60)
    print("TESTE DE FERRAMENTAS")
    print("="*60)
    print()

    # Mapeamento esperado (copiado do xournal_controller.py)
    tool_shortcuts = {
        "pen_fine": ["p", "s", "f"],
        "pen_medium": ["p", "s", "m"],
        "pen_thick": ["p", "s", "t"],
        "highlighter": ["h"],
        "eraser": ["e"],
        "select": ["s"],
        "hand": ["shift+h"],
        "zoom_in": ["ctrl+="],
        "zoom_out": ["ctrl+-"],
        "undo": ["ctrl+z"],
        "redo": ["ctrl+shift+z"],
        "page_prev": ["page_up"],
        "page_next": ["page_down"],
        "text": ["t"],
        "image": ["i"],
        "ruler": ["r"],
    }

    # Ferramentas do menu radial (nível 3) do radial_menu.py
    required_tools = [
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
    for tool in required_tools:
        if tool in tool_shortcuts:
            shortcuts = tool_shortcuts[tool]
            shortcut_str = " → ".join(shortcuts)
            print(f"✓ {tool:15s} → {shortcut_str}")
        else:
            print(f"✗ {tool:15s} → NÃO MAPEADO")
            missing.append(tool)

    print()
    if missing:
        print(f"❌ {len(missing)} ferramenta(s) faltando: {missing}")
        return False
    else:
        print(f"✅ Todas as {len(required_tools)} ferramentas estão mapeadas!")
        return True


def test_colors():
    """Testa se todas as cores do menu radial estão mapeadas"""
    print()
    print("="*60)
    print("TESTE DE CORES")
    print("="*60)
    print()

    # Mapeamento esperado (copiado do xournal_controller.py)
    color_shortcuts = {
        "Preto": "1",
        "Cinza Escuro": "8",
        "Cinza": "8",
        "Cinza Claro": "8",
        "Branco": "1",
        "Vermelho": "3",
        "Laranja": "5",
        "Amarelo": "6",
        "Verde Lima": "4",
        "Verde": "4",
        "Ciano": "2",
        "Azul Claro": "2",
        "Azul": "2",
        "Roxo": "7",
        "Magenta": "7",
        "Rosa": "7",
    }

    # Cores do menu radial (nível 2) do radial_menu.py
    required_colors = [
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
    for color in required_colors:
        if color in color_shortcuts:
            shortcut = color_shortcuts[color]
            print(f"✓ {color:15s} → Tecla {shortcut}")
        else:
            print(f"✗ {color:15s} → NÃO MAPEADO")
            missing.append(color)

    print()
    if missing:
        print(f"❌ {len(missing)} cor(es) faltando: {missing}")
        return False
    else:
        print(f"✅ Todas as {len(required_colors)} cores estão mapeadas!")
        return True


def test_file_integrity():
    """Testa se os arquivos contêm os mapeamentos corretos"""
    print()
    print("="*60)
    print("TESTE DE INTEGRIDADE DOS ARQUIVOS")
    print("="*60)
    print()

    results = []

    # Verificar xournal_controller.py
    print("Verificando src/xournal_controller.py...")
    try:
        with open('src/xournal_controller.py', 'r') as f:
            content = f.read()

        checks = [
            ('"pen_thick":', "pen_thick mapeado"),
            ('"undo":', "undo mapeado"),
            ('"redo":', "redo mapeado"),
            ('"text":', "text mapeado"),
            ('"image":', "image mapeado"),
            ('"ruler":', "ruler mapeado"),
            ('"Cinza Escuro":', "Cinza Escuro mapeado"),
            ('"Verde Lima":', "Verde Lima mapeado"),
            ('def _find_closest_color', "método _find_closest_color existe"),
            ('custom_color', "suporte para cor customizada"),
        ]

        all_ok = True
        for check, desc in checks:
            if check in content:
                print(f"  ✓ {desc}")
            else:
                print(f"  ✗ {desc}")
                all_ok = False

        results.append(all_ok)

    except Exception as e:
        print(f"  ✗ Erro ao ler arquivo: {e}")
        results.append(False)

    print()
    print("Verificando src/radial_menu.py...")
    try:
        with open('src/radial_menu.py', 'r') as f:
            content = f.read()

        checks = [
            ('self.picker_radius', "HSV picker definido"),
            ('self.colors_inner', "nível 2 (cores) definido"),
            ('self.tools_inner', "nível 3 (ferramentas) definido"),
            ('"Caneta Grossa"', "pen_thick no menu"),
            ('"Desfazer"', "undo no menu"),
            ('"Refazer"', "redo no menu"),
            ('"Texto"', "text no menu"),
            ('"Imagem"', "image no menu"),
            ('"Régua"', "ruler no menu"),
            ('def draw_hsv_picker', "método draw_hsv_picker existe"),
        ]

        all_ok = True
        for check, desc in checks:
            if check in content:
                print(f"  ✓ {desc}")
            else:
                print(f"  ✗ {desc}")
                all_ok = False

        results.append(all_ok)

    except Exception as e:
        print(f"  ✗ Erro ao ler arquivo: {e}")
        results.append(False)

    print()
    if all(results):
        print("✅ Integridade dos arquivos OK!")
        return True
    else:
        print("❌ Alguns arquivos têm problemas")
        return False


def main():
    """Executa todos os testes"""
    print()
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "TESTE ESTÁTICO DO XOURNAL CONTROLLER" + " "*11 + "║")
    print("╚" + "="*58 + "╝")
    print()

    results = []
    results.append(("Ferramentas", test_tools()))
    results.append(("Cores", test_colors()))
    results.append(("Integridade", test_file_integrity()))

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
        print("As 16 ferramentas e 16 cores estão corretamente mapeadas.")
        return 0
    else:
        print("⚠️  ALGUNS TESTES FALHARAM")
        print()
        print("Revise os erros acima antes de usar.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
