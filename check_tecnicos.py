from app import app, get_db

def check_tecnicos():
    try:
        with app.app_context():
            db = get_db()
            tecnicos = db.execute('SELECT * FROM tecnicos').fetchall()
            db.close()
            
            if not tecnicos:
                print("Nenhum técnico cadastrado no banco de dados.")
                return False
            
            print("Técnicos cadastrados:")
            for i, tecnico in enumerate(tecnicos, 1):
                print(f"{i}. {tecnico['nome']}")
            
            return True
    except Exception as e:
        print(f"Erro ao verificar técnicos: {e}")
        return False

if __name__ == "__main__":
    print("Verificando técnicos cadastrados...")
    if not check_tecnicos():
        print("\nPor favor, adicione pelo menos um técnico antes de criar um pedido.")
        print("Você pode adicionar um técnico acessando: http://localhost:5000/gerenciar/tecnicos")
