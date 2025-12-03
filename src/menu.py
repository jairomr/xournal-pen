"""Menu simples com widgets padrão PyQt6"""
from PyQt6.QtWidgets import QDialog, QPushButton, QGridLayout
from PyQt6.QtCore import pyqtSignal


class Menu(QDialog):
    """Menu com botões padrão"""

    color_selected = pyqtSignal(str)
    tool_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xournal Menu")
        self.setup()

    def setup(self):
        """Configurar botões"""
        layout = QGridLayout()

        # 8 cores
        colors = ["Preto", "Branco", "Vermelho", "Verde",
                  "Azul", "Amarelo", "Laranja", "Roxo"]

        for i, color in enumerate(colors):
            btn = QPushButton(color)
            btn.clicked.connect(lambda checked, c=color: self.color_selected.emit(c))
            layout.addWidget(btn, 0, i)

        # 8 ferramentas
        tools = ["Caneta", "Marca-Texto", "Borracha", "Seleção",
                 "Zoom+", "Zoom-", "Desfazer", "Refazer"]

        for i, tool in enumerate(tools):
            btn = QPushButton(tool)
            btn.clicked.connect(lambda checked, t=tool: self.tool_selected.emit(t))
            layout.addWidget(btn, 1, i)

        # Fechar
        close = QPushButton("Fechar")
        close.clicked.connect(self.hide)
        layout.addWidget(close, 2, 0, 1, 8)

        self.setLayout(layout)

    def show_at(self, x, y):
        """Mostrar na posição"""
        self.move(x, y)
        self.show()
