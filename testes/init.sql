-- Criação da tabela 'cpu_frequency' se não existir
CREATE TABLE IF NOT EXISTS cpu_frequency (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP NOT NULL,
    value FLOAT NOT NULL
);

-- Criação da tabela 'cpu_usage' se não existir
CREATE TABLE IF NOT EXISTS cpu_usage (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP NOT NULL,
    value FLOAT NOT NULL
);

-- Criação da tabela 'memory_usage' se não existir
CREATE TABLE IF NOT EXISTS memory_usage (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP NOT NULL,
    value FLOAT NOT NULL
);

-- Criação da tabela 'network_io' se não existir
CREATE TABLE IF NOT EXISTS network_io (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP NOT NULL,
    n_input BIGINT NOT NULL,
    n_output BIGINT NOT NULL
);
