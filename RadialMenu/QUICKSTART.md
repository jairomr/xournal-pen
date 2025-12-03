# 🚀 Guia de Início Rápido - RadialMenu Plugin

## Instalação em 3 Passos (Linux)

### 1️⃣ Instalar o Plugin

```bash
# Executar script de instalação automática
cd RadialMenu
./INSTALL.sh
```

**OU manualmente:**

```bash
# Copiar plugin
mkdir -p ~/.local/share/xournalpp/plugins
cp -r RadialMenu ~/.local/share/xournalpp/plugins/
```

### 2️⃣ Ativar no Xournal++

1. Abra o Xournal++
2. Menu: `Editar → Preferências → Plugins`
3. Marque ☑️ `RadialMenu`
4. Clique `OK`
5. **Reinicie o Xournal++**

### 3️⃣ Mapear Botão da Stylus (Opcional mas Recomendado)

#### Wacom:

```bash
# Ver dispositivos
xsetwacom list devices

# Mapear botão lateral para Alt+R (substitua "Nome do Dispositivo")
xsetwacom set "Wacom Intuos PT S Pen stylus" Button 2 "key alt r"
```

#### XP-Pen/Huion:

Abra o software da tablet (PenTablet/HuionTablet) e mapeie o botão lateral para `Alt+R`.

---

## 🎯 Como Usar

### Abrir o Menu

- **Teclado:** Pressione `Alt+R`
- **Stylus:** Pressione o botão lateral (se mapeado)

### Fechar o Menu

- Pressione `Alt+R` novamente

### Selecionar Opção

**Atualmente (via console Lua):**

```lua
-- Abrir menu
openRadialMenu()

-- Selecionar cor (1-8)
selectColor(1)  -- Preto
selectColor(2)  -- Azul
selectColor(3)  -- Vermelho

-- Selecionar ferramenta (1-8)
selectTool(1)  -- Caneta Fina
selectTool(4)  -- Marca-Texto
selectTool(5)  -- Borracha
selectTool(8)  -- Próxima Página
```

---

## 🎨 Referência Rápida

### Cores (Círculo Central)

| Posição | Cor       | Hex       |
|---------|-----------|-----------|
| 1       | Preto     | #000000   |
| 2       | Azul      | #3333cc   |
| 3       | Vermelho  | #ff0000   |
| 4       | Verde     | #00c000   |
| 5       | Laranja   | #ff7f00   |
| 6       | Amarelo   | #ffff00   |
| 7       | Magenta   | #ff00ff   |
| 8       | Cinza     | #808080   |

### Ferramentas (Anel Externo)

| Posição | Ferramenta          |
|---------|---------------------|
| 1       | Caneta Fina         |
| 2       | Caneta Média        |
| 3       | Caneta Grossa       |
| 4       | Marca-Texto         |
| 5       | Borracha            |
| 6       | Seleção             |
| 7       | Página Anterior     |
| 8       | Próxima Página      |

---

## ⚙️ Personalização Rápida

Edite `~/.local/share/xournalpp/plugins/RadialMenu/main.lua`:

### Mudar Cores:

```lua
ColorPalette = {
    {name = "Sua Cor", color = 0xRRGGBB},
    -- ... adicione mais cores
}
```

### Mudar Ferramentas:

```lua
ToolRing = {
    {
        name = "Minha Ferramenta",
        action = function()
            app.uiAction({["action"] = "ACTION_NOME"})
        end
    },
    -- ... adicione mais ferramentas
}
```

### Ajustar Tamanho:

```lua
MenuState = {
    innerRadius = 40,   -- Tamanho do círculo de cores
    outerRadius = 120,  -- Tamanho do anel de ferramentas
}
```

---

## 🆘 Problemas Comuns

### Plugin não aparece na lista

```bash
# Verificar localização
ls ~/.local/share/xournalpp/plugins/RadialMenu/

# Deve mostrar: plugin.ini, main.lua
```

### Atalho não funciona

1. Teste no teclado primeiro: `Alt+R`
2. Se funcionar, problema está no mapeamento da stylus
3. Veja `STYLUS_CONFIG.md` para instruções detalhadas

### Menu não desenha corretamente

Verifique se o Lua 5.3+ está instalado:

```bash
lua -v
```

---

## 📚 Documentação Completa

- **README.md** - Documentação completa
- **STYLUS_CONFIG.md** - Guia de configuração de stylus
- **cpp-patch/** - Patch C++ opcional (avançado)

---

## ✅ Checklist de Instalação

- [ ] Plugin copiado para `~/.local/share/xournalpp/plugins/RadialMenu/`
- [ ] Plugin ativado em Preferências → Plugins
- [ ] Xournal++ reiniciado
- [ ] Atalho `Alt+R` funciona no teclado
- [ ] Botão da stylus mapeado para `Alt+R` (opcional)
- [ ] Menu aparece ao pressionar atalho

---

## 🎉 Pronto!

Agora você pode usar o menu radial com sua stylus!

**Dica:** Pratique abrindo e fechando o menu algumas vezes para pegar o jeito. Em breve você estará trocando cores e ferramentas sem olhar! 🎨✍️
