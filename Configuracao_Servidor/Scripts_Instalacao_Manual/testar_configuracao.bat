@echo off
chcp 65001 >nul
echo ============================================================
echo      TESTE DE CONFIGURAÇÃO - REPARO2ELETRO
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/6] Testando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não instalado
    set "erro=sim"
) else (
    python --version
    echo ✅ Python OK
)
echo.

echo [2/6] Verificando ambiente virtual...
if exist "venv\Scripts\activate.bat" (
    echo ✅ Ambiente virtual existe
) else (
    echo ❌ Ambiente virtual não encontrado
    echo    Execute: instalar_servidor.bat
    set "erro=sim"
)
echo.

echo [3/6] Verificando banco de dados...
if exist "database.db" (
    echo ✅ Banco de dados existe
) else (
    echo ⚠️  Banco de dados não encontrado
    echo    Será criado na primeira execução
)
echo.

echo [4/6] Verificando arquivos do servidor...
if exist "server.py" (
    echo ✅ server.py existe
) else (
    echo ❌ server.py não encontrado
    set "erro=sim"
)

if exist "server_production.py" (
    echo ✅ server_production.py existe
) else (
    echo ⚠️  server_production.py não encontrado
)
echo.

echo [5/6] Verificando dependências...
call venv\Scripts\activate.bat 2>nul
python -c "import flask; import openpyxl; import fpdf; print('✅ Dependências básicas OK')" 2>nul
if errorlevel 1 (
    echo ❌ Dependências faltando
    echo    Execute: instalar_servidor.bat
    set "erro=sim"
)
echo.

echo [6/6] Obtendo informações de rede...
echo IP do Servidor:
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    echo    %%a
)
echo.

echo ============================================================
if defined erro (
    echo STATUS: ❌ CONFIGURAÇÃO INCOMPLETA
    echo.
    echo Por favor, execute: instalar_servidor.bat
) else (
    echo STATUS: ✅ TUDO PRONTO!
    echo.
    echo Para iniciar o servidor:
    echo   - Modo Produção: python server_production.py
    echo   - Modo Simples: python server.py
    echo   - Ou use: start_server_network.bat
)
echo ============================================================
echo.
pause
