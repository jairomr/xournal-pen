"""
Menu Radial SUPER SIMPLES - janela normal com botões
"""
from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
import math


class RadialMenuWidget(QWidget):
    """Menu radial SUPER SIMPLES - sem transparência complicada"""

    itemSelected = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Janela NORMAL - sem transparência!
        self.setWindowFlags(Qt.WindowType.Popup)  # Popup fecha ao clicar fora
        self.setStyleSheet("background-color: rgb(40, 40, 40);")  # Fundo cinza escuro

        # Tamanho
        self.menu_size = 500
        self.setFixedSize(self.menu_size, self.menu_size)
        self.center_x = self.menu_size // 2
        self.center_y = self.menu_size // 2

        # 16 cores
        self.colors = [
            ("Preto", QColor(0, 0, 0)),
            ("Cinza Escuro", QColor(64, 64, 64)),
            ("Cinza", QColor(128, 128, 128)),
            ("Cinza Claro", QColor(192, 192, 192)),
            ("Branco", QColor(255, 255, 255)),
            ("Vermelho", QColor(255, 0, 0)),
            ("Laranja", QColor(255, 127, 0)),
            ("Amarelo", QColor(255, 255, 0)),
            ("Verde Lima", QColor(127, 255, 0)),
            ("Verde", QColor(0, 192, 0)),
            ("Ciano", QColor(0, 255, 255)),
            ("Azul Claro", QColor(51, 153, 255)),
            ("Azul", QColor(51, 51, 204)),
            ("Roxo", QColor(127, 0, 255)),
            ("Magenta", QColor(255, 0, 255)),
            ("Rosa", QColor(255, 0, 127)),
        ]

        # 16 ferramentas
        self.tools = [
            ("Caneta Fina", "pen_fine", "✏"),
            ("Caneta Média", "pen_medium", "✎"),
            ("Caneta Grossa", "pen_thick", "✐"),
            ("Marca-Texto", "highlighter", "▓"),
            ("Borracha", "eraser", "⌫"),
            ("Seleção", "select", "⬚"),
            ("Mão", "hand", "✋"),
            ("Zoom +", "zoom_in", "+"),
            ("Zoom -", "zoom_out", "-"),
            ("Desfazer", "undo", "↶"),
            ("Refazer", "redo", "↷"),
            ("Pág ◄", "page_prev", "◄"),
            ("Pág ►", "page_next", "►"),
            ("Texto", "text", "T"),
            ("Imagem", "image", "🖼"),
            ("Régua", "ruler", "📏"),
        ]

        self._create_buttons()

    def _create_buttons(self):
        """Cria botões grandes e fáceis de clicar"""

        # Botões de CORES - anel do meio
        radius = 120
        size = 45

        for i, (name, color) in enumerate(self.colors):
            angle = (i * 360 / 16 - 90) * math.pi / 180  # -90 para começar no topo
            x = self.center_x + radius * math.cos(angle) - size // 2
            y = self.center_y + radius * math.sin(angle) - size // 2

            btn = QPushButton(self)
            btn.setGeometry(int(x), int(y), size, size)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgb({color.red()}, {color.green()}, {color.blue()});
                    border: 3px solid white;
                    border-radius: {size//2}px;
                    font-size: 8px;
                    color: white;
                }}
                QPushButton:hover {{
                    border: 4px solid yellow;
                }}
                QPushButton:pressed {{
                    border: 4px solid red;
                }}
            """)
            btn.clicked.connect(lambda checked, n=name, c=color: self._select_color(n, c))

        # Botões de FERRAMENTAS - anel externo
        radius = 200
        size = 55

        for i, (name, action, icon) in enumerate(self.tools):
            angle = (i * 360 / 16 - 90) * math.pi / 180
            x = self.center_x + radius * math.cos(angle) - size // 2
            y = self.center_y + radius * math.sin(angle) - size // 2

            btn = QPushButton(icon, self)
            btn.setGeometry(int(x), int(y), size, size)
            btn.setToolTip(name)  # Mostra nome ao passar mouse
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgb(220, 220, 220);
                    border: 3px solid black;
                    border-radius: {size//2}px;
                    font-size: 24px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: rgb(100, 150, 255);
                    border: 4px solid yellow;
                }}
                QPushButton:pressed {{
                    background-color: rgb(50, 100, 200);
                    border: 4px solid red;
                }}
            """)
            btn.clicked.connect(lambda checked, n=name, a=action: self._select_tool(n, a))

        # Botão FECHAR no centro
        size = 60
        btn = QPushButton("✕", self)
        btn.setGeometry(self.center_x - size//2, self.center_y - size//2, size, size)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgb(200, 50, 50);
                border: 3px solid white;
                border-radius: {size//2}px;
                color: white;
                font-size: 30px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgb(255, 100, 100);
                border: 4px solid yellow;
            }}
        """)
        btn.clicked.connect(self.hide)

    def _select_color(self, name, color):
        """Cor selecionada"""
        print(f"✓ COR: {name}")
        self.itemSelected.emit("color", {"name": name, "color": color})
        self.hide()

    def _select_tool(self, name, action):
        """Ferramenta selecionada"""
        print(f"✓ FERRAMENTA: {name} ({action})")
        self.itemSelected.emit("tool", {"name": name, "action": action})
        self.hide()

    def show_at(self, x, y):
        """Mostra menu"""
        print(f"→ Abrindo menu em ({x}, {y})")
        self.move(x - self.center_x, y - self.center_y)
        self.show()
        self.raise_()
        self.activateWindow()
