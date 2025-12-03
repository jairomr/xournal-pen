"""
Radial Menu Widget for Xournal++
Menu radial de 3 níveis: Color Picker (centro) + 16 cores + Ferramentas
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint, QRect, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPainterPath, QConicalGradient, QRadialGradient, QTabletEvent
import math
import colorsys


class RadialMenuWidget(QWidget):
    """Widget de menu radial de 3 níveis usando PyQt5"""

    # Sinal emitido quando uma opção é selecionada
    itemSelected = pyqtSignal(str, dict)  # (type, data)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurar widget
        # REMOVIDO: WA_NoSystemBackground - impede captura de eventos!
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)

        # Habilitar tracking de mouse e aceitar foco
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # CRÍTICO: Aceitar eventos de mouse
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, False)  # Forçar eventos de mouse

        # Habilitar eventos de tablet (caneta digital/mesa digitalizadora)
        self.setAttribute(Qt.WidgetAttribute.WA_TabletTracking)
        self.tablet_pressed = False

        # Configuração dos raios (3 níveis)
        self.picker_radius = 50      # Nível 1: Color picker HSV no centro
        self.colors_inner = 55       # Início do nível 2
        self.colors_outer = 120      # Fim do nível 2 (16 cores)
        self.tools_inner = 125       # Início do nível 3
        self.tools_outer = 220       # Fim do nível 3 (ferramentas)

        self.center_x = 0
        self.center_y = 0

        # Paleta de 16 cores (nível 2)
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

        # Ferramentas (nível 3 - anel externo)
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

        self.hover_level = None  # "picker", "color", "tool"
        self.hover_index = None

        # Tamanho do widget
        size = self.tools_outer * 2 + 40
        self.setFixedSize(size, size)

    def show_at(self, x, y):
        """Mostra o menu na posição especificada"""
        self.center_x = self.tools_outer + 20
        self.center_y = self.tools_outer + 20

        # Calcular posição da janela
        window_x = x - self.center_x
        window_y = y - self.center_y

        print(f"RadialMenu.show_at():")
        print(f"  → Posição do cursor: ({x}, {y})")
        print(f"  → Centro do menu: ({self.center_x}, {self.center_y})")
        print(f"  → Posição da janela: ({window_x}, {window_y})")
        print(f"  → Tamanho da janela: {self.width()}x{self.height()}")

        # Posicionar janela
        self.move(window_x, window_y)
        self.show()
        self.raise_()
        self.activateWindow()
        self.setFocus()  # Necessário para receber eventos de teclado

        print(f"  → Widget visível: {self.isVisible()}")
        print(f"  → Geometria: x={self.x()}, y={self.y()}, w={self.width()}, h={self.height()}")
        print(f"  → Mouse tracking: {self.hasMouseTracking()}")
        print(f"  → Tablet tracking: {self.testAttribute(Qt.WidgetAttribute.WA_TabletTracking)}")
        print(f"  → Focus policy: {self.focusPolicy()}")
        print()
        print("  AGUARDANDO: Toque da caneta ou clique do mouse...")

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

    def hsv_to_qcolor(self, h, s, v):
        """Converte HSV (0-1) para QColor"""
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return QColor(int(r * 255), int(g * 255), int(b * 255))

    def detect_section(self, x, y):
        """
        Detecta qual seção do menu foi tocada (3 níveis)
        Retorna: (level, index/angle)
          - level: "picker", "color", "tool", "outside"
          - index/angle: índice da fatia ou ângulo do picker
        """
        dist = self.calculate_distance(x, y)

        # Nível 1: Color picker (centro)
        if dist <= self.picker_radius:
            angle = self.calculate_angle(x, y)
            # Retorna ângulo para calcular cor HSV
            return "picker", angle

        # Nível 2: 16 cores predefinidas
        if dist > self.colors_inner and dist <= self.colors_outer:
            angle = self.calculate_angle(x, y)
            section_angle = (2 * math.pi) / len(self.colors)
            index = int(angle / section_angle)
            if index >= len(self.colors):
                index = len(self.colors) - 1
            return "color", index

        # Nível 3: Ferramentas (anel externo)
        if dist > self.tools_inner and dist <= self.tools_outer:
            angle = self.calculate_angle(x, y)
            section_angle = (2 * math.pi) / len(self.tools)
            index = int(angle / section_angle)
            if index >= len(self.tools):
                index = len(self.tools) - 1
            return "tool", index

        # Fora do menu
        return "outside", None

    def event(self, event):
        """Intercepta TODOS os eventos para debug"""
        event_type = event.type()

        # Log apenas eventos importantes
        important_events = [
            3,   # MouseButtonPress
            4,   # MouseButtonRelease
            5,   # MouseButtonDblClick
            2,   # MouseMove
            10,  # Enter
            11,  # Leave
            87,  # TabletPress
            88,  # TabletMove
            89,  # TabletRelease
        ]

        if int(event_type) in important_events:
            print(f"→ EVENT: {event_type} ({int(event_type)})")

        return super().event(event)

    def enterEvent(self, event):
        """Mouse entrou no widget"""
        print("=" * 60)
        print("→ MOUSE ENTROU NO WIDGET!")
        print("=" * 60)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Mouse saiu do widget"""
        print("→ Mouse saiu do widget")
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        """Atualiza highlight quando mouse move"""
        pos = event.pos()
        level, data = self.detect_section(pos.x(), pos.y())

        if level != self.hover_level or data != self.hover_index:
            print(f"→ Mouse move: ({pos.x()}, {pos.y()}) - seção: {level}, índice: {data}")
            self.hover_level = level
            self.hover_index = data
            self.update()  # Redesenhar

    def mousePressEvent(self, event):
        """Processa clique/toque"""
        print(f"→ mousePressEvent disparado! Botão: {event.button()}")

        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            print(f"→ Clique ESQUERDO detectado em ({pos.x()}, {pos.y()})")
            level, data = self.detect_section(pos.x(), pos.y())
            print(f"→ Seção detectada: {level}, índice: {data}")

            if level == "picker" and data is not None:
                # Seleção de cor do HSV picker
                hue = data / (2 * math.pi)  # Normalizar ângulo para 0-1
                # Distância do centro determina saturação
                dist = self.calculate_distance(pos.x(), pos.y())
                saturation = min(dist / self.picker_radius, 1.0)
                value = 1.0  # Sempre valor máximo (brilho)

                color = self.hsv_to_qcolor(hue, saturation, value)
                print(f"→ COR PICKER SELECIONADA: RGB({color.red()}, {color.green()}, {color.blue()})")
                self.itemSelected.emit("color", {"name": "Custom", "color": color})
                self.hide()

            elif level == "color" and data is not None:
                # Seleção de cor predefinida
                color_data = self.colors[data]
                print(f"→ COR SELECIONADA: {color_data['name']}")
                self.itemSelected.emit("color", color_data)
                self.hide()

            elif level == "tool" and data is not None:
                # Seleção de ferramenta
                tool_data = self.tools[data]
                print(f"→ FERRAMENTA SELECIONADA: {tool_data['name']} ({tool_data['action']})")
                self.itemSelected.emit("tool", tool_data)
                self.hide()

            elif level == "outside":
                print("→ Clique fora do menu, fechando")
                self.hide()
        else:
            print(f"→ Botão não tratado: {event.button()} (esperado: {Qt.MouseButton.LeftButton})")
            print(f"   Para fechar o menu, clique com o botão esquerdo fora do menu ou pressione ESC")

    def tabletEvent(self, event):
        """Processa eventos de tablet/caneta digital"""
        print(f"→ TABLET EVENT! Tipo: {event.type()}")
        print(f"   Posição: ({event.position().x():.0f}, {event.position().y():.0f})")
        print(f"   Pressão: {event.pressure()}")
        print(f"   Dispositivo: {event.deviceType()}")

        # TabletPress - caneta tocou a superfície
        if event.type() == QTabletEvent.Type.TabletPress:
            print("→ TABLET PRESS (caneta tocou)")
            self.tablet_pressed = True
            pos = event.position()
            x, y = int(pos.x()), int(pos.y())

            level, data = self.detect_section(x, y)
            print(f"→ Seção detectada: {level}, índice: {data}")

            if level == "picker" and data is not None:
                # Seleção de cor do HSV picker
                hue = data / (2 * math.pi)
                dist = self.calculate_distance(x, y)
                saturation = min(dist / self.picker_radius, 1.0)
                value = 1.0

                color = self.hsv_to_qcolor(hue, saturation, value)
                print(f"→ COR PICKER SELECIONADA (TABLET): RGB({color.red()}, {color.green()}, {color.blue()})")
                self.itemSelected.emit("color", {"name": "Custom", "color": color})
                self.hide()

            elif level == "color" and data is not None:
                color_data = self.colors[data]
                print(f"→ COR SELECIONADA (TABLET): {color_data['name']}")
                self.itemSelected.emit("color", color_data)
                self.hide()

            elif level == "tool" and data is not None:
                tool_data = self.tools[data]
                print(f"→ FERRAMENTA SELECIONADA (TABLET): {tool_data['name']} ({tool_data['action']})")
                self.itemSelected.emit("tool", tool_data)
                self.hide()

            elif level == "outside":
                print("→ Clique fora do menu (TABLET), fechando")
                self.hide()

            event.accept()

        # TabletMove - caneta se moveu
        elif event.type() == QTabletEvent.Type.TabletMove:
            pos = event.position()
            x, y = int(pos.x()), int(pos.y())
            level, data = self.detect_section(x, y)

            if level != self.hover_level or data != self.hover_index:
                print(f"→ Tablet move: ({x}, {y}) - seção: {level}, índice: {data}")
                self.hover_level = level
                self.hover_index = data
                self.update()

            event.accept()

        # TabletRelease - caneta levantou
        elif event.type() == QTabletEvent.Type.TabletRelease:
            print("→ TABLET RELEASE (caneta levantou)")
            self.tablet_pressed = False
            event.accept()

        else:
            event.ignore()

    def keyPressEvent(self, event):
        """Processa eventos de teclado"""
        if event.key() == Qt.Key.Key_Escape:
            print("→ ESC pressionado, fechando menu")
            self.hide()
        else:
            super().keyPressEvent(event)

    def paintEvent(self, event):
        """Desenha o menu radial de 3 níveis"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        cx = self.center_x
        cy = self.center_y
        black = QColor(0, 0, 0)

        # 0. Fundo da janela inteira (CRÍTICO para capturar eventos)
        # Retângulo semi-transparente cobrindo toda a janela
        painter.fillRect(self.rect(), QColor(0, 0, 0, 1))  # Quase invisível mas captura eventos

        # 1. Fundo semi-transparente do menu
        painter.setBrush(QBrush(QColor(0, 0, 0, 120)))  # Mais opaco para ver melhor
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(cx, cy), self.tools_outer, self.tools_outer)

        # ============================================================
        # NÍVEL 1: COLOR PICKER HSV (centro)
        # ============================================================
        self.draw_hsv_picker(painter, cx, cy)

        # Borda do picker
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(black, 3))
        painter.drawEllipse(QPoint(cx, cy), self.picker_radius, self.picker_radius)

        # ============================================================
        # NÍVEL 2: 16 CORES PREDEFINIDAS
        # ============================================================
        color_angle = 360 / len(self.colors)
        for i, color_data in enumerate(self.colors):
            start_angle_deg = i * color_angle
            end_angle_deg = (i + 1) * color_angle

            # Highlight se hover
            color = color_data["color"]
            if self.hover_level == "color" and self.hover_index == i:
                color = color.lighter(130)

            # Desenhar fatia anular
            self.draw_annular_slice(
                painter, cx, cy,
                self.colors_inner, self.colors_outer,
                start_angle_deg, end_angle_deg,
                color, QColor(0, 0, 0, 200)
            )

        # Bordas do anel de cores
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(black, 2))
        painter.drawEllipse(QPoint(cx, cy), self.colors_inner, self.colors_inner)
        painter.drawEllipse(QPoint(cx, cy), self.colors_outer, self.colors_outer)

        # ============================================================
        # NÍVEL 3: FERRAMENTAS (anel externo)
        # ============================================================
        tool_angle = 360 / len(self.tools)
        for i, tool_data in enumerate(self.tools):
            start_angle_deg = i * tool_angle
            end_angle_deg = (i + 1) * tool_angle
            mid_angle_deg = (start_angle_deg + end_angle_deg) / 2

            # Cor de fundo
            if self.hover_level == "tool" and self.hover_index == i:
                bg_color = QColor(100, 150, 255, 230)  # Azul claro (highlight)
            elif i % 2 == 0:
                bg_color = QColor(240, 240, 240, 230)
            else:
                bg_color = QColor(220, 220, 220, 230)

            # Desenhar fatia anular
            self.draw_annular_slice(
                painter, cx, cy,
                self.tools_inner, self.tools_outer,
                start_angle_deg, end_angle_deg,
                bg_color, black
            )

            # Desenhar ícone/texto da ferramenta
            mid_angle_rad = math.radians(mid_angle_deg)
            label_radius = (self.tools_inner + self.tools_outer) / 2
            label_x = cx + label_radius * math.cos(mid_angle_rad)
            label_y = cy + label_radius * math.sin(mid_angle_rad)

            painter.setPen(QPen(black))
            font = QFont("Sans", 16, QFont.Weight.Bold)
            painter.setFont(font)

            # Desenhar ícone
            icon = tool_data.get("icon", "?")
            text_rect = painter.fontMetrics().boundingRect(icon)
            text_x = label_x - text_rect.width() / 2
            text_y = label_y + text_rect.height() / 4
            painter.drawText(int(text_x), int(text_y), icon)

        # Bordas do anel de ferramentas
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(black, 2))
        painter.drawEllipse(QPoint(cx, cy), self.tools_inner, self.tools_inner)
        painter.setPen(QPen(black, 4))
        painter.drawEllipse(QPoint(cx, cy), self.tools_outer, self.tools_outer)

    def draw_hsv_picker(self, painter, cx, cy):
        """Desenha color picker HSV estilo Krita no centro"""
        # Criar gradiente cônico (hue wheel)
        gradient = QConicalGradient(cx, cy, 0)

        # Adicionar cores do espectro HSV
        for i in range(360):
            hue = i / 360.0
            color = self.hsv_to_qcolor(hue, 1.0, 1.0)
            gradient.setColorAt(i / 360.0, color)

        # Desenhar círculo com gradiente de hue
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(QPoint(cx, cy), self.picker_radius, self.picker_radius)

        # Adicionar gradiente radial (saturação: centro branco → borda colorida)
        radial_gradient = QRadialGradient(cx, cy, self.picker_radius)
        radial_gradient.setColorAt(0.0, QColor(255, 255, 255, 220))  # Centro branco
        radial_gradient.setColorAt(1.0, QColor(255, 255, 255, 0))     # Borda transparente

        painter.setBrush(QBrush(radial_gradient))
        painter.drawEllipse(QPoint(cx, cy), self.picker_radius, self.picker_radius)

    def draw_annular_slice(self, painter, cx, cy, inner_r, outer_r,
                           start_deg, end_deg, fill_color, border_color):
        """Desenha uma fatia anular (anel)"""
        start_rad = math.radians(start_deg)
        end_rad = math.radians(end_deg)

        path = QPainterPath()

        # Começar no raio interno
        x_start = cx + inner_r * math.cos(start_rad)
        y_start = cy + inner_r * math.sin(start_rad)
        path.moveTo(x_start, y_start)

        # Arco interno
        for angle_deg in range(int(start_deg), int(end_deg) + 1, 3):
            angle_rad = math.radians(angle_deg)
            x = cx + inner_r * math.cos(angle_rad)
            y = cy + inner_r * math.sin(angle_rad)
            path.lineTo(x, y)

        # Linha radial para raio externo
        x_outer = cx + outer_r * math.cos(end_rad)
        y_outer = cy + outer_r * math.sin(end_rad)
        path.lineTo(x_outer, y_outer)

        # Arco externo (reverso)
        for angle_deg in range(int(end_deg), int(start_deg) - 1, -3):
            angle_rad = math.radians(angle_deg)
            x = cx + outer_r * math.cos(angle_rad)
            y = cy + outer_r * math.sin(angle_rad)
            path.lineTo(x, y)

        # Fechar caminho
        path.closeSubpath()

        painter.setBrush(QBrush(fill_color))
        painter.setPen(QPen(border_color, 1))
        painter.drawPath(path)
