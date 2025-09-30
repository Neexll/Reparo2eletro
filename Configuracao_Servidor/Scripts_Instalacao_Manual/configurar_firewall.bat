@echo off
echo ============================================================
echo      CONFIGURAR FIREWALL - REPARO2ELETRO
echo ============================================================
echo.
echo Este script vai liberar a porta 5000 no Firewall do Windows
echo para permitir que seus funcionarios acessem o sistema.
echo.
echo IMPORTANTE: Execute este arquivo como ADMINISTRADOR
echo (Clique com botao direito > Executar como Administrador)
echo.
pause

echo.
echo Configurando regra no firewall...
echo.

netsh advfirewall firewall add rule name="Reparo2Eletro Server" dir=in action=allow protocol=TCP localport=5000 >nul 2>&1

if errorlevel 1 (
    echo.
    echo ❌ ERRO: Nao foi possivel configurar o firewall.
    echo.
    echo Possíveis causas:
    echo - Voce nao executou como Administrador
    echo - A regra ja existe
    echo.
    echo Tente executar manualmente no PowerShell como Admin:
    echo New-NetFirewallRule -DisplayName "Reparo2Eletro" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
    echo.
) else (
    echo.
    echo ✅ SUCESSO! Firewall configurado.
    echo.
    echo A porta 5000 agora esta liberada para conexoes.
    echo Seus funcionarios poderao acessar o sistema pela rede.
    echo.
)

echo.
pause
