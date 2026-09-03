from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db.session import AsyncSessionLocal
from app.engine.copilot import DiscoveryCopilot
from app.engine.schemas import CopilotResponse

router = APIRouter(tags=["copilot"])

copilot = DiscoveryCopilot()
# We need to initialize the vector store on startup, but for now we lazy load it if not loaded
_initialized = False

class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = "default"
    require_validated_only: Optional[bool] = False

@router.post("/query", response_model=CopilotResponse)
async def query_copilot(request: QueryRequest):
    global _initialized
    try:
        if not _initialized:
            async with AsyncSessionLocal() as session:
                await copilot.initialize(session)
            _initialized = True
            
        response = await copilot.query(
            user_query=request.query, 
            session_id=request.session_id,
            require_validated_only=request.require_validated_only
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
