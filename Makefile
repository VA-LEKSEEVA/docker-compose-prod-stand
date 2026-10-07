.PHONY: up down logs ps certs check

# Запуск всех сервисов
up:
	docker compose up -d --build

# Остановка всех сервисов
down:
	docker compose down

# Просмотр логов
logs:
	docker compose logs -f

# Статус контейнеров
ps:
	docker compose ps

# Генерация сертификатов (сделаем на этапе 4)
certs:
	@echo "Certificate generation will be implemented in Stage 4"

# Проверка эндпоинтов (сделаем на этапе 6)
check:
	@echo "Check will be implemented in Stage 6"