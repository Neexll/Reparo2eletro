-- Tabela de Pedidos (RMA)
DROP TABLE IF EXISTS pedidos;
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_pedido TEXT NOT NULL,
    tecnico_nome TEXT NOT NULL,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Peças Defeituosas (associadas a um pedido)
DROP TABLE IF EXISTS pecas;
CREATE TABLE pecas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    defeito TEXT NOT NULL,
    pedido_id INTEGER NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos (id)
);

-- Tabela para os tipos de peças (H61, H81, etc.)
DROP TABLE IF EXISTS tipos_pecas;
CREATE TABLE tipos_pecas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL
);

-- Tabela para os defeitos comuns associados a cada tipo de peça
DROP TABLE IF EXISTS defeitos_comuns;
CREATE TABLE defeitos_comuns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    tipo_peca_id INTEGER NOT NULL,
    FOREIGN KEY (tipo_peca_id) REFERENCES tipos_pecas (id)
);

-- Tabela para os técnicos
DROP TABLE IF EXISTS tecnicos;
CREATE TABLE tecnicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL
);
