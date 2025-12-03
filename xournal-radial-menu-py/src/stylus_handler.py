"""
Stylus Event Handler
Captura eventos do botão lateral da caneta
"""

import sys
from threading import Thread
from pynput import mouse, keyboard


class StylusHandler:
    """Gerencia captura de eventos de stylus/mouse"""

    def __init__(self, on_button_press=None, on_move=None):
        self.on_button_press = on_button_press
        self.on_move = on_move

        self.mouse_listener = None
        self.keyboard_listener = None
        self.running = False

        # Estado
        self.current_x = 0
        self.current_y = 0

    def start(self):
        """Inicia captura de eventos"""
        if self.running:
            return

        self.running = True

        # Listener de mouse (captura posição e botões)
        self.mouse_listener = mouse.Listener(
            on_move=self._on_mouse_move,
            on_click=self._on_mouse_click
        )
        self.mouse_listener.start()

        # Listener de teclado (Alt+R como alternativa)
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press
        )
        self.keyboard_listener.start()

        print("StylusHandler: Iniciado")
        print("  - Botão lateral da caneta ou botão auxiliar do mouse")
        print("  - Alt+R como alternativa")

    def stop(self):
        """Para captura de eventos"""
        self.running = False

        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()

        print("StylusHandler: Parado")

    def get_cursor_position(self):
        """Retorna posição atual do cursor"""
        return self.current_x, self.current_y

    def _on_mouse_move(self, x, y):
        """Callback quando mouse/stylus move"""
        self.current_x = x
        self.current_y = y

        if self.on_move:
            self.on_move(x, y)

    def _on_mouse_click(self, x, y, button, pressed):
        """Callback quando botão do mouse é clicado"""
        if not pressed:
            return

        # Botões que ativam o menu:
        # - Button.x1 e Button.x2 (botões auxiliares, comum em stylus)
        # - Button.middle (roda do mouse, às vezes mapeado)
        trigger_buttons = [
            mouse.Button.x1,
            mouse.Button.x2,
            mouse.Button.middle
        ]

        if button in trigger_buttons:
            print(f"StylusHandler: Botão {button} detectado em ({x}, {y})")
            if self.on_button_press:
                self.on_button_press(x, y)

    def _on_key_press(self, key):
        """Callback quando tecla é pressionada"""
        try:
            # Detectar Alt+R
            if hasattr(key, 'char') and key.char == 'r':
                if self.keyboard_listener._current_modifiers & keyboard.Key.alt:
                    print(f"StylusHandler: Alt+R detectado em ({self.current_x}, {self.current_y})")
                    if self.on_button_press:
                        self.on_button_press(self.current_x, self.current_y)
        except AttributeError:
            # Tecla especial, ignorar
            pass


if __name__ == "__main__":
    # Teste standalone
    print("=== Teste do StylusHandler ===")
    print("Pressione:")
    print("  - Botão lateral da stylus/mouse")
    print("  - Alt+R")
    print("  - Ctrl+C para sair")
    print()

    def on_press(x, y):
        print(f">>> TRIGGER em ({x}, {y})")

    def on_move(x, y):
        # Não imprimir muito para não poluir
        pass

    handler = StylusHandler(on_button_press=on_press, on_move=on_move)
    handler.start()

    try:
        # Manter rodando
        import time
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nParando...")
        handler.stop()
