"""
Servidor Flask para uso em rede local/empresa
Execute este arquivo no servidor da empresa para permitir acesso dos funcionários
"""
import os
import sys
import socket
from app import app

def get_local_ip():
    """Obtém o endereço IP local da máquina na rede"""
    try:
        # Cria um socket para conectar a um servidor externo e descobrir o IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Conecta ao servidor DNS do Google
        ip = s.getsockname()[0]  # Obtém o endereço IP local
        s.close()
        return ip
    except Exception:
        # Retorna localhost em caso de erro
        return "127.0.0.1"

if __name__ == '__main__':
    # Define o diretório de trabalho como o diretório do script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Obtém o IP local e define a porta
    local_ip = get_local_ip()
    port = 5000  # Porta padrão do Flask
    
    # Exibe o cabeçalho do servidor
    print("=" * 60)
    print("🖥️  SERVIDOR REPARO2ELETRO - MODO REDE")
    print("=" * 60)
    print(f"\n✅ Servidor iniciado com sucesso!")
    print(f"\n📍 IP do Servidor: {local_ip}")
    print(f"📍 Porta: {port}")
    print(f"\n🌐 URL de Acesso para Funcionários:")
    print(f"   http://{local_ip}:{port}/dashboard")
    print(f"\n💡 IMPORTANTE:")
    print(f"   - Compartilhe a URL acima com seus funcionários")
    print(f"   - Certifique-se que o firewall permite conexões na porta {port}")
    print(f"   - Mantenha este terminal aberto enquanto o sistema estiver em uso")
    print(f"   - Pressione Ctrl+C para encerrar o servidor")
    print("=" * 60)
    print("\n🔄 Aguardando conexões...\n")
    
    # Inicia o servidor Flask acessível pela rede local
    # host='0.0.0.0' permite acesso de qualquer IP na rede
    app.run(
        host='0.0.0.0',  # Permite acesso pela rede
        port=port,
        debug=False,
        threaded=True  # Permite múltiplas conexões simultâneas
    )
