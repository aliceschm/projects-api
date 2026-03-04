.PHONY: dev api-test api-test-down test

# Run API for development with prod DB
dev:
	uvicorn src.app_admin:app --reload

# Run API for development with test DB
api-test:
	docker-compose -f docker-compose.test.yaml up 

# Exit api-test
api-test-down:
	docker compose -f docker-compose.test.yaml down -v --remove-orphans
