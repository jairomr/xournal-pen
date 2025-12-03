"""
Testes simplificados para StylusHandler
"""
import sys
import os
import unittest.mock as mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock pynput completamente
sys.modules['pynput'] = mock.MagicMock()
sys.modules['pynput.mouse'] = mock.MagicMock()
sys.modules['pynput.keyboard'] = mock.MagicMock()

from stylus_handler import StylusHandler


def test_initialization():
    """Testa inicialização do handler"""
    handler = StylusHandler()
    assert handler is not None
    assert handler.current_x == 0
    assert handler.current_y == 0
    assert handler.alt_pressed == False
    assert handler.running == False


def test_get_cursor_position():
    """Testa obtenção da posição do cursor"""
    handler = StylusHandler()
    handler.current_x = 100
    handler.current_y = 200

    x, y = handler.get_cursor_position()
    assert x == 100
    assert y == 200


def test_on_mouse_move():
    """Testa callback de movimento do mouse"""
    handler = StylusHandler()
    handler._on_mouse_move(150, 250)

    assert handler.current_x == 150
    assert handler.current_y == 250


def test_on_mouse_move_with_callback():
    """Testa callback de movimento com handler externo"""
    positions = []

    def on_move(x, y):
        positions.append((x, y))

    handler = StylusHandler(on_move=on_move)
    handler._on_mouse_move(100, 200)
    handler._on_mouse_move(150, 250)

    assert len(positions) == 2
    assert positions[0] == (100, 200)
    assert positions[1] == (150, 250)


if __name__ == "__main__":
    test_initialization()
    test_get_cursor_position()
    test_on_mouse_move()
    test_on_mouse_move_with_callback()
    print("✓ Todos os testes simplificados do stylus handler passaram")
