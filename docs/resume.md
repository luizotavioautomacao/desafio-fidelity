## 🎯 Objetivo

O **SPV (Sistema de Pesquisa Virtual Automático)** é uma solução desenvolvida em **Python** para automatizar consultas de pesquisas nas plataformas de tribunais jurídicos do Brasil. O sistema realiza **web scraping automatizado** para verificar processos judiciais por **CPF, RG ou nome**.

---

## 🏗️ Arquitetura e Tecnologias

### Stack Principal

* **Backend:** Python 3.8+
* **Banco de Dados:** PostgreSQL 12+ (migrado do MariaDB)
* **ORM:** SQLAlchemy 2.0
* **Web Scraping:** Selenium 4.15 com Microsoft Edge WebDriver
* **Containerização:** Docker e Docker Compose
* **Testes:** Pytest com cobertura

### Arquitetura Modular

```
┌──────────────────┐
│   SPVAutomatico  │ ← Classe principal (orquestração)
├──────────────────┤
│ DatabaseService  │ ← Camada de dados
│ WebScraperService│ ← Web scraping
└──────────────────┘
```

---

## 🗂️ Modelo de Dados

O sistema utiliza um esquema PostgreSQL otimizado com as seguintes tabelas principais:

* **pesquisas**: Dados das pesquisas a serem realizadas
* **pesquisa\_spv**: Resultados das pesquisas automatizadas
* **clientes**: Informações dos clientes
* **funcionarios**: Funcionários responsáveis
* **lotes**: Agrupamentos de pesquisas
* **websites**: Configurações dos tribunais
* **estados** e **servicos**: Dados de referência

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

## 📦 Deploy e Execução

### Opções de Execução

* **Setup Automático:** `python setup.py`
* **Docker:** `docker-compose up -d`
* **Execução Local:** `./scripts/run_local.sh`
* **Modo Desenvolvimento:** Sem web scraping para testes

---

## 📊 Monitoramento e Métricas

* Logs detalhados em console e arquivo
* Estatísticas de pesquisas (pendentes, concluídas, etc.)
* Métricas de tempo de execução
* Tratamento de erros com recuperação automática

---

## ✅ Qualidade de Código

* Testes unitários com Pytest
* Cobertura de código
* Linting com Flake8
* Formatação com Black
* Type checking com MyPy

---

## 🔄 Fluxo de Trabalho

1. **Inicialização:** Carregamento de configurações e conexão com banco
2. **Busca:** Pesquisas pendentes com paginação
3. **Execução:** Web scraping para cada pesquisa
4. **Análise:** Classificação dos resultados
5. **Persistência:** Salvamento no banco de dados
6. **Controle:** Atualização de status e métricas
