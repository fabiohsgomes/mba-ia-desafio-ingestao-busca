PHONY: init
init:
	python -m venv venv

PHONY: active
active:
	source venv/bin/activate

PHONY: install
install:
	pip install -r requirements.txt

PHONY: up
up:
	docker compose -f docker-compose.yaml up -d

PHONY: down
down:
	docker compose -f docker-compose.yaml down

PHONY: logs
logs:
	docker compose -f docker-compose.yaml logs

PHONY: reload
reload: down up