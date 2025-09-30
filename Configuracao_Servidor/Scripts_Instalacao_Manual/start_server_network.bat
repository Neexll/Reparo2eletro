@echo off
echo ============================================================
echo      INICIANDO SERVIDOR REPARO2ELETRO - MODO REDE
echo ============================================================
echo.
cd /d "%~dp0"

REM Verifica se o ambiente virtual existe
if exist "venv\Scripts\activate.bat" (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate.bat
) else (
    echo AVISO: Ambiente virtual nao encontrado.
    echo Usando Python global...
    echo.
)

echo Iniciando servidor...
echo.
python server.py

pause
