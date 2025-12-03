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
        self.color_shortcuts = {
            "Preto": "1",
            "Azul": "2",
            "Vermelho": "3",
            "Verde": "4",
            "Laranja": "5",
            "Amarelo": "6",
            "Magenta": "7",
            "Cinza": "8",
        }

        # Mapeamento de ferramentas para atalhos do Xournal++
        self.tool_shortcuts = {
            "pen_fine": ["p", "s", "f"],  # Pen, Size, Fine
            "pen_medium": ["p", "s", "m"],  # Pen, Size, Medium
            "highlighter": ["h"],  # Highlighter
            "eraser": ["e"],  # Eraser
            "select": ["s"],  # Select
            "hand": ["shift+h"],  # Hand tool
            "zoom_in": ["ctrl+="],  # Zoom in
            "zoom_out": ["ctrl+-"],  # Zoom out
            "page_prev": ["page_up"],  # Previous page
            "page_next": ["page_down"],  # Next page
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

    def change_color(self, color_name):
        """Muda cor da caneta no Xournal++"""
        if color_name in self.color_shortcuts:
            shortcut = self.color_shortcuts[color_name]
            print(f"XournalController: Mudando cor para {color_name} (atalho: {shortcut})")
            self.send_shortcut(shortcut)
        else:
            print(f"XournalController: Cor desconhecida: {color_name}")

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
            self.change_color(action_data["name"])
        elif action_type == "tool":
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
