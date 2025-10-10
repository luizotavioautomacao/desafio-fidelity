#!/bin/bash

echo "🔄 Atualizando lista de pacotes..."
sudo apt update

echo "📦 Instalando cliente PostgreSQL..."
sudo apt install -y postgresql-client

echo "✅ Cliente PostgreSQL instalado com sucesso!"
