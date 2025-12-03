"""
Xournal++ Radial Menu - Aplicação Principal
Menu radial standalone para stylus
"""

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.dirname(__file__))

from radial_menu import RadialMenu
from stylus_handler import StylusHandler
from xournal_controller import XournalController


class RadialMenuApp(App):
    """Aplicação principal do menu radial"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.menu = None
        self.stylus_handler = None
        self.xournal_controller = None
        self.root_layout = None

        self.menu_open = False

    def build(self):
        """Constrói a interface da aplicação"""
        # Configurar janela
        Window.clearcolor = (0, 0, 0, 0)  # Transparente
        Window.fullscreen = False
        Window.borderless = True  # Sem bordas
        Window.always_on_top = True  # Sempre no topo
        Window.size = (Window.system_size[0], Window.system_size[1])

        # Layout principal
        self.root_layout = FloatLayout()

        # Criar menu radial
        self.menu = RadialMenu()
        self.root_layout.add_widget(self.menu)

        # Bind eventos do mouse na janela
        Window.bind(on_motion=self.on_motion)
        Window.bind(on_touch_down=self.on_touch_down)

        # Inicializar componentes
        self.xournal_controller = XournalController()

        self.stylus_handler = StylusHandler(
            on_button_press=self.on_stylus_button,
            on_move=self.on_stylus_move
        )
        self.stylus_handler.start()

        print("RadialMenuApp: Aplicação iniciada")
        print("  - Pressione botão lateral da stylus ou Alt+R para abrir menu")
        print("  - ESC para fechar menu")
        print("  - Ctrl+Q para sair da aplicação")

        return self.root_layout

    def on_motion(self, window, etype, motion_event):
        """Callback quando mouse/stylus move"""
        if self.menu_open and self.menu:
            # Converter coordenadas da janela para coordenadas do widget
            x, y = motion_event.pos
            self.menu.on_hover(x, y)

    def on_touch_down(self, window, touch):
        """Callback quando tela é tocada/clicada"""
        if self.menu_open and self.menu:
            x, y = touch.pos

            # Processar seleção
            result = self.menu.on_select(x, y)

            if result:
                print(f"RadialMenuApp: Selecionado {result['type']}: {result['data']}")

                # Executar ação no Xournal++
                self.xournal_controller.execute_action(
                    result['type'],
                    result['data']
                )

                # Fechar menu
                self.toggle_menu()

        return True

    def on_stylus_button(self, x, y):
        """Callback quando botão da stylus é pressionado"""
        print(f"RadialMenuApp: Botão stylus em ({x}, {y})")
        self.toggle_menu(x, y)

    def on_stylus_move(self, x, y):
        """Callback quando stylus move"""
        if self.menu_open and self.menu:
            self.menu.on_hover(x, y)

    def toggle_menu(self, x=None, y=None):
        """Abre/fecha o menu"""
        if self.menu_open:
            # Fechar menu
            print("RadialMenuApp: Fechando menu")
            self.menu.hide()
            self.menu_open = False

            # Esconder janela
            Window.hide()

        else:
            # Abrir menu
            if x is None or y is None:
                x, y = self.stylus_handler.get_cursor_position()

            print(f"RadialMenuApp: Abrindo menu em ({x}, {y})")

            # Mostrar janela
            Window.show()

            # Abrir menu
            self.menu.show(x, y)
            self.menu_open = True

    def on_request_close(self, *args):
        """Callback quando aplicação é fechada"""
        print("RadialMenuApp: Fechando aplicação")

        if self.stylus_handler:
            self.stylus_handler.stop()

        return False  # Permitir fechar

    def on_stop(self):
        """Chamado quando aplicação para"""
        if self.stylus_handler:
            self.stylus_handler.stop()


def main():
    """Função principal"""
    print("=" * 60)
    print("Xournal++ Radial Menu v2.0 - Python Edition")
    print("=" * 60)
    print()

    app = RadialMenuApp()
    app.run()


if __name__ == "__main__":
    main()
