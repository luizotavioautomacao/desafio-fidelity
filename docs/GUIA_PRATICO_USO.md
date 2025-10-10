# 🚀 Guia Prático - Como Usar o Sistema SPV

Este guia mostra como testar e usar o sistema SPV com web scraping e filtros.

## 📋 Índice

1. [Como Testar as Melhorias](#como-testar-as-melhorias)
2. [Como Fazer Web Scraping](#como-fazer-web-scraping)
3. [Tipos de Filtros](#tipos-de-filtros)
4. [Configuração do Sistema](#configuração-do-sistema)
5. [Exemplos Práticos](#exemplos-práticos)
6. [Troubleshooting](#troubleshooting)

## 🧪 Como Testar as Melhorias

### **1. Testes Rápidos**

```bash
# Execute todos os testes
python -m pytest tests/ -v

# Testes específicos
python -m pytest tests/test_validation_service.py -v
python -m pytest tests/test_config_service.py -v
python -m pytest tests/test_logging_service.py -v
python -m pytest tests/test_database_service.py -v
```

### **2. Demonstração das Melhorias**

```bash
# Demonstração completa das melhorias SOLID
python examples/demo_solid_implementation.py

# Exemplo de web scraping
python examples/web_scraping_exemplo.py
```

### **3. Cobertura de Código**

```bash
# Ver cobertura detalhada
python -m pytest tests/ --cov=src --cov-report=term-missing

# Relatório HTML
python -m pytest tests/ --cov=src --cov-report=html
```

## 🌐 Como Fazer Web Scraping

### **1. Configuração Básica**

```python
from src.services.config_service import ConfigService
from src.spv_automatico import create_spv_automatico

# Carrega configuração
config_service = ConfigService()

# Cria instância do SPV
spv = create_spv_automatico(config_service)
```

### **2. Execução de Pesquisa**

```python
# Define o filtro (0=CPF, 1=RG, 2=Nome, 3=RG alternativo)
spv.filtro = 0

# Executa uma pesquisa
resultado = spv.executar_pesquisa(
    nome="João Silva",
    cpf="123.456.789-09",
    rg="12.345.678-9",
    cod_pesquisa=1001
)

if resultado:
    print("✅ Pesquisa executada com sucesso!")
else:
    print("❌ Falha na pesquisa")
```

### **3. Processamento em Lote**

```python
# Processa pesquisas pendentes
pesquisas_processadas = spv.processar_pesquisas_pendentes(limit=10)
print(f"Processadas {pesquisas_processadas} pesquisas")

# Executa ciclo completo
spv.executar_ciclo_completo()
```

## 🎯 Tipos de Filtros

### **Filtro 0 - CPF**
```python
spv.filtro = 0
# Pesquisa por CPF da pessoa
# Exemplo: "123.456.789-09"
```

### **Filtro 1 - RG**
```python
spv.filtro = 1
# Pesquisa por RG da pessoa
# Exemplo: "12.345.678-9"
```

### **Filtro 2 - Nome**
```python
spv.filtro = 2
# Pesquisa por nome completo
# Exemplo: "João Silva"
```

### **Filtro 3 - RG Alternativo**
```python
spv.filtro = 3
# Pesquisa por RG (formato alternativo)
# Exemplo: "12.345.678-9"
```

## ⚙️ Configuração do Sistema

### **1. Arquivo .env**

```env
# Configuração do Banco de Dados
DATABASE_URL=postgresql://postgres:password@localhost:5432/spv_automatico
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# Configuração do WebDriver
EDGE_DRIVER_PATH=/path/to/msedgedriver
HEADLESS=True
WEBDRIVER_TIMEOUT=30
PAGE_LOAD_TIMEOUT=60

# Configuração de Scraping
WEBSITE_TYPE=TJSP
MAX_EXECUTION_TIME=600
DELAY_BETWEEN_REQUESTS=1.0
MAX_RETRIES=3

# Configuração de Logging
LOG_LEVEL=INFO
LOG_FILE=spv_automatico.log

# Modo de Desenvolvimento
DISABLE_SCRAPING=False
```

### **2. Configuração do WebDriver**

```bash
# Download do Microsoft Edge WebDriver
# Acesse: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

# Configure o caminho no .env
EDGE_DRIVER_PATH=/caminho/para/msedgedriver
```

### **3. Configuração do Banco**

```sql
-- Execute o schema do banco
\i database/schema.sql

-- Verifique se as tabelas foram criadas
\dt
```

## 💻 Exemplos Práticos

### **Exemplo 1: Pesquisa Individual**

```python
#!/usr/bin/env python3
"""
Exemplo de pesquisa individual
"""

from src.services.config_service import ConfigService
from src.spv_automatico import create_spv_automatico

def pesquisa_individual():
    # Configuração
    config_service = ConfigService()
    spv = create_spv_automatico(config_service)
    
    # Pesquisa por CPF
    spv.filtro = 0
    resultado = spv.executar_pesquisa(
        nome="João Silva",
        cpf="123.456.789-09",
        rg="12.345.678-9",
        cod_pesquisa=1001
    )
    
    if resultado:
        print("✅ Pesquisa por CPF concluída")
    
    # Pesquisa por RG
    spv.filtro = 1
    resultado = spv.executar_pesquisa(
        nome="Maria Santos",
        cpf="",
        rg="12.345.678-9",
        cod_pesquisa=1002
    )
    
    if resultado:
        print("✅ Pesquisa por RG concluída")

if __name__ == "__main__":
    pesquisa_individual()
```

### **Exemplo 2: Processamento em Lote**

```python
#!/usr/bin/env python3
"""
Exemplo de processamento em lote
"""

from src.services.config_service import ConfigService
from src.spv_automatico import create_spv_automatico

def processamento_lote():
    # Configuração
    config_service = ConfigService()
    spv = create_spv_automatico(config_service)
    
    # Processa pesquisas pendentes
    print("🔄 Processando pesquisas pendentes...")
    
    for filtro in range(4):  # 0, 1, 2, 3
        spv.filtro = filtro
        pesquisas_processadas = spv.processar_pesquisas_pendentes(limit=10)
        
        if pesquisas_processadas > 0:
            print(f"✅ Filtro {filtro}: {pesquisas_processadas} pesquisas processadas")
        else:
            print(f"ℹ️ Filtro {filtro}: Nenhuma pesquisa pendente")

if __name__ == "__main__":
    processamento_lote()
```

### **Exemplo 3: Validação de Dados**

```python
#!/usr/bin/env python3
"""
Exemplo de validação de dados
"""

from src.services.validation_service import ValidationService

def validar_dados():
    validation_service = ValidationService()
    
    # Validação de CPF
    cpf = "123.456.789-09"
    result = validation_service.validate_cpf(cpf)
    
    if result.is_valid:
        print(f"✅ CPF válido: {result.corrected_value}")
    else:
        print(f"❌ CPF inválido: {result.error_message}")
    
    # Validação de RG
    rg = "12.345.678-9"
    result = validation_service.validate_rg(rg)
    
    if result.is_valid:
        print(f"✅ RG válido: {result.corrected_value}")
    else:
        print(f"❌ RG inválido: {result.error_message}")
    
    # Validação de nome
    nome = "João Silva"
    result = validation_service.validate_nome(nome)
    
    if result.is_valid:
        print(f"✅ Nome válido: {result.corrected_value}")
    else:
        print(f"❌ Nome inválido: {result.error_message}")

if __name__ == "__main__":
    validar_dados()
```

### **Exemplo 4: Configuração Avançada**

```python
#!/usr/bin/env python3
"""
Exemplo de configuração avançada
"""

import os
from src.services.config_service import ConfigService

def configuracao_avancada():
    # Configurações via variáveis de ambiente
    os.environ['WEBSITE_TYPE'] = 'TJSP'
    os.environ['HEADLESS'] = 'False'
    os.environ['WEBDRIVER_TIMEOUT'] = '60'
    os.environ['DELAY_BETWEEN_REQUESTS'] = '2.0'
    os.environ['LOG_LEVEL'] = 'DEBUG'
    
    # Carrega configuração
    config_service = ConfigService()
    
    print("⚙️ Configurações carregadas:")
    print(f"   Website: {config_service.scraping.website_type}")
    print(f"   Headless: {config_service.webdriver.headless}")
    print(f"   Timeout: {config_service.webdriver.timeout}s")
    print(f"   Delay: {config_service.scraping.delay_between_requests}s")
    print(f"   Log Level: {config_service.logging.level}")

if __name__ == "__main__":
    configuracao_avancada()
```

## 🔧 Troubleshooting

### **Problema: Erro de WebDriver**

```bash
# Solução 1: Download manual
# Baixe o Microsoft Edge WebDriver e configure o caminho

# Solução 2: Modo de desenvolvimento
export DISABLE_SCRAPING=true
python src/spv_automatico.py

# Solução 3: Docker
docker-compose up -d
```

### **Problema: Erro de Banco de Dados**

```bash
# Verifique a conexão
psql -U postgres -d spv_automatico

# Verifique as variáveis de ambiente
echo $DATABASE_URL

# Execute o schema
psql -U postgres -d spv_automatico -f database/schema.sql
```

### **Problema: Testes Falhando**

```bash
# Reinstale as dependências
pip install -r requirements.txt

# Execute com mais detalhes
python -m pytest tests/ -v -s

# Verifique o ambiente virtual
source venv/bin/activate
```

### **Problema: Logs Não Aparecem**

```bash
# Verifique o nível de logging
export LOG_LEVEL=DEBUG

# Verifique o arquivo de log
tail -f spv_automatico.log

# Configure logging no console
export LOG_FORMAT="%(asctime)s - %(levelname)s - %(message)s"
```

## 📊 Monitoramento

### **1. Logs do Sistema**

```bash
# Acompanhe os logs em tempo real
tail -f spv_automatico.log

# Filtre por nível
grep "ERROR" spv_automatico.log
grep "INFO" spv_automatico.log
```

### **2. Estatísticas do Banco**

```sql
-- Consulta estatísticas
SELECT 
    COUNT(*) as total_pesquisas,
    COUNT(CASE WHEN data_conclusao IS NOT NULL THEN 1 END) as concluidas,
    COUNT(CASE WHEN data_conclusao IS NULL THEN 1 END) as pendentes
FROM pesquisas;
```

### **3. Resultados das Pesquisas**

```sql
-- Consulta resultados
SELECT 
    resultado,
    COUNT(*) as quantidade
FROM pesquisa_spv 
GROUP BY resultado;
```

## 🎯 Próximos Passos

1. **Configure o ambiente**:
   ```bash
   cp env.example .env
   # Edite o arquivo .env com suas configurações
   ```

2. **Execute os testes**:
   ```bash
   python -m pytest tests/ -v
   ```

3. **Teste o sistema**:
   ```bash
   python examples/web_scraping_exemplo.py
   ```

4. **Execute o sistema completo**:
   ```bash
   python src/spv_automatico.py
   ```

5. **Monitore os resultados**:
   ```bash
   tail -f spv_automatico.log
   ```

## 🎉 Conclusão

O sistema SPV está pronto para uso com:

- ✅ **Arquitetura SOLID** implementada
- ✅ **Testes abrangentes** (50+ testes)
- ✅ **Web scraping** configurável
- ✅ **Múltiplos filtros** de pesquisa
- ✅ **Validação robusta** de dados
- ✅ **Logging estruturado**
- ✅ **Configuração flexível**

Para começar, execute os exemplos e configure seu ambiente conforme necessário! 