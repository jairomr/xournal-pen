#!/usr/bin/env python3
"""
Script de execução simples do Xournal Radial Menu
Basta executar: python run.py
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importar e executar
from main import main

if __name__ == "__main__":
    main()
