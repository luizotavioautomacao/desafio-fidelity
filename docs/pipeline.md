# Arquitetura Analítica SPV – Guia Completo

## 1. Pipeline de Ingestão (ETL/ELT)

### a) Extração de Dados
- **Ferramentas sugeridas:** Airbyte, Fivetran, scripts Python (psycopg2, pandas).
- **Exemplo Python:**
```python
import pandas as pd
import psycopg2
conn = psycopg2.connect("dbname=spv user=postgres password=xxx host=localhost")
df = pd.read_sql("SELECT * FROM pesquisas WHERE data_entrada >= '2024-01-01'", conn)
df.to_csv('pesquisas_2024.csv', index=False)
```
- **Armazenamento de anexos:** Upload para S3/GCS, salvar URL no banco.

---

## 2. Transformação e Modelagem (dbt + SQL)

### a) Estrutura de Projeto dbt
```
/dbt_spv/
  models/
    staging/
      stg_pesquisas.sql
      stg_clientes.sql
    marts/
      fato_pesquisas.sql
      dim_cliente.sql
      dim_servico.sql
      dim_estado.sql
      dim_tempo.sql
```

### b) Exemplos de Modelos dbt

#### Staging (Limpeza e Padronização)
```sql
-- models/staging/stg_pesquisas.sql
SELECT
  cod_pesquisa,
  cod_cliente,
  cod_servico,
  cod_uf,
  status,
  data_entrada::date as data_entrada,
  data_conclusao::date as data_conclusao,
  EXTRACT(EPOCH FROM (data_conclusao - data_entrada))/60 as tempo_conclusao_min,
  cpf,
  rg,
  nome,
  nascimento,
  mae,
  anexo
FROM {{ source('public', 'pesquisas') }}
```

#### Dimensão Cliente
```sql
-- models/marts/dim_cliente.sql
SELECT
  cod_cliente as id_cliente,
  nome,
  cnpj,
  cpf,
  email,
  telefone,
  ativo
FROM {{ ref('stg_clientes') }}
```

#### Fato Pesquisas
```sql
-- models/marts/fato_pesquisas.sql
SELECT
  p.cod_pesquisa as id_pesquisa,
  p.data_entrada,
  p.cod_cliente,
  p.cod_servico,
  p.cod_uf,
  p.status,
  p.tempo_conclusao_min,
  p.cpf,
  p.rg,
  p.nome,
  p.nascimento,
  p.mae,
  p.anexo
FROM {{ ref('stg_pesquisas') }} p
```

#### Dimensão Tempo
```sql
-- models/marts/dim_tempo.sql
SELECT
  DISTINCT data_entrada as data,
  EXTRACT(YEAR FROM data_entrada) as ano,
  EXTRACT(MONTH FROM data_entrada) as mes,
  EXTRACT(DAY FROM data_entrada) as dia
FROM {{ ref('fato_pesquisas') }}
```

---

## 3. Data Warehouse (Star Schema)

### a) Modelo Estrela
- **Fato:** fato_pesquisas
- **Dimensões:** dim_cliente, dim_servico, dim_estado, dim_tempo

### b) DDL Exemplo
```sql
CREATE TABLE fato_pesquisas (
  id_pesquisa UUID PRIMARY KEY,
  data_entrada DATE,
  id_cliente INT,
  id_servico INT,
  id_estado INT,
  status VARCHAR(20),
  tempo_conclusao_min NUMERIC,
  cpf VARCHAR(14),
  rg VARCHAR(20),
  nome VARCHAR(200),
  nascimento DATE,
  mae VARCHAR(200),
  anexo TEXT
);

CREATE TABLE dim_cliente (...);
CREATE TABLE dim_servico (...);
CREATE TABLE dim_estado (...);
CREATE TABLE dim_tempo (...);
```

---

## 4. Materialized Views e Indexação

### a) Materialized View para Pesquisas Pendentes
```sql
CREATE MATERIALIZED VIEW mv_pesquisas_pendentes AS
SELECT * FROM pesquisas_pendentes;
-- Atualize periodicamente:
REFRESH MATERIALIZED VIEW mv_pesquisas_pendentes;
```

### b) Indexação Multicoluna
```sql
CREATE INDEX idx_spv_cod_filtro_resultado
ON pesquisa_spv (cod_pesquisa, filtro, resultado);
```

---

## 5. Versionamento de Dados (SCD/History Table)

```sql
CREATE TABLE pesquisas_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  cod_pesquisa INT,
  status VARCHAR(20),
  valid_from TIMESTAMP,
  valid_to TIMESTAMP
);
```
- Use triggers para inserir na tabela de histórico a cada update.

---

## 6. Armazenamento Externo para Anexos

- Substitua o campo `anexo TEXT` por `anexo_url TEXT`.
- Processo: Upload do arquivo para S3/GCS → salva URL no banco.

---

## 7. Metadados Flexíveis (JSONB)

- Exemplo de coluna em `servicos`:
```sql
ALTER TABLE servicos ADD COLUMN metadados JSONB;
-- Exemplo de uso:
UPDATE servicos SET metadados = '{"validar_cpf": true, "prazo_execucao": "48h"}' WHERE cod_servico = 1;
```

---

## 8. Exemplos de Queries para Dashboards

### a) Volume de Pesquisas por Mês
```sql
SELECT
  EXTRACT(YEAR FROM data_entrada) as ano,
  EXTRACT(MONTH FROM data_entrada) as mes,
  COUNT(*) as total_pesquisas
FROM fato_pesquisas
GROUP BY ano, mes
ORDER BY ano, mes;
```

### b) Tempo Médio de Conclusão por Serviço
```sql
SELECT
  s.nome as servico,
  AVG(f.tempo_conclusao_min) as tempo_medio_min
FROM fato_pesquisas f
JOIN dim_servico s ON f.id_servico = s.id_servico
WHERE f.tempo_conclusao_min IS NOT NULL
GROUP BY s.nome
ORDER BY tempo_medio_min;
```

### c) Taxa de Erro em Pesquisas SPV
```sql
SELECT
  resultado,
  COUNT(*) as total
FROM pesquisa_spv
GROUP BY resultado;
-- resultado=7 pode ser considerado erro
```

### d) Pendências por Cliente
```sql
SELECT
  c.nome as cliente,
  COUNT(*) as pendentes
FROM fato_pesquisas f
JOIN dim_cliente c ON f.id_cliente = c.id_cliente
WHERE f.status = 'PENDENTE'
GROUP BY c.nome
ORDER BY pendentes DESC;
```

---

## 9. Dashboard (Metabase/Superset/Power BI/Streamlit)

- Conecte ao Data Warehouse.
- Crie dashboards com:
  - Filtros por período, cliente, serviço, status.
  - Gráficos de linha (evolução), pizza (distribuição), tabela detalhada.
  - Drill-down: clique no cliente → vê detalhes das pesquisas.

---

## 10. Pipeline Orquestrado (Airflow/dbt)

- **Airflow DAG**:
  1. Extrai dados do PostgreSQL.
  2. Salva no Data Lake.
  3. Roda dbt para transformar/modelar.
  4. Atualiza materialized views.
  5. Notifica BI (Metabase) para atualização.

---

## Resumo Visual

```
[PostgreSQL OLTP] --(Airbyte/ETL)--> [Data Lake (S3/BigQuery)] --(dbt/Airflow)--> [Data Warehouse] --(Metabase/PowerBI)--> [Dashboards]
```

---

## Próximos passos para execução de um pipeline robusto

- Escolha as ferramentas (Airbyte, dbt, Metabase, etc).
- Implemente scripts de ingestão e transformação (exemplos acima).
- Modele o Data Warehouse (Star Schema).
- Crie dashboards com as queries sugeridas.
- Implemente versionamento e materialized views para performance e histórico.