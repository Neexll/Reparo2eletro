@echo off
title TESTAR EXPORTACAO - REPARO2ELETRO
color 0A
echo.
echo ============================================================
echo      TESTAR BOTOES DE EXPORTACAO EXCEL E PDF
echo ============================================================
echo.
echo Este script vai iniciar o aplicativo para voce testar
echo os botoes de exportacao que foram corrigidos.
echo.
echo ============================================================
echo.
pause

cd /d "%~dp0"

echo.
echo [1/2] Iniciando aplicativo...
echo.

start "" cmd /k "python desktop.py"

timeout /t 3 >nul

echo [2/2] Abrindo navegador...
echo.

start http://127.0.0.1:5000/dashboard

echo.
echo ============================================================
echo              APLICATIVO INICIADO!
echo ============================================================
echo.
echo O aplicativo esta rodando e o navegador foi aberto.
echo.
echo AGORA:
echo.
echo 1. Va para o Dashboard (se nao abriu automaticamente)
echo.
echo 2. Clique em "Exportar para Excel"
echo    - O arquivo relatorio.xlsx deve baixar
echo.
echo 3. Clique em "Exportar para PDF"
echo    - O arquivo relatorio.pdf deve baixar
echo.
echo 4. Verifique sua pasta Downloads!
echo.
echo ============================================================
echo.
echo Para ENCERRAR o aplicativo:
echo   - Feche o outro terminal (Python)
echo   - Ou pressione Ctrl+C la
echo.
echo ============================================================
echo.
pause
