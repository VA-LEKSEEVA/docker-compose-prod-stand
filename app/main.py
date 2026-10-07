import os
import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="DevOps Prod-Like Stand", version="1.0.0")

# Автоматически добавляет /metrics и собирает стандартные метрики
# (request count, latency, status codes)
Instrumentator().instrument(app).expose(app)

# Глобальные переменные для пулов подключений
db_pool = None
redis_client = None


@app.on_event("startup")
async def startup():
    """Инициализация подключений при старте приложения."""
    global db_pool, redis_client

    # asyncpg требует DSN без префикса +asyncpg
    dsn = os.getenv("DATABASE_URL", "").replace("postgresql+asyncpg", "postgresql")
    db_pool = await asyncpg.create_pool(dsn=dsn, min_size=1, max_size=5)

    redis_client = aioredis.from_url(
        os.getenv("REDIS_URL", "redis://redis:6379/0"),
        decode_responses=True,
    )


@app.on_event("shutdown")
async def shutdown():
    """Корректно закрываем соединения при остановке."""
    if db_pool:
        await db_pool.close()
    if redis_client:
        await redis_client.close()


@app.get("/")
async def root():
    return {
        "service": "DevOps Prod-Like Stand",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    """
    Liveness probe.
    Отвечает быстро, только проверяет, что процесс жив.
    """
    return {"status": "ok"}


@app.get("/ready")
async def ready():
    """
    Readiness probe.
    Проверяет подключение к БД и Redis.
    """
    try:
        async with db_pool.acquire() as conn:
            await conn.fetchval("SELECT 1")

        await redis_client.ping()

        return {
            "status": "ready",
            "database": "connected",
            "redis": "connected",
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unavailable: {str(e)}",
        )