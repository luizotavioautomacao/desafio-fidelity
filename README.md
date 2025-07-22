## Detalhes do projeto:
### Banco de Dados
1. Entendimento do [problema proposto](https://colab.research.google.com/drive/1Lxh_83CTNgOcF8jY7abYLx3vxYOw1qgr?usp=sharing) e análise das [tabelas](./docs/tables.png)  
2. Criação do [schema.sql](./storage/schema.sql)  
3. [Análise](./docs/database-analysis.md) do schema.sql  
#### Popular Banco de Dados
7. Criação do [seed.sql](./scripts/seed.sql)

### SOLID
4. Estrutura de [pastas](./src/) usando [SOLID](./docs/SOLID.md)

### Containers
5. Criação Dockerfile, docker-compose, requirements.txt e Makefile

### Variáveis de Ambiente
6. Criação do arquivo [.env](./.env.example) com as variáveis de ambiente

> ⚠️ **Importante:** Preencha todos os valores obrigatórios seguindo .env.example. A aplicação verifica a existência de variáveis críticas e **não funcionará se alguma estiver ausente**.

### Testes
8. [Testes Unitários](./tests/)

---
## Como rodar localmente?
### Dependências do Sistema Operacional
- python3   
- python3-venv  
- python3-pip
- docker-compose
- make

### Comandos no terminal
1. `make i`  
2. `make up`
3. `make load-schema`  
4. `make seed`  
5. `make exec`  
6. `make test`  
7. `make coverage`  
