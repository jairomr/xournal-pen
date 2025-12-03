"""
Menu GRADE SIMPLES - botões em linhas
"""
from PyQt6.QtWidgets import QDialog, QPushButton, QGridLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor


class RadialMenuWidget(QDialog):
    """Menu em GRADE - super simples"""

    itemSelected = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Xournal++ Menu")
        self.setModal(False)
        self.setWindowFlags(Qt.WindowType.Popup)

        layout = QGridLayout()
        layout.setSpacing(5)

        # Título
        title = QLabel("CORES")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        layout.addWidget(title, 0, 0, 1, 4)

        # 16 cores em 2 linhas de 8
        colors = [
            ("Preto", QColor(0, 0, 0)),
            ("Cinza E", QColor(64, 64, 64)),
            ("Cinza", QColor(128, 128, 128)),
            ("Cinza C", QColor(192, 192, 192)),
            ("Branco", QColor(255, 255, 255)),
            ("Vermelho", QColor(255, 0, 0)),
            ("Laranja", QColor(255, 127, 0)),
            ("Amarelo", QColor(255, 255, 0)),
            ("V.Lima", QColor(127, 255, 0)),
            ("Verde", QColor(0, 192, 0)),
            ("Ciano", QColor(0, 255, 255)),
            ("Azul C", QColor(51, 153, 255)),
            ("Azul", QColor(51, 51, 204)),
            ("Roxo", QColor(127, 0, 255)),
            ("Magenta", QColor(255, 0, 255)),
            ("Rosa", QColor(255, 0, 127)),
        ]

        row = 1
        for i, (name, color) in enumerate(colors):
            col = i % 8
            if i == 8:
                row = 2

            btn = QPushButton(name)
            btn.setFixedSize(70, 50)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgb({color.red()}, {color.green()}, {color.blue()});
                    color: white;
                    border: 2px solid white;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    border: 3px solid yellow;
                }}
            """)
            btn.clicked.connect(lambda checked, n=name, c=color: self._select_color(n, c))
            layout.addWidget(btn, row, col)

        # Título ferramentas
        title = QLabel("FERRAMENTAS")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        layout.addWidget(title, 3, 0, 1, 4)

        # 16 ferramentas em 2 linhas
        tools = [
            ("Caneta F", "pen_fine"),
            ("Caneta M", "pen_medium"),
            ("Caneta G", "pen_thick"),
            ("Marca-Texto", "highlighter"),
            ("Borracha", "eraser"),
            ("Seleção", "select"),
            ("Mão", "hand"),
            ("Zoom +", "zoom_in"),
            ("Zoom -", "zoom_out"),
            ("Desfazer", "undo"),
            ("Refazer", "redo"),
            ("Pág ◄", "page_prev"),
            ("Pág ►", "page_next"),
            ("Texto", "text"),
            ("Imagem", "image"),
            ("Régua", "ruler"),
        ]

        row = 4
        for i, (name, action) in enumerate(tools):
            col = i % 8
            if i == 8:
                row = 5

            btn = QPushButton(name)
            btn.setFixedSize(70, 50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgb(220, 220, 220);
                    border: 2px solid black;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgb(100, 150, 255);
                    border: 3px solid yellow;
                }
            """)
            btn.clicked.connect(lambda checked, n=name, a=action: self._select_tool(n, a))
            layout.addWidget(btn, row, col)

        # Botão fechar
        close_btn = QPushButton("FECHAR")
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(200, 50, 50);
                color: white;
                border: 2px solid white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgb(255, 100, 100);
            }
        """)
        close_btn.clicked.connect(self.hide)
        layout.addWidget(close_btn, 6, 0, 1, 8)

        self.setLayout(layout)
        self.setStyleSheet("background-color: rgb(50, 50, 50);")

    def _select_color(self, name, color):
        print(f"✓ COR: {name}")
        self.itemSelected.emit("color", {"name": name, "color": color})
        self.hide()

    def _select_tool(self, name, action):
        print(f"✓ FERRAMENTA: {name} ({action})")
        self.itemSelected.emit("tool", {"name": name, "action": action})
        self.hide()

    def show_at(self, x, y):
        print(f"→ Abrindo menu em ({x}, {y})")
        self.move(x - 300, y - 150)  # Centraliza aprox
        self.show()
