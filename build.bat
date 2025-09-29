@echo off
set PYTHONPATH=%~dp0
python -m PyInstaller ^
    --name="Reparo2Eletro" ^
    --onefile ^
    --windowed ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data "database.db;." ^
    --add-data "schema.sql;." ^
    --hidden-import=flask ^
    --hidden-import=flask_sqlalchemy ^
    --hidden-import=openpyxl ^
    --hidden-import=fpdf ^
    --hidden-import=matplotlib ^
    --hidden-import=sqlite3 ^
    --hidden-import=PIL ^
    --hidden-import=PIL._imaging ^
    --hidden-import=PIL._imagingcms ^
    --hidden-import=PIL._imagingft ^
    --hidden-import=PIL._imagingmath ^
    --hidden-import=PIL._imagingmorph ^
    --hidden-import=PIL._imagingtk ^
    --hidden-import=PIL._webp ^
    --hidden-import=numpy ^
    --hidden-import=jinja2 ^
    --hidden-import=markupsafe ^
    --hidden-import=werkzeug ^
    --hidden-import=itsdangerous ^
    --hidden-import=click ^
    --hidden-import=pyparsing ^
    --hidden-import=pytz ^
    --hidden-import=six ^
    --hidden-import=dateutil ^
    --hidden-import=dateutil.zoneinfo ^
    --hidden-import=matplotlib.backends.backend_agg ^
    --hidden-import=matplotlib.pyplot ^
    desktop.py

echo.
echo Compilacao concluida! O arquivo executavel esta em: dist\Reparo2Eletro.exe
echo.
pause
