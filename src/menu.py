"""Menu simples com widgets padrão PyQt6"""
from PyQt6.QtWidgets import QDialog, QPushButton, QGridLayout
from PyQt6.QtCore import pyqtSignal, Qt


class Menu(QDialog):
    """Menu com botões padrão"""

    color_selected = pyqtSignal(str)
    tool_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xournal Menu")

        # Janela sempre no topo, sem borda, fecha ao clicar fora
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )

        self.setup()

    def setup(self):
        """Configurar botões"""
        layout = QGridLayout()

        # 8 cores
        colors = ["Preto", "Branco", "Vermelho", "Verde",
                  "Azul", "Amarelo", "Laranja", "Roxo"]

        for i, color in enumerate(colors):
            btn = QPushButton(color)
            btn.setMinimumSize(80, 40)
            btn.clicked.connect(lambda checked, c=color: self._on_color(c))
            layout.addWidget(btn, 0, i)

        # 8 ferramentas
        tools = ["Caneta", "Marca-Texto", "Borracha", "Seleção",
                 "Zoom+", "Zoom-", "Desfazer", "Refazer"]

        for i, tool in enumerate(tools):
            btn = QPushButton(tool)
            btn.setMinimumSize(80, 40)
            btn.clicked.connect(lambda checked, t=tool: self._on_tool(t))
            layout.addWidget(btn, 1, i)

        # Fechar
        close = QPushButton("FECHAR")
        close.setMinimumSize(80, 40)
        close.clicked.connect(self.hide)
        layout.addWidget(close, 2, 0, 1, 8)

        self.setLayout(layout)

    def _on_color(self, color):
        """Cor clicada"""
        print(f"✓ COR CLICADA: {color}")
        self.color_selected.emit(color)
        self.hide()

    def _on_tool(self, tool):
        """Ferramenta clicada"""
        print(f"✓ FERRAMENTA CLICADA: {tool}")
        self.tool_selected.emit(tool)
        self.hide()

    def show_at(self, x, y):
        """Mostrar na posição"""
        print(f"→ show_at chamado: ({x}, {y})")
        self.move(x, y)
        self.show()
        self.raise_()
        self.activateWindow()
        print(f"→ Menu deveria estar visível agora")
