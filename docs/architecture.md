# 🏗️ Arquitetura do Sistema de Pesquisa Virtual (SPV)

## 🎯 Objetivo

O **SPV (Sistema de Pesquisa Virtual Automático)** é uma solução desenvolvida em **Python** para automatizar consultas de pesquisas nas plataformas de tribunais jurídicos do Brasil. O sistema realiza **web scraping automatizado** para verificar processos judiciais por **CPF, RG ou nome**.

---
### Stack Principal

* **Backend:** Python 3.8+
* **Banco de Dados:** PostgreSQL 12+ (migrado do MariaDB)
* **ORM:** SQLAlchemy 2.0
* **Web Scraping:** Selenium 4.15 com Microsoft Edge WebDriver
* **Containerização:** Docker e Docker Compose
* **Testes:** Pytest com cobertura

### Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    APRESENTAÇÃO                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │    CLI      │  │     API     │  │  Streamlit  │          │
│  │  (Scripts)  │  │  (Future)   │  │  (Future)   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│                    LÓGICA DE NEGÓCIO                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────────┐   │
│  │ SPVAutomatico│  │DatabaseService│  │WebScraperService│   │
│  │   (Core)     │  │   (Data)      │  │  (Scraping)     │   │
│  └──────────────┘  └───────────────┘  └─────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                    CAMADA DE DADOS                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ SQLAlchemy  │  │ PostgreSQL  │  │   Models    │          │
│  │   (ORM)     │  │  (Database) │  │  (Entities) │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Modelo de Dados

O sistema utiliza um esquema PostgreSQL otimizado com as seguintes tabelas principais:

* **pesquisas**: Dados das pesquisas a serem realizadas
* **pesquisa_spv**: Resultados das pesquisas automatizadas
* **clientes**: Informações dos clientes
* **funcionarios**: Funcionários responsáveis
* **lotes**: Agrupamentos de pesquisas
* **websites**: Configurações dos tribunais
* **estados** e **servicos**: Dados de referência

### Melhorias no Esquema

1. **Normalização**: Estrutura mais limpa e eficiente
2. **Índices**: Performance otimizada para consultas frequentes
3. **Triggers**: Atualização automática de timestamps
4. **Funções**: Consultas complexas encapsuladas
5. **Views**: Consultas simplificadas para relatórios
6. **Constraints**: Integridade referencial garantida

---

## 🚀 Funcionalidades Principais

* Web Scraping Automatizado
* Suporte a múltiplos tribunais (ex: TJSP)
* Configuração flexível via JSON
* Tratamento robusto de timeouts e erros

### Sistema de Filtros

* **Filtro 0:** Pesquisa por CPF
* **Filtro 1:** Pesquisa por RG
* **Filtro 2:** Pesquisa por Nome
* **Filtro 3:** Pesquisa por RG (alternativo)

### Classificação de Resultados

* **Resultado 1:** Nada consta
* **Resultado 2:** Criminal
* **Resultado 5:** Cível
* **Resultado 7:** Erro

### Processamento em Lotes

* Paginação para grandes volumes
* Controle de prioridade
* Execução contínua ou por ciclos

---

## ⚙️ Características Técnicas

* **Arquitetura Modular:** Código organizado em serviços reutilizáveis
* **Logging Completo:** Sistema de logs para monitoramento
* **Tratamento de Erros:** Gestão robusta de exceções
* **Configuração Flexível:** Suporte a diferentes tribunais
* **Performance Otimizada:** Índices e consultas otimizadas
* **Containerização:** Suporte completo a Docker

---

## 📊 Monitoramento e Métricas

* Logs detalhados em console e arquivo
* Tratamento de erros com recuperação automática

### 1. **Métricas de Performance**
- Tempo de execução por pesquisa
- Taxa de sucesso/erro
- Throughput (pesquisas/minuto)
- Uso de recursos (CPU, memória)

### 2. **Métricas de Negócio**
- Total de pesquisas processadas
- Distribuição por tipo de resultado (pendentes, concluídas, etc.)
- Pesquisas por cliente
- Tendências temporais

### 3. **Alertas**
- Falhas de conexão
- Timeouts excessivos
- Erros de scraping
- Problemas de banco

---

## ✅ Qualidade de Código

* Testes unitários com Pytest
* Cobertura de código

---

## 🔄 Fluxo de Execução

### 1. **Inicialização**
```
1. Carregamento de configurações (.env)
2. Conexão com banco PostgreSQL
3. Inicialização de serviços
4. Verificação de dependências
```

### 2. **Ciclo de Pesquisa**
```
1. Busca pesquisas pendentes (paginação)
2. Para cada pesquisa:
   a. Determina documento baseado no filtro
   b. Executa pesquisa no tribunal
   c. Analisa resultado
   d. Salva resultado no banco
   e. Atualiza status
3. Controle de tempo e limites
4. Tratamento de erros
```

### 3. **Gestão de Filtros**
```
Filtro 0: CPF
Filtro 1: RG
Filtro 2: Nome
Filtro 3: RG (alternativo)

- Execução sequencial por prioridade
- Controle de disponibilidade de dados
- Fallback entre filtros
```

---

## 📈 Comparação com Versão Original

| Aspecto | Versão Original | Nova Versão |
|---------|----------------|-------------|
| **Banco** | MariaDB | PostgreSQL |
| **ORM** | SQL direto | SQLAlchemy |
| **Arquitetura** | Monolítica | Modular |
| **Paginação** | LIMIT fixo | Paginação dinâmica |
| **Logging** | Print statements | Sistema estruturado |
| **Configuração** | Hardcoded | Variáveis de ambiente |
| **Testes** | Nenhum | Testes unitários |
| **Deploy** | Manual | Docker |
| **Monitoramento** | Nenhum | Métricas completas |
| **Tratamento de Erros** | Básico | Robusto |

---

## 🎯 Conclusão

A nova arquitetura do Sistema SPV representa uma evolução significativa em termos de:

- **Performance**: Processamento mais eficiente
- **Escalabilidade**: Suporte a crescimento
- **Manutenibilidade**: Código mais limpo e organizado
- **Robustez**: Melhor tratamento de erros
- **Monitoramento**: Visibilidade completa do sistema

O sistema está preparado para crescer e se adaptar às necessidades futuras, mantendo a compatibilidade com os requisitos originais enquanto adiciona capacidades modernas de desenvolvimento e operação. 

---

### 🔮 Roadmap e Melhorias Futuras

* API REST para integração
* Dashboards com Streamlit
* Suporte a mais tribunais
* Celery para tasks assíncronas
* Monitoramento avançado (Prometheus, ELK Stack para logs, Kafka, Grafana)
* Redis para cache

#### 🛠️ Pipeline Analítico e Dados

Para evolução analítica do SPV, recomenda-se a construção de um pipeline de dados moderno, incluindo:

- **ETL/ELT Automatizado:** Ferramentas como Airbyte, Fivetran ou scripts Python para extração de dados do PostgreSQL e ingestão em Data Lake/Data Warehouse.
- **Transformação e Modelagem com dbt:** Organização dos dados em camadas (staging, marts, dimensões e fatos) para facilitar análises e relatórios.
- **Data Warehouse (Star Schema):** Estrutura centralizada para análises históricas, com tabelas fato e dimensões (ex: fato_pesquisas, dim_cliente, dim_servico).
- **Materialized Views e Indexação:** Para acelerar consultas analíticas e relatórios de BI.
- **Versionamento de Dados:** Tabelas de histórico (SCD) para rastrear mudanças e garantir auditoria.
- **Armazenamento Externo de Anexos:** Upload de arquivos para S3/GCS e referência por URL no banco.
- **Metadados Flexíveis:** Uso de colunas JSONB para atributos dinâmicos em tabelas como servicos.
- **Dashboards (Metabase, Power BI, Superset, Streamlit):** Visualização de métricas de negócio, performance e operação, com queries otimizadas e filtros dinâmicos.
- **Orquestração com Airflow:** Automatização de todo o pipeline, desde a extração até a atualização de dashboards.

Essas práticas permitem:
- Análises históricas e operacionais
- Métricas de performance e negócio em tempo real
- Governança e rastreabilidade dos dados
- Escalabilidade para grandes volumes

#### 🛡️ Segurança

* Criptografia de dados sensíveis
* Controle de acesso ao banco
* Backup seguro
* Firewall e VPN
* Monitoramento de segurança

#### 🏗️ Arquitetura
* Microserviços
* Message Queues
* Load Balancing
* Auto-scaling
* CI/CD
