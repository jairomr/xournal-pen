# Xournal++ Radial Menu - Python Edition

**Menu radial standalone para Xournal++** projetado para uso com stylus/mesa digitalizadora.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-GPL--2.0-red)

## 🎯 Por Que Python?

A versão anterior em Lua tinha limitações sérias:
- ❌ Não capturava eventos de stylus nativamente
- ❌ Precisava de biblioteca externa (lgi) para posição do cursor
- ❌ Desenhava o menu na página (não era overlay)
- ❌ API limitada e bugs com addTexts

**Solução Python:**
- ✅ **Aplicação standalone** que roda em paralelo ao Xournal++
- ✅ **Captura eventos de stylus** nativamente (botão lateral)
- ✅ **Overlay real** que aparece sobre qualquer janela
- ✅ **Detecção automática** da posição do cursor
- ✅ **Build automatizado** para Linux, Windows e macOS
- ✅ **Distribuição simples** (executável único)

## 🚀 Características

### Menu Radial de 3 Níveis

- **Nível 1 (Centro):** Color picker HSV estilo Krita - Selecione qualquer cor do espectro
- **Nível 2 (Anel Médio):** 16 cores predefinidas (grayscale + cores vibrantes)
- **Nível 3 (Anel Externo):** 16 ferramentas (canetas, borracha, marca-texto, zoom, undo/redo, navegação, texto, imagem, régua)
- **Hover highlighting:** Destaque visual da fatia sob o cursor
- **Posição automática:** Menu aparece exatamente onde está a caneta

### Captura de Eventos

- **Botão lateral da stylus:** Detectado automaticamente
- **Alt+R alternativo:** Atalho de teclado como backup
- **Qualquer dispositivo:** Funciona com Wacom, XP-Pen, Huion, etc.

### Controle do Xournal++

- **Mudança de cor:** Via atalhos nativos do Xournal++
- **Mudança de ferramenta:** Pen, highlighter, eraser, hand, etc.
- **Zoom:** In/Out
- **Navegação:** Página anterior/próxima

## 📦 Instalação

### Opção 1: Executável Pré-compilado (Recomendado)

Baixe o executável para seu sistema na página de [Releases](https://github.com/seu-usuario/xournal-radial-menu/releases):

```bash
# Linux
wget https://github.com/.../xournal-radial-menu-linux
chmod +x xournal-radial-menu-linux
./xournal-radial-menu-linux

# Windows
# Baixe xournal-radial-menu-windows.exe e execute

# macOS
# Baixe xournal-radial-menu-macos e execute
```

### Opção 2: Instalação via pip

```bash
# Clonar repositório
git clone https://github.com/seu-usuario/xournal-radial-menu-py.git
cd xournal-radial-menu-py

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar
python src/main.py
```

### Opção 3: Instalação como pacote

```bash
pip install xournal-radial-menu
xournal-radial-menu
```

## 🎮 Como Usar

### 1. Iniciar a Aplicação

```bash
# Se instalou o executável
./xournal-radial-menu-linux

# Se instalou via pip
xournal-radial-menu

# Se rodando do código-fonte
python src/main.py
```

### 2. Abrir o Menu

**Com stylus:**
- Pressione o **botão lateral da caneta**
- Menu aparece na posição do cursor

**Com teclado:**
- Pressione **Alt+R**
- Menu aparece na posição do mouse

### 3. Selecionar Opção

- **Mova o cursor** até a fatia desejada (highlight aparece)
- **Toque/clique** para selecionar
- Menu fecha automaticamente

### 4. Fechar sem Selecionar

- Pressione **botão lateral** novamente
- Ou pressione **ESC**

## ⚙️ Configuração

### Customizar Cores

Edite `src/radial_menu.py`:

```python
self.colors = [
    {"name": "Preto", "rgb": (0, 0, 0)},
    {"name": "Azul", "rgb": (0.2, 0.2, 0.8)},
    # Adicione suas cores aqui
]
```

### Customizar Ferramentas

Edite `src/radial_menu.py`:

```python
self.tools = [
    {"name": "Sua Ferramenta", "action": "custom_action"},
    # Adicione suas ferramentas aqui
]
```

E em `src/xournal_controller.py`:

```python
self.tool_shortcuts = {
    "custom_action": ["tecla"],  # Atalho do Xournal++
}
```

### Customizar Atalhos do Xournal++

Edite `src/xournal_controller.py`:

```python
self.color_shortcuts = {
    "Preto": "1",  # Mude para o atalho que você usa
    "Azul": "2",
    # ...
}
```

## 🛠️ Desenvolvimento

### Requisitos

- Python 3.8+
- Kivy 2.3+
- pynput
- pyautogui

### Estrutura do Projeto

```
xournal-radial-menu-py/
├── src/
│   ├── main.py                 # Aplicação principal
│   ├── radial_menu.py          # Widget do menu radial (Kivy)
│   ├── stylus_handler.py       # Captura de eventos de stylus
│   └── xournal_controller.py   # Controle do Xournal++
├── .github/
│   └── workflows/
│       └── build.yml           # GitHub Actions (CI/CD)
├── requirements.txt
├── pyproject.toml
└── README.md
```

### Testar Componentes Individualmente

```bash
# Testar captura de stylus
python src/stylus_handler.py

# Testar controle do Xournal++
python src/xournal_controller.py
```

### Build Local

```bash
# Instalar PyInstaller
pip install pyinstaller

# Build
pyinstaller --onefile --windowed --name xournal-radial-menu src/main.py

# Executável em dist/
./dist/xournal-radial-menu
```

### Build com GitHub Actions

1. Push para branch `main`
2. Crie uma tag: `git tag v2.0.0 && git push --tags`
3. GitHub Actions faz build automático para Linux, Windows e macOS
4. Release criado automaticamente com executáveis

## 🐛 Solução de Problemas

### Botão da stylus não funciona

**Teste se está sendo detectado:**

```bash
python src/stylus_handler.py
# Pressione o botão e veja se aparece mensagem
```

**Se não detectar:**
- O botão pode estar mapeado para função diferente no driver
- Tente usar Alt+R como alternativa
- Configure o botão no driver da tablet para não ter função (passthrough)

### Menu não aparece

**Verifique se a aplicação está rodando:**

```bash
ps aux | grep xournal-radial-menu
```

**Verifique permissões:**
- Aplicação precisa de permissão para capturar eventos de teclado/mouse
- No Linux, pode precisar rodar como root (não recomendado) ou configurar udev rules

### Ações não funcionam no Xournal++

**Verifique os atalhos:**
- Os atalhos padrão podem ser diferentes na sua versão do Xournal++
- Vá em `Xournal++ → Editar → Preferências → Atalhos de Teclado`
- Ajuste os atalhos em `xournal_controller.py` conforme necessário

### Menu fica atrás do Xournal++

**Força always-on-top:**

Edite `src/main.py`:

```python
Window.always_on_top = True
```

Se não funcionar, é uma limitação do compositor de janelas. Tente:
- Desabilitar compositor (em X11)
- Usar Wayland com suporte a always-on-top

## 📚 Tecnologias Usadas

- **[Kivy](https://kivy.org/)** - Framework GUI cross-platform
- **[pynput](https://pypi.org/project/pynput/)** - Captura de eventos de entrada
- **[pyautogui](https://pypi.org/project/pyautogui/)** - Automação de teclado
- **[PyInstaller](https://pyinstaller.org/)** - Empacotamento em executável
- **[GitHub Actions](https://github.com/features/actions)** - CI/CD

## 🤝 Contribuindo

Contribuições são bem-vindas!

1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adicionar nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

GPL-2.0 - Compatível com Xournal++

## 🙏 Créditos

- Inspirado no projeto [Xournal++](https://github.com/xournalpp/xournalpp)
- Comunidade de usuários de mesa digitalizadora

## 🔗 Links

- [Repositório GitHub](https://github.com/seu-usuario/xournal-radial-menu-py)
- [Issues/Bugs](https://github.com/seu-usuario/xournal-radial-menu-py/issues)
- [Releases](https://github.com/seu-usuario/xournal-radial-menu-py/releases)
- [Xournal++ Official](https://xournalpp.github.io/)

---

**Desenvolvido com ❤️ para a comunidade Xournal++**
