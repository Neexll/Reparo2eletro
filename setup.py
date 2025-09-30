import os
import sys
import shutil
import subprocess
import ctypes
import winreg as reg
from pathlib import Path

def install():
    print("Instalando Reparo2Eletro...")
    
    # Diretório de instalação
    install_dir = os.path.join(os.environ['PROGRAMFILES'], 'Reparo2Eletro')
    
    # Criar diretório de instalação
    os.makedirs(install_dir, exist_ok=True)
    
    # Lista de arquivos a serem copiados
    files_to_copy = [
        'app.py', 'desktop.py', 'database.db', 'schema.sql',
        'requirements.txt', 'start_server.bat', 'start_server.vbs'
    ]
    
    # Copiar arquivos
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(install_dir, file))
    
    # Copiar pasta templates
    if os.path.exists('templates'):
        shutil.copytree('templates', os.path.join(install_dir, 'templates'), 
                       dirs_exist_ok=True)
    
    # Instalar dependências
    print("Instalando dependências...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", 
                         os.path.join(install_dir, 'requirements.txt')])
    
    # Criar atalho na área de trabalho
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    with open(os.path.join(desktop, 'Reparo2Eletro.lnk'), 'w') as f:
        f.write(f'''
[InternetShortcut]
URL=file:///{os.path.join(install_dir, 'start_server.vbs').replace('\\', '/')}
IconFile=C:\\Windows\\System32\\SHELL32.dll,15
IconIndex=0
''')  # 15 é o índice do ícone de pasta
    
    # Configurar inicialização automática
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key2 = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_ALL_ACCESS)
    reg.SetValueEx(key2, 'Reparo2Eletro', 0, reg.REG_SZ, 
                  f'wscript.exe "{os.path.join(install_dir, "start_server.vbs")}"')
    key2.Close()
    
    print(f"\nInstalação concluída! O aplicativo foi instalado em {install_dir}")
    print("Um atalho foi criado na sua área de trabalho.")
    print("O aplicativo será iniciado automaticamente quando você fizer login.")

def create_installer():
    print("Criando instalador...")
    # Criar executável com PyInstaller
    subprocess.check_call([
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=Reparo2Eletro_Installer',
        '--icon=NONE',
        'setup.py'
    ])
    
    # Mover o instalador para a pasta dist
    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    # Copiar arquivos adicionais para a pasta dist
    files_to_include = ['app.py', 'desktop.py', 'requirements.txt', 'schema.sql']
    for file in files_to_include:
        if os.path.exists(file):
            shutil.copy2(file, 'dist')
    
    if os.path.exists('templates'):
        shutil.copytree('templates', 'dist/templates', dirs_exist_ok=True)
    
    print("\nInstalador criado com sucesso na pasta dist!")
    print("Para instalar em outros computadores, execute o arquivo 'Reparo2Eletro_Installer.exe'.")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--create-installer':
        create_installer()
    else:
        # Verificar privilégios de administrador
        try:
            is_admin = os.getuid() == 0
        except AttributeError:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        
        if not is_admin:
            print("Este instalador requer privilégios de administrador.")
            print("Por favor, execute como administrador.")
            input("Pressione Enter para sair...")
            sys.exit(1)
            
        install()
        input("Pressione Enter para sair...")
