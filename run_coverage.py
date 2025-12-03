#!/usr/bin/env python3
"""
Script para rodar testes com cobertura
"""
import sys
import os
import subprocess

def main():
    # Diretório do projeto
    project_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(project_dir, 'src')
    tests_dir = os.path.join(project_dir, 'tests')

    # Adicionar src ao path
    sys.path.insert(0, src_dir)

    print("=" * 70)
    print("EXECUTANDO TESTES COM COBERTURA")
    print("=" * 70)
    print()

    # Descobrir todos os arquivos de teste
    test_files = []
    for filename in os.listdir(tests_dir):
        if filename.startswith('test_') and filename.endswith('.py'):
            test_files.append(os.path.join(tests_dir, filename))

    print(f"Encontrados {len(test_files)} arquivos de teste:")
    for f in test_files:
        print(f"  - {os.path.basename(f)}")
    print()

    # Primeiro rodar teste de API PyQt6 (sem coverage)
    print("Verificando APIs PyQt6...")
    print("-" * 70)
    api_test = os.path.join(tests_dir, 'test_pyqt6_api.py')
    if os.path.exists(api_test):
        result = subprocess.run(
            ['python', api_test],
            cwd=project_dir,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print("✗ ERRO: Teste de API PyQt6 falhou!")
            print(result.stderr)
            return 1
    print()

    # Rodar coverage
    print("Rodando testes com cobertura...")
    print("-" * 70)

    # Limpar dados anteriores
    subprocess.run(['coverage', 'erase'], cwd=project_dir)

    # Rodar cada teste com coverage
    for test_file in test_files:
        print(f"\nRodando {os.path.basename(test_file)}...")
        result = subprocess.run(
            ['coverage', 'run', '-a', '--source=src', test_file],
            cwd=project_dir,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)

    print()
    print("=" * 70)
    print("RELATÓRIO DE COBERTURA")
    print("=" * 70)
    print()

    # Mostrar relatório resumido (excluir GUI e _version)
    result = subprocess.run(
        ['coverage', 'report', '--omit=src/_version.py,src/main.py'],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    print(result.stdout)
    print()
    print("Observação: main.py (GUI) excluído da cobertura")

    # Gerar relatório HTML
    subprocess.run(
        ['coverage', 'html', '--omit=src/_version.py,src/main.py'],
        cwd=project_dir
    )
    print()
    print("✓ Relatório HTML gerado em: htmlcov/index.html")
    print()

    # Extrair percentual de cobertura
    lines = result.stdout.split('\n')
    for line in lines:
        if 'TOTAL' in line:
            parts = line.split()
            if len(parts) >= 4:
                coverage_pct = parts[-1].rstrip('%')
                try:
                    coverage_value = float(coverage_pct)
                    print(f"Cobertura total: {coverage_value}%")

                    if coverage_value >= 85:
                        print(f"✓ META ATINGIDA: {coverage_value}% >= 85%")
                        return 0
                    else:
                        print(f"✗ ABAIXO DA META: {coverage_value}% < 85%")
                        print(f"  Faltam {85 - coverage_value:.1f}% para atingir a meta")
                        return 1
                except ValueError:
                    pass

    return 1

if __name__ == '__main__':
    sys.exit(main())
