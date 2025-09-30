@echo off
chcp 65001 >nul
echo ============================================================
echo      CRIAR DISTRIBUICAO DO SERVIDOR - REPARO2ELETRO
echo ============================================================
echo.

REM Volta para pasta raiz do projeto
cd /d "%~dp0\..\.."

echo [1/4] Verificando ambiente virtual...
if not exist "venv\Scripts\activate.bat" (
    echo X Ambiente virtual nao encontrado!
    echo.
    echo Por favor, execute primeiro: instalar_servidor.bat
    echo.
    pause
    exit /b 1
)
echo OK Ambiente virtual encontrado
echo.

echo [2/4] Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo OK Ambiente ativado
echo.

echo [3/4] Instalando/Verificando PyInstaller...
echo Aguarde, instalando dependencias...
echo.
pip install pyinstaller waitress --quiet
if errorlevel 1 (
    echo X Erro ao instalar PyInstaller
    pause
    exit /b 1
)
echo OK PyInstaller instalado
echo.

echo [4/4] Criando build...
echo ATENCAO: Isso pode demorar 5-10 minutos!
echo.
python build_server.py

if errorlevel 1 (
    echo.
    echo X Erro ao criar build
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo                 OK BUILD CONCLUIDO!
echo ============================================================
echo.
echo  A pasta 'dist_servidor' foi criada com sucesso!
echo.
echo  PROXIMOS PASSOS:
echo.
echo 1. Copie a pasta 'dist_servidor' para o servidor da empresa
echo    ^(Pode usar pendrive, rede compartilhada, etc.^)
echo.
echo 2. No servidor, abra a pasta 'dist_servidor'
echo.
echo 3. Execute: INICIAR_SERVIDOR.bat
echo.
echo  VANTAGENS desta distribuicao:
echo    - Nao precisa Python instalado no servidor
echo    - Nao precisa instalar dependencias
echo    - Basta copiar e executar
echo    - Portavel e independente
echo.
echo ============================================================
echo.
echo Abrindo pasta dist_servidor...
start "" dist_servidor
echo.
pause
