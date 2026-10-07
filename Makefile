.PHONY: up down down-v logs ps check clean

up:
	docker compose up -d --build

down:
	docker compose down

down-v:
	docker compose down -v

logs:
	docker compose logs -f

ps:
	docker compose ps

check:
	@echo "=== Health ==="
	@curl -s http://localhost:8000/health || echo "❌ Backend down"
	@echo "\n=== Ready ==="
	@curl -s http://localhost:8000/ready || echo "❌ Backend not ready"
	@echo "\n=== Root ==="
	@curl -s http://localhost:8000/ || echo "❌ Unreachable"
	@echo ""

clean:
	docker compose down -v --remove-orphans
	docker system prune -f