#!/bin/bash

# Script para baixar o Microsoft Edge WebDriver
# Este script tenta diferentes abordagens para obter o WebDriver

set -e

EDGE_DRIVER_PATH=${EDGE_DRIVER_PATH:-"/usr/bin/msedgedriver"}
DOWNLOAD_DIR="/tmp"

echo "🔍 Verificando se o Edge WebDriver já existe..."
if [ -f "$EDGE_DRIVER_PATH" ] && [ -x "$EDGE_DRIVER_PATH" ]; then
    echo "✅ Edge WebDriver já existe e é executável"
    exit 0
fi

echo "📥 Baixando Microsoft Edge WebDriver..."

# Tenta obter a versão do Edge instalado
EDGE_VERSION=""
if command -v microsoft-edge &> /dev/null; then
    EDGE_VERSION=$(microsoft-edge --version 2>/dev/null | cut -d' ' -f3 | cut -d'.' -f1)
    echo "📋 Versão do Edge detectada: $EDGE_VERSION"
fi

# Se não conseguiu detectar a versão, usa uma versão estável conhecida
if [ -z "$EDGE_VERSION" ]; then
    EDGE_VERSION="120"
    echo "⚠️  Não foi possível detectar a versão do Edge, usando versão padrão: $EDGE_VERSION"
fi

# URLs para tentar baixar o WebDriver
URLS=(
    "https://msedgedriver.azureedge.net/${EDGE_VERSION}.0.2210.91/edgedriver_linux64.zip"
    "https://msedgedriver.azureedge.net/${EDGE_VERSION}.0.0.0/edgedriver_linux64.zip"
    "https://msedgedriver.azureedge.net/120.0.2210.91/edgedriver_linux64.zip"
    "https://msedgedriver.azureedge.net/119.0.2151.97/edgedriver_linux64.zip"
)

# Tenta baixar de diferentes URLs
for url in "${URLS[@]}"; do
    echo "🔄 Tentando baixar de: $url"
    
    if wget --timeout=30 --tries=3 -O "$DOWNLOAD_DIR/msedgedriver.zip" "$url" 2>/dev/null; then
        echo "✅ Download bem-sucedido de: $url"
        
        # Extrai o arquivo
        if unzip -q "$DOWNLOAD_DIR/msedgedriver.zip" -d "$DOWNLOAD_DIR/"; then
            # Move para o local correto
            if [ -f "$DOWNLOAD_DIR/msedgedriver" ]; then
                mv "$DOWNLOAD_DIR/msedgedriver" "$EDGE_DRIVER_PATH"
                chmod +x "$EDGE_DRIVER_PATH"
                rm -f "$DOWNLOAD_DIR/msedgedriver.zip"
                echo "✅ Edge WebDriver instalado com sucesso em: $EDGE_DRIVER_PATH"
                exit 0
            else
                echo "❌ Arquivo msedgedriver não encontrado no zip"
            fi
        else
            echo "❌ Erro ao extrair o arquivo zip"
        fi
    else
        echo "❌ Falha ao baixar de: $url"
    fi
done

# Se chegou até aqui, tenta usar o ChromeDriver como fallback
echo "🔄 Tentando usar ChromeDriver como fallback..."
if command -v chromedriver &> /dev/null; then
    echo "✅ ChromeDriver encontrado, criando symlink..."
    ln -sf $(which chromedriver) "$EDGE_DRIVER_PATH"
    echo "✅ Symlink criado para ChromeDriver"
    exit 0
fi

echo "❌ Não foi possível baixar ou encontrar o Edge WebDriver"
echo "💡 Soluções alternativas:"
echo "   1. Monte o WebDriver como volume: -v /path/to/msedgedriver:/usr/bin/msedgedriver"
echo "   2. Configure EDGE_DRIVER_PATH para um caminho válido"
echo "   3. Use o modo headless sem WebDriver (configuração específica)"

exit 1 