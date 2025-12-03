# Instalação no Windows

## Opção 1: Executável Pré-compilado (Recomendado) ⭐

### Passo 1: Baixar o Executável

1. Acesse a página de releases: https://github.com/jairomr/xournal-pen/releases
2. Baixe o arquivo **`xournal-radial-menu-windows.exe`** da versão mais recente (v2.1.0)
3. Salve em uma pasta de sua preferência (exemplo: `C:\Programas\XournalRadialMenu\`)

### Passo 2: Executar

1. **Clique duas vezes** no arquivo `xournal-radial-menu-windows.exe`
2. Se o Windows Defender perguntar, clique em **"Mais informações"** → **"Executar mesmo assim"**
   - Isso é normal para executáveis não assinados
3. Uma janela de terminal vai abrir mostrando:
   ```
   ============================================================
   Xournal++ Radial Menu v2.1.0 - Python/PyQt5 Edition
   ============================================================

   ✓ Aplicação iniciada
     - Pressione botão lateral da stylus ou Alt+R para abrir menu
     - ESC para fechar menu
     - Ctrl+Q para sair da aplicação
   ```

### Passo 3: Usar

- **Abra o Xournal++**
- **Pressione o botão lateral da sua stylus** (ou Alt+R) para abrir o menu radial
- **Navegue** com o mouse/stylus sobre o menu
- **Clique** para selecionar ferramenta ou cor

### Passo 4: Criar Atalho (Opcional)

Para iniciar automaticamente com o Windows:

1. **Clique direito** em `xournal-radial-menu-windows.exe`
2. Selecione **"Criar atalho"**
3. Mova o atalho para a pasta de inicialização:
   - Pressione `Win + R`
   - Digite: `shell:startup`
   - Pressione Enter
   - Cole o atalho na pasta que abrir

---

## Opção 2: Executar com Python (Para Desenvolvedores)

### Pré-requisitos

- **Python 3.9+** instalado: https://www.python.org/downloads/
  - ⚠️ Marque a opção **"Add Python to PATH"** durante a instalação!

### Passo 1: Baixar o Código

**Via Git:**
```cmd
git clone https://github.com/jairomr/xournal-pen.git
cd xournal-pen
```

**Ou baixe o ZIP:**
1. https://github.com/jairomr/xournal-pen/archive/refs/heads/main.zip
2. Extraia em uma pasta
3. Abra o prompt de comando nessa pasta

### Passo 2: Instalar Dependências

```cmd
# Opção A: Com pip (padrão)
pip install -r requirements.txt

# Opção B: Com UV (10-100x mais rápido) ⭐
uv pip install -r requirements.txt

# Opção C: Com ambiente virtual
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**⚠️ Importante:** Sempre use `requirements.txt`, não instale pacotes individuais!

### Passo 3: Executar

```cmd
python run.py
```

---

## Opção 3: Compilar Você Mesmo

### Pré-requisitos

- Python 3.8+ com pip
- Git (opcional)

### Passos

1. **Clone o repositório** (ou baixe o ZIP)
   ```cmd
   git clone https://github.com/jairomr/xournal-pen.git
   cd xournal-pen
   ```

2. **Crie ambiente virtual**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale dependências + PyInstaller**
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   ```

4. **Compile com PyInstaller**
   ```cmd
   pyinstaller --onefile ^
     --name xournal-radial-menu-windows ^
     --noconsole ^
     --hidden-import=pkg_resources.py2_warn ^
     --hidden-import=radial_menu ^
     --hidden-import=stylus_handler ^
     --hidden-import=xournal_controller ^
     --hidden-import=_version ^
     --paths=src ^
     src\main.py
   ```

5. **Executável gerado em:**
   ```
   dist\xournal-radial-menu-windows.exe
   ```

---

## Solução de Problemas

### ❌ "Python não é reconhecido como comando"

**Solução:** Python não está no PATH
1. Reinstale o Python
2. Marque a opção **"Add Python to PATH"**
3. Ou adicione manualmente:
   - `C:\Users\SeuUsuario\AppData\Local\Programs\Python\Python311\`
   - `C:\Users\SeuUsuario\AppData\Local\Programs\Python\Python311\Scripts\`

### ❌ Windows Defender bloqueia o executável

**Solução:** Isso é normal para executáveis não assinados
1. Clique em **"Mais informações"**
2. Clique em **"Executar mesmo assim"**
3. Ou adicione exceção no Windows Defender

### ❌ Menu não abre com botão da stylus

**Soluções:**
1. Teste com **Alt+R** primeiro
2. Verifique se sua stylus tem botão lateral configurado
3. No painel de controle da tablet (Wacom, XP-Pen, Huion):
   - Configure o botão lateral para **"Botão do meio do mouse"** ou **"Botão extra"**

### ❌ "ImportError: DLL load failed"

**Solução:** Faltam bibliotecas do sistema
1. Instale o **Visual C++ Redistributable**:
   - https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Reinicie o computador

### ❌ Aplicação abre mas não detecta stylus

**Solução:**
- Use o atalho **Alt+R** como alternativa
- Ou configure o botão da stylus para simular **Alt+R** no driver

---

## Configuração da Stylus/Mesa Digitalizadora

### Wacom

1. Abra **Wacom Tablet Properties**
2. Selecione sua caneta
3. Configure o **Botão Lateral**:
   - Opção 1: "Botão do meio do mouse"
   - Opção 2: "Keystroke" → Configure para **Alt+R**

### XP-Pen

1. Abra **PenTablet** (software da XP-Pen)
2. Vá em **"Configurações da Caneta"**
3. Configure o **Botão Superior ou Inferior**:
   - Selecione "Teclado"
   - Configure: **Alt+R**

### Huion

1. Abra **HuionTablet**
2. Selecione **"Configurações da Caneta"**
3. Configure o botão:
   - "Teclado" → **Alt+R**

---

## Usando o Menu Radial

### Nível 1 (Centro): Color Picker HSV
- **Clique no centro** para escolher qualquer cor
- Ângulo = Matiz (cor)
- Distância do centro = Saturação (intensidade)

### Nível 2 (Anel Médio): 16 Cores Predefinidas
- Preto, Cinza Escuro, Cinza, Cinza Claro, Branco
- Vermelho, Laranja, Amarelo, Verde Lima, Verde
- Ciano, Azul Claro, Azul, Roxo, Magenta, Rosa

### Nível 3 (Anel Externo): 16 Ferramentas
- ✏ Canetas (fina, média, grossa)
- ▓ Marca-texto
- ⌫ Borracha
- ⬚ Seleção
- ✋ Mão (navegação)
- ± Zoom In/Out
- ↶↷ Desfazer/Refazer
- ◄► Navegação de páginas
- T Texto
- 🖼 Imagem
- 📏 Régua

---

## Desinstalação

### Executável Pré-compilado
1. Delete o arquivo `.exe`
2. Delete o atalho (se criou)
3. Pronto!

### Instalação via Python
1. Delete a pasta do projeto
2. Desative o ambiente virtual: `deactivate`
3. Pronto!

---

## Suporte

**Issues:** https://github.com/jairomr/xournal-pen/issues
**Documentação:** https://github.com/jairomr/xournal-pen/blob/main/README.md

---

**Versão:** v2.1.0
**Compatibilidade:** Windows 7/8/10/11 (64-bit)
