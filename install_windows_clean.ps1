# Script PowerShell de limpeza completa para Windows
# Execute: .\install_windows_clean.ps1

Write-Host "========================================"  -ForegroundColor Cyan
Write-Host "LIMPEZA COMPLETA - Xournal Radial Menu" -ForegroundColor Cyan
Write-Host "========================================"  -ForegroundColor Cyan
Write-Host ""

# 1. Remover ambiente virtual
Write-Host "[1/6] Removendo ambiente virtual antigo..." -ForegroundColor Yellow
if (Test-Path .venv) {
    Remove-Item -Recurse -Force .venv
    Write-Host "✓ .venv removido" -ForegroundColor Green
} else {
    Write-Host "✓ .venv não existia" -ForegroundColor Green
}

# 2. Remover cache do UV
Write-Host ""
Write-Host "[2/6] Removendo cache do UV..." -ForegroundColor Yellow
$uvCache = "$env:LOCALAPPDATA\uv\cache"
if (Test-Path $uvCache) {
    Remove-Item -Recurse -Force $uvCache
    Write-Host "✓ Cache do UV removido" -ForegroundColor Green
} else {
    Write-Host "✓ Cache do UV não existia" -ForegroundColor Green
}

# 3. Remover arquivos de lock
Write-Host ""
Write-Host "[3/6] Removendo arquivos de lock..." -ForegroundColor Yellow
@("uv.lock", ".python-version", "pyproject.toml.lock") | ForEach-Object {
    if (Test-Path $_) {
        Remove-Item -Force $_
        Write-Host "✓ $_ removido" -ForegroundColor Green
    }
}

# 4. Verificar git status
Write-Host ""
Write-Host "[4/6] Verificando código atualizado..." -ForegroundColor Yellow
git pull
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠ Aviso: git pull falhou, continuando..." -ForegroundColor Yellow
}

# 5. Verificar requirements.txt
Write-Host ""
Write-Host "[5/6] Verificando requirements.txt..." -ForegroundColor Yellow
$content = Get-Content requirements.txt -Raw
if ($content -match "PyQt5==5\.15\.2") {
    Write-Host "✓ PyQt5==5.15.2 encontrado em requirements.txt" -ForegroundColor Green
} else {
    Write-Host "✗ ERRO: requirements.txt não tem PyQt5==5.15.2" -ForegroundColor Red
    Write-Host "Conteúdo atual:" -ForegroundColor Yellow
    Get-Content requirements.txt | Select-String "PyQt5"
    Write-Host ""
    Write-Host "Execute manualmente:" -ForegroundColor Yellow
    Write-Host "  git pull" -ForegroundColor White
    Write-Host "  git status" -ForegroundColor White
    exit 1
}

# 6. Instalar dependências
Write-Host ""
Write-Host "[6/6] Instalando dependências com UV..." -ForegroundColor Yellow
Write-Host "Executando: uv pip install --no-cache -r requirements.txt" -ForegroundColor Cyan
uv pip install --no-cache -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "INSTALAÇÃO COMPLETA COM SUCESSO!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""

    Write-Host "Versões instaladas:" -ForegroundColor Cyan
    uv pip list | Select-String "PyQt5"

    Write-Host ""
    Write-Host "Próximos passos:" -ForegroundColor Yellow
    Write-Host "  python test_imports.py   # Testar imports" -ForegroundColor White
    Write-Host "  python run.py            # Executar aplicação" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "ERRO NA INSTALAÇÃO" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Copie a mensagem de erro acima e reporte." -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Pressione ENTER para sair"
