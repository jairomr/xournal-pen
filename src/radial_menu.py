"""
Radial Menu SIMPLES usando QPushButton
"""
from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont
import math


class RadialMenuWidget(QWidget):
    """Menu radial SIMPLES com botões reais"""

    itemSelected = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurar widget
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Tamanho do widget
        self.menu_size = 480
        self.setFixedSize(self.menu_size, self.menu_size)
        self.center_x = self.menu_size // 2
        self.center_y = self.menu_size // 2

        # 16 cores predefinidas
        self.colors = [
            {"name": "Preto", "color": QColor(0, 0, 0)},
            {"name": "Cinza Escuro", "color": QColor(64, 64, 64)},
            {"name": "Cinza", "color": QColor(128, 128, 128)},
            {"name": "Cinza Claro", "color": QColor(192, 192, 192)},
            {"name": "Branco", "color": QColor(255, 255, 255)},
            {"name": "Vermelho", "color": QColor(255, 0, 0)},
            {"name": "Laranja", "color": QColor(255, 127, 0)},
            {"name": "Amarelo", "color": QColor(255, 255, 0)},
            {"name": "Verde Lima", "color": QColor(127, 255, 0)},
            {"name": "Verde", "color": QColor(0, 192, 0)},
            {"name": "Ciano", "color": QColor(0, 255, 255)},
            {"name": "Azul Claro", "color": QColor(51, 153, 255)},
            {"name": "Azul", "color": QColor(51, 51, 204)},
            {"name": "Roxo", "color": QColor(127, 0, 255)},
            {"name": "Magenta", "color": QColor(255, 0, 255)},
            {"name": "Rosa", "color": QColor(255, 0, 127)},
        ]

        # 16 ferramentas
        self.tools = [
            {"name": "Caneta Fina", "action": "pen_fine", "icon": "✏"},
            {"name": "Caneta Média", "action": "pen_medium", "icon": "✎"},
            {"name": "Caneta Grossa", "action": "pen_thick", "icon": "✐"},
            {"name": "Marca-Texto", "action": "highlighter", "icon": "▓"},
            {"name": "Borracha", "action": "eraser", "icon": "⌫"},
            {"name": "Seleção", "action": "select", "icon": "⬚"},
            {"name": "Mão", "action": "hand", "icon": "✋"},
            {"name": "Zoom In", "action": "zoom_in", "icon": "+"},
            {"name": "Zoom Out", "action": "zoom_out", "icon": "-"},
            {"name": "Desfazer", "action": "undo", "icon": "↶"},
            {"name": "Refazer", "action": "redo", "icon": "↷"},
            {"name": "Pág. Anterior", "action": "page_prev", "icon": "◄"},
            {"name": "Próxima Pág.", "action": "page_next", "icon": "►"},
            {"name": "Texto", "action": "text", "icon": "T"},
            {"name": "Imagem", "action": "image", "icon": "🖼"},
            {"name": "Régua", "action": "ruler", "icon": "📏"},
        ]

        # Criar botões
        self.color_buttons = []
        self.tool_buttons = []
        self._create_buttons()

    def _create_buttons(self):
        """Cria QPushButton para cada cor e ferramenta"""

        # Criar 16 botões de cores (anel médio)
        colors_radius = 90
        button_size = 40

        for i, color_data in enumerate(self.colors):
            angle = (i * 360 / 16) * math.pi / 180
            x = self.center_x + colors_radius * math.cos(angle) - button_size // 2
            y = self.center_y + colors_radius * math.sin(angle) - button_size // 2

            btn = QPushButton(self)
            btn.setGeometry(int(x), int(y), button_size, button_size)

            color = color_data["color"]
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgb({color.red()}, {color.green()}, {color.blue()});
                    border: 2px solid black;
                    border-radius: {button_size//2}px;
                }}
                QPushButton:hover {{
                    border: 3px solid white;
                }}
            """)

            btn.clicked.connect(lambda checked, c=color_data: self._on_color_clicked(c))
            self.color_buttons.append(btn)

        # Criar 16 botões de ferramentas (anel externo)
        tools_radius = 170
        button_size = 50

        for i, tool_data in enumerate(self.tools):
            angle = (i * 360 / 16) * math.pi / 180
            x = self.center_x + tools_radius * math.cos(angle) - button_size // 2
            y = self.center_y + tools_radius * math.sin(angle) - button_size // 2

            btn = QPushButton(tool_data["icon"], self)
            btn.setGeometry(int(x), int(y), button_size, button_size)
            btn.setFont(QFont("Sans", 20))

            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(240, 240, 240, 230);
                    border: 2px solid black;
                    border-radius: {button_size//2}px;
                    color: black;
                }}
                QPushButton:hover {{
                    background-color: rgba(100, 150, 255, 230);
                    border: 3px solid white;
                }}
            """)

            btn.clicked.connect(lambda checked, t=tool_data: self._on_tool_clicked(t))
            self.tool_buttons.append(btn)

    def _on_color_clicked(self, color_data):
        """Callback quando cor é clicada"""
        print(f"→ COR SELECIONADA: {color_data['name']}")
        self.itemSelected.emit("color", color_data)
        self.hide()

    def _on_tool_clicked(self, tool_data):
        """Callback quando ferramenta é clicada"""
        print(f"→ FERRAMENTA SELECIONADA: {tool_data['name']} ({tool_data['action']})")
        self.itemSelected.emit("tool", tool_data)
        self.hide()

    def show_at(self, x, y):
        """Mostra o menu na posição especificada"""
        print(f"→ Abrindo menu em ({x}, {y})")
        self.move(x - self.center_x, y - self.center_y)
        self.show()
        self.raise_()
        self.activateWindow()
        self.setFocus()

    def keyPressEvent(self, event):
        """ESC fecha o menu"""
        if event.key() == Qt.Key.Key_Escape:
            print("→ ESC pressionado, fechando menu")
            self.hide()

    def paintEvent(self, event):
        """Desenha fundo do menu"""
        painter = QPainter(self)

        # Fundo semi-transparente
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(self.center_x - 220, self.center_y - 220, 440, 440)
