@echo off
echo ============================================================
echo      TESTAR FUNCOES DE EXPORTACAO
echo ============================================================
echo.
echo Testando se as rotas de exportacao estao funcionando...
echo.
cd /d "%~dp0"

python -c "from app import app; print('Rotas disponiveis:'); [print(f'  - {rule}') for rule in app.url_map.iter_rules() if 'export' in str(rule)]"

echo.
echo Se apareceram rotas /export e /export/pdf, esta OK!
echo.
pause
