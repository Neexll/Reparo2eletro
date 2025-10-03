from app import app, init_db, get_db
import sqlite3

def check_tables_exist():
    required_tables = ['pedidos', 'pecas', 'tipos_pecas', 'defeitos_comuns', 'tecnicos']
    missing_tables = []
    
    try:
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            
            # Verifica cada tabela necessária
            for table in required_tables:
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
                if not cursor.fetchone():
                    missing_tables.append(table)
            
            cursor.close()
            db.close()
            
            return missing_tables
    except Exception as e:
        print(f"Erro ao verificar tabelas: {e}")
        return None

def main():
    print("Verificando banco de dados...")
    missing_tables = check_tables_exist()
    
    if missing_tables is None:
        print("Erro ao verificar o banco de dados.")
        return
    
    if missing_tables:
        print(f"Tabelas ausentes: {', '.join(missing_tables)}")
        print("Inicializando banco de dados...")
        try:
            with app.app_context():
                init_db()
            print("Banco de dados inicializado com sucesso!")
        except Exception as e:
            print(f"Erro ao inicializar o banco de dados: {e}")
    else:
        print("Todas as tabelas necessárias existem no banco de dados.")

if __name__ == "__main__":
    main()
