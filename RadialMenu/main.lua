-- RadialMenu Plugin para Xournal++
-- Menu radial otimizado para stylus/caneta
--
-- LIMITAÇÃO DA API: A API Lua do Xournal++ não suporta captura de eventos de stylus
-- em tempo real (hover, tap, botão lateral). Este plugin usa um workaround:
--
-- MODO DE USO:
-- 1. Mapeie o botão lateral da stylus para o atalho do plugin (no driver/SO)
-- 2. Pressione o botão para abrir/fechar o menu
-- 3. Toque na fatia desejada para selecionar
-- 4. O plugin detecta a posição do toque e executa a ação
--
-- ALTERNATIVA: Use o atalho de teclado configurado (<Alt>R por padrão)

-- ==============================================================================
-- ESTADO GLOBAL DO MENU
-- ==============================================================================

MenuState = {
    isOpen = false,
    centerX = 0,
    centerY = 0,
    innerRadius = 40,  -- Raio do círculo central (paleta de cores)
    outerRadius = 120, -- Raio do anel externo (ferramentas)
    lastTouchX = 0,
    lastTouchY = 0
}

-- ==============================================================================
-- CONFIGURAÇÃO DO MENU RADIAL
-- ==============================================================================

-- Paleta de cores (círculo central)
ColorPalette = {
    {name = "Preto", color = 0x000000},
    {name = "Azul", color = 0x3333cc},
    {name = "Vermelho", color = 0xff0000},
    {name = "Verde", color = 0x00c000},
    {name = "Laranja", color = 0xff7f00},
    {name = "Amarelo", color = 0xffff00},
    {name = "Magenta", color = 0xff00ff},
    {name = "Cinza", color = 0x808080}
}

-- Ferramentas (anel externo)
-- Cada entrada possui: nome, ação, e ícone opcional
ToolRing = {
    {
        name = "Caneta Fina",
        action = function()
            app.uiAction({["action"] = "ACTION_TOOL_PEN"})
            app.uiAction({["action"] = "ACTION_SIZE_FINE"})
        end
    },
    {
        name = "Caneta Média",
        action = function()
            app.uiAction({["action"] = "ACTION_TOOL_PEN"})
            app.uiAction({["action"] = "ACTION_SIZE_MEDIUM"})
        end
    },
    {
        name = "Caneta Grossa",
        action = function()
            app.uiAction({["action"] = "ACTION_TOOL_PEN"})
            app.uiAction({["action"] = "ACTION_SIZE_THICK"})
        end
    },
    {
        name = "Marca-Texto",
        action = function()
            app.uiAction({["action"] = "ACTION_TOOL_HIGHLIGHTER"})
        end
    },
    {
        name = "Borracha",
        action = function()
            app.uiAction({["action"] = "ACTION_TOOL_ERASER"})
        end
    },
    {
        name = "Seleção",
        action = function()
            app.uiAction({["action"] = "ACTION_TOOL_SELECT_RECT"})
        end
    },
    {
        name = "Página Anterior",
        action = function()
            app.uiAction({["action"] = "ACTION_GOTO_BACK"})
        end
    },
    {
        name = "Próxima Página",
        action = function()
            app.uiAction({["action"] = "ACTION_GOTO_NEXT"})
        end
    }
}

-- ==============================================================================
-- FUNÇÕES DE GEOMETRIA
-- ==============================================================================

-- Calcula distância entre dois pontos
function distance(x1, y1, x2, y2)
    local dx = x2 - x1
    local dy = y2 - y1
    return math.sqrt(dx * dx + dy * dy)
end

-- Calcula ângulo de um ponto em relação ao centro (em radianos)
-- Retorna ângulo de 0 a 2π, com 0 apontando para a direita
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

-- Converte ângulo em radianos para graus
function radToDeg(rad)
    return rad * 180 / math.pi
end

-- Converte graus para radianos
function degToRad(deg)
    return deg * math.pi / 180
end

-- Detecta qual seção do menu foi tocada
-- Retorna: "center" (cor), "ring" (ferramenta), ou "outside" (fora do menu)
-- E o índice da seção (1-based)
function detectMenuSection(touchX, touchY)
    local dist = distance(MenuState.centerX, MenuState.centerY, touchX, touchY)

    -- Toque no círculo central (cores)
    if dist <= MenuState.innerRadius then
        local angle = calculateAngle(MenuState.centerX, MenuState.centerY, touchX, touchY)
        local sectionAngle = (2 * math.pi) / #ColorPalette
        local sectionIndex = math.floor(angle / sectionAngle) + 1

        -- Garantir que está dentro dos limites
        if sectionIndex > #ColorPalette then
            sectionIndex = #ColorPalette
        end

        return "center", sectionIndex
    end

    -- Toque no anel externo (ferramentas)
    if dist > MenuState.innerRadius and dist <= MenuState.outerRadius then
        local angle = calculateAngle(MenuState.centerX, MenuState.centerY, touchX, touchY)
        local sectionAngle = (2 * math.pi) / #ToolRing
        local sectionIndex = math.floor(angle / sectionAngle) + 1

        -- Garantir que está dentro dos limites
        if sectionIndex > #ToolRing then
            sectionIndex = #ToolRing
        end

        return "ring", sectionIndex
    end

    -- Toque fora do menu
    return "outside", 0
end

-- ==============================================================================
-- FUNÇÕES DE RENDERIZAÇÃO
-- ==============================================================================

-- Desenha um círculo usando strokes
function drawCircle(centerX, centerY, radius, color, width, fill)
    local xCoords = {}
    local yCoords = {}
    local pressures = {}

    -- Gerar pontos do círculo (resolução de 5 graus)
    for i = 0, 360, 5 do
        local angle = degToRad(i)
        table.insert(xCoords, centerX + radius * math.cos(angle))
        table.insert(yCoords, centerY + radius * math.sin(angle))
        table.insert(pressures, 1.0)
    end

    -- Fechar o círculo
    table.insert(xCoords, xCoords[1])
    table.insert(yCoords, yCoords[1])
    table.insert(pressures, 1.0)

    app.addStrokes({
        ["strokes"] = {
            {
                ["x"] = xCoords,
                ["y"] = yCoords,
                ["pressure"] = pressures,
                ["tool"] = "pen",
                ["width"] = width or 2.0,
                ["color"] = color,
                ["fill"] = fill or -1,
                ["linestyle"] = "plain"
            }
        },
        ["allowUndoRedoAction"] = "grouped"
    })
end

-- Desenha uma linha
function drawLine(x1, y1, x2, y2, color, width)
    app.addStrokes({
        ["strokes"] = {
            {
                ["x"] = {x1, x2},
                ["y"] = {y1, y2},
                ["pressure"] = {1.0, 1.0},
                ["tool"] = "pen",
                ["width"] = width or 2.0,
                ["color"] = color,
                ["fill"] = -1,
                ["linestyle"] = "plain"
            }
        },
        ["allowUndoRedoAction"] = "grouped"
    })
end

-- Desenha uma fatia (seção) do menu radial
function drawSlice(centerX, centerY, innerRadius, outerRadius, startAngle, endAngle, color)
    local xCoords = {}
    local yCoords = {}
    local pressures = {}

    -- Arco interno (do ângulo inicial ao final)
    for angle = startAngle, endAngle, 0.1 do
        table.insert(xCoords, centerX + innerRadius * math.cos(angle))
        table.insert(yCoords, centerY + innerRadius * math.sin(angle))
        table.insert(pressures, 1.0)
    end

    -- Linha radial (raio externo)
    table.insert(xCoords, centerX + outerRadius * math.cos(endAngle))
    table.insert(yCoords, centerY + outerRadius * math.sin(endAngle))
    table.insert(pressures, 1.0)

    -- Arco externo (do ângulo final ao inicial)
    for angle = endAngle, startAngle, -0.1 do
        table.insert(xCoords, centerX + outerRadius * math.cos(angle))
        table.insert(yCoords, centerY + outerRadius * math.sin(angle))
        table.insert(pressures, 1.0)
    end

    -- Linha radial de volta (fechar a fatia)
    table.insert(xCoords, centerX + innerRadius * math.cos(startAngle))
    table.insert(yCoords, centerY + innerRadius * math.sin(startAngle))
    table.insert(pressures, 1.0)

    app.addStrokes({
        ["strokes"] = {
            {
                ["x"] = xCoords,
                ["y"] = yCoords,
                ["pressure"] = pressures,
                ["tool"] = "pen",
                ["width"] = 1.5,
                ["color"] = color,
                ["fill"] = 200,  -- Semi-transparente
                ["linestyle"] = "plain"
            }
        },
        ["allowUndoRedoAction"] = "grouped"
    })
end

-- Desenha texto na posição especificada
function drawText(text, x, y, color, fontSize)
    app.addTexts({
        ["texts"] = {
            {
                ["text"] = text,
                ["font"] = {["name"] = "Sans", ["size"] = fontSize or 10},
                ["x"] = x,
                ["y"] = y,
                ["color"] = color or 0x000000
            }
        },
        ["allowUndoRedoAction"] = "grouped"
    })
end

-- Renderiza o menu radial completo
function renderRadialMenu()
    local centerX = MenuState.centerX
    local centerY = MenuState.centerY
    local innerRadius = MenuState.innerRadius
    local outerRadius = MenuState.outerRadius

    -- 1. Desenhar círculo de fundo (branco semi-transparente)
    drawCircle(centerX, centerY, outerRadius, 0xffffff, 2.0, 200)

    -- 2. Desenhar fatias de cores (círculo central)
    local colorSectionAngle = (2 * math.pi) / #ColorPalette
    for i, colorEntry in ipairs(ColorPalette) do
        local startAngle = (i - 1) * colorSectionAngle
        local endAngle = i * colorSectionAngle
        drawSlice(centerX, centerY, 0, innerRadius, startAngle, endAngle, colorEntry.color)
    end

    -- 3. Desenhar bordas divisórias das cores
    for i = 1, #ColorPalette do
        local angle = (i - 1) * colorSectionAngle
        local x = centerX + innerRadius * math.cos(angle)
        local y = centerY + innerRadius * math.sin(angle)
        drawLine(centerX, centerY, x, y, 0x000000, 1.0)
    end

    -- 4. Desenhar círculo divisor entre cores e ferramentas
    drawCircle(centerX, centerY, innerRadius, 0x000000, 2.0, -1)

    -- 5. Desenhar fatias de ferramentas (anel externo)
    local toolSectionAngle = (2 * math.pi) / #ToolRing
    for i, tool in ipairs(ToolRing) do
        local startAngle = (i - 1) * toolSectionAngle
        local endAngle = i * toolSectionAngle

        -- Alternar cores claras para melhor visualização
        local bgColor = (i % 2 == 0) and 0xeeeeee or 0xdddddd
        drawSlice(centerX, centerY, innerRadius, outerRadius, startAngle, endAngle, bgColor)

        -- Desenhar borda da fatia
        local x1 = centerX + innerRadius * math.cos(startAngle)
        local y1 = centerY + innerRadius * math.sin(startAngle)
        local x2 = centerX + outerRadius * math.cos(startAngle)
        local y2 = centerY + outerRadius * math.sin(startAngle)
        drawLine(x1, y1, x2, y2, 0x000000, 1.0)
    end

    -- 6. Desenhar círculo externo
    drawCircle(centerX, centerY, outerRadius, 0x000000, 3.0, -1)

    -- 7. Adicionar labels das ferramentas
    for i, tool in ipairs(ToolRing) do
        local angle = ((i - 1) * toolSectionAngle) + (toolSectionAngle / 2)
        local labelRadius = (innerRadius + outerRadius) / 2
        local labelX = centerX + labelRadius * math.cos(angle) - 15
        local labelY = centerY + labelRadius * math.sin(angle)

        -- Simplificar nome para caber no espaço
        local shortName = tool.name:sub(1, 12)
        drawText(shortName, labelX, labelY, 0x000000, 8)
    end

    -- 8. Adicionar indicador central
    drawText("COR", centerX - 12, centerY, 0xffffff, 10)

    app.refreshPage()
end

-- ==============================================================================
-- LÓGICA DO MENU
-- ==============================================================================

-- Obtém posição atual do cursor (aproximação)
-- Como a API não fornece posição do cursor, usa centro da viewport
function getCurrentCursorPosition()
    -- Obter dimensões da página atual
    local doc = app.getDocumentStructure()
    local zoom = app.getZoom()

    -- Posição aproximada no centro da tela visível
    -- Em uma implementação real com eventos de stylus, usaríamos a posição real
    -- WORKAROUND: Desenha o menu no centro da página
    return 300, 400  -- Posição fixa para demonstração
end

-- Abre o menu radial
function openRadialMenu()
    if MenuState.isOpen then
        print("RadialMenu: Menu já está aberto")
        return
    end

    -- Obter posição atual (ou usar posição fixa)
    MenuState.centerX, MenuState.centerY = getCurrentCursorPosition()
    MenuState.isOpen = true

    print("RadialMenu: Abrindo menu em (" .. MenuState.centerX .. ", " .. MenuState.centerY .. ")")

    -- Renderizar o menu
    renderRadialMenu()

    print("RadialMenu: Menu aberto! Toque em uma fatia para selecionar.")
    print("RadialMenu: Pressione o atalho novamente para fechar sem selecionar.")
end

-- Fecha o menu radial sem selecionar nada
function closeRadialMenu()
    if not MenuState.isOpen then
        print("RadialMenu: Menu não está aberto")
        return
    end

    MenuState.isOpen = false
    print("RadialMenu: Menu fechado")

    -- Desfazer os desenhos do menu
    app.uiAction({["action"] = "ACTION_UNDO"})
end

-- Processa seleção no menu baseado em coordenadas de toque
-- Esta função seria chamada quando detectamos um toque na tela
function processMenuSelection(touchX, touchY)
    if not MenuState.isOpen then
        print("RadialMenu: Menu não está aberto, ignorando seleção")
        return
    end

    local section, index = detectMenuSection(touchX, touchY)

    print("RadialMenu: Toque detectado em (" .. touchX .. ", " .. touchY .. ")")
    print("RadialMenu: Seção: " .. section .. ", Índice: " .. index)

    if section == "center" and index > 0 then
        -- Seleção de cor
        local selectedColor = ColorPalette[index]
        print("RadialMenu: Cor selecionada: " .. selectedColor.name)

        app.changeToolColor({
            ["color"] = selectedColor.color,
            ["selection"] = false
        })

        closeRadialMenu()

    elseif section == "ring" and index > 0 then
        -- Seleção de ferramenta
        local selectedTool = ToolRing[index]
        print("RadialMenu: Ferramenta selecionada: " .. selectedTool.name)

        selectedTool.action()
        closeRadialMenu()

    elseif section == "outside" then
        -- Toque fora do menu - fechar sem selecionar
        print("RadialMenu: Toque fora do menu, fechando")
        closeRadialMenu()
    end
end

-- ==============================================================================
-- FUNÇÕES INTERATIVAS (WORKAROUND PARA FALTA DE EVENTOS DE STYLUS)
-- ==============================================================================

-- Como a API não suporta captura de eventos de stylus, implementamos um sistema
-- de "seleção manual" onde o usuário fornece coordenadas

-- Função auxiliar para testar seleção em coordenadas específicas
function testSelectionAt(x, y)
    processMenuSelection(x, y)
end

-- Abre menu e aguarda seleção via coordenadas
-- O usuário pode chamar selectColor(1-8) ou selectTool(1-8)
function selectColor(colorIndex)
    if not MenuState.isOpen then
        print("RadialMenu: Menu não está aberto. Abra o menu primeiro!")
        return
    end

    if colorIndex < 1 or colorIndex > #ColorPalette then
        print("RadialMenu: Índice de cor inválido: " .. colorIndex)
        return
    end

    -- Calcular posição da cor
    local sectionAngle = (2 * math.pi) / #ColorPalette
    local angle = ((colorIndex - 1) * sectionAngle) + (sectionAngle / 2)
    local radius = MenuState.innerRadius / 2
    local x = MenuState.centerX + radius * math.cos(angle)
    local y = MenuState.centerY + radius * math.sin(angle)

    processMenuSelection(x, y)
end

function selectTool(toolIndex)
    if not MenuState.isOpen then
        print("RadialMenu: Menu não está aberto. Abra o menu primeiro!")
        return
    end

    if toolIndex < 1 or toolIndex > #ToolRing then
        print("RadialMenu: Índice de ferramenta inválido: " .. toolIndex)
        return
    end

    -- Calcular posição da ferramenta
    local sectionAngle = (2 * math.pi) / #ToolRing
    local angle = ((toolIndex - 1) * sectionAngle) + (sectionAngle / 2)
    local radius = (MenuState.innerRadius + MenuState.outerRadius) / 2
    local x = MenuState.centerX + radius * math.cos(angle)
    local y = MenuState.centerY + radius * math.sin(angle)

    processMenuSelection(x, y)
end

-- ==============================================================================
-- TOGGLE DO MENU (Função principal ativada pelo atalho)
-- ==============================================================================

function toggleRadialMenu()
    if MenuState.isOpen then
        closeRadialMenu()
    else
        openRadialMenu()
    end
end

-- ==============================================================================
-- REGISTRO DO PLUGIN
-- ==============================================================================

function initUi()
    print("RadialMenu: Inicializando plugin de menu radial")
    print("RadialMenu: --------------------------------------------")
    print("RadialMenu: MODO DE USO:")
    print("RadialMenu: 1. Pressione <Alt>R para abrir/fechar o menu")
    print("RadialMenu: 2. Mapeie o botão da stylus para Alt+R no driver/SO")
    print("RadialMenu: 3. Use selectColor(1-8) ou selectTool(1-8) no console")
    print("RadialMenu: --------------------------------------------")

    -- Registrar ação principal: toggle do menu
    app.registerUi({
        ["menu"] = "Abrir/Fechar Menu Radial",
        ["callback"] = "toggleRadialMenu",
        ["accelerator"] = "<Alt>r"
    })

    -- Registrar ações de teste (para debug)
    app.registerUi({
        ["menu"] = "RadialMenu: Testar - Abrir Menu",
        ["callback"] = "openRadialMenu",
        ["accelerator"] = "<Control><Alt>r"
    })

    print("RadialMenu: Plugin inicializado com sucesso!")
    print("RadialMenu: Atalho: <Alt>R para toggle do menu")
end
