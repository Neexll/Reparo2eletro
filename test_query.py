import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
try:
    cursor.execute('''
        SELECT p.id, p.numero_pedido, p.tecnico_nome, strftime('%d/%m/%Y %H:%M', p.data_criacao) as data_formatada,
               GROUP_CONCAT(i.nome, ', ') as itens_defeituosos
        FROM pedidos p
        LEFT JOIN pecas i ON p.id = i.pedido_id
        GROUP BY p.id ORDER BY p.id DESC
    ''')
    results = cursor.fetchall()
    print('Query executada com sucesso!')
    print('Número de resultados:', len(results))
    for row in results[:3]:
        print(row)
except Exception as e:
    print('Erro na query:', e)
finally:
    conn.close()
