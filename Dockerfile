FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala Microsoft Edge
RUN wget -q -O - https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge-dev.list \
    && apt-get update \
    && apt-get install -y microsoft-edge-stable \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Cria diretórios necessários
RUN mkdir -p logs /usr/bin/edge_driver

# Script para baixar o WebDriver
COPY scripts/download_webdriver.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/download_webdriver.sh

# Variáveis de ambiente internas do Python
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1


# Comando padrão
CMD ["python", "src/spv_automatico.py"] 