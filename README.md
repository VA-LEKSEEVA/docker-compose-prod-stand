# Docker Compose Production-Like Stand

Локальный стенд, имитирующий production-окружение для тестирования микросервисов.

## Стек

- **Backend:** FastAPI (Python 3.11)
- **БД:** PostgreSQL 16
- **Кеш:** Redis 7
- **Reverse Proxy:** Nginx + TLS *(в разработке)*
- **Мониторинг:** Prometheus + Grafana *(в разработке)*

## Быстрый старт

```bash
# 1. Копируем переменные окружения
cp .env.example .env

# 2. Поднимаем стенд
make up

# 3. Проверяем
make check
