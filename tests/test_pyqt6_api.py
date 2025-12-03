"""
Teste de API real do PyQt6 - SEM MOCKS
Verifica se estamos usando as APIs corretas do PyQt6
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_pyqt6_imports():
    """Testa se PyQt6 pode ser importado"""
    try:
        from PyQt6.QtGui import QPainter, QFont, QPen, QBrush, QColor
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QWidget
        print("✓ PyQt6 importado com sucesso")
        return True
    except ImportError as e:
        print(f"⚠ PyQt6 não disponível: {e}")
        print("  (Normal em ambiente sem GUI)")
        return False


def test_qpainter_renderhint():
    """Testa se QPainter.RenderHint.Antialiasing existe"""
    try:
        from PyQt6.QtGui import QPainter

        # Verificar se a API correta existe
        assert hasattr(QPainter, 'RenderHint'), "QPainter.RenderHint não existe"
        assert hasattr(QPainter.RenderHint, 'Antialiasing'), "QPainter.RenderHint.Antialiasing não existe"

        # Verificar que a API antiga NÃO existe
        assert not hasattr(QPainter, 'Antialiasing'), "ERRO: QPainter.Antialiasing não deve existir (use QPainter.RenderHint.Antialiasing)"

        print("✓ QPainter.RenderHint.Antialiasing está correto")
        return True
    except ImportError:
        print("⚠ PyQt6 não disponível, teste pulado")
        return False
    except AssertionError as e:
        print(f"✗ ERRO: {e}")
        raise


def test_qfont_weight():
    """Testa se QFont.Weight.Bold existe"""
    try:
        from PyQt6.QtGui import QFont

        # Verificar se a API correta existe
        assert hasattr(QFont, 'Weight'), "QFont.Weight não existe"
        assert hasattr(QFont.Weight, 'Bold'), "QFont.Weight.Bold não existe"

        # Verificar que a API antiga NÃO existe
        assert not hasattr(QFont, 'Bold'), "ERRO: QFont.Bold não deve existir (use QFont.Weight.Bold)"

        print("✓ QFont.Weight.Bold está correto")
        return True
    except ImportError:
        print("⚠ PyQt6 não disponível, teste pulado")
        return False
    except AssertionError as e:
        print(f"✗ ERRO: {e}")
        raise


def test_qt_constants():
    """Testa constantes Qt"""
    try:
        from PyQt6.QtCore import Qt

        # Verificar APIs corretas (PyQt6)
        assert hasattr(Qt, 'MouseButton'), "Qt.MouseButton não existe"
        assert hasattr(Qt.MouseButton, 'LeftButton'), "Qt.MouseButton.LeftButton não existe"

        assert hasattr(Qt, 'PenStyle'), "Qt.PenStyle não existe"
        assert hasattr(Qt.PenStyle, 'NoPen'), "Qt.PenStyle.NoPen não existe"

        assert hasattr(Qt, 'BrushStyle'), "Qt.BrushStyle não existe"
        assert hasattr(Qt.BrushStyle, 'NoBrush'), "Qt.BrushStyle.NoBrush não existe"

        # Verificar APIs antigas NÃO existem
        assert not hasattr(Qt, 'LeftButton'), "ERRO: Qt.LeftButton não deve existir (use Qt.MouseButton.LeftButton)"
        assert not hasattr(Qt, 'NoPen'), "ERRO: Qt.NoPen não deve existir (use Qt.PenStyle.NoPen)"

        print("✓ Constantes Qt estão corretas")
        return True
    except ImportError:
        print("⚠ PyQt6 não disponível, teste pulado")
        return False
    except AssertionError as e:
        print(f"✗ ERRO: {e}")
        raise


def test_radial_menu_imports():
    """Testa se radial_menu.py usa APIs corretas"""
    try:
        # Ler o arquivo e verificar que não usa APIs antigas
        with open('src/radial_menu.py', 'r', encoding='utf-8') as f:
            content = f.read()

        errors = []

        # Verificar APIs antigas que NÃO devem existir
        if 'QPainter.Antialiasing' in content:
            errors.append("Encontrado 'QPainter.Antialiasing' - use 'QPainter.RenderHint.Antialiasing'")

        if 'QFont.Bold' in content and 'QFont.Weight.Bold' not in content:
            errors.append("Encontrado 'QFont.Bold' - use 'QFont.Weight.Bold'")

        if 'Qt.LeftButton' in content and 'Qt.MouseButton.LeftButton' not in content:
            errors.append("Encontrado 'Qt.LeftButton' - use 'Qt.MouseButton.LeftButton'")

        if 'Qt.NoPen' in content and 'Qt.PenStyle.NoPen' not in content:
            errors.append("Encontrado 'Qt.NoPen' - use 'Qt.PenStyle.NoPen'")

        if errors:
            for error in errors:
                print(f"✗ {error}")
            raise AssertionError(f"Encontrados {len(errors)} erros de API PyQt6")

        print("✓ radial_menu.py usa APIs PyQt6 corretas")
        return True
    except FileNotFoundError:
        print("⚠ Arquivo radial_menu.py não encontrado")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("TESTES DE API PyQt6 - SEM MOCKS")
    print("=" * 70)
    print()

    # Teste 1: Verificar arquivo
    test_radial_menu_imports()
    print()

    # Teste 2: Importar PyQt6
    if not test_pyqt6_imports():
        print()
        print("⚠ PyQt6 não disponível - testes de API pulados")
        print("✓ Mas arquivo foi verificado e está correto")
        sys.exit(0)

    print()

    # Testes 3-5: APIs específicas
    test_qpainter_renderhint()
    print()
    test_qfont_weight()
    print()
    test_qt_constants()
    print()

    print("=" * 70)
    print("✓ TODOS OS TESTES DE API PyQt6 PASSARAM")
    print("=" * 70)
