-- Popula estados
INSERT INTO estados (uf, nome) VALUES 
('SP', 'São Paulo'),
('RJ', 'Rio de Janeiro'),
('MG', 'Minas Gerais')
ON CONFLICT (uf) DO NOTHING;

-- Popula serviços
INSERT INTO servicos (nome, descricao, civel, criminal) VALUES 
('Pesquisa Cível', 'Pesquisa de processos cíveis', TRUE, FALSE),
('Pesquisa Criminal', 'Pesquisa de processos criminais', FALSE, TRUE),
('Pesquisa Geral', 'Pesquisa geral de processos', TRUE, TRUE);
-- ON CONFLICT DO NOTHING;

-- Popula clientes (com cod_cliente explícito)
INSERT INTO clientes (nome, cnpj, cpf, email, telefone) VALUES
('Cliente 1', '12.345.678/0001-00', NULL, 'cliente1@email.com', '11999999999'),
('Luiz da Silva', NULL, '451.122.510-93', 'welcome@gmail.com', '19925664394');

-- Popula pesquisas
INSERT INTO pesquisas (
    cod_cliente, cod_uf, cod_servico, tipo, cpf, cod_uf_nascimento, cod_uf_rg, data_entrada, nome, rg, nascimento, mae, anexo
) VALUES
  (1, 1, 1, 0, '45112251093', 1, 1, NOW(), 'Luiz da Silva', '279835619', '2000-07-22', 'Adriana da Silva', NULL),
  (2, 1, 2, 0, '07422567074', 1, 1, NOW(), 'Maria Santos', '457674167', '1985-05-10', 'Ana Santos', NULL),
  (1, 1, 3, 0, '61240168004', 1, 1, NOW(), 'Pedro Costa', '444853996', '1978-12-20', 'Clara Costa', NULL),
  (2, 1, 1, 0, '37904837021', 1, 1, NOW(), 'Lucas Lima', '444924978', '1995-07-15', 'Beatriz Lima', NULL);

-- Popula websites (se necessário para scraping)
INSERT INTO websites (nome, url, tipo, configuracao) VALUES 
('TJSP', 'https://esaj.tjsp.jus.br/cpopg/open.do', 'TJSP', '{"selectors": {"tipo_pesquisa": "//*[@id=\"cbPesquisa\"]", "campo_cpf": "//*[@id=\"campo_DOCPARTE\"]", "campo_nome": "//*[@id=\"campo_NMPARTE\"]", "botao_consultar": "//*[@id=\"botaoConsultarProcessos\"]"}}');
-- ON CONFLICT (nome) DO NOTHING;

INSERT INTO funcionarios (nome, cpf, email) VALUES ('Funcionario Teste', '472.841.100-15', 'teste@exemplo.com');