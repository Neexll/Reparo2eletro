import threading
import webbrowser
import os
import sys
import socket
from app import app

def get_local_ip():
    """Obtém o endereço IP local da máquina"""
    try:
        # Cria um socket para conectar a um servidor externo
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def resource_path(relative_path):
    """Obtém o caminho absoluto para um recurso, funciona tanto em desenvolvimento quanto no PyInstaller"""
    try:
        # O PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def run_app():
    # Configura o servidor Flask para rodar apenas no localhost (127.0.0.1)
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

def open_browser():
    # Aguarda um pouco para garantir que o servidor esteja rodando
    import time
    time.sleep(2)
    local_ip = get_local_ip()
    url = f'http://{local_ip}:5000/dashboard'
    print(f"\nAcesse o sistema em qualquer dispositivo da rede local usando:")
    print(f"URL: {url}")
    print("Pressione Ctrl+C para encerrar o servidor\n")
    # Abre o navegador padrão na página do dashboard
    webbrowser.open(url)

if __name__ == '__main__':
    # Define o diretório de trabalho para o diretório do script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Inicia o servidor Flask em uma thread separada
    flask_thread = threading.Thread(target=run_app)
    flask_thread.daemon = True
    flask_thread.start()

    # Abre o navegador em uma thread separada
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    # Mantém o programa rodando
    try:
        while True:
            flask_thread.join(1)
    except KeyboardInterrupt:
        print("\nAplicação encerrada pelo usuário")
        sys.exit(0)
