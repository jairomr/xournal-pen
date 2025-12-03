# Configuração de Stylus para RadialMenu

Guia completo para mapear o botão lateral da caneta para abrir o menu radial.

## 🎯 Objetivo

Mapear o **botão lateral da stylus** para o atalho **`Alt+R`** que abre/fecha o menu radial.

---

## 🐧 Linux

### Wacom Tablets

#### 1. Identificar o dispositivo

```bash
xsetwacom list devices
```

**Exemplo de saída:**
```
Wacom Intuos PT S Pen stylus      id: 12  type: STYLUS
Wacom Intuos PT S Pen eraser      id: 13  type: ERASER
Wacom Intuos PT S Pad pad         id: 14  type: PAD
```

#### 2. Testar botões

Descubra qual é o número do botão lateral:

```bash
xsetwacom get "Wacom Intuos PT S Pen stylus" Button 1
xsetwacom get "Wacom Intuos PT S Pen stylus" Button 2
xsetwacom get "Wacom Intuos PT S Pen stylus" Button 3
```

Normalmente:
- **Button 1** = Ponta da caneta (tip)
- **Button 2** = Botão lateral inferior
- **Button 3** = Botão lateral superior

#### 3. Mapear botão para Alt+R

```bash
# Mapear botão lateral inferior
xsetwacom set "Wacom Intuos PT S Pen stylus" Button 2 "key alt r"

# OU botão lateral superior
xsetwacom set "Wacom Intuos PT S Pen stylus" Button 3 "key alt r"

# OU ambos (recomendado)
xsetwacom set "Wacom Intuos PT S Pen stylus" Button 2 "key alt r"
xsetwacom set "Wacom Intuos PT S Pen stylus" Button 3 "key alt r"
```

#### 4. Tornar permanente

**Método A: Adicionar ao ~/.bashrc ou ~/.profile**

```bash
# Editar arquivo
nano ~/.bashrc

# Adicionar no final:
if command -v xsetwacom &> /dev/null; then
    xsetwacom set "Wacom Intuos PT S Pen stylus" Button 2 "key alt r"
    xsetwacom set "Wacom Intuos PT S Pen stylus" Button 3 "key alt r"
fi
```

**Método B: Criar script de autostart**

```bash
# Criar arquivo
mkdir -p ~/.config/autostart
nano ~/.config/autostart/wacom-setup.desktop
```

Conteúdo:
```ini
[Desktop Entry]
Type=Application
Name=Wacom Setup
Exec=/bin/bash -c 'sleep 2 && xsetwacom set "Wacom Intuos PT S Pen stylus" Button 2 "key alt r"'
Hidden=false
X-GNOME-Autostart-enabled=true
```

**Método C: Usar GUI (KDE)**

1. `Configurações do Sistema → Tablet Gráfica`
2. Selecione a caneta
3. Vá em aba `Botões`
4. Clique no botão lateral
5. Selecione `Atalho de teclado` → `Alt+R`

---

### XP-Pen Tablets

#### Interface Gráfica (Recomendado)

1. Abra `PenTablet` (aplicativo da XP-Pen)
2. Vá em `Configurações da Caneta`
3. Clique no botão lateral
4. Selecione `Atalho de teclado`
5. Pressione `Alt+R`
6. Clique em `Aplicar`

#### Linha de Comando (xbindkeys)

```bash
# Instalar xbindkeys
sudo apt install xbindkeys xbindkeys-config xdotool

# Descobrir código do botão
xev | grep button
# Pressione o botão lateral e anote o número (ex: button 8, 9, ou 10)

# Criar/editar configuração
nano ~/.xbindkeysrc
```

Adicione (substitua `b:10` pelo número correto):

```
# Botão lateral da caneta XP-Pen
"xdotool key alt+r"
  b:10
```

Ou use `xte`:

```bash
sudo apt install xautomation

# Adicione ao ~/.xbindkeysrc:
"xte 'keydown Alt_L' 'key r' 'keyup Alt_L'"
  b:10
```

Recarregar configuração:

```bash
killall xbindkeys
xbindkeys
```

Tornar permanente (autostart):

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/xbindkeys.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=XBindKeys
Exec=xbindkeys
Hidden=false
X-GNOME-Autostart-enabled=true
EOF
```

---

### Huion Tablets

Similiar ao XP-Pen:

#### Interface Gráfica

1. Abra `HuionTablet`
2. `Configurações da Caneta`
3. Mapeie botão lateral para `Alt+R`

#### Linha de Comando

Mesmo processo do XP-Pen usando `xbindkeys`.

---

### Tablets Genéricos (evdev/libinput)

```bash
# Listar dispositivos de entrada
xinput list

# Encontrar propriedades do dispositivo
xinput list-props <ID>

# Criar script de mapeamento
nano ~/stylus-setup.sh
```

Conteúdo:

```bash
#!/bin/bash
# Substitua <DEVICE_ID> pelo ID do seu dispositivo
xinput set-button-map <DEVICE_ID> 1 2 3 4 5 6 7 8 9
xbindkeys
```

---

## 🪟 Windows

### Wacom Tablets

1. Abra `Wacom Tablet Properties` (ícone na bandeja do sistema)
2. Selecione `Pen` (Caneta) na lista de dispositivos
3. Na aba `Application` (Aplicação), selecione `All Other` ou `Xournal++`
4. Clique no **botão lateral** no diagrama da caneta
5. Selecione `Keystroke...` (Tecla de atalho)
6. Pressione `Alt+R` na caixa de diálogo
7. Clique em `OK`
8. Clique em `OK` novamente para salvar

### XP-Pen Tablets

1. Abra `PenTablet` (software da XP-Pen)
2. Clique na aba `Pen` (Caneta)
3. Clique no **botão lateral inferior** ou **superior**
4. Selecione `Keyboard` (Teclado)
5. Clique em `Settings` (Configurações)
6. Pressione `Alt+R`
7. Clique em `OK`
8. Clique em `Apply` (Aplicar)

### Huion Tablets

1. Abra `HuionTablet` ou `Huion Tablet Driver`
2. Vá em `Pen Settings` (Configurações da Caneta)
3. Clique no **botão lateral**
4. Selecione `Keyboard` ou `Keystroke`
5. Digite ou pressione `Alt+R`
6. Clique em `OK` e `Apply`

### AutoHotkey (Universal - Todas as Tablets)

Se o software da tablet não funcionar bem:

1. **Instale AutoHotkey:** https://www.autohotkey.com/

2. **Crie um script** `RadialMenu.ahk`:

```ahk
; RadialMenu - Mapear botão da caneta para Alt+R
; Ajuste os botões conforme necessário

; Botão Joystick 1 (comum em stylus)
Joy1::Send !r
return

; Botão Joystick 2
Joy2::Send !r
return

; Ou use código de botão específico (descobrir com KeyHistory)
; Para Wacom: pode ser Button 2 ou 3
; Para XP-Pen: pode ser Button 8, 9, ou 10

; Alternativa: Mapear botão direito do mouse quando stylus está ativa
; Útil se o botão lateral simula clique direito
#If WinActive("ahk_exe xournalpp.exe")
RButton::Send !r
#If

; MODO AVANÇADO: Detectar stylus proximity
; Descomentar se necessário
; #If (DllCall("GetSystemMetrics", "Int", 94)) ; SM_DIGITIZER
; Button4::Send !r
; Button5::Send !r
; #If
```

3. **Execute o script** (duplo-clique)

4. **Tornar permanente:**
   - Pressione `Win+R`
   - Digite `shell:startup`
   - Copie o arquivo `.ahk` para esta pasta
   - Ou crie um atalho dele

#### Descobrir código do botão (AutoHotkey)

Execute este script temporário:

```ahk
; Descobrir código do botão da stylus
#Persistent
SetTimer, CheckButtons, 100
return

CheckButtons:
Loop, 32 {
    if GetKeyState(A_Index . "Joy1") {
        ToolTip, Botão Joy%A_Index% pressionado
    }
}

; Ou verificar botões do mouse
Loop, 10 {
    keyName := "Button" . A_Index
    if GetKeyState(keyName) {
        ToolTip, %keyName% pressionado
    }
}
return

; Pressione Esc para sair
Esc::ExitApp
```

---

## 🍎 macOS

### Wacom Tablets

1. Abra `Wacom Tablet Utility` ou `Wacom Desktop Center`
2. Selecione seu dispositivo
3. Clique na aba `Pen`
4. Clique no botão lateral no diagrama
5. Selecione `Keyboard` → `Modifier + Key`
6. Configure como `Option + R` (Alt = Option no Mac)
7. Clique em `OK`

### XP-Pen / Huion

Similar ao Windows, use o software fornecido pela marca.

### BetterTouchTool (Universal)

1. **Instale BetterTouchTool:** https://folivora.ai/

2. Configure:
   - Adicione novo `Generic Device`
   - Capture o botão da stylus
   - Mapeie para `⌥R` (Option+R)

---

## ✅ Testar Configuração

### Linux

```bash
# Método 1: Verificar mapeamento (Wacom)
xsetwacom get "Wacom Intuos PT S Pen stylus" Button 2

# Método 2: Monitorar eventos
xev | grep button
# Pressione o botão e veja o output

# Método 3: Verificar teclado
xev | grep -A2 --line-buffered '^KeyPress'
# Pressione o botão, deve mostrar "Alt" e "r"
```

### Windows

1. Abra o Bloco de Notas
2. Pressione o botão lateral da caneta
3. Deve aparecer nada (apenas Alt+R não produz texto)
4. Abra Xournal++ e teste

### Verificar no Xournal++

1. Abra o Xournal++
2. Ative o plugin RadialMenu
3. Pressione o botão lateral da caneta
4. O menu radial deve aparecer!

---

## 🔧 Solução de Problemas

### Botão não funciona

**Causa:** Mapeamento incorreto ou conflito

**Solução:**
- Verifique se o software da tablet está rodando
- Teste o atalho `Alt+R` no teclado primeiro
- Desabilite outros softwares de mapeamento (conflito)
- Verifique logs/eventos do sistema

### Atalho funciona mas botão não

**Causa:** Driver não está enviando o evento corretamente

**Solução Linux:**
```bash
# Ver eventos raw
sudo evtest
# Selecione o dispositivo da caneta e pressione o botão

# Ou usar libinput
sudo libinput debug-events
```

**Solução Windows:**
- Reinstale o driver da tablet
- Teste com AutoHotkey
- Verifique conflitos com outros programas

### Múltiplos atalhos sendo acionados

**Causa:** Mapeamento duplicado

**Solução:**
- Remova mapeamentos conflitantes
- Use apenas um método (xsetwacom OU xbindkeys, não ambos)
- Verifique configurações globais do desktop environment

### Botão funciona em outros apps mas não no Xournal++

**Causa:** Xournal++ capturando o evento diferente

**Solução:**
- Verifique em Preferências → Mouse se botão está mapeado
- Tente um atalho diferente (ex: `Ctrl+Alt+R`)
- Verifique se o plugin está ativo

---

## 📚 Referências

### Linux
- **xsetwacom:** `man xsetwacom`
- **xbindkeys:** https://wiki.archlinux.org/title/Xbindkeys
- **libinput:** https://wayland.freedesktop.org/libinput/doc/latest/

### Windows
- **AutoHotkey Docs:** https://www.autohotkey.com/docs/
- **Wacom Support:** https://www.wacom.com/support
- **XP-Pen Support:** https://www.xp-pen.com/support

### macOS
- **BetterTouchTool:** https://docs.folivora.ai/

---

## 🎯 Mapeamentos Recomendados

### Configuração Ideal (2 botões laterais)

- **Botão Superior:** `Alt+R` (Abrir Menu Radial)
- **Botão Inferior:** `Ctrl+Z` (Desfazer)

### Configuração Alternativa (1 botão lateral)

- **Botão Lateral:** `Alt+R` (Menu Radial)
- **Duplo-toque no botão:** `Ctrl+Z` (requer config avançada)

---

**Após configurar, teste no Xournal++ e aproveite o menu radial! 🎨**
