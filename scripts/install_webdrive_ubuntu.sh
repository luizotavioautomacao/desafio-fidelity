#!/bin/bash
# Script para instalar Selenium, Microsoft Edge e Edge WebDriver no Ubuntu
# Uso: bash scripts/install_selenium_ubuntu.sh

set -e

# 1. Criar ambiente virtual Python
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual Python..."
    python3 -m venv venv
fi

# 2. Ativar ambiente virtual e instalar Selenium
source venv/bin/activate

echo "Instalando Selenium via pip..."
pip install selenium

deactivate

# 3. Baixar Edge WebDriver compatível
EDGE_VERSION=$(microsoft-edge --version | awk '{print $3}')
DRIVER_URL="https://msedgedriver.azureedge.net/${EDGE_VERSION}/edgedriver_linux64.zip"

TMP_DIR=$(mktemp -d)
cd $TMP_DIR

echo "Baixando Edge WebDriver versão $EDGE_VERSION..."
if ! wget -q "$DRIVER_URL" -O edgedriver_linux64.zip; then
    echo "❌ Versão $EDGE_VERSION indisponível. Buscando versão compatível estável..."
    COMPATIBLE_VERSION=$(wget -qO- https://msedgedriver.azureedge.net/LATEST_STABLE)
    echo "➡️ Usando versão alternativa: $COMPATIBLE_VERSION"
    DRIVER_URL="https://msedgedriver.azureedge.net/${COMPATIBLE_VERSION}/edgedriver_linux64.zip"
    wget -q "$DRIVER_URL" -O edgedriver_linux64.zip || {
        echo "❌ Falha ao baixar o Edge WebDriver para a versão $COMPATIBLE_VERSION também."
        exit 1
    }
fi

unzip -o edgedriver_linux64.zip

# 4. Copiar msedgedriver para /usr/local/bin
sudo mv msedgedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/msedgedriver

cd -
rm -rf $TMP_DIR

echo -e "\n✅ Instalação concluída!"
echo "- Selenium instalado no ambiente virtual ./venv"
echo "- Microsoft Edge instalado"
echo "- Edge WebDriver (msedgedriver) disponível em /usr/local/bin/msedgedriver"
echo "- Configure o caminho no .env: EDGE_DRIVER_PATH=/usr/local/bin/msedgedriver"
