"""
Xournal++ Controller
Controla o Xournal++ via automação de teclado
"""

import pyautogui
import time
from typing import Tuple


class XournalController:
    """Controlador para enviar comandos ao Xournal++"""

    def __init__(self):
        # Desabilitar failsafe do pyautogui
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.05  # Pequeno delay entre comandos

        # Mapeamento de cores para atalhos (customizável)
        # Xournal++ tipicamente tem 8 atalhos de cor (1-8)
        # Cores adicionais são mapeadas para as mais próximas
        self.color_shortcuts = {
            "Preto": "1",
            "Cinza Escuro": "8",  # Mapeia para cinza
            "Cinza": "8",
            "Cinza Claro": "8",
            "Branco": "1",  # Mapeia para preto (trocar se necessário)
            "Vermelho": "3",
            "Laranja": "5",
            "Amarelo": "6",
            "Verde Lima": "4",  # Mapeia para verde
            "Verde": "4",
            "Ciano": "2",  # Mapeia para azul
            "Azul Claro": "2",
            "Azul": "2",
            "Roxo": "7",  # Mapeia para magenta
            "Magenta": "7",
            "Rosa": "7",  # Mapeia para magenta
        }

        # Mapeamento de ferramentas para atalhos do Xournal++
        self.tool_shortcuts = {
            "pen_fine": ["p", "s", "f"],  # Pen, Size, Fine
            "pen_medium": ["p", "s", "m"],  # Pen, Size, Medium
            "pen_thick": ["p", "s", "t"],  # Pen, Size, Thick
            "highlighter": ["h"],  # Highlighter
            "eraser": ["e"],  # Eraser
            "select": ["s"],  # Select
            "hand": ["shift+h"],  # Hand tool
            "zoom_in": ["ctrl+="],  # Zoom in
            "zoom_out": ["ctrl+-"],  # Zoom out
            "undo": ["ctrl+z"],  # Undo
            "redo": ["ctrl+shift+z"],  # Redo
            "page_prev": ["page_up"],  # Previous page
            "page_next": ["page_down"],  # Next page
            "text": ["t"],  # Text tool
            "image": ["i"],  # Image tool
            "ruler": ["r"],  # Ruler tool
        }

    def send_shortcut(self, keys):
        """Envia atalho de teclado para aplicação ativa"""
        if isinstance(keys, str):
            keys = [keys]

        for key_combo in keys:
            if "+" in key_combo:
                # Atalho com modificador (ctrl+c, shift+a, etc)
                parts = key_combo.split("+")
                modifiers = parts[:-1]
                key = parts[-1]
                pyautogui.hotkey(*modifiers, key)
            else:
                # Tecla simples
                pyautogui.press(key_combo)

            time.sleep(0.05)

    def change_color(self, color_name, custom_color=None):
        """
        Muda cor da caneta no Xournal++

        Args:
            color_name: Nome da cor predefinida
            custom_color: QColor personalizada do HSV picker (opcional)
        """
        if custom_color is not None:
            # Cor customizada do HSV picker
            print(f"XournalController: Cor customizada RGB({custom_color.red()}, "
                  f"{custom_color.green()}, {custom_color.blue()})")
            print("→ Aviso: Cores customizadas do HSV picker não são suportadas via atalho.")
            print("→ Considere usar uma das 16 cores predefinidas no nível 2 do menu.")
            # Tentar mapear para cor mais próxima (opcional)
            closest = self._find_closest_color(custom_color)
            if closest:
                print(f"→ Usando cor mais próxima: {closest}")
                color_name = closest

        if color_name in self.color_shortcuts:
            shortcut = self.color_shortcuts[color_name]
            print(f"XournalController: Mudando cor para {color_name} (atalho: {shortcut})")
            self.send_shortcut(shortcut)
        else:
            print(f"XournalController: Cor desconhecida: {color_name}")

    def _find_closest_color(self, qcolor):
        """
        Encontra a cor predefinida mais próxima de uma QColor

        Args:
            qcolor: QColor a ser comparada

        Returns:
            str: Nome da cor mais próxima
        """
        # Importar apenas quando necessário
        try:
            from PyQt6.QtGui import QColor
        except ImportError:
            return None

        # Cores predefinidas com seus RGB
        predefined = {
            "Preto": (0, 0, 0),
            "Vermelho": (255, 0, 0),
            "Azul": (51, 51, 204),
            "Verde": (0, 192, 0),
            "Laranja": (255, 127, 0),
            "Amarelo": (255, 255, 0),
            "Magenta": (255, 0, 255),
            "Cinza": (128, 128, 128),
        }

        # Calcular distância euclidiana no espaço RGB
        min_distance = float('inf')
        closest_name = None

        r1, g1, b1 = qcolor.red(), qcolor.green(), qcolor.blue()

        for name, (r2, g2, b2) in predefined.items():
            distance = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_name = name

        return closest_name

    def change_tool(self, tool_action):
        """Muda ferramenta no Xournal++"""
        if tool_action in self.tool_shortcuts:
            shortcuts = self.tool_shortcuts[tool_action]
            print(f"XournalController: Mudando para {tool_action} (atalhos: {shortcuts})")
            for shortcut in shortcuts:
                self.send_shortcut(shortcut)
        else:
            print(f"XournalController: Ferramenta desconhecida: {tool_action}")

    def execute_action(self, action_type, action_data):
        """
        Executa ação com base na seleção do menu

        Args:
            action_type: "color" ou "tool"
            action_data: dict com informações da ação
        """
        if action_type == "color":
            # Verificar se tem cor customizada do HSV picker
            custom_color = action_data.get("color", None)
            if "name" in action_data:
                self.change_color(action_data["name"], custom_color)
        elif action_type == "tool":
            if "action" in action_data:
                self.change_tool(action_data["action"])

    @staticmethod
    def is_xournal_active():
        """
        Verifica se Xournal++ está em foco

        Returns:
            bool: True se Xournal++ está ativo
        """
        try:
            import pygetwindow as gw
            active_window = gw.getActiveWindow()
            if active_window:
                title = active_window.title.lower()
                return "xournal" in title or "xopp" in title
        except Exception as e:
            print(f"XournalController: Erro ao verificar janela ativa: {e}")
            return False

        return False


if __name__ == "__main__":
    # Teste standalone
    print("=== Teste do XournalController ===")
    print("Certifique-se que o Xournal++ está aberto e em foco!")
    print()

    controller = XournalController()

    # Verificar se Xournal++ está ativo
    if controller.is_xournal_active():
        print("✓ Xournal++ detectado!")
    else:
        print("⚠ Xournal++ NÃO detectado (certifique-se que está em foco)")

    print()
    print("Testando mudanças de ferramenta...")
    print("(Aguarde 2 segundos e foque o Xournal++)")
    time.sleep(2)

    # Testar algumas mudanças
    controller.change_tool("pen_medium")
    time.sleep(0.5)

    controller.change_color("Vermelho")
    time.sleep(0.5)

    controller.change_tool("highlighter")
    time.sleep(0.5)

    controller.change_color("Amarelo")

    print()
    print("Teste concluído! Verifique o Xournal++")
