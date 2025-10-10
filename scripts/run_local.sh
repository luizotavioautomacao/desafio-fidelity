#!/bin/bash

# Script para executar o Sistema SPV localmente
# Este script configura o ambiente e executa o sistema

set -e

echo "🚀 Sistema de Pesquisa Virtual Automático - Execução Local"
echo "=========================================================="

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale o Python 3.8+ primeiro."
    exit 1
fi

# Verifica se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativa o ambiente virtual
echo "🐍 Ativando ambiente virtual..."
source venv/bin/activate

# Instala dependências se necessário
if [ ! -f "venv/lib/python*/site-packages/sqlalchemy" ]; then
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
fi

# Verifica se o arquivo .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado. Criando configuração padrão..."
    cat > .env << EOF
# Configuração do Banco de Dados PostgreSQL
DATABASE_URL=postgresql://postgres:password@localhost:5432/spv_automatico

# Caminho para o Microsoft Edge WebDriver
EDGE_DRIVER_PATH=

# Configurações do Sistema
MAX_EXECUTION_TIME=600
INTERVALO_ESPERA=60
MAX_TENTATIVAS=20

# Configurações de Logging
LOG_LEVEL=INFO
LOG_FILE=spv_automatico.log

# Configurações do Web Scraper
WEBSITE_TYPE=TJSP
HEADLESS=true
TIMEOUT=30

# Configurações de Performance
BATCH_SIZE=100
PAUSE_BETWEEN_REQUESTS=1
EOF
    echo "✅ Arquivo .env criado. Configure as variáveis conforme necessário."
fi

# Verifica se o PostgreSQL está rodando
echo "🗄️ Verificando conexão com PostgreSQL..."
if ! python3 -c "
import psycopg2
try:
    import os
    from dotenv import load_dotenv
    load_dotenv()
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    conn.close()
    print('✅ Conexão com PostgreSQL OK')
except Exception as e:
    print(f'❌ Erro de conexão: {e}')
    exit(1)
" 2>/dev/null; then
    echo "❌ Não foi possível conectar ao PostgreSQL."
    echo "💡 Certifique-se de que:"
    echo "   1. O PostgreSQL está instalado e rodando"
    echo "   2. O banco 'spv_automatico' existe"
    echo "   3. As credenciais no .env estão corretas"
    echo ""
    echo "🔧 Para iniciar apenas o PostgreSQL com Docker:"
    echo "   docker-compose up postgres -d"
    exit 1
fi

# Verifica se o Edge WebDriver está disponível
echo "🌐 Verificando Edge WebDriver..."
if [ -z "$EDGE_DRIVER_PATH" ] || [ ! -f "$EDGE_DRIVER_PATH" ]; then
    echo "⚠️  Edge WebDriver não encontrado."
    echo "💡 Opções:"
    echo "   1. Baixe o msedgedriver manualmente e configure EDGE_DRIVER_PATH no .env"
    echo "   2. Use o modo de desenvolvimento (sem web scraping)"
    echo "   3. Execute com Docker: docker-compose up -d"
    echo ""
    
    read -p "Deseja continuar em modo de desenvolvimento (sem web scraping)? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        export DISABLE_SCRAPING=true
        echo "✅ Modo de desenvolvimento ativado"
    else
        echo "❌ Execute o setup completo primeiro: python scripts/setup.py"
        exit 1
    fi
else
    echo "✅ Edge WebDriver encontrado: $EDGE_DRIVER_PATH"
fi

# Cria diretório de logs se não existir
mkdir -p logs

echo ""
echo "🚀 Iniciando Sistema SPV..."
echo "📝 Logs serão salvos em: logs/spv_automatico.log"
echo "⏹️  Pressione Ctrl+C para parar"
echo ""

# Executa o sistema
python3 src/spv_automatico.py 