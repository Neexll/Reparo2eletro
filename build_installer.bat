@echo off
echo Criando instalador do Reparo2Eletro...

:: Verificar se o PyInstaller está instalado
pip show pyinstaller >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)

echo Criando executável...
pyinstaller --onefile --windowed --name Reparo2Eletro_Installer setup.py

if %ERRORLEVEL% NEQ 0 (
    echo Erro ao criar o instalador.
    pause
    exit /b 1
)

echo Copiando arquivos para a pasta dist...
if not exist dist mkdir dist

:: Copiar arquivos necessários
copy Reparo2Eletro_Installer.exe dist\ >nul
copy app.py dist\ >nul
copy desktop.py dist\ >nul
copy requirements.txt dist\ >nul
copy schema.sql dist\ >nul
copy README.md dist\ >nul

:: Copiar pastas
xcopy /E /I /Y templates dist\templates >nul
xcopy /E /I /Y static dist\static >nul

echo.
echo Instalador criado com sucesso na pasta dist!
echo.
echo Para instalar em outros computadores, execute o arquivo 'dist\Reparo2Eletro_Installer.exe' como administrador.
echo.
pause
