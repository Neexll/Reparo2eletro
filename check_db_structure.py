import sqlite3
import os

def check_database_structure():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
    
    if not os.path.exists(db_path):
        print("Database file not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tabelas existentes
        print("\n=== Tabelas no banco de dados ===")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            print(f"\nTabela: {table[0]}")
            
            # Verificar colunas de cada tabela
            cursor.execute(f"PRAGMA table_info({table[0]})")
            columns = cursor.fetchall()
            print("Colunas:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
        
        # Verificar dados na tabela pedidos
        try:
            cursor.execute("SELECT * FROM pedidos LIMIT 1")
            pedido_sample = cursor.fetchone()
            if pedido_sample:
                print("\n=== Exemplo de dados na tabela pedidos ===")
                cursor.execute("PRAGMA table_info(pedidos)")
                columns = [col[1] for col in cursor.fetchall()]
                print(dict(zip(columns, pedido_sample)))
        except sqlite3.Error as e:
            print(f"\nErro ao acessar a tabela pedidos: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"Erro ao verificar o banco de dados: {e}")

if __name__ == "__main__":
    print("=== Verificação da Estrutura do Banco de Dados ===")
    check_database_structure()
