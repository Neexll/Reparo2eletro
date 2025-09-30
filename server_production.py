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
import sqlite3

try:
    from waitress import serve
except ImportError:
    print("ERRO: Waitress nao esta instalado!")
    print("\nPara instalar, execute:")
    print("   pip install waitress")
    print("\nOu use o servidor padrao executando:")
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

def init_database():
    """Inicializa o banco de dados se não existir"""
    db_path = 'database.db'
    
    # Se o banco já existe e tem tabelas, não faz nada
    if os.path.exists(db_path):
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
        schema_path = 'schema.sql'
        if not os.path.exists(schema_path):
            if hasattr(sys, '_MEIPASS'):
                schema_path = os.path.join(sys._MEIPASS, 'schema.sql')
        
        if os.path.exists(schema_path):
            conn = sqlite3.connect(db_path)
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = f.read()
            conn.executescript(schema)
            conn.commit()
            conn.close()
            print("Banco de dados criado!")
        else:
            print("AVISO: schema.sql nao encontrado")
    except Exception as e:
        print(f"Erro ao criar banco: {e}")

if __name__ == '__main__':
    # Define o diretório de trabalho
    try:
        if hasattr(sys, '_MEIPASS'):
            os.chdir(os.path.dirname(sys.executable))
        else:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass
    
    # Inicializa banco de dados
    init_database()
    
    local_ip = get_local_ip()
    port = 5000
    threads = 10  # Número de threads para lidar com requisições simultâneas
    
    print("=" * 70)
    print("SERVIDOR REPARO2ELETRO - MODO PRODUCAO (WAITRESS)")
    print("=" * 70)
    print(f"\nServidor iniciado com sucesso!")
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
