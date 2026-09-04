from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import health, copilot, evidence

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.db.session import AsyncSessionLocal
    from app.models.analyses import Analysis
    from sqlalchemy import update
    import uuid
    import logging
    
    logger = logging.getLogger(__name__)
    
    # Run data-layer migration for invalid Google Pay record
    try:
        async with AsyncSessionLocal() as session:
            bad_id = uuid.UUID('aef3490c-a41c-4356-81d4-34ab969f3422')
            result = await session.execute(
                update(Analysis)
                .where(Analysis.id == bad_id)
                .values(validation_status='irrelevant')
            )
            await session.commit()
            logger.info("Migrated invalid google pay record to irrelevant")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        
    yield

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
