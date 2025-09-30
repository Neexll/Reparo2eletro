@echo off
chcp 65001 >nul
echo ============================================================
echo      BUILD SERVIDOR COMPLETO - REPARO2ELETRO
echo      (Instala + Compila tudo automaticamente)
echo ============================================================
echo.

REM Volta para pasta raiz do projeto
cd /d "%~dp0\..\.."

echo [PASSO 1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo X ERRO: Python nao esta instalado!
    echo.
    echo Por favor, instale Python 3.8 ou superior de:
    echo https://python.org/downloads
    echo.
    echo Durante a instalacao, marque: Add to PATH
    echo.
    pause
    exit /b 1
)
echo OK Python encontrado
python --version
echo.

echo [PASSO 2/5] Criando ambiente virtual...
if exist "venv" (
    echo OK Ambiente virtual ja existe
) else (
    echo Criando ambiente virtual (pode demorar 1-2 minutos)...
    python -m venv venv
    if errorlevel 1 (
        echo X Erro ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo OK Ambiente virtual criado
)
echo.

echo [PASSO 3/5] Ativando ambiente virtual e instalando dependencias...
call venv\Scripts\activate.bat
echo Instalando dependencias (pode demorar 3-5 minutos)...
echo Por favor, aguarde...
echo.
pip install --upgrade pip >nul 2>&1
pip install Flask openpyxl fpdf2 matplotlib waitress pyinstaller --quiet
if errorlevel 1 (
    echo X Erro ao instalar dependencias
    echo Tentando novamente sem --quiet...
    pip install Flask openpyxl fpdf2 matplotlib waitress pyinstaller
    pause
)
echo OK Dependencias instaladas
echo.

echo [PASSO 4/5] Criando build com PyInstaller...
echo.
echo ============================================================
echo ATENCAO: Este processo pode demorar 5-10 minutos!
echo Nao feche esta janela. Aguarde ate o final.
echo ============================================================
echo.
timeout /t 3 >nul

python build_server.py

if errorlevel 1 (
    echo.
    echo X Erro ao criar build
    echo.
    pause
    exit /b 1
)

echo.
echo [PASSO 5/5] Verificando resultado...
if exist "dist_servidor\Reparo2Eletro_Server.exe" (
    echo OK Build criado com sucesso!
) else (
    echo X AVISO: Executavel nao encontrado
)
echo.

echo ============================================================
echo              OK PROCESSO CONCLUIDO!
echo ============================================================
echo.
echo  Pasta criada: dist_servidor\
echo.
echo  PROXIMOS PASSOS:
echo.
echo  1. Copie TODA a pasta "dist_servidor" para o servidor
echo.
echo  2. No servidor, execute: INICIAR_SERVIDOR.bat
echo.
echo  3. Configure o firewall se necessario
echo.
echo ============================================================
echo.

if exist "dist_servidor" (
    echo Abrindo pasta dist_servidor...
    start "" dist_servidor
    echo.
)

pause
