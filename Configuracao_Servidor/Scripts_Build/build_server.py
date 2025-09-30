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
    print("🔨 CRIANDO BUILD DO SERVIDOR - REPARO2ELETRO")
    print("=" * 70)
    print()
    
    # Limpa builds anteriores
    print("Limpando builds anteriores...")
    for folder in ['build', 'dist_servidor']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  ✓ {folder}/ removido")
    
    print()
    print("Compilando servidor com PyInstaller...")
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
    print("Criando estrutura de distribuição...")
    
    # Cria pasta de distribuição
    os.makedirs('dist_servidor', exist_ok=True)
    
    # Move o executável
    exe_name = 'Reparo2Eletro_Server.exe'
    if os.path.exists(f'dist/{exe_name}'):
        shutil.move(f'dist/{exe_name}', f'dist_servidor/{exe_name}')
        print(f"  ✓ {exe_name} movido")
    
    # Copia arquivos necessários
    arquivos_copiar = [
        'schema.sql',
        'database.db',  # Se existir
    ]
    
    for arquivo in arquivos_copiar:
        if os.path.exists(arquivo):
            shutil.copy(arquivo, 'dist_servidor/')
            print(f"  ✓ {arquivo} copiado")
    
    # Copia pastas necessárias
    pastas_copiar = ['templates', 'static']
    for pasta in pastas_copiar:
        if os.path.exists(pasta):
            shutil.copytree(pasta, f'dist_servidor/{pasta}')
            print(f"  ✓ {pasta}/ copiado")
    
    # Cria README para distribuição
    criar_readme_distribuicao()
    
    # Cria scripts auxiliares
    criar_scripts_distribuicao()
    
    # Limpa pasta build
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    print()
    print("=" * 70)
    print("✅ BUILD CONCLUÍDO COM SUCESSO!")
    print("=" * 70)
    print()
    print(f"📁 Pasta criada: {os.path.abspath('dist_servidor')}")
    print()
    print("📦 PRÓXIMOS PASSOS:")
    print("   1. Copie a pasta 'dist_servidor' para o servidor da empresa")
    print("   2. No servidor, execute: INICIAR_SERVIDOR.bat")
    print("   3. Configure o firewall (se necessário)")
    print()
    print("💡 VANTAGENS:")
    print("   ✓ Não precisa instalar Python no servidor")
    print("   ✓ Não precisa instalar dependências")
    print("   ✓ Basta copiar e executar")
    print("   ✓ Tudo está incluído em um único executável")
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
Tudo está incluído no executável.


═══════════════════════════════════════════════════════════════════════════
  🚀 INÍCIO RÁPIDO
═══════════════════════════════════════════════════════════════════════════

  1. Copie TODA esta pasta para o servidor da empresa

  2. Execute: INICIAR_SERVIDOR.bat
     (Ou clique 2x em: Reparo2Eletro_Server.exe)

  3. Anote a URL que aparecer (exemplo: http://192.168.1.100:5000)

  4. Configure o firewall (se necessário):
     - Execute como Admin: CONFIGURAR_FIREWALL.bat

  5. Compartilhe a URL com seus funcionários


═══════════════════════════════════════════════════════════════════════════
  📁 ARQUIVOS INCLUÍDOS
═══════════════════════════════════════════════════════════════════════════

  Reparo2Eletro_Server.exe  - Executável principal
  templates/                 - Páginas HTML
  static/                    - CSS, JS, imagens
  schema.sql                 - Estrutura do banco
  database.db                - Banco de dados (criado automaticamente)
  
  INICIAR_SERVIDOR.bat       - Atalho para iniciar
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
    print("  ✓ LEIA-ME.txt criado")

def criar_scripts_distribuicao():
    """Cria scripts auxiliares para a distribuição"""
    
    # Script para iniciar servidor
    iniciar = """@echo off
chcp 65001 >nul
echo ============================================================
echo      INICIANDO SERVIDOR REPARO2ELETRO
echo ============================================================
echo.
cd /d "%~dp0"
echo Aguarde...
echo.
Reparo2Eletro_Server.exe
pause
"""
    
    with open('dist_servidor/INICIAR_SERVIDOR.bat', 'w', encoding='utf-8') as f:
        f.write(iniciar)
    print("  ✓ INICIAR_SERVIDOR.bat criado")
    
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
    print("  ✓ CONFIGURAR_FIREWALL.bat criado")
    
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
    print("  ✓ FAZER_BACKUP.bat criado")

if __name__ == '__main__':
    try:
        criar_build_servidor()
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERRO AO CRIAR BUILD")
        print("=" * 70)
        print()
        print(f"Erro: {e}")
        print()
        print("Verifique se você tem PyInstaller instalado:")
        print("  pip install pyinstaller")
        print()
        sys.exit(1)
