"""
Radial Menu Widget for Xournal++
Menu radial visual usando Kivy com detecção de toque/hover
"""

from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Triangle
from kivy.graphics.instructions import InstructionGroup
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel
import math


class RadialMenu(Widget):
    """Widget de menu radial circular"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Configuração do menu
        self.inner_radius = 60  # Raio interno (cores)
        self.outer_radius = 180  # Raio externo (ferramentas)
        self.center_x = 0
        self.center_y = 0

        # Paleta de cores (círculo central)
        self.colors = [
            {"name": "Preto", "rgb": (0, 0, 0)},
            {"name": "Azul", "rgb": (0.2, 0.2, 0.8)},
            {"name": "Vermelho", "rgb": (1, 0, 0)},
            {"name": "Verde", "rgb": (0, 0.75, 0)},
            {"name": "Laranja", "rgb": (1, 0.5, 0)},
            {"name": "Amarelo", "rgb": (1, 1, 0)},
            {"name": "Magenta", "rgb": (1, 0, 1)},
            {"name": "Cinza", "rgb": (0.5, 0.5, 0.5)},
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

        self.selected_section = None
        self.selected_index = None
        self.hover_section = None
        self.hover_index = None

        self.is_visible = False

    def show(self, x, y):
        """Mostra o menu na posição especificada"""
        self.center_x = x
        self.center_y = y
        self.is_visible = True
        self.draw_menu()

    def hide(self):
        """Esconde o menu"""
        self.is_visible = False
        self.canvas.clear()

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

    def on_hover(self, x, y):
        """Atualiza highlight quando cursor passa sobre o menu"""
        if not self.is_visible:
            return

        section, index = self.detect_section(x, y)
        if section != self.hover_section or index != self.hover_index:
            self.hover_section = section
            self.hover_index = index
            self.draw_menu()

    def on_select(self, x, y):
        """Processa seleção quando usuário clica/toca"""
        if not self.is_visible:
            return None

        section, index = self.detect_section(x, y)

        if section == "color" and index is not None:
            return {"type": "color", "data": self.colors[index]}
        elif section == "tool" and index is not None:
            return {"type": "tool", "data": self.tools[index]}

        return None

    def draw_menu(self):
        """Desenha o menu radial completo"""
        self.canvas.clear()

        if not self.is_visible:
            return

        with self.canvas:
            # 1. Fundo semi-transparente
            Color(0, 0, 0, 0.3)
            Ellipse(
                pos=(self.center_x - self.outer_radius,
                     self.center_y - self.outer_radius),
                size=(self.outer_radius * 2, self.outer_radius * 2)
            )

            # 2. Desenhar fatias de cores (círculo central)
            color_angle = (2 * math.pi) / len(self.colors)
            for i, color_data in enumerate(self.colors):
                start_angle = i * color_angle
                end_angle = (i + 1) * color_angle

                # Highlight se hover
                alpha = 1.0 if (self.hover_section == "color" and self.hover_index == i) else 0.8

                Color(color_data["rgb"][0], color_data["rgb"][1], color_data["rgb"][2], alpha)

                # Desenhar fatia usando polígono
                self._draw_slice(
                    self.center_x, self.center_y,
                    0, self.inner_radius,
                    start_angle, end_angle
                )

                # Linha divisória
                Color(0, 0, 0, 0.5)
                end_x = self.center_x + self.inner_radius * math.cos(start_angle)
                end_y = self.center_y + self.inner_radius * math.sin(start_angle)
                Line(points=[self.center_x, self.center_y, end_x, end_y], width=1)

            # 3. Círculo divisor
            Color(0, 0, 0, 1)
            Line(
                circle=(self.center_x, self.center_y, self.inner_radius),
                width=2
            )

            # 4. Desenhar fatias de ferramentas (anel externo)
            tool_angle = (2 * math.pi) / len(self.tools)
            for i, tool_data in enumerate(self.tools):
                start_angle = i * tool_angle
                end_angle = (i + 1) * tool_angle

                # Alternar cores de fundo
                if self.hover_section == "tool" and self.hover_index == i:
                    Color(0.3, 0.6, 1.0, 0.9)  # Azul claro (highlight)
                elif i % 2 == 0:
                    Color(0.9, 0.9, 0.9, 0.9)
                else:
                    Color(0.85, 0.85, 0.85, 0.9)

                self._draw_slice(
                    self.center_x, self.center_y,
                    self.inner_radius, self.outer_radius,
                    start_angle, end_angle
                )

                # Linha divisória
                Color(0, 0, 0, 0.5)
                inner_x = self.center_x + self.inner_radius * math.cos(start_angle)
                inner_y = self.center_y + self.inner_radius * math.sin(start_angle)
                outer_x = self.center_x + self.outer_radius * math.cos(start_angle)
                outer_y = self.center_y + self.outer_radius * math.sin(start_angle)
                Line(points=[inner_x, inner_y, outer_x, outer_y], width=1)

                # Desenhar label da ferramenta
                mid_angle = (start_angle + end_angle) / 2
                label_radius = (self.inner_radius + self.outer_radius) / 2
                label_x = self.center_x + label_radius * math.cos(mid_angle)
                label_y = self.center_y + label_radius * math.sin(mid_angle)

                self._draw_text(tool_data["name"][:10], label_x, label_y, 12)

            # 5. Círculo externo
            Color(0, 0, 0, 1)
            Line(
                circle=(self.center_x, self.center_y, self.outer_radius),
                width=3
            )

            # 6. Label central
            self._draw_text("COR", self.center_x, self.center_y, 16, (1, 1, 1))

    def _draw_slice(self, cx, cy, inner_r, outer_r, start_angle, end_angle):
        """Desenha uma fatia do menu (seção entre dois ângulos)"""
        points = []

        # Arco interno
        steps = 20
        for i in range(steps + 1):
            angle = start_angle + (end_angle - start_angle) * i / steps
            x = cx + inner_r * math.cos(angle)
            y = cy + inner_r * math.sin(angle)
            points.extend([x, y])

        # Arco externo (reverso)
        for i in range(steps + 1):
            angle = end_angle - (end_angle - start_angle) * i / steps
            x = cx + outer_r * math.cos(angle)
            y = cy + outer_r * math.sin(angle)
            points.extend([x, y])

        # Fechar polígono
        if len(points) > 0:
            Line(points=points + points[:2], close=True, width=1)

    def _draw_text(self, text, x, y, size=14, color=(0, 0, 0)):
        """Desenha texto na posição especificada"""
        label = CoreLabel(text=text, font_size=size)
        label.refresh()
        texture = label.texture

        Color(*color, 1)
        from kivy.graphics import Rectangle
        Rectangle(
            texture=texture,
            pos=(x - texture.width / 2, y - texture.height / 2),
            size=texture.size
        )
