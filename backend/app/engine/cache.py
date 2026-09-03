import hashlib
import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.analyses import Analysis

class CacheManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    def generate_cache_key(self, conversation_id: str, stage: str, model_name: str, prompt_version: str, schema_version: str) -> str:
        """
        Generates a unique deterministic string for caching purposes based on the user's instructions.
        """
        raw = f"{conversation_id}_{stage}_{model_name}_{prompt_version}_{schema_version}"
        return hashlib.sha256(raw.encode('utf-8')).hexdigest()

    async def get_cached_analysis(self, conversation_id: uuid.UUID, model_name: str, prompt_version: str, schema_version: str) -> Optional[Analysis]:
        """
        Returns the existing Analysis if it exactly matches the provenance signatures.
        """
        result = await self.db.execute(
            select(Analysis).where(
                Analysis.conversation_id == conversation_id,
                Analysis.model_name == model_name,
                Analysis.prompt_version == prompt_version,
                Analysis.schema_version == schema_version
            )
        )
        return result.scalars().first()
