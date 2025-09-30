"""
Servidor Flask para PRODUÇÃO usando Waitress
Melhor performance e estabilidade para múltiplos usuários simultâneos

INSTALAÇÃO:
pip install waitress

USO:
python server_production.py
"""
import os
import sys
import socket

try:
    from waitress import serve
except ImportError:
    print("❌ ERRO: Waitress não está instalado!")
    print("\nPara instalar, execute:")
    print("   pip install waitress")
    print("\nOu use o servidor padrão executando:")
    print("   python server.py")
    sys.exit(1)

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

if __name__ == '__main__':
    # Define o diretório de trabalho
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    local_ip = get_local_ip()
    port = 5000
    threads = 10  # Número de threads para lidar com requisições simultâneas
    
    print("=" * 70)
    print("🖥️  SERVIDOR REPARO2ELETRO - MODO PRODUÇÃO (WAITRESS)")
    print("=" * 70)
    print(f"\n✅ Servidor iniciado com sucesso!")
    print(f"\n📍 IP do Servidor: {local_ip}")
    print(f"📍 Porta: {port}")
    print(f"⚙️  Threads: {threads}")
    print(f"\n🌐 URL de Acesso para Funcionários:")
    print(f"   http://{local_ip}:{port}/dashboard")
    print(f"\n💡 VANTAGENS DO MODO PRODUÇÃO:")
    print(f"   ✓ Maior estabilidade")
    print(f"   ✓ Melhor performance com múltiplos usuários")
    print(f"   ✓ Tratamento adequado de erros")
    print(f"   ✓ Suporta até {threads} requisições simultâneas")
    print(f"\n💡 IMPORTANTE:")
    print(f"   - Compartilhe a URL acima com seus funcionários")
    print(f"   - Certifique-se que o firewall permite conexões na porta {port}")
    print(f"   - Mantenha este terminal aberto enquanto o sistema estiver em uso")
    print(f"   - Pressione Ctrl+C para encerrar o servidor")
    print("=" * 70)
    print("\n🔄 Servidor rodando. Aguardando conexões...\n")
    
    try:
        # Inicia o servidor Waitress
        serve(
            app,
            host='0.0.0.0',  # Permite acesso pela rede
            port=port,
            threads=threads,  # Threads para requisições simultâneas
            channel_timeout=60,  # Timeout de 60 segundos
            cleanup_interval=30,  # Limpeza a cada 30 segundos
            asyncore_use_poll=True  # Melhor performance no Windows
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor encerrado pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ ERRO ao iniciar o servidor: {e}")
        sys.exit(1)
