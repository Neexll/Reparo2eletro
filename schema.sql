-- Tabela que armazena os pedidos de reparo (RMA - Return Merchandise Authorization)
DROP TABLE IF EXISTS pedidos;
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificador único do pedido
    numero_pedido TEXT NOT NULL,           -- Número do pedido (ex: RMA-2023-001)
    tecnico_nome TEXT NOT NULL,            -- Nome do técnico responsável
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP  -- Data de criação automática
);

-- Tabela que armazena as peças defeituosas de cada pedido
DROP TABLE IF EXISTS pecas;
CREATE TABLE pecas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificador único da peça
    nome TEXT NOT NULL,                   -- Nome da peça (ex: Placa Mãe H61)
    defeito TEXT NOT NULL,                -- Descrição do defeito
    pedido_id INTEGER NOT NULL,           -- ID do pedido ao qual a peça pertence
    FOREIGN KEY (pedido_id) REFERENCES pedidos (id)  -- Chave estrangeira para a tabela pedidos
);

-- Tabela que armazena os tipos de peças disponíveis
DROP TABLE IF EXISTS tipos_pecas;
CREATE TABLE tipos_pecas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificador único do tipo de peça
    nome TEXT UNIQUE NOT NULL             -- Nome do tipo de peça (ex: H61, H81, Fonte ATX)
);

-- Tabela que armazena os defeitos comuns para cada tipo de peça
DROP TABLE IF EXISTS defeitos_comuns;
CREATE TABLE defeitos_comuns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificador único do defeito
    descricao TEXT NOT NULL,              -- Descrição do defeito
    tipo_peca_id INTEGER NOT NULL,        -- ID do tipo de peça relacionado
    FOREIGN KEY (tipo_peca_id) REFERENCES tipos_pecas (id)  -- Chave estrangeira para tipos_pecas
);

-- Tabela que armazena os técnicos da oficina
DROP TABLE IF EXISTS tecnicos;
CREATE TABLE tecnicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificador único do técnico
    nome TEXT UNIQUE NOT NULL             -- Nome do técnico (deve ser único)
);
