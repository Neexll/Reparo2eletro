import sqlite3
import os

def add_linha_column():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
    
    if not os.path.exists(db_path):
        print("Database file not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar se a coluna já existe
        cursor.execute("PRAGMA table_info(pedidos)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'linha' in columns:
            print("A coluna 'linha' já existe na tabela 'pedidos'.")
            return True
        
        # Adicionar a coluna 'linha' com valor padrão 1
        print("Adicionando a coluna 'linha' à tabela 'pedidos'...")
        cursor.execute("""
        ALTER TABLE pedidos 
        ADD COLUMN linha INTEGER CHECK(linha IN (1, 2, 3, 4)) DEFAULT 1
        """)
        
        # Atualizar registros existentes para terem linha = 1
        cursor.execute("UPDATE pedidos SET linha = 1 WHERE linha IS NULL")
        
        conn.commit()
        print("Coluna 'linha' adicionada com sucesso!")
        return True
        
    except sqlite3.Error as e:
        print(f"Erro ao adicionar a coluna 'linha': {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== Corrigir Estrutura do Banco de Dados ===")
    print("Adicionando a coluna 'linha' à tabela 'pedidos'...")
    
    if add_linha_column():
        print("\nCorreção aplicada com sucesso!")
    else:
        print("\nFalha ao aplicar a correção.")
