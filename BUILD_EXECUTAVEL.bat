@echo off
title BUILD SERVIDOR - REPARO2ELETRO
color 0A
echo.
echo ============================================================
echo      CRIAR EXECUTAVEIS - REPARO2ELETRO
echo ============================================================
echo.
echo Este script vai criar DOIS executaveis:
echo.
echo  1. Reparo2Eletro.exe - Aplicativo Desktop
echo     (abre automaticamente no navegador)
echo.
echo  2. Reparo2Eletro_Server.exe - Servidor de Rede
echo     (para funcionarios acessarem pela rede)
echo.
echo Tempo estimado: 15-20 minutos
echo.
echo ============================================================
echo.
pause

cd /d "%~dp0"

echo.
echo [1/5] Verificando Python...
echo.
python --version 2>nul
if errorlevel 1 (
    echo.
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale Python 3.8 ou superior:
    echo https://python.org/downloads
    echo.
    echo Durante instalacao, marque: "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
echo.
echo [OK] Python encontrado!
echo.
pause

echo.
echo [2/5] Criando ambiente virtual...
echo.
if exist venv (
    echo [OK] Ambiente virtual ja existe
) else (
    echo Criando ambiente virtual ^(1-2 minutos^)...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo [ERRO] Falha ao criar ambiente virtual
        echo.
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado!
)
echo.
pause
echo.
echo [3/5] Instalando dependencias...
echo.
echo Isso pode demorar 3-5 minutos. Aguarde...
echo.
call venv\Scripts\activate
echo Aguarde, instalando dependencias...
echo.
pip install Flask openpyxl fpdf2 matplotlib waitress pyinstaller pywebview
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao instalar dependencias
    echo.
    pause
{{ ... }}
)
echo.
echo [OK] Dependencias instaladas!
echo.
pause

echo.
echo [4/5] Criando executaveis com PyInstaller...
echo.
echo ============================================================
echo   ATENCAO: Este processo vai demorar 10-15 minutos!
echo   Serao criados 2 executaveis.
echo   NAO FECHE esta janela!
echo ============================================================
echo.
pause

python build_server.py
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao criar executavel
    echo.
    pause
    exit /b 1
)

echo.
echo [5/5] Verificando resultado...
echo.
if exist dist_servidor\Reparo2Eletro.exe (
    echo [OK] Reparo2Eletro.exe criado!
) else (
    echo [AVISO] Reparo2Eletro.exe nao encontrado
)
if exist dist_servidor\Reparo2Eletro_Server.exe (
    echo [OK] Reparo2Eletro_Server.exe criado!
) else (
    echo [AVISO] Reparo2Eletro_Server.exe nao encontrado
)
echo.
echo Localizacao: %CD%\dist_servidor
echo.

echo.
echo ============================================================
echo              PROCESSO CONCLUIDO!
echo ============================================================
echo.
echo Pasta criada: dist_servidor\
echo.
echo COMO USAR:
echo.
echo MODO DESKTOP (Uso pessoal):
echo  1. Entre na pasta dist_servidor
echo  2. Execute: ABRIR_APLICATIVO.bat
echo     (ou clique em Reparo2Eletro.exe)
echo.
echo MODO SERVIDOR (Compartilhar na rede):
echo  1. Copie pasta "dist_servidor" para o servidor
echo  2. Execute: INICIAR_SERVIDOR.bat
echo     (ou clique em Reparo2Eletro_Server.exe)
echo  3. Compartilhe a URL com funcionarios
echo.
echo ============================================================
echo.

if exist dist_servidor (
    echo Abrindo pasta dist_servidor...
    explorer dist_servidor
)

echo.
echo Pressione qualquer tecla para fechar...
pause >nul
