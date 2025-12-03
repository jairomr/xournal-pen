# RadialMenu - Plugin de Menu Radial para Xournal++

Plugin de menu radial (pie menu) otimizado para uso com stylus/mesa digitalizadora.

## 🎯 Características

- **Menu circular intuitivo** com paleta de cores central e ferramentas no anel externo
- **Otimizado para stylus** - Projetado para uso com caneta/mesa digitalizadora
- **Seleção rápida** de cores e ferramentas sem precisar navegar em menus tradicionais
- **8 cores predefinidas** no círculo central
- **8 ferramentas** no anel externo (canetas, borracha, marca-texto, navegação de páginas, etc.)

## ⚠️ Limitação Importante

A API de plugins Lua do Xournal++ **não suporta captura direta de eventos de stylus** (hover, tap, botão lateral).

**Solução implementada:**
- O menu é ativado por **atalho de teclado** (`Alt+R`)
- Você deve **mapear o botão lateral da stylus** para este atalho no driver/sistema operacional

## 📦 Instalação

### Linux

1. **Copie a pasta do plugin** para o diretório de plugins do Xournal++:

```bash
# Criar diretório de plugins se não existir
mkdir -p ~/.local/share/xournalpp/plugins

# Copiar o plugin
cp -r RadialMenu ~/.local/share/xournalpp/plugins/
```

2. **Abra o Xournal++**

3. **Ative o plugin:**
   - Vá em `Editar → Preferências → Plugins`
   - Marque a caixa `RadialMenu`
   - Clique em `OK`

4. **Reinicie o Xournal++**

### Windows

1. Copie a pasta `RadialMenu` para:
   ```
   C:\Users\<seu-usuario>\AppData\Local\xournalpp\plugins\
   ```

2. Siga os passos 2-4 da instalação Linux

## ⚙️ Configuração da Stylus

Para usar o plugin com o botão lateral da caneta:

### Linux (Wacom, XP-Pen, Huion, etc.)

#### Método 1: xsetwacom (Wacom)

```bash
# Listar dispositivos
xsetwacom list devices

# Exemplo de saída:
# Wacom Intuos PT S Pen stylus    id: 12  type: STYLUS

# Mapear botão 2 (lateral) para Alt+R
xsetwacom set "Wacom Intuos PT S Pen stylus" Button 2 "key alt r"

# Mapear botão 3 (outro botão lateral, se houver)
xsetwacom set "Wacom Intuos PT S Pen stylus" Button 3 "key alt r"
```

Para tornar permanente, adicione ao `~/.bashrc` ou `~/.profile`:

```bash
# No final do arquivo
xsetwacom set "Wacom Intuos PT S Pen stylus" Button 2 "key alt r"
```

#### Método 2: Digimend/Generic Tablets (XP-Pen, Huion)

Use `xbindkeys`:

```bash
# Instalar xbindkeys
sudo apt install xbindkeys

# Criar arquivo de configuração
xbindkeys --defaults > ~/.xbindkeysrc

# Editar ~/.xbindkeysrc e adicionar:
"xte 'keydown Alt_L' 'key r' 'keyup Alt_L'"
  b:10

# Recarregar configuração
xbindkeys -p
```

#### Método 3: Interface Gráfica (KDE)

1. `Configurações do Sistema → Entrada de Dispositivos → Tablet Gráfica`
2. Selecione sua caneta
3. Na aba `Botões`, mapeie o botão lateral para `Alt+R`

### Windows

#### Método 1: Software do Fabricante

**Wacom:**
1. Abra `Wacom Tablet Properties`
2. Selecione sua caneta
3. Clique no botão lateral
4. Escolha `Keystroke` → `Alt+R`

**XP-Pen / Huion:**
1. Abra o software da tablet (PenTablet/HuionTablet)
2. Vá em configurações da caneta
3. Mapeie o botão lateral para `Alt+R`

#### Método 2: AutoHotkey (Universal)

Crie um script AHK:

```ahk
; Mapear botão lateral da caneta para Alt+R
Joy1::Send !r
Joy2::Send !r
```

## 🎨 Uso do Plugin

### Atalhos de Teclado

- **`Alt+R`** - Abre/fecha o menu radial (toggle)
- **`Ctrl+Alt+R`** - Abre o menu (teste)

### Workflow com Stylus

1. **Pressione o botão lateral da caneta** (mapeado para Alt+R)
   - O menu radial aparece na tela

2. **Para fechar sem selecionar:**
   - Pressione o botão lateral novamente

3. **Para selecionar uma opção:**
   - **(Implementação atual)** Use as funções de console (veja abaixo)
   - **(Implementação futura)** Simplesmente toque na fatia desejada

### Funções do Console (Workaround)

Como a API não captura toques em tempo real, você pode usar o console Lua:

```lua
-- Abrir menu
openRadialMenu()

-- Selecionar cor (1-8)
selectColor(1)  -- Preto
selectColor(2)  -- Azul
selectColor(3)  -- Vermelho
-- ... e assim por diante

-- Selecionar ferramenta (1-8)
selectTool(1)   -- Caneta Fina
selectTool(2)   -- Caneta Média
selectTool(3)   -- Caneta Grossa
selectTool(4)   -- Marca-Texto
selectTool(5)   -- Borracha
selectTool(6)   -- Seleção
selectTool(7)   -- Página Anterior
selectTool(8)   -- Próxima Página

-- Fechar menu
closeRadialMenu()
```

## 🎨 Paleta de Cores

O círculo central contém 8 cores:

1. **Preto** (#000000)
2. **Azul** (#3333cc)
3. **Vermelho** (#ff0000)
4. **Verde** (#00c000)
5. **Laranja** (#ff7f00)
6. **Amarelo** (#ffff00)
7. **Magenta** (#ff00ff)
8. **Cinza** (#808080)

## 🛠️ Ferramentas do Anel Externo

O anel externo contém 8 ferramentas:

1. **Caneta Fina** - Muda para caneta com espessura fina
2. **Caneta Média** - Muda para caneta com espessura média
3. **Caneta Grossa** - Muda para caneta com espessura grossa
4. **Marca-Texto** - Muda para marca-texto
5. **Borracha** - Muda para ferramenta de borracha
6. **Seleção** - Muda para ferramenta de seleção retangular
7. **Página Anterior** - Navega para página anterior
8. **Próxima Página** - Navega para próxima página

## ⚙️ Personalização

Você pode editar o arquivo `main.lua` para customizar:

### Adicionar/Remover Cores

Edite a tabela `ColorPalette`:

```lua
ColorPalette = {
    {name = "Sua Cor", color = 0xRRGGBB},
    -- ... mais cores
}
```

### Adicionar/Remover Ferramentas

Edite a tabela `ToolRing`:

```lua
ToolRing = {
    {
        name = "Nome da Ferramenta",
        action = function()
            app.uiAction({["action"] = "ACTION_NOME_DA_ACAO"})
        end
    },
    -- ... mais ferramentas
}
```

### Ajustar Tamanhos

No início de `main.lua`:

```lua
MenuState = {
    innerRadius = 40,  -- Raio do círculo de cores
    outerRadius = 120, -- Raio do anel de ferramentas
    -- ...
}
```

## 🔧 Solução de Problemas

### Plugin não aparece na lista

- Verifique se a pasta está no local correto
- Certifique-se que os arquivos `plugin.ini` e `main.lua` existem
- Reinicie o Xournal++

### Erro ao ativar o plugin

- Abra o Xournal++ no terminal para ver mensagens de erro:
  ```bash
  xournalpp
  ```
- Verifique a sintaxe do Lua no `main.lua`

### Atalho não funciona

- Verifique se não há conflito com outros atalhos
- Tente um atalho diferente editando `plugin.ini`

### Botão da stylus não abre o menu

- Verifique o mapeamento do botão no driver/sistema
- Teste o atalho `Alt+R` no teclado primeiro
- Use `xev` (Linux) ou ferramentas de teste para verificar se o botão envia eventos

## 🚀 Desenvolvimento Futuro

### Implementação Completa com C++ (Patch)

Para suporte COMPLETO a eventos de stylus (hover, tap, botão), seria necessário:

1. Modificar o código-fonte C++ do Xournal++
2. Adicionar hooks no `AbstractInputHandler`
3. Expor eventos de stylus para plugins Lua

Um patch C++ de exemplo está disponível em `cpp-patch/` (se incluído).

### Funcionalidades Planejadas

- [ ] Detecção automática de posição do cursor da stylus
- [ ] Hover highlighting em tempo real
- [ ] Duplo-toque para abrir menu (alternativa ao botão lateral)
- [ ] Animações de abertura/fechamento
- [ ] Gestos de radial (circular motion)
- [ ] Múltiplas paletas de cores configuráveis
- [ ] Histórico de cores recentes
- [ ] Ferramentas favoritas customizáveis

## 📄 Licença

Este plugin é fornecido "como está", sem garantias. Sinta-se livre para modificar e distribuir.

## 🤝 Contribuições

Contribuições são bem-vindas! Se você melhorar o plugin:

1. Teste suas mudanças
2. Documente as modificações
3. Compartilhe com a comunidade

## 📚 Recursos

- [Documentação de Plugins do Xournal++](https://xournalpp.github.io/guide/plugins/plugins/)
- [Repositório do Xournal++](https://github.com/xournalpp/xournalpp)
- [API Lua do Xournal++](https://github.com/xournalpp/xournalpp/blob/master/plugins/luapi_application.def.lua)

## ❓ FAQ

**P: Por que o menu não responde aos toques da caneta automaticamente?**

R: A API de plugins Lua não tem acesso a eventos de stylus em tempo real. É uma limitação da arquitetura atual do Xournal++. O workaround é usar atalhos de teclado mapeados no botão da caneta.

**P: Posso ter detecção de hover real?**

R: Não com a API Lua atual. Seria necessário um patch C++ (veja seção "Desenvolvimento Futuro").

**P: Como adiciono mais cores/ferramentas?**

R: Edite as tabelas `ColorPalette` e `ToolRing` no arquivo `main.lua`. O plugin recalcula automaticamente os ângulos.

**P: O menu fica permanente na página?**

R: Sim, atualmente o menu é desenhado como strokes normais. Use `Ctrl+Z` ou a função de fechar para remover. Uma versão com overlay não-destrutivo requer modificação C++.

**P: Funciona no Android/iOS?**

R: Xournal++ não tem versões oficiais para mobile. Este plugin é para desktop (Linux/Windows/Mac).

---

**Desenvolvido para a comunidade Xournal++**
*Melhorando a experiência com mesa digitalizadora* ✍️
