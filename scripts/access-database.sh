#!/bin/bash

# Caminho absoluto para o diretório do script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Caminho absoluto para a raiz do projeto (um nível acima do diretório do script)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Caminho para o arquivo .env na raiz do projeto
ENV_PATH="$PROJECT_ROOT/.env"

# Carrega variáveis do .env
if [ -f "$ENV_PATH" ]; then
  export $(grep -v '^#' "$ENV_PATH" | xargs)
else
  echo "❌ Arquivo .env não encontrado em $ENV_PATH"
  exit 1
fi

# Verifica se todas as variáveis estão definidas
if [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ] || [ -z "$DB_NAME" ]; then
  echo "❌ Variáveis de ambiente incompletas."
  exit 1
fi

# Monta o DATABASE_URL dinamicamente
DATABASE_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

echo "🔗 Conectando ao banco de dados usando as variáveis do .env..."
PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"
