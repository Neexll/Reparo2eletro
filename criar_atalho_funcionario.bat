@echo off
chcp 65001 >nul
echo ============================================================
echo      CRIAR ATALHO PARA FUNCIONÁRIOS
echo ============================================================
echo.
echo Este script vai criar um atalho .bat que você pode
echo distribuir para seus funcionários.
echo.

cd /d "%~dp0"

REM Detectar IP automaticamente
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4" ^| findstr /v "127.0.0.1"') do (
    set "SERVER_IP=%%a"
    goto :found_ip
)

:found_ip
REM Remove espaços em branco
set "SERVER_IP=%SERVER_IP: =%"

echo IP do Servidor detectado: %SERVER_IP%
echo.

if "%SERVER_IP%"=="" (
    echo ❌ Não foi possível detectar o IP automaticamente.
    echo.
    set /p SERVER_IP="Digite o IP do servidor manualmente: "
)

echo.
echo Criando atalho...

REM Criar arquivo BAT para funcionários
(
echo @echo off
echo start http://%SERVER_IP%:5000/dashboard
echo exit
) > "Abrir_Reparo2Eletro.bat"

echo.
echo ✅ Atalho criado com sucesso!
echo.
echo Arquivo criado: Abrir_Reparo2Eletro.bat
echo.
echo PRÓXIMOS PASSOS:
echo 1. Copie o arquivo "Abrir_Reparo2Eletro.bat" para o desktop dos funcionários
echo 2. Funcionários podem clicar nele para abrir o sistema
echo.
echo Você também pode criar um ícone personalizado:
echo - Clique com botão direito no arquivo
echo - Criar atalho
echo - Clique direito no atalho e escolha "Propriedades"
echo - Clique em "Alterar ícone"
echo.
pause
