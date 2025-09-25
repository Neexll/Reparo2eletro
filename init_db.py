import sqlite3

# Conecta ao banco de dados
connection = sqlite3.connect('database.db')

# Recria as tabelas a partir do schema.sql
with open('schema.sql') as f:
    connection.executescript(f.read())

# Dados iniciais que estavam no app.py
pecas_e_defeitos = {
    'H61': ['Pino LGA amassado', 'Não dá vídeo', 'BIOS corrompida', 'Porta SATA não funciona'],
    'H81': ['Não reconhece memórias', 'Rede não funciona', 'Portas USB em curto'],
    'Placa de Vídeo': ['Artefatos na tela', 'Sem sinal de vídeo'],
    'Fonte ATX': ['Não liga', 'Tensão baixa (12V)', 'Cheiro de queimado'],
    'Memória RAM': ['Tela azul', 'Não da vídeo' , 'Travando'],
}

cursor = connection.cursor()

# Itera sobre os tipos de peças e insere no banco
for peca_nome, defeitos in pecas_e_defeitos.items():
    # Insere o tipo da peça e obtém o ID
    cursor.execute("INSERT INTO tipos_pecas (nome) VALUES (?)", (peca_nome,))
    tipo_peca_id = cursor.lastrowid

    # Itera sobre os defeitos e os insere, associando ao tipo de peça
    for defeito in defeitos:
        cursor.execute("INSERT INTO defeitos_comuns (descricao, tipo_peca_id) VALUES (?, ?)", (defeito, tipo_peca_id))

# Adiciona alguns técnicos iniciais
tecnicos_iniciais = ['Anderson', 'Carlos', 'Mariana']
for tecnico in tecnicos_iniciais:
    cursor.execute("INSERT INTO tecnicos (nome) VALUES (?)", (tecnico,))

# Salva as alterações e fecha a conexão
connection.commit()
connection.close()

print("Banco de dados inicializado e populado com sucesso!")
