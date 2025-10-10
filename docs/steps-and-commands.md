## Banco de Dados  

### Local  
cd script  
chmod +x access-database.sh  

### Docker  
make db  

#### Comandos
\dt - listar todas as tabelas
\d - pesquisa_spv
\l - lista todos os bancos de dados

# Edge WebDrive

microsoft-edge --version
which msedgedriver
/usr/local/bin/msedgedriver
command -v msedgedriver
ls -l /usr/local/bin/msedgedriver



VERSION=$(microsoft-edge --version | awk '{print $3}')
echo "Versão do Edge: $VERSION"

pip install selenium --break-system-packages


wget "https://msedgedriver.azureedge.net/$VERSION/edgedriver_linux64.zip" -O /tmp/edgedriver_linux64.zip
unzip -l /tmp/edgedriver_linux64.zip

https://developer.microsoft.com/pt-br/microsoft-edge/tools/webdriver?form=MA13LH#downloads

sudo systemctl status postgresql
docker compose up -d postgres
docker exec -i spv_postgres psql -U postgres -d spv_automatico < database/schema.sql

-- 1. Remova todos os duplicados, mantendo apenas um
DELETE FROM websites
WHERE website_id NOT IN (
  SELECT MIN(website_id)
  FROM websites
  GROUP BY nome
);

-- 2. Agora adicione a constraint UNIQUE
ALTER TABLE websites ADD CONSTRAINT unique_nome UNIQUE (nome);

docker compose down -v --remove-orphans

docker rm -f spv_postgres