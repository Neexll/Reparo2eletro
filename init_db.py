import sqlite3

# Conecta ao banco de dados SQLite
connection = sqlite3.connect('database.db')

# Lê o arquivo schema.sql e executa os comandos SQL para criar as tabelas
with open('schema.sql', encoding='utf-8') as f:
    connection.executescript(f.read())

# Dicionário com os dados iniciais de peças e defeitos
pecas_e_defeitos = {
    'H61': ['Pino LGA amassado', 'Não dá vídeo', 'BIOS corrompida', 'Porta SATA não funciona'],
    'H81': ['Não reconhece memórias', 'Rede não funciona', 'Portas USB em curto'],
    'Placa de Vídeo': ['Artefatos na tela', 'Sem sinal de vídeo'],
    'Fonte ATX': ['Não liga', 'Tensão baixa (12V)', 'Cheiro de queimado'],
    'Memória RAM': ['Tela azul', 'Não da vídeo' , 'Travando'],
}

# Cria um cursor para executar comandos SQL
cursor = connection.cursor()

# Itera sobre cada tipo de peça e seus respectivos defeitos
for peca_nome, defeitos in pecas_e_defeitos.items():
    # Insere o nome da peça na tabela tipos_pecas e obtém o ID gerado
    cursor.execute("INSERT INTO tipos_pecas (nome) VALUES (?)", (peca_nome,))
    tipo_peca_id = cursor.lastrowid

    # Para cada defeito da peça, insere na tabela defeitos_comuns
    # associando ao ID do tipo de peça
    for defeito in defeitos:
        cursor.execute("""
            INSERT INTO defeitos_comuns (descricao, tipo_peca_id) 
            VALUES (?, ?)
        """, (defeito, tipo_peca_id))

# Adiciona alguns técnicos iniciais
tecnicos_iniciais = ['Anderson', 'Carlos', 'Mariana']
for tecnico in tecnicos_iniciais:
    cursor.execute("INSERT INTO tecnicos (nome) VALUES (?)", (tecnico,))

# Salva as alterações e fecha a conexão
connection.commit()
connection.close()

print("Banco de dados inicializado e populado com sucesso!")
