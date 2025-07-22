-- Esquema do banco de dados para sistema de pesquisa automatizada
-- Baseado no diagrama fornecido com melhorias na estrutura

-- Extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de estados brasileiros
CREATE TABLE estados (
    cod_uf SERIAL PRIMARY KEY,
    uf VARCHAR(2) NOT NULL UNIQUE,
    cod_fornecedor INTEGER,
    nome VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de serviços
CREATE TABLE servicos (
    cod_servico SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    civel BOOLEAN DEFAULT FALSE,
    criminal BOOLEAN DEFAULT FALSE,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de clientes
CREATE TABLE clientes (
    cod_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    cnpj VARCHAR(18),
    cpf VARCHAR(14),
    email VARCHAR(100),
    telefone VARCHAR(20),
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de funcionários
CREATE TABLE funcionarios (
    cod_funcionario SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    email VARCHAR(100),
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de lotes
CREATE TABLE lotes (
    cod_lote SERIAL PRIMARY KEY,
    cod_lote_prazo INTEGER,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cod_funcionario INTEGER REFERENCES funcionarios(cod_funcionario),
    tipo VARCHAR(50),
    prioridade INTEGER DEFAULT 1,
    status VARCHAR(20) DEFAULT 'ABERTO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de pesquisas
CREATE TABLE pesquisas (
    cod_pesquisa SERIAL PRIMARY KEY,
    cod_cliente INTEGER REFERENCES clientes(cod_cliente),
    cod_uf INTEGER REFERENCES estados(cod_uf),
    cod_servico INTEGER REFERENCES servicos(cod_servico),
    tipo INTEGER DEFAULT 0, -- 0: Normal, 1: Urgente, etc.
    cpf VARCHAR(14),
    cod_uf_nascimento INTEGER REFERENCES estados(cod_uf),
    cod_uf_rg INTEGER REFERENCES estados(cod_uf),
    data_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_conclusao TIMESTAMP,
    nome VARCHAR(200),
    nome_corrigido VARCHAR(200),
    rg VARCHAR(20),
    rg_corrigido VARCHAR(20),
    nascimento DATE,
    mae VARCHAR(200),
    mae_corrigido VARCHAR(200),
    anexo TEXT,
    status VARCHAR(20) DEFAULT 'PENDENTE',
    prioridade INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de relacionamento entre lotes e pesquisas
CREATE TABLE lote_pesquisas (
    cod_lote_pesquisa SERIAL PRIMARY KEY,
    cod_lote INTEGER REFERENCES lotes(cod_lote),
    cod_pesquisa INTEGER REFERENCES pesquisas(cod_pesquisa),
    cod_funcionario INTEGER REFERENCES funcionarios(cod_funcionario),
    cod_funcionario_conclusao INTEGER REFERENCES funcionarios(cod_funcionario),
    cod_fornecedor INTEGER,
    data_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_conclusao TIMESTAMP,
    cod_uf INTEGER REFERENCES estados(cod_uf),
    obs TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cod_lote, cod_pesquisa)
);

-- Tabela de resultados de pesquisa SPV
CREATE TABLE pesquisa_spv (
    cod_pesquisa_spv SERIAL PRIMARY KEY,
    cod_pesquisa INTEGER REFERENCES pesquisas(cod_pesquisa),
    cod_spv INTEGER DEFAULT 1,
    cod_spv_computador INTEGER,
    cod_spv_tipo INTEGER,
    cod_funcionario INTEGER REFERENCES funcionarios(cod_funcionario),
    filtro INTEGER NOT NULL, -- 0: CPF, 1: RG, 2: Nome, 3: RG alternativo
    website_id INTEGER DEFAULT 1,
    resultado INTEGER, -- 1: Nada consta, 2: Criminal, 5: Cível, 7: Erro
    data_execucao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tempo_execucao DECIMAL(10,2),
    erro TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de configurações de websites
CREATE TABLE websites (
    website_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    url VARCHAR(500) NOT NULL,
    tipo VARCHAR(50), -- TJSP, TJRJ, etc.
    ativo BOOLEAN DEFAULT TRUE,
    configuracao JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para melhor performance
CREATE INDEX idx_pesquisas_status ON pesquisas(status);
CREATE INDEX idx_pesquisas_data_entrada ON pesquisas(data_entrada);
CREATE INDEX idx_pesquisas_cpf ON pesquisas(cpf);
CREATE INDEX idx_pesquisas_rg ON pesquisas(rg);
CREATE INDEX idx_pesquisas_nome ON pesquisas(nome);
CREATE INDEX idx_pesquisa_spv_cod_pesquisa ON pesquisa_spv(cod_pesquisa);
CREATE INDEX idx_pesquisa_spv_resultado ON pesquisa_spv(resultado);
CREATE INDEX idx_pesquisa_spv_filtro ON pesquisa_spv(filtro);
CREATE INDEX idx_lote_pesquisas_cod_lote ON lote_pesquisas(cod_lote);
CREATE INDEX idx_lote_pesquisas_cod_pesquisa ON lote_pesquisas(cod_pesquisa);

-- Função para atualizar o timestamp de updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para atualizar updated_at automaticamente
CREATE TRIGGER update_estados_updated_at BEFORE UPDATE ON estados FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_servicos_updated_at BEFORE UPDATE ON servicos FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_clientes_updated_at BEFORE UPDATE ON clientes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_funcionarios_updated_at BEFORE UPDATE ON funcionarios FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_lotes_updated_at BEFORE UPDATE ON lotes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_pesquisas_updated_at BEFORE UPDATE ON pesquisas FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_lote_pesquisas_updated_at BEFORE UPDATE ON lote_pesquisas FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_pesquisa_spv_updated_at BEFORE UPDATE ON pesquisa_spv FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_websites_updated_at BEFORE UPDATE ON websites FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Dados iniciais
INSERT INTO estados (uf, nome) VALUES 
('SP', 'São Paulo'),
('RJ', 'Rio de Janeiro'),
('MG', 'Minas Gerais'),
('RS', 'Rio Grande do Sul'),
('PR', 'Paraná'),
('SC', 'Santa Catarina'),
('BA', 'Bahia'),
('GO', 'Goiás'),
('PE', 'Pernambuco'),
('CE', 'Ceará');

INSERT INTO servicos (nome, descricao, civel, criminal) VALUES 
('Pesquisa Cível', 'Pesquisa de processos cíveis', TRUE, FALSE),
('Pesquisa Criminal', 'Pesquisa de processos criminais', FALSE, TRUE),
('Pesquisa Geral', 'Pesquisa geral de processos', TRUE, TRUE);

INSERT INTO websites (nome, url, tipo, configuracao) VALUES 
('TJSP', 'https://esaj.tjsp.jus.br/cpopg/open.do', 'TJSP', '{"selectors": {"tipo_pesquisa": "//*[@id=\"cbPesquisa\"]", "campo_cpf": "//*[@id=\"campo_DOCPARTE\"]", "campo_nome": "//*[@id=\"campo_NMPARTE\"]", "botao_consultar": "//*[@id=\"botaoConsultarProcessos\"]"}}');

-- View para facilitar consultas de pesquisas pendentes
CREATE VIEW pesquisas_pendentes AS
SELECT 
    p.cod_pesquisa,
    p.cod_cliente,
    c.nome as nome_cliente,
    p.cod_uf,
    e.uf,
    p.cod_servico,
    s.nome as nome_servico,
    p.tipo,
    p.cpf,
    p.cod_uf_nascimento,
    p.cod_uf_rg,
    p.data_entrada,
    p.nome,
    p.nome_corrigido,
    p.rg,
    p.rg_corrigido,
    p.nascimento,
    p.mae,
    p.mae_corrigido,
    p.anexo,
    p.status,
    p.prioridade
FROM pesquisas p
INNER JOIN clientes c ON p.cod_cliente = c.cod_cliente
INNER JOIN estados e ON p.cod_uf = e.cod_uf
INNER JOIN servicos s ON p.cod_servico = s.cod_servico
WHERE p.data_conclusao IS NULL 
AND p.status = 'PENDENTE'
AND p.cpf IS NOT NULL 
AND p.cpf != '';

-- Função para obter pesquisas pendentes com paginação
CREATE OR REPLACE FUNCTION get_pesquisas_pendentes(
    p_filtro INTEGER DEFAULT 0,
    p_limit INTEGER DEFAULT 100,
    p_offset INTEGER DEFAULT 0
)
RETURNS TABLE (
    cod_pesquisa INTEGER,
    cod_cliente INTEGER,
    nome_cliente VARCHAR,
    uf VARCHAR,
    data_entrada TIMESTAMP,
    nome VARCHAR,
    cpf VARCHAR,
    rg VARCHAR,
    nascimento DATE,
    mae VARCHAR,
    anexo TEXT,
    resultado INTEGER,
    spv_tipo INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT 
        p.cod_pesquisa,
        p.cod_cliente,
        c.nome as nome_cliente,
        e.uf,
        p.data_entrada,
        COALESCE(p.nome_corrigido, p.nome) AS nome,
        p.cpf,
        COALESCE(p.rg_corrigido, p.rg) AS rg,
        p.nascimento,
        COALESCE(p.mae_corrigido, p.mae) AS mae,
        p.anexo,
        ps.resultado,
        ps.cod_spv_tipo
    FROM pesquisas p
    INNER JOIN clientes c ON p.cod_cliente = c.cod_cliente
    INNER JOIN servicos s ON p.cod_servico = s.cod_servico
    LEFT JOIN lote_pesquisas lp ON p.cod_pesquisa = lp.cod_pesquisa
    LEFT JOIN lotes l ON l.cod_lote = lp.cod_lote
    LEFT JOIN estados e ON e.cod_uf = p.cod_uf
    LEFT JOIN pesquisa_spv ps ON ps.cod_pesquisa = p.cod_pesquisa 
        AND ps.cod_spv = 1 
        AND ps.filtro = p_filtro
    WHERE p.data_conclusao IS NULL
    AND ps.resultado IS NULL
    AND p.tipo = 0
    AND p.cpf IS NOT NULL 
    AND p.cpf != ''
    AND (p_filtro = 0 OR (p_filtro IN (1, 3) AND p.rg IS NOT NULL AND p.rg != ''))
    AND (e.uf = 'SP' OR p.cod_uf_nascimento = 26 OR p.cod_uf_rg = 26)
    ORDER BY nome ASC, ps.resultado DESC
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql; 