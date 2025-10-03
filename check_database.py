import sqlite3

def check_tables():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Verifica se as tabelas existem
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("\nTabelas no banco de dados:")
        for table in tables:
            print(f"- {table[0]}")
        
        # Conta o número de registros em cada tabela
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"\nRegistros em '{table_name}': {count}")
            
            # Mostra os primeiros 5 registros de cada tabela
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                columns = [description[0] for description in cursor.description]
                print("Colunas:", ", ".join(columns))
                print("Primeiros registros:")
                for row in cursor.fetchall():
                    print(row)
        
        conn.close()
    except Exception as e:
        print(f"Erro ao verificar o banco de dados: {e}")

if __name__ == "__main__":
    print("Verificando banco de dados...")
    check_tables()
