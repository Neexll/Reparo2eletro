import sqlite3

def add_sample_data():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Limpa as tabelas
        cursor.execute("DELETE FROM tecnicos")
        cursor.execute("DELETE FROM tipos_pecas")
        cursor.execute("DELETE FROM defeitos_comuns")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('tecnicos', 'tipos_pecas', 'defeitos_comuns')")
        
        # Adiciona um técnico de exemplo
        cursor.execute("INSERT INTO tecnicos (nome) VALUES (?)", ("Técnico 1",))
        
        # Adiciona um tipo de peça de exemplo
        cursor.execute("INSERT INTO tipos_pecas (nome) VALUES (?)", ("Placa Mãe H61",))
        tipo_peca_id = cursor.lastrowid
        
        # Adiciona alguns defeitos comuns para a peça
        defeitos = [
            ("Não liga", tipo_peca_id),
            ("Sem vídeo", tipo_peca_id),
            ("Reiniciando sozinho", tipo_peca_id)
        ]
        cursor.executemany("INSERT INTO defeitos_comuns (descricao, tipo_peca_id) VALUES (?, ?)", defeitos)
        
        conn.commit()
        print("Dados de exemplo adicionados com sucesso!")
        
    except Exception as e:
        print(f"Erro ao adicionar dados de exemplo: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Adicionando dados de exemplo...")
    add_sample_data()
