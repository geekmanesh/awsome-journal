COMPOSE_FILE      = docker-compose.yml
COMPOSE_CMD       = docker compose -f $(COMPOSE_FILE)
BACKEND_SERVICE   = backend   # service name in docker-compose.yml
DB_SERVICE        = db
PYTHON_CMD        = python

.PHONY: help build up down restart logs logs-app logs-db shell db-shell psql \
        migrate makemigrations test lint format clean reset-db

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

build:
	$(COMPOSE_CMD) build --no-cache

up:
	$(COMPOSE_CMD) up

up-d: up -d

down:
	$(COMPOSE_CMD) down

restart: down up

logs:
	$(COMPOSE_CMD) logs -f

logs-app:
	$(COMPOSE_CMD) logs -f $(BACKEND_SERVICE)

logs-db:
	$(COMPOSE_CMD) logs -f $(DB_SERVICE)

shell:
	$(COMPOSE_CMD) exec $(BACKEND_SERVICE) /bin/bash || $(COMPOSE_CMD) exec $(BACKEND_SERVICE) /bin/sh

db-shell:
	$(COMPOSE_CMD) exec $(DB_SERVICE) psql -U $$DB_USER -d $$DB_NAME

psql:
	@echo "Make sure your .env file matches the container's credentials"
	PGPASSWORD=$$(grep DB_PASSWORD .env | cut -d '=' -f2) psql \
		-h localhost -p 5432 \
		-U $$(grep DB_USER .env | cut -d '=' -f2) \
		-d $$(grep DB_NAME .env | cut -d '=' -f2)

alembic-upgrade:
	$(COMPOSE_CMD) exec $(BACKEND_SERVICE) alembic upgrade head

alembic-revision:
	@if [ -z "$(msg)" ]; then \
		echo "Usage: make makemigrations msg='your message here'"; \
		exit 1; \
	fi
	$(COMPOSE_CMD) exec $(BACKEND_SERVICE) alembic revision --autogenerate -m "$(msg)"

test:
	$(COMPOSE_CMD) exec $(BACKEND_SERVICE) pytest -v

lint:
	$(COMPOSE_CMD) exec $(BACKEND_SERVICE) ruff check .

format:
	$(COMPOSE_CMD) exec $(BACKEND_SERVICE) ruff format .

clean:
	$(COMPOSE_CMD) down -v
	docker system prune -f

reset-db:
	$(COMPOSE_CMD) down -v
	$(COMPOSE_CMD) up -d db
	@echo "Waiting for PostgreSQL to start..."
	sleep 5
	$(COMPOSE_CMD) up -d $(BACKEND_SERVICE)
	@echo "Database reset complete. Run 'make migrate' to recreate tables."