import logging
from app.engine.gemini import GeminiClient
from app.engine.schemas import DeepAnalysis
from app.engine.prompts import DEEP_ANALYSIS_PROMPT_V1

logger = logging.getLogger(__name__)

class DeepAnalyzer:
    def __init__(self, client: GeminiClient):
        self.client = client
        self.prompt_version = "deep-analysis-v1.0"
        self.schema_version = "deep-analysis-v1.0"
        self.stage = "deep_analysis"

    async def analyze(self, conversation_text: str) -> DeepAnalysis:
        logger.debug("Running deep analysis for conversation")
        analysis = await self.client.extract_structured(
            prompt=DEEP_ANALYSIS_PROMPT_V1,
            text=conversation_text,
            schema=DeepAnalysis
        )
        return analysis
