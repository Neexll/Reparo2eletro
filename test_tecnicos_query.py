import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
try:
    cursor.execute('SELECT id, nome FROM tecnicos ORDER BY nome')
    tecnicos = cursor.fetchall()
    print('Query executada com sucesso!')
    print('Número de técnicos:', len(tecnicos))
    for tecnico in tecnicos:
        print(tecnico)
except Exception as e:
    print('Erro na query:', e)
    import traceback
    traceback.print_exc()
finally:
    conn.close()
