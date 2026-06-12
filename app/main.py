from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import settings
from app.database import Base, engine
from app.routes import health, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables (Alembic handles this in production)
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: nothing to clean up yet


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# Prometheus metric - exposes /metrics endpoint automatically
Instrumentator().instrument(app).expose(app)

app.include_router(health.router)
app.include_router(tasks.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }
