import logging
from app.engine.gemini import GeminiClient
from app.engine.schemas import RelevanceDecision
from app.engine.prompts import RELEVANCE_PROMPT_V1

logger = logging.getLogger(__name__)

class RelevanceGate:
    def __init__(self, client: GeminiClient):
        self.client = client
        self.prompt_version = "relevance-v1.0"
        self.schema_version = "relevance-v1.0"
        self.stage = "relevance"

    async def evaluate(self, conversation_text: str) -> RelevanceDecision:
        logger.debug("Evaluating relevance for conversation")
        decision = await self.client.extract_structured(
            prompt=RELEVANCE_PROMPT_V1,
            text=conversation_text,
            schema=RelevanceDecision
        )
        return decision
