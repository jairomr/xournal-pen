#!/bin/bash
#
# Script de instalação do Xournal++ Radial Menu (Python Edition)
#

set -e

echo "=========================================="
echo "  Xournal++ Radial Menu - Instalador"
echo "=========================================="
echo ""

# Detectar Python
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python não encontrado!"
    echo "Instale Python 3.8+ primeiro:"
    echo "  sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

echo "✓ Python encontrado: $($PYTHON_CMD --version)"
echo ""

# Verificar pip
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "❌ pip não encontrado!"
    echo "Instale pip:"
    echo "  sudo apt install python3-pip"
    exit 1
fi

echo "✓ pip encontrado"
echo ""

# Criar ambiente virtual
echo "Criando ambiente virtual..."
$PYTHON_CMD -m venv venv

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo "Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Criar script de execução
echo "Criando script de execução..."
cat > run.sh << 'EOF'
#!/bin/bash
# Script para executar o Xournal++ Radial Menu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Ativar ambiente virtual
source venv/bin/activate

# Executar aplicação
python src/main.py
EOF

chmod +x run.sh

# Criar arquivo .desktop (opcional)
echo ""
read -p "Criar atalho no menu de aplicações? (s/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[SsYy]$ ]]; then
    DESKTOP_FILE="$HOME/.local/share/applications/xournal-radial-menu.desktop"
    INSTALL_DIR="$(pwd)"

    mkdir -p "$HOME/.local/share/applications"

    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Type=Application
Name=Xournal++ Radial Menu
Comment=Menu radial para stylus
Exec=$INSTALL_DIR/run.sh
Icon=input-tablet
Terminal=false
Categories=Graphics;Utility;
Keywords=xournal;stylus;pen;menu;
EOF

    echo "✓ Atalho criado: $DESKTOP_FILE"
fi

echo ""
echo "=========================================="
echo "  ✅ Instalação concluída!"
echo "=========================================="
echo ""
echo "Para executar:"
echo "  ./run.sh"
echo ""
echo "Ou se criou o atalho:"
echo "  Procure por 'Xournal++ Radial Menu' no menu de aplicações"
echo ""
echo "Uso:"
echo "  1. Inicie a aplicação (./run.sh)"
echo "  2. Abra o Xournal++"
echo "  3. Pressione o botão lateral da stylus ou Alt+R"
echo "  4. Menu aparece na posição do cursor!"
echo ""
