from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import health, copilot, evidence

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic here
    yield
    # Shutdown logic here

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")] if settings.ALLOWED_ORIGINS else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(copilot.router, prefix=f"{settings.API_V1_STR}/copilot")
app.include_router(evidence.router, prefix=f"{settings.API_V1_STR}/evidence")
