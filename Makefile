
.PHONY: dev api-test api-test-down test

dev:
	uvicorn src.main:app --reload

api-test:
	docker compose -f docker-compose.test.yaml up --build api db

api-test-down:
	docker compose -f docker-compose.test.yaml down -v

test:
	docker compose -f docker-compose.test.yaml up --build --abort-on-container-exit --exit-code-from tests
	docker compose -f docker-compose.test.yaml down -v
