# Configuração do WebDriver - Guia de Solução de Problemas

## 🚨 Problema: Erro ao baixar WebDriver no Docker

Se você encontrou o erro:
```
wget: unable to resolve host address 'msedgedriver.azureedge.net'
```

Este é um problema comum de conectividade durante o build do Docker. Aqui estão as soluções:

## 🔧 Soluções

### Solução 1: Usar Docker com Download Automático (Recomendado)

O Dockerfile foi atualizado para ser mais robusto:

```bash
# Execute o Docker Compose atualizado
docker-compose up -d
```

O novo Dockerfile:
- Usa uma versão fixa do WebDriver (120.0.2210.91)
- Inclui script de fallback
- Tenta múltiplas URLs de download

### Solução 2: Execução Local (Mais Simples)

```bash
# Use o script automático
chmod +x scripts/run_local.sh
./scripts/run_local.sh
```

Este script:
- Configura o ambiente automaticamente
- Oferece modo de desenvolvimento sem WebDriver
- Detecta problemas e sugere soluções

### Solução 3: Download Manual do WebDriver

1. **Baixe o WebDriver manualmente:**
   - Acesse: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
   - Baixe a versão compatível com seu sistema

2. **Configure o caminho:**
   ```bash
   # Crie o diretório
   mkdir -p edge_driver
   
   # Mova o WebDriver para o diretório
   mv msedgedriver edge_driver/
   
   # Configure no .env
   echo "EDGE_DRIVER_PATH=./edge_driver/msedgedriver" >> .env
   ```

3. **Execute localmente:**
   ```bash
   python src/spv_automatico.py
   ```

### Solução 4: Usar Docker com Volume

```bash
# Descomente a linha no docker-compose.yml
# - ./edge_driver/msedgedriver:/usr/bin/msedgedriver

# Execute
docker-compose up -d
```

### Solução 5: Modo de Desenvolvimento (Sem Web Scraping)

Para desenvolvimento e testes sem web scraping:

```bash
# Local
export DISABLE_SCRAPING=true
python src/spv_automatico.py

# Docker
docker-compose --profile dev up spv_app_dev -d
```

## 🐳 Docker Compose Atualizado

O `docker-compose.yml` foi atualizado com:

1. **Script de inicialização robusto:**
   ```yaml
   command: >
     sh -c "
       echo '🔍 Verificando WebDriver...' &&
       /usr/local/bin/download_webdriver.sh &&
       echo '🚀 Iniciando aplicação...' &&
       python src/spv_automatico.py
     "
   ```

2. **Serviço de desenvolvimento:**
   ```yaml
   spv_app_dev:
     profiles:
       - dev
     environment:
       DISABLE_SCRAPING: "true"
   ```

3. **Volumes configuráveis:**
   ```yaml
   volumes:
     - ./logs:/app/logs
     # - ./edge_driver/msedgedriver:/usr/bin/msedgedriver
   ```

## 📋 Scripts Disponíveis

### `scripts/download_webdriver.sh`
- Tenta múltiplas URLs de download
- Usa versões conhecidas como fallback
- Detecta ChromeDriver como alternativa
- Fornece instruções claras em caso de falha

### `scripts/run_local.sh`
- Configuração automática do ambiente
- Verificação de dependências
- Modo de desenvolvimento opcional
- Instruções claras de troubleshooting

## 🔍 Verificação de Status

### Verificar se o WebDriver está funcionando:

```bash
# Teste local
python3 -c "
from selenium import webdriver
from selenium.webdriver.edge.service import Service
import os
driver_path = os.getenv('EDGE_DRIVER_PATH', '/usr/bin/msedgedriver')
try:
    service = Service(driver_path)
    driver = webdriver.Edge(service=service)
    print('✅ WebDriver funcionando!')
    driver.quit()
except Exception as e:
    print(f'❌ Erro: {e}')
"
```

### Verificar logs do Docker:

```bash
# Ver logs da aplicação
docker-compose logs spv_app

# Ver logs específicos do WebDriver
docker-compose logs spv_app | grep -i webdriver
```

## 🛠️ Troubleshooting Avançado

### Problema: Timeout no download

```bash
# Aumente o timeout no script
sed -i 's/--timeout=30/--timeout=60/' scripts/download_webdriver.sh
```

### Problema: Proxy ou firewall

```bash
# Configure proxy no Docker
docker-compose up -d --build --build-arg HTTP_PROXY=http://proxy:port
```

### Problema: Versão incompatível

```bash
# Force uma versão específica
export EDGE_VERSION=119
docker-compose up -d --build
```

## 📞 Suporte

Se nenhuma das soluções funcionar:

1. **Verifique a conectividade:**
   ```bash
   curl -I https://msedgedriver.azureedge.net/120.0.2210.91/edgedriver_linux64.zip
   ```

2. **Use o modo de desenvolvimento:**
   ```bash
   export DISABLE_SCRAPING=true
   python src/spv_automatico.py
   ```

3. **Abra uma issue no GitHub** com:
   - Logs completos do erro
   - Sistema operacional
   - Versão do Docker
   - Comando executado

## 🎯 Resumo das Soluções

| Problema | Solução Recomendada | Alternativa |
|----------|-------------------|-------------|
| Erro de download no Docker | `docker-compose up -d` (versão atualizada) | Download manual |
| Sem WebDriver local | `./scripts/run_local.sh` | Modo desenvolvimento |
| Timeout de rede | Usar versão fixa no Dockerfile | Proxy/VPN |
| Versão incompatível | Script de fallback | Download manual específico |

A versão atualizada do sistema resolve a maioria dos problemas de WebDriver automaticamente! 