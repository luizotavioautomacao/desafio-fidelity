# 🧪 Guia Completo de Testes

Este guia mostra como testar todas as melhorias implementadas no sistema SPV seguindo os princípios SOLID.

## 📋 Pré-requisitos

Certifique-se de ter o ambiente configurado:

```bash
make i
```

## 🚀 Como Testar as Melhorias

### 1. **Testes Unitários**

Execute os testes unitários para verificar cada componente isoladamente:

```bash
# Todos os testes unitários
make test

# Testes específicos por serviço
PYTHONPATH=. venv/bin/python -m pytest tests/test_validation_service.py -v
PYTHONPATH=. venv/bin/python -m pytest tests/test_validation_service.py -v
PYTHONPATH=. venv/bin/python -m pytest tests/test_config_service.py -v
PYTHONPATH=. venv/bin/python -m pytest tests/test_logging_service.py -v
PYTHONPATH=. venv/bin/python -m pytest tests/test_database_service.py -v
```

### 2. **Testes de Integração**

Execute os testes de integração para verificar a interação entre componentes:

```bash
# Testes de integração
PYTHONPATH=. venv/bin/python -m pytest tests/test_integration.py -v
```

### 3. **Cobertura de Testes**

Verifique a cobertura de código:

```bash
# Cobertura completa
make coverage

# Relatório HTML de cobertura
make coverage-html
```

> 📄 **Documentação** da [cobertura de testes](./coverage.md)


## 🔍 O que Testar

### **1. Princípio da Responsabilidade Única (SRP)**

#### - ValidationService
```bash
PYTHONPATH=. venv/bin/python -m pytest tests/test_validation_service.py::TestValidationService::test_validate_cpf_valid -v
```

##### **O que testa:**
- Validação de CPF com dígitos verificadores
- Validação de RG
- Validação de nomes
- Sanitização de documentos

#### - ConfigService
```bash
PYTHONPATH=. venv/bin/python -m pytest tests/test_config_service.py::TestConfigService::test_database_config_defaults -v
```

##### **O que testa:**
- Carregamento de configurações do banco
- Configurações do WebDriver
- Configurações de scraping
- Configurações de logging

#### - LoggingService
```bash
PYTHONPATH=. venv/bin/python -m pytest tests/test_logging_service.py::TestLoggingService::test_log_execution_start -v
```

##### **O que testa:**
- Configuração de loggers
- Métodos de logging estruturado
- Tratamento de diferentes tipos de log

### **2. Princípio da Inversão de Dependência (DIP)**

#### Injeção de Dependência
```bash
PYTHONPATH=. venv/bin/python -m pytest tests/test_integration.py::TestIntegration::test_create_spv_automatico -v
```

**O que testa:**
- Criação do SPV com injeção de dependência
- Verificação de todos os serviços injetados
- Baixo acoplamento entre componentes

### **3. Interfaces (ISP)**

#### - DatabaseService
```bash
PYTHONPATH=. venv/bin/python -m pytest tests/test_database_service.py::TestDatabaseService::test_get_pesquisas_pendentes -v
```

##### **O que testa:**
- Implementação da interface IDatabaseService
- Operações de banco de dados
- Tratamento de erros

### **4. Tratamento de Erros**

#### - Validação de Erros
```bash
PYTHONPATH=. venv/bin/python -m pytest tests/test_validation_service.py::TestValidationService::test_validate_cpf_invalid -v
```

##### **O que testa:**
- Validação de dados inválidos
- Mensagens de erro apropriadas
- Recuperação de erros

#### - Erros de Banco
```bash
PYTHONPATH=. venv/bin/python -m pytest tests/test_database_service.py::TestDatabaseService::test_erro_na_consulta -v
```

##### **O que testa:**
- Tratamento de erros de banco de dados
- Rollback de transações
- Logging de erros

## 📊 Resultados

### **Testes Unitários**
- ✅ 40+ testes passando
- ✅ Cobertura de código > 68%
- ✅ Serviços testados isoladamente

### **Testes de Integração**
- ✅ Integração entre componentes funcionando
- ✅ Injeção de dependência operacional
- ✅ Fluxo completo do sistema

### **Demonstração**
- ✅ Validação de dados funcionando
- ✅ Configuração centralizada
- ✅ Logging estruturado
- ✅ Tratamento de erros robusto

## 📈 Métricas de Qualidade

### **Antes x Depois**
- ❌ Código monolítico x ✅ Código modular e organizado
- ❌ Dificuldade para testar x ✅ Alta testabilidade (>68% cobertura)
- ❌ Alto acoplamento x ✅ Baixo acoplamento (injeção de dependência)
- ❌ Tratamento de erros básico x ✅ Tratamento robusto de erros
- ✅ Configuração centralizada
- ✅ Logging estruturado