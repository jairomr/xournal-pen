"""
Testes finais de integração
"""
import sys
import os
import unittest.mock as mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock PyQt6
sys.modules['PyQt6'] = mock.MagicMock()
sys.modules['PyQt6.QtWidgets'] = mock.MagicMock()
sys.modules['PyQt6.QtCore'] = mock.MagicMock()
sys.modules['PyQt6.QtGui'] = mock.MagicMock()

# Mock pynput
sys.modules['pynput'] = mock.MagicMock()
sys.modules['pynput.mouse'] = mock.MagicMock()
sys.modules['pynput.keyboard'] = mock.MagicMock()

# Mock pyautogui
sys.modules['pyautogui'] = mock.MagicMock()

from stylus_handler import StylusHandler
from xournal_controller import XournalController


def test_stylus_lifecycle_complete():
    """Teste ciclo de vida completo"""
    handler = StylusHandler()
    assert not handler.running

    # Start
    handler.start()
    assert handler.running
    assert handler.mouse_listener is not None
    assert handler.keyboard_listener is not None

    # Atualizar posição
    handler._on_mouse_move(100, 200)
    x, y = handler.get_cursor_position()
    assert x == 100
    assert y == 200

    # Stop
    handler.stop()
    assert not handler.running


def test_stylus_callbacks_complete():
    """Teste callbacks completos"""
    move_calls = []
    press_calls = []

    def on_move(x, y):
        move_calls.append((x, y))

    def on_press(x, y):
        press_calls.append((x, y))

    handler = StylusHandler(on_button_press=on_press, on_move=on_move)

    # Testar movimento
    handler._on_mouse_move(50, 60)
    handler._on_mouse_move(70, 80)
    assert len(move_calls) == 2
    assert move_calls[0] == (50, 60)
    assert move_calls[1] == (70, 80)


def test_controller_comprehensive():
    """Teste abrangente do controller"""
    controller = XournalController()

    # Verificar estruturas
    assert len(controller.tool_shortcuts) == 16
    assert len(controller.color_shortcuts) == 16

    # Mockar send_shortcut
    sent = []

    def mock_send(keys):
        sent.append(keys)

    controller.send_shortcut = mock_send

    # Testar todas as ferramentas
    for tool_name in controller.tool_shortcuts:
        sent.clear()
        controller.change_tool(tool_name)
        assert len(sent) > 0, f"Tool {tool_name} didn't send shortcut"

    # Testar todas as cores
    for color_name in controller.color_shortcuts:
        sent.clear()
        controller.change_color(color_name)
        assert len(sent) > 0, f"Color {color_name} didn't send shortcut"

    # Testar ferramenta inválida
    sent.clear()
    controller.change_tool("invalid_tool")
    assert len(sent) == 0

    # Testar cor inválida
    sent.clear()
    controller.change_color("invalid_color")
    assert len(sent) == 0


def test_controller_execute_comprehensive():
    """Teste execução abrangente"""
    controller = XournalController()

    tool_executed = []
    color_executed = []

    def mock_tool(name):
        tool_executed.append(name)

    def mock_color(name, custom=None):
        color_executed.append((name, custom))

    controller.change_tool = mock_tool
    controller.change_color = mock_color

    # Executar ação de ferramenta
    controller.execute_action("tool", {"action": "pen_fine"})
    assert len(tool_executed) == 1
    assert tool_executed[0] == "pen_fine"

    # Executar ação de cor
    controller.execute_action("color", {"name": "Vermelho"})
    assert len(color_executed) == 1
    assert color_executed[0][0] == "Vermelho"

    # Testar tipo desconhecido
    controller.execute_action("unknown", {})


def test_send_shortcut_variations():
    """Teste variações de send_shortcut"""
    import pyautogui
    pyautogui.hotkey = mock.MagicMock()
    pyautogui.press = mock.MagicMock()

    controller = XournalController()

    # String simples
    controller.send_shortcut("a")

    # Lista simples
    controller.send_shortcut(["b"])

    # Atalho com modificador
    controller.send_shortcut(["ctrl+z"])

    # Múltiplos atalhos
    controller.send_shortcut(["x", "y", "z"])

    # Atalho complexo
    controller.send_shortcut(["ctrl+shift+z"])


if __name__ == "__main__":
    test_stylus_lifecycle_complete()
    test_stylus_callbacks_complete()
    test_controller_comprehensive()
    test_controller_execute_comprehensive()
    test_send_shortcut_variations()
    print("✓ Todos os testes finais de integração passaram")
