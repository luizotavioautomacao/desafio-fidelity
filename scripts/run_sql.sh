#!/bin/bash

DB_PATH="../storage/development.sqlite3"

if [ -z "$1" ]; then
  echo "Uso: ./run_sql.sh nome_do_script.sql"
  exit 1
fi

SQL_FILE="./$1"

if [ ! -f "$SQL_FILE" ]; then
  echo "Arquivo SQL não encontrado: $SQL_FILE"
  exit 1
fi

sqlite3 -header -column "$DB_PATH" < "$SQL_FILE"
