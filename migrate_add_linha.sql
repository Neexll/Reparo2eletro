-- Migration script to add 'linha' column to pedidos table

-- Disable foreign key constraints
PRAGMA foreign_keys=off;

-- Begin transaction
BEGIN TRANSACTION;

-- Create a new table with the updated schema
CREATE TABLE pedidos_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_pedido TEXT NOT NULL,
    tecnico_nome TEXT NOT NULL,
    linha INTEGER CHECK(linha IN (1, 2, 3, 4)),
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Copy data from old table to new table (set default linha to 1 for existing records)
INSERT INTO pedidos_new (id, numero_pedido, tecnico_nome, linha, data_criacao)
SELECT id, numero_pedido, tecnico_nome, 1, data_criacao
FROM pedidos;

-- Drop the old table
DROP TABLE pedidos;

-- Rename the new table to the original name
ALTER TABLE pedidos_new RENAME TO pedidos;

-- Recreate indexes
CREATE INDEX IF NOT EXISTS idx_pedidos_numero_pedido ON pedidos(numero_pedido);
CREATE INDEX IF NOT EXISTS idx_pedidos_tecnico_nome ON pedidos(tecnico_nome);
CREATE INDEX IF NOT EXISTS idx_pedidos_data_criacao ON pedidos(data_criacao);

-- Commit the transaction
COMMIT;

-- Re-enable foreign key constraints
PRAGMA foreign_keys=on;

-- Verify the changes
PRAGMA table_info(pedidos);
