"""
Testes profundos para XournalController para aumentar cobertura
"""
import sys
import os
import unittest.mock as mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock tudo
sys.modules['PyQt6'] = mock.MagicMock()
sys.modules['PyQt6.QtWidgets'] = mock.MagicMock()
sys.modules['PyQt6.QtCore'] = mock.MagicMock()
sys.modules['PyQt6.QtGui'] = mock.MagicMock()
sys.modules['pynput'] = mock.MagicMock()
sys.modules['pynput.mouse'] = mock.MagicMock()
sys.modules['pynput.keyboard'] = mock.MagicMock()
sys.modules['pyautogui'] = mock.MagicMock()

from xournal_controller import XournalController


def test_change_color_with_custom():
    """Testa mudança de cor com cor customizada"""
    controller = XournalController()

    # Mock QColor
    class MockColor:
        def __init__(self, r, g, b):
            self._r, self._g, self._b = r, g, b

        def red(self):
            return self._r

        def green(self):
            return self._g

        def blue(self):
            return self._b

    import PyQt6.QtGui as QtGui
    QtGui.QColor = MockColor

    # Mock send_shortcut para rastrear chamadas
    sent = []

    def mock_send(keys):
        sent.append(keys)

    controller.send_shortcut = mock_send

    # Testar cor customizada próxima ao vermelho
    custom = MockColor(250, 10, 10)
    controller.change_color("Vermelho", custom_color=custom)
    assert len(sent) > 0


def test_change_color_custom_no_match():
    """Testa cor customizada sem match próximo"""
    controller = XournalController()

    class MockColor:
        def __init__(self, r, g, b):
            self._r, self._g, self._b = r, g, b

        def red(self):
            return self._r

        def green(self):
            return self._g

        def blue(self):
            return self._b

    import PyQt6.QtGui as QtGui
    QtGui.QColor = MockColor

    # Mock _find_closest_color para retornar None
    controller._find_closest_color = mock.MagicMock(return_value=None)
    controller.send_shortcut = mock.MagicMock()

    # Cor customizada sem match
    custom = MockColor(200, 100, 50)
    controller.change_color("InvalidName", custom_color=custom)
    # Não deve enviar atalho se não encontrar cor


def test_execute_action_color_with_custom():
    """Testa execute_action com cor customizada"""
    controller = XournalController()

    class MockColor:
        def __init__(self, r, g, b):
            self._r, self._g, self._b = r, g, b

        def red(self):
            return self._r

        def green(self):
            return self._g

        def blue(self):
            return self._b

    color_calls = []

    def mock_change_color(name, custom=None):
        color_calls.append((name, custom))

    controller.change_color = mock_change_color

    # Ação com cor customizada
    custom = MockColor(255, 0, 0)
    controller.execute_action("color", {"name": "Custom", "color": custom})

    assert len(color_calls) == 1
    assert color_calls[0][1] is not None


def test_execute_action_empty_data():
    """Testa execute_action com dados vazios"""
    controller = XournalController()

    tool_calls = []
    color_calls = []

    def mock_tool(name):
        tool_calls.append(name)

    def mock_color(name, custom=None):
        color_calls.append((name, custom))

    controller.change_tool = mock_tool
    controller.change_color = mock_color

    # Tool sem "action"
    controller.execute_action("tool", {})
    assert len(tool_calls) == 0

    # Color sem "name"
    controller.execute_action("color", {})
    assert len(color_calls) == 0

    # Color com name mas sem color
    controller.execute_action("color", {"name": "Vermelho"})
    assert len(color_calls) == 1


def test_all_tool_shortcuts():
    """Testa que todos os atalhos de ferramentas funcionam"""
    import pyautogui
    pyautogui.hotkey = mock.MagicMock()
    pyautogui.press = mock.MagicMock()

    controller = XournalController()

    for tool_name, shortcuts in controller.tool_shortcuts.items():
        controller.change_tool(tool_name)

        # Verificar que pyautogui foi chamado
        assert pyautogui.hotkey.called or pyautogui.press.called

        # Reset mocks
        pyautogui.hotkey.reset_mock()
        pyautogui.press.reset_mock()


def test_all_color_shortcuts():
    """Testa que todos os atalhos de cores funcionam"""
    import pyautogui
    pyautogui.hotkey = mock.MagicMock()
    pyautogui.press = mock.MagicMock()

    controller = XournalController()

    for color_name, shortcuts in controller.color_shortcuts.items():
        controller.change_color(color_name)

        # Verificar que pyautogui foi chamado
        assert pyautogui.hotkey.called or pyautogui.press.called

        # Reset mocks
        pyautogui.hotkey.reset_mock()
        pyautogui.press.reset_mock()


def test_send_shortcut_string():
    """Testa send_shortcut com string"""
    import pyautogui
    pyautogui.press = mock.MagicMock()

    controller = XournalController()

    # Enviar string diretamente
    controller.send_shortcut("a")
    pyautogui.press.assert_called()


def test_send_shortcut_with_modifier():
    """Testa send_shortcut com modificadores"""
    import pyautogui
    pyautogui.hotkey = mock.MagicMock()

    controller = XournalController()

    # Ctrl+Z
    controller.send_shortcut(["ctrl+z"])
    pyautogui.hotkey.assert_called_with("ctrl", "z")


def test_send_shortcut_simple():
    """Testa send_shortcut sem modificador"""
    import pyautogui
    pyautogui.press = mock.MagicMock()

    controller = XournalController()

    # Tecla simples
    controller.send_shortcut(["a"])
    pyautogui.press.assert_called_with("a")


if __name__ == "__main__":
    test_change_color_with_custom()
    test_change_color_custom_no_match()
    test_execute_action_color_with_custom()
    test_execute_action_empty_data()
    test_all_tool_shortcuts()
    test_all_color_shortcuts()
    test_send_shortcut_string()
    test_send_shortcut_with_modifier()
    test_send_shortcut_simple()
    print("✓ Todos os testes profundos do xournal controller passaram")
