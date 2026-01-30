DOCKER_COMPOSE = docker compose
BACKEND_SVC = backend


up:
	$(DOCKER_COMPOSE) up -d --build

down:
	$(DOCKER_COMPOSE) down

watch:
	$(DOCKER_COMPOSE) up --build

stop:
	$(DOCKER_COMPOSE) down 

clean:
	$(DOCKER_COMPOSE) down -v

install-deps:
	$(DOCKER_COMPOSE) exec $(BACKEND_SVC) pip install $(PKG)
	$(DOCKER_COMPOSE) exec $(BACKEND_SVC) pip freeze > ./backend/requirements.txt
	@echo "Package $(PKG) installed and ./backend/requirements.txt updated."

migrate-gen:
	$(DOCKER_COMPOSE) exec $(BACKEND_SVC) alembic revision --autogenerate -m "$(MSG)"

migrate-up:
	$(DOCKER_COMPOSE) exec $(BACKEND_SVC) alembic upgrade head
	
migrate-down:
	$(DOCKER_COMPOSE) exec $(BACKEND_SVC) alembic downgrade -1


.PHONY: build up down watch install-deps migrate-gen migrate-up migrate-down
