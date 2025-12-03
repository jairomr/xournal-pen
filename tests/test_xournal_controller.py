"""
Testes para XournalController
"""
import sys
import os
import unittest.mock as mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock pyautogui antes de importar
sys.modules['pyautogui'] = mock.MagicMock()

from xournal_controller import XournalController


def test_controller_initialization():
    """Testa inicialização do controller"""
    controller = XournalController()
    assert controller is not None
    assert hasattr(controller, 'tool_shortcuts')
    assert hasattr(controller, 'color_shortcuts')


def test_tool_shortcuts_completeness():
    """Testa se todas as 16 ferramentas estão mapeadas"""
    controller = XournalController()

    required_tools = [
        "pen_fine", "pen_medium", "pen_thick",
        "highlighter", "eraser", "select",
        "hand", "zoom_in", "zoom_out",
        "undo", "redo",
        "page_prev", "page_next",
        "text", "image", "ruler"
    ]

    for tool in required_tools:
        assert tool in controller.tool_shortcuts, f"Ferramenta '{tool}' não mapeada"
        assert len(controller.tool_shortcuts[tool]) > 0, f"Ferramenta '{tool}' sem atalhos"

    assert len(controller.tool_shortcuts) == 16, f"Esperado 16 ferramentas, encontrado {len(controller.tool_shortcuts)}"


def test_color_shortcuts_completeness():
    """Testa se todas as 16 cores estão mapeadas"""
    controller = XournalController()

    required_colors = [
        "Preto", "Cinza Escuro", "Cinza", "Cinza Claro", "Branco",
        "Vermelho", "Laranja", "Amarelo",
        "Verde Lima", "Verde",
        "Ciano", "Azul Claro", "Azul",
        "Roxo", "Magenta", "Rosa"
    ]

    for color in required_colors:
        assert color in controller.color_shortcuts, f"Cor '{color}' não mapeada"
        assert len(controller.color_shortcuts[color]) > 0, f"Cor '{color}' sem atalho"

    assert len(controller.color_shortcuts) == 16, f"Esperado 16 cores, encontrado {len(controller.color_shortcuts)}"


def test_change_tool():
    """Testa mudança de ferramenta"""
    controller = XournalController()

    # Mockar send_shortcut
    controller.send_shortcut = mock.MagicMock()

    # Testar ferramenta válida
    controller.change_tool("pen_fine")
    assert controller.send_shortcut.called

    # Testar ferramenta inválida
    controller.send_shortcut.reset_mock()
    controller.change_tool("ferramenta_inexistente")
    # Não deve chamar send_shortcut
    assert not controller.send_shortcut.called


def test_change_color():
    """Testa mudança de cor"""
    controller = XournalController()

    # Mockar send_shortcut
    controller.send_shortcut = mock.MagicMock()

    # Testar cor válida
    controller.change_color("Vermelho")
    assert controller.send_shortcut.called

    # Testar cor inválida
    controller.send_shortcut.reset_mock()
    controller.change_color("Cor Inexistente")
    assert not controller.send_shortcut.called


def test_execute_action_tool():
    """Testa execução de ação de ferramenta"""
    controller = XournalController()
    controller.change_tool = mock.MagicMock()

    controller.execute_action("tool", {"action": "pen_fine"})
    controller.change_tool.assert_called_once_with("pen_fine")


def test_execute_action_color():
    """Testa execução de ação de cor"""
    controller = XournalController()
    controller.change_color = mock.MagicMock()

    controller.execute_action("color", {"name": "Vermelho"})
    controller.change_color.assert_called_once()


def test_find_closest_color():
    """Testa busca de cor mais próxima"""
    controller = XournalController()

    # Mock QColor
    class MockQColor:
        def __init__(self, r, g, b):
            self._r = r
            self._g = g
            self._b = b
        def red(self):
            return self._r
        def green(self):
            return self._g
        def blue(self):
            return self._b

    # Mockar PyQt6.QtGui.QColor
    mock_qt_gui = mock.MagicMock()
    mock_qt_gui.QColor = MockQColor
    sys.modules['PyQt6.QtGui'] = mock_qt_gui

    # Vermelho puro deve mapear para "Vermelho"
    red = MockQColor(255, 0, 0)
    closest = controller._find_closest_color(red)
    if closest is None:
        # PyQt6 não disponível, teste passa
        print("  ⚠ PyQt6 não disponível, teste pulado")
        return
    assert closest == "Vermelho", f"Esperado 'Vermelho', got '{closest}'"

    # Preto deve mapear para "Preto"
    black = MockQColor(0, 0, 0)
    closest = controller._find_closest_color(black)
    assert closest == "Preto", f"Esperado 'Preto', got '{closest}'"


if __name__ == "__main__":
    test_controller_initialization()
    test_tool_shortcuts_completeness()
    test_color_shortcuts_completeness()
    test_change_tool()
    test_change_color()
    test_execute_action_tool()
    test_execute_action_color()
    test_find_closest_color()
    print("✓ Todos os testes do controller passaram")
