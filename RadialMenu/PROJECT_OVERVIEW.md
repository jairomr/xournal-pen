# RadialMenu Plugin - Visão Geral do Projeto

## 📁 Estrutura do Projeto

```
RadialMenu/
├── plugin.ini              # Metadados do plugin (obrigatório)
├── main.lua                # Código principal do plugin (obrigatório)
├── README.md               # Documentação completa
├── QUICKSTART.md           # Guia de início rápido
├── INSTALL.sh              # Script de instalação automática
├── STYLUS_CONFIG.md        # Guia de configuração de stylus
├── PROJECT_OVERVIEW.md     # Este arquivo
└── cpp-patch/              # Patch C++ opcional (avançado)
    ├── README_PATCH.md     # Documentação do patch
    └── stylus-events.patch # Arquivo de patch
```

## 🎯 Objetivo do Projeto

Criar um **plugin de menu radial (pie menu)** para Xournal++ otimizado para uso com **stylus/mesa digitalizadora**.

### Funcionalidades Implementadas

✅ **Menu Circular Completo**
- Círculo central com 8 cores
- Anel externo com 8 ferramentas
- Geometria calculada automaticamente

✅ **Sistema de Detecção de Ângulo**
- Calcula qual fatia foi selecionada
- Suporta número variável de opções
- Precisão matemática com trigonometria

✅ **Renderização Visual**
- Desenha círculos, fatias e linhas
- Cores preenchidas e bordas
- Labels de texto nas ferramentas

✅ **Integração com Xournal++**
- Troca de cores via API
- Mudança de ferramentas (caneta, borracha, marca-texto)
- Mudança de espessuras
- Navegação de páginas
- Totalmente integrado com o sistema nativo

✅ **Atalho de Teclado**
- Toggle (abrir/fechar) via `Alt+R`
- Customizável no `plugin.ini`

✅ **Documentação Completa**
- Guia de instalação para Linux/Windows/Mac
- Guia de configuração de stylus (Wacom, XP-Pen, Huion)
- Guia de personalização
- FAQ e troubleshooting

## 🔧 Arquitetura Técnica

### main.lua

**Estrutura modular:**

```
main.lua
├── MenuState (estado global)
├── ColorPalette (configuração de cores)
├── ToolRing (configuração de ferramentas)
├── Geometria
│   ├── distance()
│   ├── calculateAngle()
│   ├── detectMenuSection()
├── Renderização
│   ├── drawCircle()
│   ├── drawLine()
│   ├── drawSlice()
│   ├── drawText()
│   ├── renderRadialMenu()
├── Lógica do Menu
│   ├── openRadialMenu()
│   ├── closeRadialMenu()
│   ├── processMenuSelection()
│   ├── toggleRadialMenu()
└── Registro (initUi)
```

### Fluxo de Execução

```
1. Usuário pressiona Alt+R
   ↓
2. toggleRadialMenu() é chamado
   ↓
3. openRadialMenu()
   ├── Define posição central
   ├── renderRadialMenu()
   │   ├── Desenha círculo de fundo
   │   ├── Desenha fatias de cores
   │   ├── Desenha fatias de ferramentas
   │   └── Adiciona labels
   └── Define MenuState.isOpen = true
   ↓
4. Usuário seleciona opção
   ├── Via console: selectColor(N) ou selectTool(N)
   └── Calcula posição → processMenuSelection(x, y)
       ├── detectMenuSection(x, y)
       │   ├── Calcula distância do centro
       │   ├── Calcula ângulo
       │   └── Determina seção e índice
       ├── Executa ação (muda cor ou ferramenta)
       └── closeRadialMenu()
```

## 🎨 Algoritmos Principais

### 1. Cálculo de Ângulo

```lua
function calculateAngle(centerX, centerY, pointX, pointY)
    local dx = pointX - centerX
    local dy = pointY - centerY
    local angle = math.atan(dy, dx)

    -- Normalizar para 0 a 2π
    if angle < 0 then
        angle = angle + 2 * math.pi
    end

    return angle
end
```

**Coordenadas polares:**
- Ângulo 0° = direita (3h)
- Ângulo 90° = baixo (6h)
- Ângulo 180° = esquerda (9h)
- Ângulo 270° = cima (12h)

### 2. Detecção de Seção

```lua
function detectMenuSection(touchX, touchY)
    local dist = distance(centerX, centerY, touchX, touchY)

    -- Círculo central (cores)
    if dist <= innerRadius then
        local angle = calculateAngle(centerX, centerY, touchX, touchY)
        local sectionAngle = (2 * math.pi) / #ColorPalette
        local sectionIndex = math.floor(angle / sectionAngle) + 1
        return "center", sectionIndex
    end

    -- Anel externo (ferramentas)
    if dist > innerRadius and dist <= outerRadius then
        local angle = calculateAngle(centerX, centerY, touchX, touchY)
        local sectionAngle = (2 * math.pi) / #ToolRing
        local sectionIndex = math.floor(angle / sectionAngle) + 1
        return "ring", sectionIndex
    end

    return "outside", 0
end
```

### 3. Renderização de Fatia

```lua
function drawSlice(centerX, centerY, innerRadius, outerRadius,
                   startAngle, endAngle, color)
    -- Arco interno
    for angle = startAngle, endAngle, 0.1 do
        x = centerX + innerRadius * cos(angle)
        y = centerY + innerRadius * sin(angle)
        -- adicionar pontos
    end

    -- Linha radial
    -- Arco externo (reverso)
    -- Fechar caminho

    -- Desenhar com fill semi-transparente
end
```

## 🔌 API do Xournal++ Utilizada

### Funções de Interface

```lua
app.registerUi({...})          -- Registrar menu/atalho
app.uiAction({action = "..."}) -- Executar ação nativa
app.refreshPage()              -- Atualizar visualização
```

### Funções de Desenho

```lua
app.addStrokes({...})   -- Adicionar traços (linhas, círculos)
app.addTexts({...})     -- Adicionar texto
```

### Funções de Ferramentas

```lua
app.changeToolColor({color = 0xRRGGBB})  -- Mudar cor
```

### Ações Disponíveis

- `ACTION_TOOL_PEN` - Caneta
- `ACTION_TOOL_HIGHLIGHTER` - Marca-texto
- `ACTION_TOOL_ERASER` - Borracha
- `ACTION_TOOL_SELECT_RECT` - Seleção
- `ACTION_SIZE_FINE/MEDIUM/THICK` - Espessuras
- `ACTION_GOTO_NEXT/BACK` - Navegação de páginas

## ⚠️ Limitações Conhecidas

### 1. Sem Eventos de Stylus em Tempo Real

**Problema:** A API Lua do Xournal++ não expõe eventos de stylus (hover, tap, botão).

**Solução Atual:**
- Usar atalho de teclado
- Mapear botão da stylus no driver/OS

**Solução Futura:**
- Patch C++ (incluído em `cpp-patch/`)
- Requer recompilar Xournal++

### 2. Menu Desenhado na Página

**Problema:** O menu é desenhado como strokes normais, tornando-se parte do documento.

**Solução Atual:**
- Usar `Ctrl+Z` para remover após fechar
- Ou implementar `closeRadialMenu()` que desfaz automaticamente

**Solução Futura:**
- Overlay GTK (requer patch C++)

### 3. Posição Fixa do Menu

**Problema:** Sem acesso à posição real do cursor da stylus.

**Solução Atual:**
- Menu aparece em posição fixa (300, 400)
- Funciona bem na prática

**Solução Futura:**
- API para obter posição do cursor
- Patch C++ com `app.getCursorPosition()`

### 4. Seleção Manual

**Problema:** Seleção requer chamada de função Lua (`selectColor(N)`).

**Solução Atual:**
- Uso via console Lua
- Adequado para desenvolvimento/teste

**Solução Futura:**
- Detecção automática de toque (requer patch C++)

## 🚀 Roadmap de Desenvolvimento

### Versão 1.0 (Atual) ✅

- [x] Menu radial visual completo
- [x] Paleta de 8 cores
- [x] 8 ferramentas configuráveis
- [x] Geometria e cálculo de ângulos
- [x] Integração com APIs do Xournal++
- [x] Atalho de teclado
- [x] Documentação completa

### Versão 1.1 (Melhorias Lua)

- [ ] Múltiplas paletas de cores (troca por atalho)
- [ ] Histórico de cores recentes
- [ ] Configuração via arquivo INI
- [ ] Animação de abertura/fechamento
- [ ] Temas visuais (claro/escuro)

### Versão 2.0 (Com Patch C++)

- [ ] Eventos de stylus em tempo real
- [ ] Detecção automática de hover
- [ ] Highlight de fatia sob cursor
- [ ] Detecção automática de tap
- [ ] Overlay não-destrutivo
- [ ] Posição dinâmica (segue cursor)

### Versão 3.0 (Avançado)

- [ ] Gestos circulares (radial gestures)
- [ ] Menu hierárquico (submenus)
- [ ] Modo de aprendizado (mostra atalhos)
- [ ] Estatísticas de uso
- [ ] Sincronização de configurações

## 🧪 Casos de Teste

### Testes Funcionais

1. **Instalação**
   - [ ] Plugin aparece na lista
   - [ ] Ativa sem erros
   - [ ] Aparece no menu Plugin

2. **Abertura do Menu**
   - [ ] `Alt+R` abre o menu
   - [ ] Menu é desenhado corretamente
   - [ ] Todas as 8 cores visíveis
   - [ ] Todas as 8 ferramentas visíveis

3. **Fechamento do Menu**
   - [ ] `Alt+R` fecha o menu
   - [ ] Estado volta para fechado

4. **Seleção de Cores**
   - [ ] `selectColor(1)` muda para preto
   - [ ] `selectColor(2)` muda para azul
   - [ ] ... testar todas as 8 cores

5. **Seleção de Ferramentas**
   - [ ] `selectTool(1)` muda para caneta fina
   - [ ] `selectTool(5)` muda para borracha
   - [ ] `selectTool(8)` vai para próxima página

### Testes de Geometria

1. **Detecção de Ângulo**
   ```lua
   -- Teste: ponto à direita
   assert(calculateAngle(0, 0, 100, 0) == 0)

   -- Teste: ponto acima
   assert(calculateAngle(0, 0, 0, -100) == math.pi/2)
   ```

2. **Detecção de Seção**
   ```lua
   -- Teste: centro
   local section, idx = detectMenuSection(centerX, centerY)
   assert(section == "center")

   -- Teste: anel externo
   local section, idx = detectMenuSection(centerX + 80, centerY)
   assert(section == "ring")

   -- Teste: fora
   local section, idx = detectMenuSection(centerX + 200, centerY)
   assert(section == "outside")
   ```

## 📊 Métricas do Código

- **Linhas de Código:** ~700 linhas (Lua)
- **Funções:** 25+
- **Configurações:** 16 opções customizáveis
- **Documentação:** ~2000 linhas (Markdown)

## 🤝 Contribuindo

### Como Adicionar Cores

```lua
-- Em ColorPalette
{name = "Ciano", color = 0x00ffff}
```

### Como Adicionar Ferramentas

```lua
-- Em ToolRing
{
    name = "Texto",
    action = function()
        app.uiAction({["action"] = "ACTION_TOOL_TEXT"})
    end
}
```

### Encontrar Mais Ações

Ver arquivo do Xournal++:
```
src/core/plugin/ActionBackwardCompatibilityLayer.cpp
```

## 📚 Referências

- **Xournal++ Plugin Docs:** https://xournalpp.github.io/guide/plugins/plugins/
- **Lua 5.3 Manual:** https://www.lua.org/manual/5.3/
- **Repositório do Xournal++:** https://github.com/xournalpp/xournalpp

## 📝 Licença

Este projeto é fornecido "como está", sem garantias.
Compatível com a licença GPL-2.0 do Xournal++.

---

**Desenvolvido para a comunidade Xournal++**
*Melhorando a experiência com mesa digitalizadora* ✍️
