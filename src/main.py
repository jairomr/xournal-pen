"""Aplicação principal"""
import sys
from PyQt6.QtWidgets import QApplication
from pynput import keyboard, mouse
from menu import Menu


def main():
    app = QApplication(sys.argv)
    menu = Menu()

    # Estado Alt
    alt_pressed = False

    def on_press(key):
        nonlocal alt_pressed
        if key in [keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r]:
            alt_pressed = True
        elif alt_pressed and hasattr(key, 'char') and key.char in ['r', 'R']:
            # Alt+R - mostrar menu na posição do mouse
            pos = mouse.Controller().position
            menu.show_at(pos[0], pos[1])

    def on_release(key):
        nonlocal alt_pressed
        if key in [keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r]:
            alt_pressed = False

    # Conectar sinais
    menu.color_selected.connect(lambda c: print(f"Cor: {c}"))
    menu.tool_selected.connect(lambda t: print(f"Ferramenta: {t}"))

    # Iniciar listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    print("Menu iniciado. Pressione Alt+R para abrir.")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
