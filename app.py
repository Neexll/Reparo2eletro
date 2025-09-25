from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, Response, jsonify
import sqlite3
from datetime import datetime
import io
import csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.chart import BarChart, PieChart, Reference, Series
from openpyxl.chart.label import DataLabelList
from openpyxl.utils import get_column_letter
import collections

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para sessões e mensagens flash

# Configuração do banco de dados
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = sqlite3.connect(
        'database.db',
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row
    return db

def close_db(e=None):
    db = getattr(Flask, '_database', None)
    if db is not None:
        db.close()

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
def index():
    db = get_db()
    # Junta pedidos e peças para listar os itens de cada pedido
    pedidos = db.execute('''
        SELECT p.id, p.numero_pedido, p.tecnico_nome, strftime('%d/%m/%Y %H:%M', p.data_criacao) as data_formatada,
               GROUP_CONCAT(i.nome, ', ') as itens_defeituosos
        FROM pedidos p
        LEFT JOIN pecas i ON p.id = i.pedido_id
        GROUP BY p.id
        ORDER BY p.id DESC
    ''').fetchall()
    db.close()
    return render_template('index.html', pedidos=pedidos)

@app.route('/pedido/add', methods=['GET', 'POST'])
def add_pedido():
    if request.method == 'POST':
        numero_pedido = request.form.get('numero_pedido', '').strip()
        tecnico_nome = request.form.get('tecnico_nome', '').strip()

        if not numero_pedido or not tecnico_nome:
            flash('Número do pedido and nome do técnico são obrigatórios.', 'error')
            return redirect(url_for('add_pedido'))

        db = get_db()
        try:
            cursor = db.cursor()
            cursor.execute('INSERT INTO pedidos (numero_pedido, tecnico_nome) VALUES (?, ?)', (numero_pedido, tecnico_nome))
            pedido_id = cursor.lastrowid

            # Processar peças adicionadas
            nomes_pecas = request.form.getlist('peca_nome[]')
            defeitos_pecas = request.form.getlist('peca_defeito[]')

            for nome, defeito in zip(nomes_pecas, defeitos_pecas):
                if nome and defeito:
                    cursor.execute('INSERT INTO pecas (nome, defeito, pedido_id) VALUES (?, ?, ?)', (nome, defeito, pedido_id))

            db.commit()
            flash('Pedido e peças foram salvos com sucesso!', 'success')
            return redirect(url_for('view_pedido', id=pedido_id))
        except sqlite3.Error as e:
            flash(f'Erro ao criar pedido: {e}', 'error')
        finally:
            db.close()
        return redirect(url_for('add_pedido'))

    db = get_db()
    tecnicos = db.execute('SELECT nome FROM tecnicos ORDER BY nome').fetchall()
    tipos_pecas = db.execute('SELECT id, nome FROM tipos_pecas ORDER BY nome').fetchall()
    db.close()
    return render_template('add_pedido.html', tecnicos=tecnicos, tipos_pecas=tipos_pecas)

@app.route('/pedido/<int:id>/edit', methods=['GET', 'POST'])
def edit_pedido(id):
    db = get_db()
    pedido = db.execute('SELECT * FROM pedidos WHERE id = ?', (id,)).fetchone()
    if not pedido:
        flash('Pedido não encontrado.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        numero_pedido = request.form.get('numero_pedido', '').strip()
        tecnico_nome = request.form.get('tecnico_nome', '').strip()

        if not numero_pedido or not tecnico_nome:
            flash('Número do pedido e nome do técnico são obrigatórios.', 'error')
            return redirect(url_for('edit_pedido', id=id))

        try:
            cursor = db.cursor()
            # Atualiza os detalhes do pedido
            cursor.execute('UPDATE pedidos SET numero_pedido = ?, tecnico_nome = ? WHERE id = ?', (numero_pedido, tecnico_nome, id))

            # Deleta as peças antigas para reinserir as novas (abordagem mais simples)
            cursor.execute('DELETE FROM pecas WHERE pedido_id = ?', (id,))

            # Processa as peças enviadas
            nomes_pecas = request.form.getlist('peca_nome[]')
            defeitos_pecas = request.form.getlist('peca_defeito[]')

            for nome, defeito in zip(nomes_pecas, defeitos_pecas):
                if nome and defeito:
                    cursor.execute('INSERT INTO pecas (nome, defeito, pedido_id) VALUES (?, ?, ?)', (nome, defeito, id))

            db.commit()
            flash('Pedido atualizado com sucesso!', 'success')
            return redirect(url_for('view_pedido', id=id))
        except sqlite3.Error as e:
            flash(f'Erro ao atualizar pedido: {e}', 'error')
        finally:
            db.close()
        return redirect(url_for('edit_pedido', id=id))

    # Método GET
    pecas = db.execute('SELECT * FROM pecas WHERE pedido_id = ?', (id,)).fetchall()
    tecnicos = db.execute('SELECT nome FROM tecnicos ORDER BY nome').fetchall()
    tipos_pecas = db.execute('SELECT id, nome FROM tipos_pecas ORDER BY nome').fetchall()
    db.close()
    return render_template('edit_pedido.html', pedido=pedido, pecas=pecas, tecnicos=tecnicos, tipos_pecas=tipos_pecas)

@app.route('/pedido/<int:id>')
def view_pedido(id):
    db = get_db()
    pedido = db.execute('SELECT * FROM pedidos WHERE id = ?', (id,)).fetchone()
    if not pedido:
        return 'Pedido não encontrado', 404
    
    pecas = db.execute('SELECT * FROM pecas WHERE pedido_id = ?', (id,)).fetchall()
    db.close()
    return render_template('view_pedido.html', pedido=pedido, pecas=pecas)

@app.route('/pedido/<int:pedido_id>/add_peca', methods=['POST'])
def add_peca_to_pedido(pedido_id):
    nome_peca = request.form.get('peca', '').strip()
    defeito = request.form.get('defeito', '').strip()

    if not nome_peca or not defeito:
        flash('Nome da peça e defeito são obrigatórios.', 'error')
        return redirect(url_for('view_pedido', id=pedido_id))

    try:
        db = get_db()
        db.execute('INSERT INTO pecas (nome, defeito, pedido_id) VALUES (?, ?, ?)', (nome_peca, defeito, pedido_id))
        db.commit()
        flash('Peça adicionada ao pedido com sucesso!', 'success')
    except sqlite3.Error as e:
        flash(f'Erro ao adicionar peça: {e}', 'error')
    finally:
        db.close()
    return redirect(url_for('view_pedido', id=pedido_id))

@app.route('/api/pecas/<int:peca_id>/defeitos')
def get_defeitos(peca_id):
    db = get_db()
    defeitos = db.execute(
        'SELECT descricao FROM defeitos_comuns WHERE tipo_peca_id = ? ORDER BY descricao',
        (peca_id,)
    ).fetchall()
    db.close()
    # Converte o resultado para uma lista de strings
    return jsonify([d['descricao'] for d in defeitos])

@app.route('/add_peca_tipo', methods=['POST'])
def add_peca_tipo():
    nome_peca = request.form.get('nome_peca', '').strip()
    defeitos_str = request.form.get('defeitos', '').strip()

    if not nome_peca or not defeitos_str:
        flash('Nome da peça e pelo menos um defeito são obrigatórios.', 'error')
        return redirect(url_for('manage_pecas'))

    defeitos = [d.strip() for d in defeitos_str.split(',') if d.strip()]

    db = get_db()
    try:
        # Verifica se a peça já existe
        cursor = db.cursor()
        cursor.execute('SELECT id FROM tipos_pecas WHERE nome = ?', (nome_peca,))
        peca_existente = cursor.fetchone()

        if peca_existente:
            flash(f'O tipo de peça "{nome_peca}" já existe.', 'error')
        else:
            # Insere o novo tipo de peça
            cursor.execute('INSERT INTO tipos_pecas (nome) VALUES (?)', (nome_peca,))
            tipo_peca_id = cursor.lastrowid

            # Insere os defeitos associados
            for defeito in defeitos:
                cursor.execute('INSERT INTO defeitos_comuns (descricao, tipo_peca_id) VALUES (?, ?)', (defeito, tipo_peca_id))
            
            db.commit()
            flash(f'Novo tipo de peça "{nome_peca}" adicionado com sucesso!', 'success')

    except sqlite3.IntegrityError as e:
        db.rollback()
        flash(f'Erro ao adicionar a peça: {e}', 'error')
    finally:
        db.close()

    return redirect(url_for('manage_pecas'))

@app.route('/pedido/<int:id>/delete', methods=['POST'])
def delete_pedido(id):
    db = get_db()
    try:
        # Deleta primeiro as peças associadas ao pedido
        db.execute('DELETE FROM pecas WHERE pedido_id = ?', (id,))
        # Depois deleta o pedido principal
        db.execute('DELETE FROM pedidos WHERE id = ?', (id,))
        db.commit()
        flash('Pedido e todas as suas peças foram removidos com sucesso!', 'success')
    except sqlite3.Error as e:
        db.rollback()
        flash(f'Erro ao remover o pedido: {e}', 'error')
    finally:
        db.close()
    return redirect(url_for('index'))

@app.route('/manage_pecas')
def manage_pecas():
    db = get_db()
    tipos_pecas = db.execute('SELECT id, nome FROM tipos_pecas ORDER BY nome').fetchall()
    db.close()
    return render_template('manage_pecas.html', tipos_pecas=tipos_pecas)

@app.route('/edit_peca_tipo/<int:id>', methods=['GET', 'POST'])
def edit_peca_tipo(id):
    db = get_db()
    # Busca o tipo de peça para garantir que ele existe
    tipo_peca = db.execute('SELECT id, nome FROM tipos_pecas WHERE id = ?', (id,)).fetchone()
    if tipo_peca is None:
        flash('Tipo de peça não encontrado.', 'error')
        return redirect(url_for('manage_pecas'))

    if request.method == 'POST':
        nome_peca = request.form.get('nome_peca', '').strip()
        defeitos_str = request.form.get('defeitos', '').strip()

        if not nome_peca or not defeitos_str:
            flash('Nome da peça e pelo menos um defeito são obrigatórios.', 'error')
            # Se houver erro, recarrega a página com os dados atuais
            defeitos_rows = db.execute('SELECT descricao FROM defeitos_comuns WHERE tipo_peca_id = ?', (id,)).fetchall()
            defeitos_str_atual = ', '.join([d['descricao'] for d in defeitos_rows])
            return render_template('edit_peca_tipo.html', tipo_peca=tipo_peca, defeitos_str=defeitos_str_atual)

        defeitos_list = [d.strip() for d in defeitos_str.split(',') if d.strip()]

        try:
            cursor = db.cursor()
            # Atualiza o nome da peça
            cursor.execute('UPDATE tipos_pecas SET nome = ? WHERE id = ?', (nome_peca, id))
            # Deleta os defeitos antigos
            cursor.execute('DELETE FROM defeitos_comuns WHERE tipo_peca_id = ?', (id,))
            # Insere os novos defeitos
            for defeito in defeitos_list:
                cursor.execute('INSERT INTO defeitos_comuns (descricao, tipo_peca_id) VALUES (?, ?)', (defeito, id))
            db.commit()
            flash('Tipo de peça atualizado com sucesso!', 'success')
            return redirect(url_for('manage_pecas'))
        except sqlite3.Error as e:
            db.rollback()
            flash(f'Erro ao atualizar o tipo de peça: {e}', 'error')
        finally:
            db.close()
        return redirect(url_for('edit_peca_tipo', id=id))

    # Método GET: Carrega os dados para exibir no formulário
    defeitos_rows = db.execute('SELECT descricao FROM defeitos_comuns WHERE tipo_peca_id = ?', (id,)).fetchall()
    db.close()
    defeitos_str = ', '.join([d['descricao'] for d in defeitos_rows])
    
    return render_template('edit_peca_tipo.html', tipo_peca=tipo_peca, defeitos_str=defeitos_str)

@app.route('/delete_peca_tipo/<int:id>', methods=['POST'])
def delete_peca_tipo(id):
    db = get_db()
    try:
        # Em uma transação, primeiro deleta os defeitos e depois a peça
        cursor = db.cursor()
        cursor.execute('DELETE FROM defeitos_comuns WHERE tipo_peca_id = ?', (id,))
        cursor.execute('DELETE FROM tipos_pecas WHERE id = ?', (id,))
        db.commit()
        flash('Tipo de peça removido com sucesso!', 'success')
    except sqlite3.Error as e:
        db.rollback()
        flash(f'Erro ao remover o tipo de peça: {e}', 'error')
    finally:
        db.close()
    return redirect(url_for('manage_pecas'))

# --- Rotas para Gerenciamento de Técnicos ---

@app.route('/manage_tecnicos')
def manage_tecnicos():
    db = get_db()
    tecnicos = db.execute('SELECT id, nome FROM tecnicos ORDER BY nome').fetchall()
    db.close()
    return render_template('manage_tecnicos.html', tecnicos=tecnicos)

@app.route('/add_tecnico', methods=['POST'])
def add_tecnico():
    nome = request.form.get('nome', '').strip()
    if nome:
        try:
            db = get_db()
            db.execute('INSERT INTO tecnicos (nome) VALUES (?)', (nome,))
            db.commit()
            flash('Técnico adicionado com sucesso!', 'success')
        except sqlite3.IntegrityError:
            flash('Este técnico já existe.', 'error')
        finally:
            db.close()
    else:
        flash('O nome do técnico é obrigatório.', 'error')
    return redirect(url_for('manage_tecnicos'))

@app.route('/delete_tecnico/<int:id>', methods=['POST'])
def delete_tecnico(id):
    try:
        db = get_db()
        db.execute('DELETE FROM tecnicos WHERE id = ?', (id,))
        db.commit()
        flash('Técnico removido com sucesso!', 'success')
    except sqlite3.Error as e:
        flash(f'Erro ao remover técnico: {e}', 'error')
    finally:
        db.close()
    return redirect(url_for('manage_tecnicos'))

@app.route('/export')
def export():
    db = get_db()

    # 1. Dados para a lista de peças
    pecas_list = db.execute('''
        SELECT p.numero_pedido, p.tecnico_nome, i.nome, i.defeito, STRFTIME('%d/%m/%Y', p.data_criacao) as data_formatada
        FROM pedidos p JOIN pecas i ON p.id = i.pedido_id
        ORDER BY p.id DESC
    ''').fetchall()

    # 2. Dados para o gráfico de pizza
    pie_chart_data = db.execute('''
        SELECT nome || ' - ' || defeito as label, COUNT(*) as total
        FROM pecas
        GROUP BY label
        ORDER BY total DESC
    ''').fetchall()

    # 3. Dados para o gráfico de barras
    bar_chart_stats = db.execute('''
        SELECT strftime('%Y-%m', p.data_criacao) as mes, i.nome as peca_nome, COUNT(i.id) as total
        FROM pedidos p JOIN pecas i ON p.id = i.pedido_id
        GROUP BY mes, peca_nome
        ORDER BY mes, peca_nome
    ''').fetchall()
    db.close()

    wb = Workbook()
    
    # --- Aba 1: Relatório de Peças ---
    ws_report = wb.active
    ws_report.title = "Relatório de Peças"
    headers = ['PEDIDO', 'DEFEITO', 'PEÇA', '+', '+', 'TECNICO', 'DATA']
    ws_report.append(headers)
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="000000", end_color="000000", fill_type="solid") # Cor preta
    for cell in ws_report[1]:
        cell.font = header_font
        cell.fill = header_fill
    for peca in pecas_list:
        ws_report.append([
            peca['numero_pedido'], 
            peca['defeito'], 
            peca['nome'], 
            '', # Coluna '+' vazia
            '', # Coluna '+' vazia
            peca['tecnico_nome'], 
            peca['data_formatada']
        ])
    for col in ws_report.columns:
        max_length = max(len(str(cell.value or '')) for cell in col)
        ws_report.column_dimensions[get_column_letter(col[0].column)].width = max_length + 2

    # --- Aba 2: Dashboard com Gráficos ---
    ws_dashboard = wb.create_sheet(title="Dashboard")
    ws_data = wb.create_sheet(title="ChartData")
    ws_data.sheet_state = 'hidden' # Oculta a aba de dados

    # --- Criação do Gráfico de Pizza ---
    if pie_chart_data:
        # Calcula o total para as porcentagens
        total_pecas = sum(row['total'] for row in pie_chart_data)
        
        # Cria rótulos personalizados: "Peça - Defeito - Quantidade - %"
        ws_data.append(['Categoria', 'Total', 'Label_Personalizado'])
        for row in pie_chart_data:
            # Separa peça e defeito do label original
            parts = row['label'].split(' - ')
            peca = parts[0] if len(parts) > 0 else ''
            defeito = parts[1] if len(parts) > 1 else ''
            quantidade = row['total']
            porcentagem = round((quantidade / total_pecas) * 100, 1)
            
            # Cria o label personalizado
            label_personalizado = f"{peca} - {defeito} - {quantidade} - {porcentagem}%"
            ws_data.append([label_personalizado, row['total'], label_personalizado])
        
        pie = PieChart()
        labels = Reference(ws_data, min_col=3, min_row=2, max_row=len(pie_chart_data) + 1)  # Usa a coluna dos labels personalizados
        data = Reference(ws_data, min_col=2, min_row=1, max_row=len(pie_chart_data) + 1)
        pie.add_data(data, titles_from_data=True)
        pie.set_categories(labels)
        pie.title = "Peças por Defeito"
        pie.height, pie.width = 12, 18
        pie.legend.position = 'r'
        pie.style = 26
        # Remove os rótulos de dados pois as informações já estão na legenda
        ws_dashboard.add_chart(pie, "A1")

    # --- Criação do Gráfico de Barras ---
    if bar_chart_stats:
        # Pivotar os dados
        bar_data_pivot = collections.defaultdict(lambda: collections.defaultdict(int))
        all_pecas = sorted(list(set(row['peca_nome'] for row in bar_chart_stats)))
        all_months = sorted(list(set(row['mes'] for row in bar_chart_stats)))
        for row in bar_chart_stats:
            bar_data_pivot[row['mes']][row['peca_nome']] = row['total']
        
        # Escrever dados pivotados na aba de dados
        bar_data_start_row = ws_data.max_row + 2
        header_bar = ['Mês'] + all_pecas
        ws_data.append(header_bar)
        
        for month in all_months:
            row_data = [month] + [bar_data_pivot[month].get(peca, 0) for peca in all_pecas]
            ws_data.append(row_data)

        # Criar o gráfico
        bar = BarChart()
        bar.type = "col"
        bar.style = 10
        bar.grouping = "clustered"
        bar.y_axis.title = 'Quantidade'

        # Título dinâmico e formatação
        if len(all_months) == 1:
            try:
                date_obj = datetime.strptime(all_months[0], '%Y-%m')
                year = date_obj.strftime('%Y')
                month_number = int(date_obj.strftime('%m'))

                meses_pt_br = {
                    1: 'JANEIRO', 2: 'FEVEREIRO', 3: 'MARÇO', 4: 'ABRIL',
                    5: 'MAIO', 6: 'JUNHO', 7: 'JULHO', 8: 'AGOSTO',
                    9: 'SETEMBRO', 10: 'OUTUBRO', 11: 'NOVEMBRO', 12: 'DEZEMBRO'
                }

                month_name_pt = meses_pt_br.get(month_number, '')
                bar.title = f"Volume Mensal de Peças - {month_name_pt} {year}"
            except ValueError:
                bar.title = "Volume Mensal de Peças"
        else:
            bar.title = "Volume Mensal de Peças"

        # Aumenta o tamanho da fonte do título
        bar.title.tx.rich.p[0].pPr.defRPr.sz = 1400 # 14pt
        bar.height, bar.width = 12, 24 # Tamanho reduzido
        bar.legend = None # Remove a legenda, pois os rótulos estarão nas barras
        bar.y_axis.majorGridlines = None
        bar.gapWidth = 100

        # Configura os rótulos de dados para mostrar "Nome da Peça - Valor"
        bar.dLbls = DataLabelList()
        bar.dLbls.showVal = True
        bar.dLbls.showSerName = True
        bar.dLbls.separator = ' - '
        bar.dLbls.showCatName = False


        # Referenciar os dados de forma explícita para cada série
        categories_ref = Reference(ws_data, min_col=1, min_row=bar_data_start_row + 1, max_row=ws_data.max_row)
        bar.set_categories(categories_ref)
        for i, peca_nome in enumerate(all_pecas):
            data_ref = Reference(ws_data, min_col=i + 2, min_row=bar_data_start_row + 1, max_row=ws_data.max_row)
            series = Series(data_ref, title=peca_nome)
            bar.series.append(series)
        ws_dashboard.add_chart(bar, "A30")

    # --- Finalização ---
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return Response(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": "attachment;filename=relatorio_completo_com_graficos.xlsx"}
    )

@app.route('/api/stats/pecas_por_defeito')
def pecas_por_defeito_stats():
    db = get_db()
    stats = db.execute('''
        SELECT nome, defeito, COUNT(*) as total
        FROM pecas
        GROUP BY nome, defeito
        ORDER BY total DESC
    ''').fetchall()
    db.close()

    # Formata os dados para o gráfico
    chart_data = [
        {
            'label': f"{row['nome']} - {row['defeito']}",
            'total': row['total']
        }
        for row in stats
    ]
    return jsonify(chart_data)

@app.route('/api/stats/pecas_mensal')
def pecas_mensal_stats():
    db = get_db()
    stats = db.execute('''
        SELECT 
            strftime('%Y-%m', p.data_criacao) as mes,
            i.nome as peca_nome,
            COUNT(i.id) as total
        FROM pedidos p
        JOIN pecas i ON p.id = i.pedido_id
        GROUP BY mes, peca_nome
        ORDER BY mes, peca_nome
    ''').fetchall()
    db.close()

    # Processar os dados para o formato de gráfico de barras empilhadas
    data_by_month = collections.defaultdict(lambda: collections.defaultdict(int))
    all_pecas = set()
    all_months = []

    for row in stats:
        mes = row['mes']
        peca_nome = row['peca_nome']
        total = row['total']
        
        if mes not in all_months:
            all_months.append(mes)
        all_pecas.add(peca_nome)
        data_by_month[mes][peca_nome] = total

    all_months.sort()
    sorted_pecas = sorted(list(all_pecas))

    datasets = []
    for peca in sorted_pecas:
        dataset = {
            'label': peca,
            'data': [data_by_month[month][peca] for month in all_months]
        }
        datasets.append(dataset)

    chart_data = {
        'labels': all_months,
        'datasets': datasets
    }

    return jsonify(chart_data)

if __name__ == '__main__':
    # Descomente a linha abaixo apenas na primeira execução para criar o banco de dados
    # init_db()
    app.run(debug=True)
