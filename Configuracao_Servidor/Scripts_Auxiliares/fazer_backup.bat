@echo off
chcp 65001 >nul
echo ============================================================
echo      BACKUP DO BANCO DE DADOS - REPARO2ELETRO
echo ============================================================
echo.

cd /d "%~dp0"

REM Verifica se o banco de dados existe
if not exist "database.db" (
    echo ❌ ERRO: Banco de dados não encontrado!
    echo.
    echo Certifique-se de que o arquivo database.db existe.
    pause
    exit /b 1
)

REM Cria pasta de backups se não existir
if not exist "backups" mkdir backups

REM Gera nome do arquivo com data e hora
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a-%%b)
set mytime=%mytime: =0%

set backup_name=backups\database_backup_%mydate%_%mytime%.db

echo Criando backup...
echo.
echo Arquivo original: database.db
echo Arquivo backup:   %backup_name%
echo.

REM Copia o arquivo
copy database.db "%backup_name%" >nul

if errorlevel 1 (
    echo ❌ ERRO ao criar backup!
    pause
    exit /b 1
)

echo ✅ Backup criado com sucesso!
echo.
echo Localização: %cd%\%backup_name%
echo.

REM Mostra tamanho do arquivo
for %%I in ("database.db") do echo Tamanho: %%~zI bytes
echo.

REM Lista backups existentes
echo Backups existentes:
echo.
dir /b backups\*.db 2>nul
if errorlevel 1 (
    echo   Nenhum backup anterior encontrado
) else (
    echo.
    echo Total de backups:
    for /f %%i in ('dir /b backups\*.db ^| find /c /v ""') do echo   %%i arquivo(s)
)

echo.
echo ============================================================
echo 💡 DICA: Execute este script regularmente para não perder dados!
echo    Sugestão: Uma vez por semana ou antes de atualizações
echo ============================================================
echo.
pause
