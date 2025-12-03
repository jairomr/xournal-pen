"""
Radial Menu Widget for Xournal++
Menu radial visual usando PyQt5 (sem dependência de OpenGL)
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint, QRect, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPainterPath
import math


class RadialMenuWidget(QWidget):
    """Widget de menu radial circular usando PyQt5"""

    # Sinal emitido quando uma opção é selecionada
    itemSelected = pyqtSignal(str, dict)  # (type, data)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurar widget
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

        # Configuração do menu
        self.inner_radius = 60  # Raio interno (cores)
        self.outer_radius = 180  # Raio externo (ferramentas)
        self.center_x = 0
        self.center_y = 0

        # Paleta de cores (círculo central)
        self.colors = [
            {"name": "Preto", "color": QColor(0, 0, 0)},
            {"name": "Azul", "color": QColor(51, 51, 204)},
            {"name": "Vermelho", "color": QColor(255, 0, 0)},
            {"name": "Verde", "color": QColor(0, 192, 0)},
            {"name": "Laranja", "color": QColor(255, 127, 0)},
            {"name": "Amarelo", "color": QColor(255, 255, 0)},
            {"name": "Magenta", "color": QColor(255, 0, 255)},
            {"name": "Cinza", "color": QColor(128, 128, 128)},
        ]

        # Ferramentas (anel externo)
        self.tools = [
            {"name": "Caneta Fina", "action": "pen_fine"},
            {"name": "Caneta Média", "action": "pen_medium"},
            {"name": "Marca-Texto", "action": "highlighter"},
            {"name": "Borracha", "action": "eraser"},
            {"name": "Seleção", "action": "select"},
            {"name": "Mão", "action": "hand"},
            {"name": "Zoom In", "action": "zoom_in"},
            {"name": "Zoom Out", "action": "zoom_out"},
            {"name": "Pág. Anterior", "action": "page_prev"},
            {"name": "Próxima Pág.", "action": "page_next"},
        ]

        self.hover_section = None
        self.hover_index = None

        # Tamanho do widget
        size = self.outer_radius * 2 + 40
        self.setFixedSize(size, size)

    def show_at(self, x, y):
        """Mostra o menu na posição especificada"""
        self.center_x = self.outer_radius + 20
        self.center_y = self.outer_radius + 20

        # Posicionar janela
        self.move(x - self.center_x, y - self.center_y)
        self.show()
        self.raise_()
        self.activateWindow()

    def calculate_angle(self, x, y):
        """Calcula o ângulo de um ponto em relação ao centro"""
        dx = x - self.center_x
        dy = y - self.center_y
        angle = math.atan2(dy, dx)
        if angle < 0:
            angle += 2 * math.pi
        return angle

    def calculate_distance(self, x, y):
        """Calcula a distância de um ponto ao centro"""
        dx = x - self.center_x
        dy = y - self.center_y
        return math.sqrt(dx * dx + dy * dy)

    def detect_section(self, x, y):
        """
        Detecta qual seção do menu foi tocada
        Retorna: (section, index) onde section = "color", "tool" ou "outside"
        """
        dist = self.calculate_distance(x, y)

        # Círculo central (cores)
        if dist <= self.inner_radius:
            angle = self.calculate_angle(x, y)
            section_angle = (2 * math.pi) / len(self.colors)
            index = int(angle / section_angle)
            if index >= len(self.colors):
                index = len(self.colors) - 1
            return "color", index

        # Anel externo (ferramentas)
        if dist > self.inner_radius and dist <= self.outer_radius:
            angle = self.calculate_angle(x, y)
            section_angle = (2 * math.pi) / len(self.tools)
            index = int(angle / section_angle)
            if index >= len(self.tools):
                index = len(self.tools) - 1
            return "tool", index

        # Fora do menu
        return "outside", None

    def mouseMoveEvent(self, event):
        """Atualiza highlight quando mouse move"""
        pos = event.pos()
        section, index = self.detect_section(pos.x(), pos.y())

        if section != self.hover_section or index != self.hover_index:
            self.hover_section = section
            self.hover_index = index
            self.update()  # Redesenhar

    def mousePressEvent(self, event):
        """Processa clique/toque"""
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            section, index = self.detect_section(pos.x(), pos.y())

            if section == "color" and index is not None:
                self.itemSelected.emit("color", self.colors[index])
                self.hide()
            elif section == "tool" and index is not None:
                self.itemSelected.emit("tool", self.tools[index])
                self.hide()
            elif section == "outside":
                self.hide()

    def paintEvent(self, event):
        """Desenha o menu radial"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.center_x
        cy = self.center_y

        # 1. Fundo semi-transparente
        painter.setBrush(QBrush(QColor(0, 0, 0, 100)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPoint(cx, cy), self.outer_radius, self.outer_radius)

        # 2. Desenhar fatias de cores (círculo central)
        color_angle = 360 / len(self.colors)
        for i, color_data in enumerate(self.colors):
            start_angle = i * color_angle * 16  # Qt usa 1/16 de grau
            span_angle = color_angle * 16

            # Highlight se hover
            color = color_data["color"]
            if self.hover_section == "color" and self.hover_index == i:
                color = color.lighter(120)

            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.black, 2))

            # Desenhar fatia circular (pie)
            rect = QRect(
                cx - self.inner_radius,
                cy - self.inner_radius,
                self.inner_radius * 2,
                self.inner_radius * 2
            )
            painter.drawPie(rect, int(start_angle), int(span_angle))

        # 3. Círculo divisor
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(Qt.black, 3))
        painter.drawEllipse(QPoint(cx, cy), self.inner_radius, self.inner_radius)

        # 4. Desenhar fatias de ferramentas (anel externo)
        tool_angle = 360 / len(self.tools)
        for i, tool_data in enumerate(self.tools):
            start_angle_deg = i * tool_angle
            end_angle_deg = (i + 1) * tool_angle

            start_angle_rad = math.radians(start_angle_deg)
            end_angle_rad = math.radians(end_angle_deg)

            # Cor de fundo
            if self.hover_section == "tool" and self.hover_index == i:
                bg_color = QColor(100, 150, 255, 230)  # Azul claro (highlight)
            elif i % 2 == 0:
                bg_color = QColor(230, 230, 230, 230)
            else:
                bg_color = QColor(210, 210, 210, 230)

            # Criar polígono da fatia
            path = QPainterPath()
            path.moveTo(cx, cy)

            # Arco interno
            for angle_deg in range(int(start_angle_deg), int(end_angle_deg) + 1, 5):
                angle_rad = math.radians(angle_deg)
                x = cx + self.inner_radius * math.cos(angle_rad)
                y = cy + self.inner_radius * math.sin(angle_rad)
                if angle_deg == int(start_angle_deg):
                    path.lineTo(x, y)
                else:
                    path.lineTo(x, y)

            # Linha até raio externo
            x_outer = cx + self.outer_radius * math.cos(end_angle_rad)
            y_outer = cy + self.outer_radius * math.sin(end_angle_rad)
            path.lineTo(x_outer, y_outer)

            # Arco externo (reverso)
            for angle_deg in range(int(end_angle_deg), int(start_angle_deg) - 1, -5):
                angle_rad = math.radians(angle_deg)
                x = cx + self.outer_radius * math.cos(angle_rad)
                y = cy + self.outer_radius * math.sin(angle_rad)
                path.lineTo(x, y)

            # Fechar caminho
            path.closeSubpath()

            painter.setBrush(QBrush(bg_color))
            painter.setPen(QPen(Qt.black, 1))
            painter.drawPath(path)

            # Desenhar label da ferramenta
            mid_angle_deg = (start_angle_deg + end_angle_deg) / 2
            mid_angle_rad = math.radians(mid_angle_deg)
            label_radius = (self.inner_radius + self.outer_radius) / 2
            label_x = cx + label_radius * math.cos(mid_angle_rad)
            label_y = cy + label_radius * math.sin(mid_angle_rad)

            painter.setPen(QPen(Qt.black))
            font = QFont("Sans", 9, QFont.Bold)
            painter.setFont(font)

            # Desenhar texto centralizado
            text = tool_data["name"][:12]
            text_rect = painter.fontMetrics().boundingRect(text)
            text_x = label_x - text_rect.width() / 2
            text_y = label_y + text_rect.height() / 4
            painter.drawText(int(text_x), int(text_y), text)

        # 5. Círculo externo
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(Qt.black, 4))
        painter.drawEllipse(QPoint(cx, cy), self.outer_radius, self.outer_radius)

        # 6. Label central
        painter.setPen(QPen(Qt.white))
        font = QFont("Sans", 12, QFont.Bold)
        painter.setFont(font)
        text = "COR"
        text_rect = painter.fontMetrics().boundingRect(text)
        text_x = cx - text_rect.width() / 2
        text_y = cy + text_rect.height() / 4
        painter.drawText(int(text_x), int(text_y), text)
