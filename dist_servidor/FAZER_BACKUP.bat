@echo off
chcp 65001 >nul
echo ============================================================
echo      BACKUP DO BANCO DE DADOS
echo ============================================================
echo.
cd /d "%~dp0"

if not exist "database.db" (
    echo ❌ Banco de dados não encontrado!
    pause
    exit /b 1
)

if not exist "backups" mkdir backups

for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a-%%b)
set mytime=%mytime: =0%

set backup_name=backups\database_%mydate%_%mytime%.db

copy database.db "%backup_name%" >nul

if errorlevel 1 (
    echo ❌ Erro ao criar backup
) else (
    echo ✅ Backup criado: %backup_name%
)
echo.
pause
