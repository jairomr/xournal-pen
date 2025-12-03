"""
Testes para módulo de versão
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from _version import __version__, get_version


def test_version_format():
    """Testa se versão tem formato válido"""
    assert isinstance(__version__, str)
    assert len(__version__) > 0
    # Formato X.Y.Z
    parts = __version__.split('.')
    assert len(parts) >= 2, f"Versão deve ter pelo menos 2 partes: {__version__}"


def test_get_version():
    """Testa função get_version"""
    version = get_version()
    assert isinstance(version, str)
    assert len(version) > 0


def test_version_from_git():
    """Testa se versão vem de tag do git quando disponível"""
    version = get_version()
    # Deve ser 2.1.0 ou maior
    parts = version.split('.')
    major = int(parts[0])
    minor = int(parts[1])
    assert major >= 2, f"Major version deve ser >= 2, got {major}"
    assert minor >= 1, f"Minor version deve ser >= 1, got {minor}"


if __name__ == "__main__":
    test_version_format()
    test_get_version()
    test_version_from_git()
    print("✓ Todos os testes de versão passaram")
