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
        print(f"Tecla pressionada: {key}, Alt: {alt_pressed}")

        if key in [keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r]:
            alt_pressed = True
            print("Alt pressionado")
        else:
            # Verificar se é 'r'
            is_r = False
            if hasattr(key, 'char') and key.char:
                is_r = key.char.lower() == 'r'

            if alt_pressed and is_r:
                print("Alt+R detectado! Abrindo menu...")
                pos = mouse.Controller().position
                print(f"Posição do mouse: {pos}")
                menu.show_at(pos[0], pos[1])

    def on_release(key):
        nonlocal alt_pressed
        if key in [keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r]:
            alt_pressed = False
            print("Alt solto")

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
