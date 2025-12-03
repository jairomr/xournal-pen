"""
Xournal++ Radial Menu - Aplicação Principal
Menu radial standalone para stylus usando PyQt5
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from radial_menu import RadialMenuWidget
from stylus_handler import StylusHandler
from xournal_controller import XournalController


class RadialMenuApp:
    """Aplicação principal do menu radial"""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.menu = RadialMenuWidget()
        self.stylus_handler = StylusHandler(
            on_button_press=self.on_stylus_button
        )
        self.xournal_controller = XournalController()

        # Conectar sinal de seleção
        self.menu.itemSelected.connect(self.on_item_selected)

        # Iniciar captura de stylus
        self.stylus_handler.start()

        print("="*60)
        print("Xournal++ Radial Menu v2.1.0 - Python/PyQt5 Edition")
        print("="*60)
        print()
        print("✓ Aplicação iniciada")
        print("  - Pressione botão lateral da stylus ou Alt+R para abrir menu")
        print("  - ESC para fechar menu")
        print("  - Ctrl+Q para sair da aplicação")
        print()

    def on_stylus_button(self, x, y):
        """Callback quando botão da stylus é pressionado"""
        print(f"→ Botão stylus detectado em ({x}, {y})")

        if self.menu.isVisible():
            print("→ Fechando menu")
            self.menu.hide()
        else:
            print(f"→ Abrindo menu em ({x}, {y})")
            self.menu.show_at(x, y)

    def on_item_selected(self, item_type, item_data):
        """Callback quando item é selecionado"""
        print(f"→ Selecionado {item_type}: {item_data}")

        # Executar ação no Xournal++
        self.xournal_controller.execute_action(item_type, item_data)

    def run(self):
        """Executa a aplicação"""
        # Timer para processar eventos periodicamente
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: None)  # Apenas mantém o loop ativo
        self.timer.start(100)

        return self.app.exec_()

    def cleanup(self):
        """Limpeza ao sair"""
        print("\n→ Encerrando aplicação...")
        if self.stylus_handler:
            self.stylus_handler.stop()


def main():
    """Função principal"""
    app = RadialMenuApp()

    try:
        exit_code = app.run()
    finally:
        app.cleanup()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
