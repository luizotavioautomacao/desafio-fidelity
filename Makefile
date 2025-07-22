
include .env
export $(shell sed 's/=.*//' .env)
i:
	@echo "📦 Criando virtualenv e instalando dependências..."
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt
up:
	docker compose up -d postgres
down:
	docker compose down -v
db:
	docker exec -it spv_postgres psql -U $(DB_USER) -d $(DB_NAME)
load-schema:
	docker exec -i spv_postgres psql -U $(DB_USER) -d $(DB_NAME) < storage/schema.sql
seed:
	docker exec -i spv_postgres psql -U $(DB_USER) -d $(DB_NAME) < scripts/seed.sql
exec:
	PYTHONPATH=. venv/bin/python src/spv_automatico.py
db:
	docker exec -it spv_postgres psql -U $(DB_USER) -d $(DB_NAME)
test:
	PYTHONPATH=src venv/bin/python -m pytest tests/ -v
coverage:
	PYTHONPATH=src venv/bin/python -m pytest tests/ -v --cov=src --cov-report=term-missing
coverage-html:
	PYTHONPATH=src venv/bin/python -m pytest tests/ --cov=src --cov-report=html