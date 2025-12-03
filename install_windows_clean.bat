@echo off
REM Script de limpeza completa para Windows
REM Execute este script para limpar TUDO antes de reinstalar

echo ========================================
echo LIMPEZA COMPLETA - Xournal Radial Menu
echo ========================================
echo.

echo [1/5] Removendo ambiente virtual antigo...
if exist .venv (
    rmdir /s /q .venv
    echo ✓ .venv removido
) else (
    echo ✓ .venv nao existia
)

echo.
echo [2/5] Removendo cache do UV...
if exist %LOCALAPPDATA%\uv\cache (
    rmdir /s /q %LOCALAPPDATA%\uv\cache
    echo ✓ Cache do UV removido
) else (
    echo ✓ Cache do UV nao existia
)

echo.
echo [3/5] Removendo arquivos de lock...
if exist uv.lock (
    del /q uv.lock
    echo ✓ uv.lock removido
)
if exist .python-version (
    del /q .python-version
    echo ✓ .python-version removido
)
echo ✓ Arquivos de lock limpos

echo.
echo [4/5] Verificando requirements.txt...
findstr /C:"PyQt5==5.15.2" requirements.txt >nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ PyQt5==5.15.2 encontrado em requirements.txt
) else (
    echo ✗ ERRO: requirements.txt nao tem PyQt5==5.15.2
    echo Execute: git pull
    pause
    exit /b 1
)

echo.
echo [5/5] Instalando dependencias com UV...
uv pip install --no-cache -r requirements.txt

echo.
echo ========================================
echo INSTALACAO COMPLETA
echo ========================================
echo.
echo Verifique a versao do PyQt5:
uv pip list | findstr PyQt5
echo.
echo Se mostrar PyQt5 5.15.2, execute:
echo   python test_imports.py
echo   python run.py
echo.
pause
