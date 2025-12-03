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

        # Rastreamento de teclas modificadoras
        self.alt_pressed = False

    def start(self):
        """Inicia captura de eventos"""
        if self.running:
            return

        self.running = True

        # Listener de mouse (apenas para capturar posição)
        self.mouse_listener = mouse.Listener(
            on_move=self._on_mouse_move
        )
        self.mouse_listener.start()

        # Listener de teclado (Alt+R)
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self.keyboard_listener.start()

        print("StylusHandler: Iniciado")
        print("  - Pressione Alt+R para abrir menu radial")

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

    def _on_key_press(self, key):
        """Callback quando tecla é pressionada"""
        try:
            # Rastrear Alt
            if key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                self.alt_pressed = True
                return

            # Detectar R quando Alt está pressionado
            if self.alt_pressed:
                if hasattr(key, 'char') and key.char and key.char.lower() == 'r':
                    # Obter posição atual do cursor diretamente
                    mouse_controller = mouse.Controller()
                    pos = mouse_controller.position
                    self.current_x, self.current_y = pos
                    print(f"StylusHandler: Alt+R detectado em ({self.current_x}, {self.current_y})")
                    if self.on_button_press:
                        self.on_button_press(self.current_x, self.current_y)
        except AttributeError:
            pass

    def _on_key_release(self, key):
        """Callback quando tecla é solta"""
        try:
            # Liberar Alt
            if key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                self.alt_pressed = False
        except AttributeError:
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
