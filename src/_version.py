"""
Versão do Xournal Radial Menu
Este arquivo é gerado automaticamente durante o build
"""

import subprocess
import os


def get_version():
    """
    Obtém versão da tag do git ou retorna fallback
    """
    try:
        # Tentar pegar da tag do git
        version = subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0'],
            stderr=subprocess.DEVNULL,
            cwd=os.path.dirname(os.path.dirname(__file__))
        ).decode('utf-8').strip()

        # Remover 'v' do início se existir
        if version.startswith('v'):
            version = version[1:]

        return version
    except Exception:
        # Fallback: versão padrão
        return "2.1.0"


__version__ = get_version()
