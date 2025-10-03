from app import app, init_db

if __name__ == '__main__':
    print("Inicializando o banco de dados...")
    init_db()
    print("Banco de dados inicializado com sucesso!")
