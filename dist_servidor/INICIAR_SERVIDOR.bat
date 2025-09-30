@echo off
chcp 65001 >nul
echo ============================================================
echo      INICIANDO SERVIDOR REPARO2ELETRO - MODO REDE
echo ============================================================
echo.
echo Este modo permite que funcionarios acessem pela rede.
echo.
cd /d "%~dp0"
echo Aguarde...
echo.
Reparo2Eletro_Server.exe
pause
