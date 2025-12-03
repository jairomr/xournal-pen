#!/bin/bash
#
# Script de instalação automática do RadialMenu Plugin para Xournal++
# Uso: ./INSTALL.sh
#

set -e

echo "=================================================="
echo "  RadialMenu Plugin - Instalador para Xournal++  "
echo "=================================================="
echo ""

# Detectar diretório de plugins
PLUGIN_DIR=""

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLUGIN_DIR="$HOME/.local/share/xournalpp/plugins"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    PLUGIN_DIR="$HOME/Library/Application Support/xournalpp/plugins"
else
    echo "Sistema operacional não suportado automaticamente."
    echo "Por favor, copie manualmente a pasta RadialMenu para:"
    echo "  Linux: ~/.local/share/xournalpp/plugins/"
    echo "  Windows: C:\\Users\\<usuario>\\AppData\\Local\\xournalpp\\plugins\\"
    echo "  macOS: ~/Library/Application Support/xournalpp/plugins/"
    exit 1
fi

echo "Diretório de plugins: $PLUGIN_DIR"
echo ""

# Criar diretório se não existir
if [ ! -d "$PLUGIN_DIR" ]; then
    echo "Criando diretório de plugins..."
    mkdir -p "$PLUGIN_DIR"
fi

# Obter diretório deste script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Nome do plugin
PLUGIN_NAME="RadialMenu"

# Verificar se já existe instalação prévia
if [ -d "$PLUGIN_DIR/$PLUGIN_NAME" ]; then
    echo "⚠️  Instalação prévia detectada em: $PLUGIN_DIR/$PLUGIN_NAME"
    echo ""
    read -p "Deseja sobrescrever? (s/N): " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[SsYy]$ ]]; then
        echo "Instalação cancelada."
        exit 0
    fi

    echo "Removendo instalação anterior..."
    rm -rf "$PLUGIN_DIR/$PLUGIN_NAME"
fi

# Copiar plugin
echo "Instalando plugin..."
cp -r "$SCRIPT_DIR" "$PLUGIN_DIR/$PLUGIN_NAME"

echo ""
echo "✅ Plugin instalado com sucesso!"
echo ""
echo "Próximos passos:"
echo ""
echo "1. Abra o Xournal++"
echo "2. Vá em: Editar → Preferências → Plugins"
echo "3. Marque a caixa 'RadialMenu'"
echo "4. Clique em OK e reinicie o Xournal++"
echo ""
echo "5. Configure o botão da stylus para Alt+R:"
echo ""
echo "   • Wacom: xsetwacom set \"<dispositivo>\" Button 2 \"key alt r\""
echo "   • Outras: veja README.md para instruções detalhadas"
echo ""
echo "6. Pressione Alt+R (ou botão da stylus) para abrir o menu!"
echo ""
echo "=================================================="
echo "Para desinstalar: rm -rf $PLUGIN_DIR/$PLUGIN_NAME"
echo "Documentação completa: cat $PLUGIN_DIR/$PLUGIN_NAME/README.md"
echo "=================================================="
