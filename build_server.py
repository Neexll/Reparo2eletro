"""
Script para criar distribuição do servidor
Gera um executável independente que não precisa de Python instalado
"""
import PyInstaller.__main__
import os
import shutil
import sys

def criar_build_servidor():
    print("=" * 70)
    print("CRIANDO BUILD DO SERVIDOR - REPARO2ELETRO")
    print("=" * 70)
    print()
    
    # Limpa builds anteriores
    print("Limpando builds anteriores...")
    import time
    for folder in ['build', 'dist_servidor', 'dist']:
        if os.path.exists(folder):
            try:
                # Tenta remover várias vezes (caso esteja bloqueado)
                for tentativa in range(3):
                    try:
                        shutil.rmtree(folder)
                        print(f"  OK {folder}/ removido")
                        break
                    except PermissionError:
                        if tentativa < 2:
                            print(f"  AVISO {folder}/ bloqueado, aguardando...")
                            time.sleep(2)
                        else:
                            print(f"  AVISO {folder}/ nao pode ser removido (esta em uso)")
                            print(f"     Por favor, feche todos os programas e tente novamente")
                            sys.exit(1)
            except Exception as e:
                print(f"  AVISO Erro ao remover {folder}/: {e}")
    
    print()
    print("=" * 70)
    print("PASSO 1/2: Compilando SERVIDOR (Reparo2Eletro_Server.exe)")
    print("=" * 70)
    print()
    print("Isso pode demorar alguns minutos...")
    print()
    
    # Configurações do PyInstaller
    PyInstaller.__main__.run([
        'server_production.py',              # Arquivo principal
        '--name=Reparo2Eletro_Server',       # Nome do executável
        '--onefile',                          # Tudo em um arquivo
        '--console',                          # Mantém console visível
        '--icon=NONE',                        # Sem ícone personalizado
        '--add-data=templates;templates',     # Inclui templates
        '--add-data=static;static',           # Inclui arquivos estáticos
        '--add-data=schema.sql;.',            # Inclui schema
        '--hidden-import=waitress',           # Importações ocultas
        '--hidden-import=flask',
        '--hidden-import=openpyxl',
        '--hidden-import=fpdf',
        '--hidden-import=matplotlib',
        '--collect-all=flask',
        '--collect-all=jinja2',
        '--collect-all=werkzeug',
        '--noconfirm',                        # Não pedir confirmação
    ])
    
    print()
    print("=" * 70)
    print("PASSO 2/2: Compilando APLICATIVO DESKTOP (Reparo2Eletro.exe)")
    print("=" * 70)
    print()
    
    # Compila o aplicativo desktop
    PyInstaller.__main__.run([
        'desktop_app.py',                     # Arquivo principal
        '--name=Reparo2Eletro',               # Nome do executável
        '--onefile',                          # Tudo em um arquivo
        '--windowed',                         # Sem console (modo janela)
        '--icon=NONE',                        # Sem ícone personalizado
        '--add-data=templates;templates',     # Inclui templates
        '--add-data=static;static',           # Inclui arquivos estáticos
        '--add-data=schema.sql;.',            # Inclui schema
        '--hidden-import=flask',
        '--hidden-import=openpyxl',
        '--hidden-import=fpdf',
        '--hidden-import=matplotlib',
        '--hidden-import=webbrowser',
        '--hidden-import=threading',
        '--hidden-import=webview',
        '--hidden-import=webview.platforms.winforms',
        '--collect-all=flask',
        '--collect-all=jinja2',
        '--collect-all=werkzeug',
        '--collect-all=webview',
        '--noconfirm',                        # Não pedir confirmação
    ])
    
    print()
    print("Criando estrutura de distribuição...")
    
    # Cria pasta de distribuição
    os.makedirs('dist_servidor', exist_ok=True)
    
    # Move os executáveis
    exe_server = 'Reparo2Eletro_Server.exe'
    exe_desktop = 'Reparo2Eletro.exe'
    
    if os.path.exists(f'dist/{exe_server}'):
        shutil.move(f'dist/{exe_server}', f'dist_servidor/{exe_server}')
        print(f"  OK {exe_server} movido")
    
    if os.path.exists(f'dist/{exe_desktop}'):
        shutil.move(f'dist/{exe_desktop}', f'dist_servidor/{exe_desktop}')
        print(f"  OK {exe_desktop} movido")
    
    # Copia arquivos necessários
    arquivos_copiar = [
        'schema.sql',
        'database.db',  # Se existir
    ]
    
    for arquivo in arquivos_copiar:
        if os.path.exists(arquivo):
            shutil.copy(arquivo, 'dist_servidor/')
            print(f"  OK {arquivo} copiado")
    
    # Copia pastas necessárias
    pastas_copiar = ['templates', 'static']
    for pasta in pastas_copiar:
        if os.path.exists(pasta):
            shutil.copytree(pasta, f'dist_servidor/{pasta}')
            print(f"  OK {pasta}/ copiado")
    
    # Cria README para distribuição
    criar_readme_distribuicao()
    
    # Cria scripts auxiliares
    criar_scripts_distribuicao()
    
    # Cria atalhos de inicialização
    criar_atalhos_inicializacao()
    
    # Limpa pasta build
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    print()
    print("=" * 70)
    print("BUILD CONCLUIDO COM SUCESSO!")
    print("=" * 70)
    print()
    print(f"Pasta criada: {os.path.abspath('dist_servidor')}")
    print()
    print("PROXIMOS PASSOS:")
    print("   1. Copie a pasta 'dist_servidor' para o servidor da empresa")
    print("   2. No servidor, execute: INICIAR_SERVIDOR.bat")
    print("   3. Configure o firewall (se necessario)")
    print()
    print("VANTAGENS:")
    print("   - Nao precisa instalar Python no servidor")
    print("   - Nao precisa instalar dependencias")
    print("   - Basta copiar e executar")
    print("   - Tudo esta incluido nos executaveis")
    print()

def criar_readme_distribuicao():
    """Cria README para a pasta de distribuição"""
    readme = """╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║            🎯 REPARO2ELETRO - DISTRIBUIÇÃO PARA SERVIDOR                 ║
║                         Versão Portátil                                   ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝


✅ ESTA É UMA VERSÃO COMPLETA E PORTÁTIL!

Não precisa instalar Python ou dependências.
Tudo está incluído nos executáveis.

DOIS MODOS DE USO:
• MODO DESKTOP: Para usar apenas no computador local
• MODO SERVIDOR: Para compartilhar com funcionários na rede


═══════════════════════════════════════════════════════════════════════════
  🚀 MODO DESKTOP (Uso Pessoal)
═══════════════════════════════════════════════════════════════════════════

  Para usar apenas no seu computador:

  1. Execute: ABRIR_APLICATIVO.bat
     (Ou clique 2x em: Reparo2Eletro.exe)

  2. O navegador abrirá automaticamente

  3. Use o sistema normalmente


═══════════════════════════════════════════════════════════════════════════
  🌐 MODO SERVIDOR (Compartilhar na Rede)
═══════════════════════════════════════════════════════════════════════════

  Para que funcionários acessem pela rede:

  1. Execute: INICIAR_SERVIDOR.bat
     (Ou clique 2x em: Reparo2Eletro_Server.exe)

  2. Anote a URL que aparecer (exemplo: http://192.168.1.100:5000)

  3. Configure o firewall (se necessário):
     - Execute como Admin: CONFIGURAR_FIREWALL.bat

  4. Compartilhe a URL com seus funcionários


═══════════════════════════════════════════════════════════════════════════
  📁 ARQUIVOS INCLUÍDOS
═══════════════════════════════════════════════════════════════════════════

  Reparo2Eletro.exe          - Aplicativo Desktop (abre navegador)
  Reparo2Eletro_Server.exe   - Servidor de Rede (para funcionários)
  templates/                 - Páginas HTML
  static/                    - CSS, JS, imagens
  schema.sql                 - Estrutura do banco
  database.db                - Banco de dados (criado automaticamente)
  
  ABRIR_APLICATIVO.bat       - Abre o aplicativo desktop
  INICIAR_SERVIDOR.bat       - Inicia servidor na rede
  CONFIGURAR_FIREWALL.bat    - Configura firewall
  FAZER_BACKUP.bat           - Backup do banco


═══════════════════════════════════════════════════════════════════════════
  ⚠️ IMPORTANTE
═══════════════════════════════════════════════════════════════════════════

  ✓ Mantenha a janela do servidor aberta
  ✓ Servidor e funcionários devem estar na mesma rede
  ✓ Faça backup regular do arquivo database.db
  ✓ Porta 5000 deve estar liberada no firewall


═══════════════════════════════════════════════════════════════════════════
  🆘 PROBLEMAS?
═══════════════════════════════════════════════════════════════════════════

  Erro: "Porta já em uso"
  → Execute: netstat -ano | findstr :5000
  → Feche o programa que está usando a porta

  Funcionários não conseguem acessar
  → Verifique se estão na mesma rede
  → Configure o firewall: CONFIGURAR_FIREWALL.bat
  → Confirme o IP do servidor: ipconfig

  Antivírus bloqueando
  → Adicione exceção para Reparo2Eletro_Server.exe
  → Isso é normal com executáveis do PyInstaller


═══════════════════════════════════════════════════════════════════════════

                    Versão: 1.0 | Data: 30/09/2025

═══════════════════════════════════════════════════════════════════════════
"""
    
    with open('dist_servidor/LEIA-ME.txt', 'w', encoding='utf-8') as f:
        f.write(readme)
    print("  OK LEIA-ME.txt criado")

def criar_atalhos_inicializacao():
    """Cria atalhos para abrir o aplicativo facilmente"""
    
    # Atalho para aplicativo desktop
    atalho_desktop = """@echo off
echo ============================================================
echo      ABRINDO REPARO2ELETRO - MODO DESKTOP
echo ============================================================
echo.
cd /d "%~dp0"
start "" Reparo2Eletro.exe
exit
"""
    
    with open('dist_servidor/ABRIR_APLICATIVO.bat', 'w', encoding='utf-8') as f:
        f.write(atalho_desktop)
    print("  OK ABRIR_APLICATIVO.bat criado")

def criar_scripts_distribuicao():
    """Cria scripts auxiliares para a distribuição"""
    
    # Script para iniciar servidor
    iniciar = """@echo off
chcp 65001 >nul
echo ============================================================
echo      INICIANDO SERVIDOR REPARO2ELETRO - MODO REDE
echo ============================================================
echo.
echo Este modo permite que funcionarios acessem pela rede.
echo.
cd /d "%~dp0"
echo Aguarde...
echo.
Reparo2Eletro_Server.exe
pause
"""
    
    with open('dist_servidor/INICIAR_SERVIDOR.bat', 'w', encoding='utf-8') as f:
        f.write(iniciar)
    print("  OK INICIAR_SERVIDOR.bat criado")
    
    # Script para configurar firewall
    firewall = """@echo off
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
"""
    
    with open('dist_servidor/CONFIGURAR_FIREWALL.bat', 'w', encoding='utf-8') as f:
        f.write(firewall)
    print("  OK CONFIGURAR_FIREWALL.bat criado")
    
    # Script para fazer backup
    backup = """@echo off
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

set backup_name=backups\\database_%mydate%_%mytime%.db

copy database.db "%backup_name%" >nul

if errorlevel 1 (
    echo ❌ Erro ao criar backup
) else (
    echo ✅ Backup criado: %backup_name%
)
echo.
pause
"""
    
    with open('dist_servidor/FAZER_BACKUP.bat', 'w', encoding='utf-8') as f:
        f.write(backup)
    print("  OK FAZER_BACKUP.bat criado")

if __name__ == '__main__':
    try:
        criar_build_servidor()
    except Exception as e:
        print()
        print("=" * 70)
        print("ERRO AO CRIAR BUILD")
        print("=" * 70)
        print()
        print(f"Erro: {e}")
        print()
        print("Verifique se voce tem PyInstaller instalado:")
        print("  pip install pyinstaller")
        print()
        sys.exit(1)
