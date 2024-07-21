-- Cria a tabela 'umidade' se ela não existir
CREATE TABLE IF NOT EXISTS umidade (
    time TIMESTAMP NOT NULL, -- Armazena a data e hora do registro
    value DECIMAL(5, 2) NOT NULL -- Armazena o valor da umidade, com até 3 dígitos à esquerda e 2 à direita do ponto decimal
);

-- Cria a tabela 'temperatura' se ela não existir
CREATE TABLE IF NOT EXISTS temperatura (
    time TIMESTAMP NOT NULL, -- Armazena a data e hora do registro
    value DECIMAL(5, 2) NOT NULL -- Armazena o valor da temperatura, com até 3 dígitos à esquerda e 2 à direita do ponto decimal
);
