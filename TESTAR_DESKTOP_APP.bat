@echo off
title TESTAR APLICATIVO DESKTOP - REPARO2ELETRO
color 0A
echo.
echo ============================================================
echo      TESTAR APLICATIVO DESKTOP COM EXPORTACAO
echo ============================================================
echo.
echo Este script vai iniciar o aplicativo desktop com
echo janela nativa para testar a exportacao de arquivos.
echo.
echo FUNCIONALIDADES A TESTAR:
echo  1. Janela nativa (nao navegador)
echo  2. Exportacao Excel (com dialogo de salvar)
echo  3. Exportacao PDF (com dialogo de salvar)
echo  4. Renomear arquivo ao salvar
echo.
echo ============================================================
echo.
pause

cd /d "%~dp0"

echo.
echo Instalando pywebview (se necessario)...
echo.
pip install pywebview --quiet

echo.
echo Iniciando aplicativo desktop...
echo.
python desktop_app.py

pause
