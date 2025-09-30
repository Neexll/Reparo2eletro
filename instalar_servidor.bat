@echo off
chcp 65001 >nul
echo ============================================================
echo      INSTALADOR AUTOMÁTICO - REPARO2ELETRO SERVIDOR
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não está instalado!
    echo.
    echo Por favor, instale o Python 3.8 ou superior:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python encontrado
echo.

echo [2/5] Criando ambiente virtual...
if exist "venv" (
    echo ⚠️  Ambiente virtual já existe. Pulando...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ❌ ERRO ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo ✅ Ambiente virtual criado
)
echo.

echo [3/5] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ ERRO ao ativar ambiente virtual
    pause
    exit /b 1
)
echo ✅ Ambiente virtual ativado
echo.

echo [4/5] Instalando dependências...
echo Isso pode demorar alguns minutos...
echo.
pip install -r requirements_production.txt --quiet
if errorlevel 1 (
    echo ⚠️  Erro ao instalar algumas dependências de produção
    echo Tentando instalar dependências básicas...
    pip install -r requirements.txt --quiet
)
echo ✅ Dependências instaladas
echo.

echo [5/5] Verificando banco de dados...
if exist "database.db" (
    echo ✅ Banco de dados já existe
) else (
    echo ⚠️  Banco de dados não encontrado
    echo Criando banco de dados...
    python -c "from app import init_db; init_db()" 2>nul
    if exist "database.db" (
        echo ✅ Banco de dados criado
    ) else (
        echo ℹ️  Será criado na primeira execução
    )
)
echo.

echo ============================================================
echo                 INSTALAÇÃO CONCLUÍDA! ✅
echo ============================================================
echo.
echo 📌 PRÓXIMOS PASSOS:
echo.
echo 1. Configure o firewall (execute como Administrador):
echo    PowerShell: New-NetFirewallRule -DisplayName "Reparo2Eletro" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
echo.
echo 2. Para iniciar o servidor, escolha uma opção:
echo.
echo    OPÇÃO A - Modo Produção (Recomendado):
echo       python server_production.py
echo.
echo    OPÇÃO B - Modo Rede Simples:
echo       python server.py
echo.
echo    OPÇÃO C - Usar atalho:
echo       Clique 2x em: start_server_network.bat
echo.
echo ============================================================
echo.
pause
