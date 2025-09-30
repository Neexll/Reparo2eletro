"""
Aplicativo Desktop com Interface Gráfica
Usa pywebview para criar uma janela nativa ao invés de abrir no navegador
"""
import threading
import os
import sys
import time
import socket
import sqlite3
import base64
from app import app

def get_local_ip():
    """Obtém o endereço IP local da máquina"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def init_database():
    """Inicializa o banco de dados se não existir"""
    db_path = 'database.db'
    
    # Se o banco já existe, não faz nada
    if os.path.exists(db_path):
        # Verifica se tem tabelas
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            conn.close()
            
            if len(tables) > 0:
                print(f"Banco de dados OK ({len(tables)} tabelas)")
                return
        except:
            pass
    
    # Cria o banco de dados
    print("Criando banco de dados...")
    try:
        # Lê o schema
        schema_path = 'schema.sql'
        if not os.path.exists(schema_path):
            # Tenta path alternativo (PyInstaller)
            import sys
            if hasattr(sys, '_MEIPASS'):
                schema_path = os.path.join(sys._MEIPASS, 'schema.sql')
        
        if os.path.exists(schema_path):
            conn = sqlite3.connect(db_path)
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = f.read()
            conn.executescript(schema)
            conn.commit()
            conn.close()
            print("Banco de dados criado com sucesso!")
        else:
            print("AVISO: schema.sql não encontrado. Banco pode estar vazio.")
    except Exception as e:
        print(f"Erro ao criar banco: {e}")

class Api:
    """API exposta ao JavaScript para salvar arquivos"""
    
    def save_file(self, base64_data, default_filename):
        """
        Salva um arquivo recebido como base64
        Abre diálogo para o usuário escolher onde salvar
        """
        try:
            import webview
            
            # Decodifica o base64
            file_data = base64.b64decode(base64_data)
            
            # Determina o tipo de arquivo pela extensão
            if default_filename.endswith('.xlsx'):
                file_types = ('Excel Files (*.xlsx)', 'All files (*.*)')
            elif default_filename.endswith('.pdf'):
                file_types = ('PDF Files (*.pdf)', 'All files (*.*)')
            else:
                file_types = ('All files (*.*)',)
            
            # Abre diálogo para salvar arquivo
            result = webview.windows[0].create_file_dialog(
                webview.SAVE_DIALOG,
                directory=os.path.expanduser('~'),
                save_filename=default_filename,
                file_types=file_types
            )
            
            if result:
                # Salva o arquivo
                file_path = result if isinstance(result, str) else result[0]
                with open(file_path, 'wb') as f:
                    f.write(file_data)
                return {'status': 'success', 'path': file_path}
            else:
                return {'status': 'cancelled'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

def run_flask():
    """Inicia o servidor Flask"""
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False, threaded=True)

def main():
    # Define o diretório de trabalho
    try:
        # Se for PyInstaller, usa o diretório do executável
        if hasattr(sys, '_MEIPASS'):
            # Muda para o diretório onde está o executável
            os.chdir(os.path.dirname(sys.executable))
        else:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass
    
    # Inicializa banco de dados
    init_database()
    
    # Inicia o servidor Flask em uma thread separada
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Aguarda o Flask iniciar
    time.sleep(2)
    
    try:
        # Tenta usar pywebview (janela nativa)
        import webview
        
        print("=" * 60)
        print("  REPARO2ELETRO - APLICATIVO DESKTOP")
        print("=" * 60)
        print("\nIniciando interface gráfica...")
        print("Aguarde alguns segundos...\n")
        
        # Cria a instância da API
        api = Api()
        
        # Cria a janela do aplicativo
        window = webview.create_window(
            'Reparo2Eletro',
            'http://127.0.0.1:5000/dashboard',
            width=1400,
            height=900,
            resizable=True,
            fullscreen=False,
            min_size=(1024, 768),
            js_api=api
        )
        
        # Inicia a interface gráfica
        webview.start()
        
    except ImportError:
        # Se pywebview não estiver instalado, abre no navegador
        print("=" * 60)
        print("  REPARO2ELETRO - MODO NAVEGADOR")
        print("=" * 60)
        print("\nPywebview não instalado. Abrindo no navegador...")
        print("\nPara usar modo desktop, instale:")
        print("  pip install pywebview")
        print()
        
        import webbrowser
        url = 'http://127.0.0.1:5000/dashboard'
        print(f"Abrindo: {url}\n")
        webbrowser.open(url)
        
        # Mantém o programa rodando
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nAplicação encerrada")
            sys.exit(0)

if __name__ == '__main__':
    main()
