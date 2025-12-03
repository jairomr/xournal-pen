# Patch C++ para Eventos de Stylus - RadialMenu

## ⚠️ Aviso Importante

Este patch é **OPCIONAL** e **AVANÇADO**. O plugin funciona sem ele usando atalhos de teclado.

**Este patch:**
- Modifica o código-fonte C++ do Xournal++
- Adiciona suporte para captura de eventos de stylus em plugins Lua
- Permite detecção de hover, tap e botões da caneta em tempo real
- **Requer recompilar o Xournal++ do zero**

## 🎯 O que este patch faz

### Sem o patch (estado atual):
```
Caneta/Stylus → [Xournal++ C++] → Plugin Lua (sem eventos)
                      ↓
                 Atalho de teclado → Plugin
```

### Com o patch:
```
Caneta/Stylus → [Xournal++ C++ MODIFICADO] → Plugin Lua
                      ↓                           ↓
                 Eventos de stylus →  hover_event()
                                      tap_event()
                                      button_event()
```

## 📋 Pré-requisitos

### Ferramentas de Build

**Linux (Ubuntu/Debian):**
```bash
sudo apt install \
    build-essential \
    cmake \
    git \
    libgtk-3-dev \
    libpoppler-glib-dev \
    portaudio19-dev \
    libsndfile1-dev \
    libzip-dev \
    liblua5.3-dev \
    libgtksourceview-4-dev \
    gettext \
    libc6-dev \
    libx11-dev \
    libxi-dev
```

**Arch Linux:**
```bash
sudo pacman -S \
    base-devel \
    cmake \
    git \
    gtk3 \
    poppler-glib \
    portaudio \
    libsndfile \
    libzip \
    lua \
    gtksourceview4
```

**Fedora:**
```bash
sudo dnf install \
    gcc-c++ \
    cmake \
    git \
    gtk3-devel \
    poppler-glib-devel \
    portaudio-devel \
    libsndfile-devel \
    libzip-devel \
    lua-devel \
    gtksourceview4-devel
```

### Espaço em Disco
- **Código-fonte:** ~50 MB
- **Build:** ~500 MB
- **Instalado:** ~20 MB
- **Total necessário:** ~600 MB

### Tempo de Compilação
- Sistema moderno (8 cores): ~5-10 minutos
- Sistema antigo (2 cores): ~20-30 minutos

## 🚀 Instalação Passo-a-Passo

### 1. Clonar o repositório do Xournal++

```bash
cd ~/
git clone https://github.com/xournalpp/xournalpp.git
cd xournalpp

# (Opcional) Usar a versão estável mais recente
git checkout $(git describe --tags --abbrev=0)
```

### 2. Aplicar o patch

```bash
# Copiar o arquivo de patch
cp /caminho/para/RadialMenu/cpp-patch/stylus-events.patch .

# Aplicar o patch
git apply stylus-events.patch

# Verificar se foi aplicado
git status
```

Se houver erros:
```bash
# Tentar com patch command
patch -p1 < stylus-events.patch

# Ou aplicar manualmente seguindo o diff
```

### 3. Compilar o Xournal++

```bash
# Criar diretório de build
mkdir build
cd build

# Configurar com CMake
cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local

# Compilar (use número de cores do seu CPU)
make -j$(nproc)

# Opcional: Executar testes
make test
```

### 4. Instalar

```bash
# Instalar (requer sudo)
sudo make install

# OU instalar localmente (sem sudo)
cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/.local
make -j$(nproc)
make install
```

### 5. Verificar instalação

```bash
# Verificar versão
xournalpp --version

# Deve mostrar algo como:
# Xournal++ 1.x.x (custom build)

# Executar
xournalpp
```

## 🔧 Modificações do Patch

### Arquivos Modificados

#### 1. `src/core/plugin/luapi_application.cpp`

**Adicionado:**
- Função `registerStylusHandler(callback)` - Registra handler Lua para eventos de stylus
- Função `getStylusState()` - Obtém estado atual da stylus (posição, pressão, botões)

#### 2. `src/core/control/xojfile/LoadHandler.cpp` ou similar

**Adicionado:**
- Hook para eventos GDK de stylus/pointer
- Callback para plugins quando stylus move, toca, ou botão é pressionado

#### 3. `plugins/luapi_application.def.lua`

**Adicionado documentação:**
```lua
-- Register a handler for stylus events
-- @param handler table with callbacks: {hover, tap, button}
function app.registerStylusHandler(handler) end

-- Get current stylus state
-- @return table {x, y, pressure, buttons, proximity}
function app.getStylusState() end
```

### API Lua Exposta

Com o patch, plugins podem usar:

```lua
-- Registrar callbacks de stylus
app.registerStylusHandler({
    -- Chamado quando stylus move (hover ou tocando)
    hover = function(x, y, pressure)
        print("Hover em: " .. x .. ", " .. y)
        print("Pressão: " .. pressure)
    end,

    -- Chamado quando stylus toca na tela
    tap = function(x, y, pressure)
        print("Tap em: " .. x .. ", " .. y)
    end,

    -- Chamado quando botão lateral é pressionado
    button = function(buttonNum, pressed, x, y)
        print("Botão " .. buttonNum .. " = " .. tostring(pressed))
    end,

    -- Chamado quando stylus entra em proximidade
    proximity_in = function()
        print("Stylus detectada")
    end,

    -- Chamado quando stylus sai de proximidade
    proximity_out = function()
        print("Stylus removida")
    end
})

-- Obter estado atual da stylus
local state = app.getStylusState()
print("Posição: " .. state.x .. ", " .. state.y)
print("Pressão: " .. state.pressure)
print("Proximidade: " .. tostring(state.proximity))
print("Botão 1: " .. tostring(state.buttons[1]))
print("Botão 2: " .. tostring(state.buttons[2]))
```

## 📝 Plugin Modificado (com eventos de stylus)

Com o patch aplicado, o plugin RadialMenu pode ser atualizado:

```lua
-- Versão AVANÇADA com eventos de stylus
function initUi()
    -- Registrar atalho como fallback
    app.registerUi({
        ["menu"] = "Abrir/Fechar Menu Radial",
        ["callback"] = "toggleRadialMenu",
        ["accelerator"] = "<Alt>r"
    })

    -- Registrar handler de stylus
    app.registerStylusHandler({
        button = function(buttonNum, pressed, x, y)
            -- Botão lateral pressionado
            if buttonNum == 2 and pressed then
                MenuState.centerX = x
                MenuState.centerY = y
                toggleRadialMenu()
            end
        end,

        hover = function(x, y, pressure)
            if MenuState.isOpen then
                -- Destacar fatia sob o cursor
                highlightSliceAt(x, y)
            end
        end,

        tap = function(x, y, pressure)
            if MenuState.isOpen then
                -- Processar seleção
                processMenuSelection(x, y)
            end
        end
    })
end

function highlightSliceAt(x, y)
    local section, index = detectMenuSection(x, y)
    -- Redesenhar menu com destaque
    -- ... implementação visual ...
end
```

## 🧪 Testar o Patch

### Teste Básico

Crie um plugin de teste:

```lua
-- test-stylus.lua
function initUi()
    app.registerUi({
        ["menu"] = "Testar Eventos Stylus",
        ["callback"] = "startTest"
    })
end

function startTest()
    print("=== TESTE DE EVENTOS DE STYLUS ===")

    if not app.registerStylusHandler then
        print("ERRO: Patch não foi aplicado!")
        print("A função app.registerStylusHandler não existe.")
        return
    end

    print("✓ Patch aplicado corretamente!")
    print("Movendo a stylus para testar...")

    app.registerStylusHandler({
        hover = function(x, y, pressure)
            print(string.format("HOVER: x=%.1f, y=%.1f, pressure=%.2f", x, y, pressure))
        end,

        tap = function(x, y, pressure)
            print(string.format("TAP: x=%.1f, y=%.1f, pressure=%.2f", x, y, pressure))
        end,

        button = function(buttonNum, pressed, x, y)
            local state = pressed and "PRESSIONADO" or "SOLTO"
            print(string.format("BOTÃO %d: %s em (%.1f, %.1f)", buttonNum, state, x, y))
        end,

        proximity_in = function()
            print("✓ Stylus detectada (proximity in)")
        end,

        proximity_out = function()
            print("✗ Stylus removida (proximity out)")
        end
    })

    print("=== Teste iniciado. Mova a stylus e pressione botões. ===")
end
```

### Teste de Estado

```lua
function checkStylusState()
    if not app.getStylusState then
        print("ERRO: Função getStylusState não existe!")
        return
    end

    local state = app.getStylusState()
    print("=== ESTADO DA STYLUS ===")
    print("Posição: (" .. state.x .. ", " .. state.y .. ")")
    print("Pressão: " .. state.pressure)
    print("Proximidade: " .. tostring(state.proximity))
    print("Botões: " .. table.concat(state.buttons, ", "))
end
```

## 🔨 Desenvolvimento do Patch

Se você quiser criar ou modificar o patch:

### Estrutura de GDK Event

```cpp
// Em src/core/control/Control.cpp ou similar
bool Control::onStylusEvent(GdkEvent* event) {
    GdkDevice* device = gdk_event_get_source_device(event);
    GdkInputSource source = gdk_device_get_source(device);

    // Verificar se é stylus/pen
    if (source != GDK_SOURCE_PEN && source != GDK_SOURCE_ERASER) {
        return false;
    }

    double x, y, pressure = 0.0;
    gdk_event_get_coords(event, &x, &y);
    gdk_event_get_axis(event, GDK_AXIS_PRESSURE, &pressure);

    guint button = 0;
    gdk_event_get_button(event, &button);

    // Chamar plugin handlers
    this->pluginController->notifyStylusEvent(event->type, x, y, pressure, button);

    return false; // Não consumir o evento
}
```

### Bridge para Lua

```cpp
// Em src/core/plugin/Plugin.cpp
int Plugin::registerStylusHandler(lua_State* L) {
    Plugin* plugin = Plugin::checkFromLua(L);

    if (!lua_istable(L, 1)) {
        return luaL_error(L, "registerStylusHandler: argument must be a table");
    }

    // Armazenar referência para a tabela de callbacks
    lua_pushvalue(L, 1);
    plugin->stylusHandlerRef = luaL_ref(L, LUA_REGISTRYINDEX);

    return 0;
}

void Plugin::notifyStylusEvent(const std::string& eventType, double x, double y,
                                double pressure, int button) {
    if (this->stylusHandlerRef == LUA_NOREF) {
        return;
    }

    lua_State* L = this->lua;

    // Recuperar tabela de callbacks
    lua_rawgeti(L, LUA_REGISTRYINDEX, this->stylusHandlerRef);

    // Obter callback específico (hover, tap, button, etc.)
    lua_getfield(L, -1, eventType.c_str());

    if (!lua_isfunction(L, -1)) {
        lua_pop(L, 2);
        return;
    }

    // Push argumentos
    lua_pushnumber(L, x);
    lua_pushnumber(L, y);
    if (eventType == "button") {
        lua_pushinteger(L, button);
    } else {
        lua_pushnumber(L, pressure);
    }

    // Chamar função
    if (lua_pcall(L, eventType == "button" ? 3 : 2, 0, 0) != 0) {
        g_warning("Error in stylus handler: %s", lua_tostring(L, -1));
        lua_pop(L, 1);
    }

    lua_pop(L, 1); // Pop callback table
}
```

## 🐛 Troubleshooting

### Patch não aplica

```bash
# Ver diferenças
git diff

# Reverter mudanças
git reset --hard

# Aplicar manualmente
# Edite os arquivos seguindo o conteúdo de stylus-events.patch
```

### Erros de compilação

```bash
# Limpar build
rm -rf build
mkdir build
cd build

# Reconfigurar
cmake .. -DCMAKE_BUILD_TYPE=Debug

# Compilar com output verbose
make VERBOSE=1
```

### Plugin não detecta funções novas

```bash
# Verificar se a versão customizada está rodando
which xournalpp
xournalpp --version

# Pode ser necessário remover versão instalada
sudo apt remove xournalpp

# E usar apenas a versão compilada
export PATH=$HOME/.local/bin:$PATH
```

## 📚 Referências

- **GDK Input Device API:** https://docs.gtk.org/gdk3/class.Device.html
- **GDK Events:** https://docs.gtk.org/gdk3/union.Event.html
- **Lua C API:** https://www.lua.org/manual/5.3/manual.html#4
- **Xournal++ Source:** https://github.com/xournalpp/xournalpp

## ⚖️ Licença

Este patch segue a mesma licença do Xournal++ (GPL-2.0).

## 🤝 Contribuir

Se você melhorar o patch:

1. Teste extensivamente
2. Documente mudanças
3. Considere submeter PR ao repositório oficial do Xournal++

---

**Status:** Patch conceitual - Adaptações específicas podem ser necessárias dependendo da versão do Xournal++.
