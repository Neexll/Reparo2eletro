#!/usr/bin/env python3
import sqlite3

def populate_initial_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        # Adicionar técnicos iniciais
        tecnicos = [
            'João Silva',
            'Maria Santos',
            'Carlos Oliveira',
            'Ana Costa',
            'Pedro Lima',
            'Lucia Ferreira',
            'Roberto Alves',
            'Isabela Rocha'
        ]

        print("Inserindo técnicos...")
        for tecnico in tecnicos:
            try:
                cursor.execute('INSERT INTO tecnicos (nome) VALUES (?)', (tecnico,))
                print(f"  OK: {tecnico}")
            except sqlite3.IntegrityError:
                print(f"  - {tecnico} já existe")

        # Adicionar tipos de peças comuns
        tipos_pecas = [
            ('Placa de Vídeo', 'Problemas de vídeo, artefatos, superaquecimento'),
            ('Processador', 'Superaquecimento, instabilidade, falha total'),
            ('Memória RAM', 'Não inicializa, tela azul, erros de memória'),
            ('Placa Mãe', 'Não liga, problemas de boot, slots defeituosos'),
            ('Fonte de Alimentação', 'Não liga, instável, ruídos'),
            ('HD/SSD', 'Não reconhecido, lentidão, bad sectors'),
            ('Cooler/Fan', 'Ruído excessivo, não gira, vibração'),
            ('Gabinete', 'Portas USB defeituosas, problemas de encaixe')
        ]

        print("\nInserindo tipos de peças...")
        for nome, defeitos in tipos_pecas:
            try:
                # Inserir tipo de peça
                cursor.execute('INSERT INTO tipos_pecas (nome) VALUES (?)', (nome,))
                tipo_peca_id = cursor.lastrowid
                print(f"  ✓ {nome}")

                # Inserir defeitos comuns
                defeitos_list = [d.strip() for d in defeitos.split(',') if d.strip()]
                for defeito in defeitos_list:
                    cursor.execute('INSERT INTO defeitos_comuns (descricao, tipo_peca_id) VALUES (?, ?)', (defeito, tipo_peca_id))
                    print(f"    - {defeito}")

            except sqlite3.IntegrityError:
                print(f"  - {nome} já existe")

        conn.commit()
        print("\n✅ Dados iniciais inseridos com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao inserir dados: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    populate_initial_data()
