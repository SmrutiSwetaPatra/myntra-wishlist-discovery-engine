import os
import json
import logging
from typing import Type, TypeVar, Any
from google import genai
from google.genai import types
from pydantic import BaseModel
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, RetryError
from app.core.config import settings
from app.engine.rate_limiter import global_limiter
from google.genai.errors import APIError

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

class LLMError(Exception):
    pass

class GeminiClient:
    def __init__(self, model_name: str = "gemini-3.6-flash"):
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment, falling back to attempting direct client init which checks GOOGLE_API_KEY")
        self.model_name = model_name

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=4, max=20),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    async def _execute_with_transient_retry(self, full_prompt: str, schema: Type[T]) -> T:
        """
        Inner execution method that handles transient non-429 errors using tenacity.
        """
        client = genai.Client(api_key=self.api_key)
        response = await client.aio.models.generate_content(
            model=self.model_name,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0.1,
            )
        )
        
        if not response.text:
            raise LLMError("Empty response from Gemini")
            
        data = json.loads(response.text)
        return schema.model_validate(data)

    async def extract_structured(self, prompt: str, text: str, schema: Type[T]) -> T:
        """
        Calls Gemini to extract structured JSON matching the Pydantic schema.
        Handles rate limits directly by parsing Retry-After for 429s.
        """
        full_prompt = f"{prompt}\n\nCONVERSATION TEXT:\n{text}"
        
        # Max attempts specifically for 429 quota exhaustion
        max_429_retries = 3
        attempts = 0
        
        while attempts < max_429_retries:
            attempts += 1
            await global_limiter.acquire()
            
            try:
                return await self._execute_with_transient_retry(full_prompt, schema)
            except Exception as e:
                # Determine if it is a 429 RESOURCE_EXHAUSTED
                is_429 = False
                retry_delay = 60.0 # Default if we can't parse it
                
                # Unwrap RetryError from Tenacity if it wrapped an APIError
                original_error = e.last_attempt.exception() if isinstance(e, RetryError) else e
                
                if isinstance(original_error, APIError):
                    if original_error.code == 429:
                        is_429 = True
                        # Try to parse the specific retry delay from the details
                        try:
                            # The google-genai APIError doesn't expose `details` cleanly as an attribute sometimes, 
                            # but it is usually available via str(e) or e.message
                            error_str = str(original_error)
                            if 'retryDelay' in error_str:
                                # We can parse it from string representation roughly
                                # "retryDelay": "33s"
                                import re
                                match = re.search(r"'retryDelay':\s*'(\d+)s'", error_str)
                                if match:
                                    retry_delay = float(match.group(1)) + 1.0 # Add 1s buffer
                        except Exception as parse_e:
                            logger.warning(f"Failed to parse retry delay from 429 error: {parse_e}")
                
                if is_429 and attempts < max_429_retries:
                    logger.warning(f"429 Quota Exceeded. Sleeping for {retry_delay}s before retry {attempts}/{max_429_retries}...")
                    await asyncio.sleep(retry_delay)
                    continue
                else:
                    logger.error(f"Error calling Gemini: {str(e)}")
                    raise LLMError(f"Extraction failed: {str(e)}") from e
