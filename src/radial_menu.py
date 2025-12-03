"""
Menu SIMPLES usando APENAS widgets padrão do PyQt6
Sem customização desnecessária
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QWidget, QGridLayout
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor


class RadialMenuWidget(QDialog):
    """Menu simples - apenas botões padrão"""

    itemSelected = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Xournal++ Menu")
        self.setupUI()

    def setupUI(self):
        """Configurar interface usando apenas widgets padrão"""
        layout = QVBoxLayout()

        # Seção de Cores
        colors_label = QLabel("CORES")
        layout.addWidget(colors_label)

        colors_layout = self._create_colors_section()
        layout.addLayout(colors_layout)

        # Seção de Ferramentas
        tools_label = QLabel("FERRAMENTAS")
        layout.addWidget(tools_label)

        tools_layout = self._create_tools_section()
        layout.addLayout(tools_layout)

        # Botão Fechar
        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.hide)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def _create_colors_section(self):
        """Criar seção de cores usando QGridLayout padrão"""
        layout = QGridLayout()

        colors = [
            ("Preto", 0, 0, 0),
            ("Cinza", 128, 128, 128),
            ("Branco", 255, 255, 255),
            ("Vermelho", 255, 0, 0),
            ("Laranja", 255, 127, 0),
            ("Amarelo", 255, 255, 0),
            ("Verde", 0, 192, 0),
            ("Azul", 0, 0, 255),
        ]

        for i, (name, r, g, b) in enumerate(colors):
            btn = QPushButton(name)
            btn.clicked.connect(
                lambda checked, n=name, rgb=(r,g,b): self._on_color_selected(n, rgb)
            )
            layout.addWidget(btn, i // 4, i % 4)

        return layout

    def _create_tools_section(self):
        """Criar seção de ferramentas usando QGridLayout padrão"""
        layout = QGridLayout()

        tools = [
            ("Caneta Fina", "pen_fine"),
            ("Caneta Média", "pen_medium"),
            ("Caneta Grossa", "pen_thick"),
            ("Marca-Texto", "highlighter"),
            ("Borracha", "eraser"),
            ("Seleção", "select"),
            ("Zoom +", "zoom_in"),
            ("Zoom -", "zoom_out"),
        ]

        for i, (name, action) in enumerate(tools):
            btn = QPushButton(name)
            btn.clicked.connect(
                lambda checked, n=name, a=action: self._on_tool_selected(n, a)
            )
            layout.addWidget(btn, i // 4, i % 4)

        return layout

    def _on_color_selected(self, name, rgb):
        """Cor selecionada"""
        print(f"✓ COR: {name}")
        color = QColor(rgb[0], rgb[1], rgb[2])
        self.itemSelected.emit("color", {"name": name, "color": color})
        self.hide()

    def _on_tool_selected(self, name, action):
        """Ferramenta selecionada"""
        print(f"✓ FERRAMENTA: {name} ({action})")
        self.itemSelected.emit("tool", {"name": name, "action": action})
        self.hide()

    def show_at(self, x, y):
        """Mostrar menu na posição especificada"""
        self.move(x, y)
        self.show()
