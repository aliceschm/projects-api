.PHONY: dev api-test api-test-down test

# Run API for development with prod DB
dev:
	uvicorn src.main:app --reload

# Run API for development with test DB
api-test:
	docker compose -f docker-compose.test.yaml up -d --build api db

# Exit api-test
api-test-down:
	docker compose -f docker-compose.test.yaml down -v --remove-orphans

# Only run pytest
pytest:
	docker compose -f docker-compose.test.yaml run --rm tests

# Build, run pytest and close
test:
	docker compose -f docker-compose.test.yaml up --build --abort-on-container-exit --exit-code-from tests
	docker compose -f docker-compose.test.yaml down -v --remove-orphans

