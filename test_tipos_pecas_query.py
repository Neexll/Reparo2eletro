import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
try:
    cursor.execute('SELECT id, nome FROM tipos_pecas ORDER BY nome')
    tipos_pecas = cursor.fetchall()
    print('Query executada com sucesso!')
    print('Número de tipos de peças:', len(tipos_pecas))
    for tipo in tipos_pecas:
        print(tipo)
except Exception as e:
    print('Erro na query:', e)
    import traceback
    traceback.print_exc()
finally:
    conn.close()
