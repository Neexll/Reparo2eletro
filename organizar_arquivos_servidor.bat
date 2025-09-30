@echo off
chcp 65001 >nul
echo ============================================================
echo      ORGANIZANDO ARQUIVOS DE SERVIDOR
echo ============================================================
echo.

cd /d "%~dp0"

REM Cria pasta principal
if not exist "Configuracao_Servidor" mkdir "Configuracao_Servidor"

REM Cria subpastas
if not exist "Configuracao_Servidor\Documentacao" mkdir "Configuracao_Servidor\Documentacao"
if not exist "Configuracao_Servidor\Scripts_Build" mkdir "Configuracao_Servidor\Scripts_Build"
if not exist "Configuracao_Servidor\Scripts_Instalacao_Manual" mkdir "Configuracao_Servidor\Scripts_Instalacao_Manual"
if not exist "Configuracao_Servidor\Scripts_Auxiliares" mkdir "Configuracao_Servidor\Scripts_Auxiliares"

echo Copiando arquivos...
echo.

REM ===== GUIAS E DOCUMENTAÇÃO =====
echo [1/4] Copiando documentação...

copy "LEIA_PRIMEIRO.txt" "Configuracao_Servidor\" >nul 2>&1
copy "QUAL_METODO_ESCOLHER.txt" "Configuracao_Servidor\Documentacao\" >nul 2>&1
copy "RESUMO_FINAL.txt" "Configuracao_Servidor\Documentacao\" >nul 2>&1
copy "COMECE_AQUI.txt" "Configuracao_Servidor\Documentacao\" >nul 2>&1
copy "GUIA_RAPIDO.txt" "Configuracao_Servidor\Documentacao\" >nul 2>&1
copy "GUIA_BUILD_DISTRIBUICAO.md" "Configuracao_Servidor\Documentacao\" >nul 2>&1
copy "GUIA_INSTALACAO_SERVIDOR.md" "Configuracao_Servidor\Documentacao\" >nul 2>&1
copy "README_SERVIDOR.txt" "Configuracao_Servidor\Documentacao\" >nul 2>&1
copy "INDICE_ARQUIVOS.txt" "Configuracao_Servidor\Documentacao\" >nul 2>&1

REM ===== SCRIPTS DE BUILD =====
echo [2/4] Copiando scripts de build...

copy "build_server.bat" "Configuracao_Servidor\Scripts_Build\" >nul 2>&1
copy "build_server.py" "Configuracao_Servidor\Scripts_Build\" >nul 2>&1
copy "requirements_production.txt" "Configuracao_Servidor\Scripts_Build\" >nul 2>&1

REM ===== SCRIPTS DE INSTALAÇÃO MANUAL =====
echo [3/4] Copiando scripts de instalação manual...

copy "instalar_servidor.bat" "Configuracao_Servidor\Scripts_Instalacao_Manual\" >nul 2>&1
copy "configurar_firewall.bat" "Configuracao_Servidor\Scripts_Instalacao_Manual\" >nul 2>&1
copy "testar_configuracao.bat" "Configuracao_Servidor\Scripts_Instalacao_Manual\" >nul 2>&1
copy "start_server_network.bat" "Configuracao_Servidor\Scripts_Instalacao_Manual\" >nul 2>&1
copy "server.py" "Configuracao_Servidor\Scripts_Instalacao_Manual\" >nul 2>&1
copy "server_production.py" "Configuracao_Servidor\Scripts_Instalacao_Manual\" >nul 2>&1

REM ===== SCRIPTS AUXILIARES =====
echo [4/4] Copiando scripts auxiliares...

copy "criar_atalho_funcionario.bat" "Configuracao_Servidor\Scripts_Auxiliares\" >nul 2>&1
copy "fazer_backup.bat" "Configuracao_Servidor\Scripts_Auxiliares\" >nul 2>&1
copy "EXEMPLO_ATALHO_FUNCIONARIOS.html" "Configuracao_Servidor\Scripts_Auxiliares\" >nul 2>&1

REM ===== CRIAR README NA PASTA =====
(
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║          REPARO2ELETRO - CONFIGURAÇÃO DE SERVIDOR            ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo.
echo 🎯 COMECE POR AQUI
echo ══════════════════════════════════════════════════════════════
echo.
echo 1. Leia: LEIA_PRIMEIRO.txt
echo.
echo 2. Escolha seu método:
echo    → Documentacao\QUAL_METODO_ESCOLHER.txt
echo.
echo 3. Execute os scripts da pasta correspondente:
echo    → Scripts_Build\             (para Build Executável^)
echo    → Scripts_Instalacao_Manual\ (para Instalação Manual^)
echo.
echo.
echo 📁 ESTRUTURA DAS PASTAS
echo ══════════════════════════════════════════════════════════════
echo.
echo Configuracao_Servidor\
echo ├─ LEIA_PRIMEIRO.txt            ← COMECE AQUI! ⭐
echo ├─ Documentacao\                ← Todos os guias
echo ├─ Scripts_Build\               ← Para criar executável
echo ├─ Scripts_Instalacao_Manual\   ← Para instalar com Python
echo └─ Scripts_Auxiliares\          ← Atalhos e backups
echo.
echo.
echo ⚡ ATALHO RÁPIDO
echo ══════════════════════════════════════════════════════════════
echo.
echo Quer a solução MAIS FÁCIL?
echo.
echo → Vá para: Scripts_Build\
echo → Execute: build_server.bat
echo → Aguarde criar a pasta dist_servidor
echo → Copie para o servidor e execute INICIAR_SERVIDOR.bat
echo.
echo ✅ PRONTO!
echo.
echo.
echo Versão: 1.0 ^| Data: 30/09/2025
) > "Configuracao_Servidor\README.txt"

echo.
echo ============================================================
echo                 ✅ ORGANIZAÇÃO CONCLUÍDA!
echo ============================================================
echo.
echo 📁 Pasta criada: Configuracao_Servidor\
echo.
echo 📂 Estrutura:
echo    ├─ LEIA_PRIMEIRO.txt (COMECE AQUI!)
echo    ├─ Documentacao\
echo    ├─ Scripts_Build\
echo    ├─ Scripts_Instalacao_Manual\
echo    └─ Scripts_Auxiliares\
echo.
echo 🎯 Próximo passo:
echo    Abra a pasta e leia: LEIA_PRIMEIRO.txt
echo.
echo ============================================================
echo.

REM Abre a pasta criada
start "" "Configuracao_Servidor"

pause
