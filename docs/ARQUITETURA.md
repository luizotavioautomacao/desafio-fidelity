# Arquitetura do Sistema de Pesquisa Virtual Automático (SPV)

## Visão Geral

O Sistema de Pesquisa Virtual Automático foi redesenhado com uma arquitetura moderna, modular e escalável, migrando do MariaDB para PostgreSQL e implementando boas práticas de desenvolvimento.

## 🏗️ Arquitetura Geral

```
┌─────────────────────────────────────────────────────────────┐
│                    APRESENTAÇÃO                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   CLI       │  │   API       │  │   Web UI    │         │
│  │  (Scripts)  │  │  (Future)   │  │  (Future)   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                    LÓGICA DE NEGÓCIO                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ SPVAutomatico│  │DatabaseService│ │WebScraperService│    │
│  │   (Core)    │  │   (Data)    │  │  (Scraping) │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                    CAMADA DE DADOS                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ SQLAlchemy  │  │ PostgreSQL  │  │   Models    │         │
│  │   (ORM)     │  │  (Database) │  │  (Entities) │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Estrutura de Diretórios

```
desafio-fidelity/
├── database/
│   └── schema.sql              # Esquema PostgreSQL
├── src/
│   ├── config/
│   │   └── database.py         # Configuração do banco
│   ├── models/
│   │   └── models.py           # Modelos SQLAlchemy
│   ├── services/
│   │   ├── database_service.py # Serviços de dados
│   │   └── web_scraper_service.py # Serviços de scraping
│   └── spv_automatico.py       # Classe principal
├── tests/
│   └── test_database_service.py # Testes unitários
├── examples/
│   └── exemplo_uso.py          # Exemplos de uso
├── requirements.txt            # Dependências
├── docker-compose.yml          # Orquestração Docker
├── Dockerfile                  # Container da aplicação
├── setup.py                    # Script de instalação
├── README.md                   # Documentação principal
└── ARQUITETURA.md              # Esta documentação
```

## 🗄️ Modelo de Dados

### Tabelas Principais

#### 1. **estados**
- Armazena estados brasileiros
- Chave primária: `cod_uf`
- Índices em `uf` para consultas rápidas

#### 2. **servicos**
- Tipos de serviços (cível, criminal)
- Campos booleanos para classificação
- Suporte a múltiplos tipos

#### 3. **clientes**
- Informações dos clientes
- Suporte a CPF e CNPJ
- Controle de status ativo/inativo

#### 4. **funcionarios**
- Funcionários responsáveis
- CPF único para identificação
- Controle de status ativo/inativo

#### 5. **pesquisas** (Tabela Central)
- Dados das pesquisas a serem realizadas
- Relacionamentos com clientes, estados e serviços
- Campos para dados originais e corrigidos
- Controle de status e prioridade

#### 6. **lotes**
- Agrupamentos de pesquisas
- Controle de prioridade e status
- Rastreamento de funcionário responsável

#### 7. **lote_pesquisas**
- Tabela de relacionamento N:N
- Rastreamento de conclusão
- Observações e metadados

#### 8. **pesquisa_spv**
- Resultados das pesquisas automatizadas
- Controle de filtros e resultados
- Métricas de tempo de execução
- Tratamento de erros

#### 9. **websites**
- Configurações dos tribunais
- Seletores CSS/XPath em JSON
- Suporte a múltiplos tribunais

### Melhorias no Esquema

1. **Normalização**: Estrutura mais limpa e eficiente
2. **Índices**: Performance otimizada para consultas frequentes
3. **Triggers**: Atualização automática de timestamps
4. **Funções**: Consultas complexas encapsuladas
5. **Views**: Consultas simplificadas para relatórios
6. **Constraints**: Integridade referencial garantida

## 🔧 Componentes Principais

### 1. **SPVAutomatico** (Core)
```python
class SPVAutomatico:
    - executar_pesquisa(): Executa pesquisa individual
    - processar_pesquisas_pendentes(): Processa lote com paginação
    - executar_ciclo_completo(): Executa todos os filtros
    - executar_loop_continuo(): Execução contínua
```

**Responsabilidades:**
- Orquestração do processo de pesquisa
- Controle de tempo de execução
- Gestão de ciclos e filtros
- Tratamento de erros e recuperação

### 2. **DatabaseService** (Data Layer)
```python
class DatabaseService:
    - get_pesquisas_pendentes(): Consulta com paginação
    - salvar_resultado_spv(): Persistência de resultados
    - get_estatisticas_pesquisas(): Métricas do sistema
    - marcar_pesquisa_concluida(): Atualização de status
```

**Responsabilidades:**
- Abstração do acesso a dados
- Consultas otimizadas com paginação
- Transações e rollback
- Métricas e estatísticas

### 3. **WebScraperService** (Scraping Layer)
```python
class WebScraperService:
    - pesquisar(): Execução de pesquisas
    - setup_driver(): Configuração do browser
    - close_driver(): Limpeza de recursos
```

**Responsabilidades:**
- Automação de browser
- Configuração de diferentes tribunais
- Tratamento de timeouts e erros
- Gestão de recursos do WebDriver

### 4. **ResultAnalyzer** (Analysis)
```python
class ResultAnalyzer:
    - analisar_resultado(): Classificação de resultados
```

**Responsabilidades:**
- Análise de conteúdo das páginas
- Classificação de resultados (nada consta, criminal, cível)
- Tratamento de casos especiais

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

## 🚀 Melhorias Implementadas

### 1. **Performance**
- **Paginação**: Processamento eficiente de grandes volumes
- **Índices**: Consultas otimizadas no PostgreSQL
- **Pool de Conexões**: Reutilização de conexões
- **Batch Processing**: Processamento em lotes

### 2. **Escalabilidade**
- **Arquitetura Modular**: Componentes independentes
- **Configuração Flexível**: Suporte a múltiplos tribunais
- **Factory Pattern**: Criação dinâmica de scrapers
- **Context Managers**: Gestão automática de recursos

### 3. **Robustez**
- **Tratamento de Erros**: Gestão completa de exceções
- **Logging**: Sistema detalhado de logs
- **Retry Logic**: Tentativas automáticas
- **Timeout Control**: Controle de tempo de execução

### 4. **Manutenibilidade**
- **Separation of Concerns**: Responsabilidades bem definidas
- **Type Hints**: Documentação de tipos
- **Documentation**: Docstrings completas
- **Testing**: Testes unitários

### 5. **Monitoramento**
- **Métricas**: Estatísticas detalhadas
- **Logs**: Rastreamento completo
- **Status Tracking**: Controle de progresso
- **Error Reporting**: Relatórios de erro

## 🔧 Configuração e Deploy

### 1. **Desenvolvimento Local**
```bash
# Setup automático
python setup.py

# Execução manual
python src/spv_automatico.py
```

### 2. **Docker**
```bash
# Deploy completo
docker-compose up -d

# Apenas banco
docker-compose up postgres
```

### 3. **Produção**
- Configuração via variáveis de ambiente
- Logs estruturados
- Monitoramento de recursos
- Backup automático do banco

## 📊 Métricas e Monitoramento

### 1. **Métricas de Performance**
- Tempo de execução por pesquisa
- Taxa de sucesso/erro
- Throughput (pesquisas/minuto)
- Uso de recursos (CPU, memória)

### 2. **Métricas de Negócio**
- Total de pesquisas processadas
- Distribuição por tipo de resultado
- Pesquisas por cliente
- Tendências temporais

### 3. **Alertas**
- Falhas de conexão
- Timeouts excessivos
- Erros de scraping
- Problemas de banco

## 🔮 Roadmap e Melhorias Futuras

### 1. **Funcionalidades**
- API REST para integração
- Interface web para monitoramento
- Suporte a mais tribunais
- Processamento assíncrono

### 2. **Tecnologias**
- Redis para cache
- Celery para tasks assíncronas
- Prometheus para métricas
- ELK Stack para logs

### 3. **Arquitetura**
- Microserviços
- Message Queues
- Load Balancing
- Auto-scaling

## 🛡️ Segurança

### 1. **Dados Sensíveis**
- Criptografia de CPFs
- Logs sem dados pessoais
- Controle de acesso ao banco
- Backup seguro

### 2. **Infraestrutura**
- HTTPS para APIs
- Firewall e VPN
- Monitoramento de segurança
- Atualizações automáticas

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

## 🎯 Conclusão

A nova arquitetura do Sistema SPV representa uma evolução significativa em termos de:

- **Performance**: Processamento mais eficiente
- **Escalabilidade**: Suporte a crescimento
- **Manutenibilidade**: Código mais limpo e organizado
- **Robustez**: Melhor tratamento de erros
- **Monitoramento**: Visibilidade completa do sistema

O sistema está preparado para crescer e se adaptar às necessidades futuras, mantendo a compatibilidade com os requisitos originais enquanto adiciona capacidades modernas de desenvolvimento e operação. 