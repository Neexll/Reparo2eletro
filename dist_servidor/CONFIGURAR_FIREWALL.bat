@echo off
echo ============================================================
echo      CONFIGURAR FIREWALL - REPARO2ELETRO
echo ============================================================
echo.
echo Execute como ADMINISTRADOR!
echo.
pause
echo.
netsh advfirewall firewall add rule name="Reparo2Eletro Server" dir=in action=allow protocol=TCP localport=5000 >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO ao configurar firewall
    echo Certifique-se de executar como Administrador
) else (
    echo ✅ Firewall configurado com sucesso!
    echo Porta 5000 liberada.
)
echo.
pause
