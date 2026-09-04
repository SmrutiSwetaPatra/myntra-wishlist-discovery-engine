import asyncio
import time
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from google.genai.errors import APIError
from pydantic import BaseModel

from app.engine.gemini import GeminiClient
from app.engine.rate_limiter import RateLimiter

class DummySchema(BaseModel):
    message: str

@pytest.fixture
def rate_limiter():
    # Use a very short interval for tests
    return RateLimiter(0.1)

@pytest.mark.asyncio
async def test_rate_limiter_spacing(rate_limiter):
    """
    Test that the rate limiter properly spaces out concurrent requests.
    """
    start_time = time.monotonic()
    
    async def worker():
        await rate_limiter.acquire()
        return time.monotonic()
        
    # Launch 3 workers concurrently
    times = await asyncio.gather(worker(), worker(), worker())
    
    # Sort the completion times
    times.sort()
    
    # The time between each completion should be at least ~0.1s
    assert (times[1] - times[0]) >= 0.09
    assert (times[2] - times[1]) >= 0.09
    
    total_time = times[2] - start_time
    assert total_time >= 0.2

@pytest.mark.asyncio
@patch('app.engine.gemini.global_limiter', new_callable=lambda: RateLimiter(0.0))
@patch('app.engine.gemini.asyncio.sleep', new_callable=AsyncMock)
async def test_gemini_client_429_retry(mock_sleep, mock_limiter):
    """
    Test that GeminiClient properly parses Retry-After from a 429 APIError
    and waits before retrying.
    """
    client = GeminiClient(model_name="gemini-2.5-flash")
    
    # Mock the inner execution
    call_count = 0
    
    async def mock_execute(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # First call raises a 429 APIError with a RetryDelay string
            error_details = {
                'error': {
                    'code': 429, 
                    'message': 'Quota exceeded.', 
                    'status': 'RESOURCE_EXHAUSTED', 
                    'details': [{'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '33s'}]
                }
            }
            # The python SDK APIError init needs message and code (or response)
            # We'll just construct a basic one and mock __str__ or message
            mock_response = MagicMock()
            mock_response.status_code = 429
            mock_response.text = str(error_details)
            err = APIError(429, error_details)
            err.__str__ = lambda self: str(error_details)
            raise err
            
        elif call_count == 2:
            return DummySchema(message="success")
            
    client._execute_with_transient_retry = AsyncMock(side_effect=mock_execute)
    
    result = await client.extract_structured("Test prompt", "Test text", DummySchema)
    
    assert result.message == "success"
    assert call_count == 2
    
    # Verify that sleep was called with exactly 34.0 seconds (33s parsed + 1s buffer)
    mock_sleep.assert_called_once_with(34.0)

@pytest.mark.asyncio
@patch('app.engine.gemini.global_limiter', new_callable=lambda: RateLimiter(0.0))
@patch('app.engine.gemini.asyncio.sleep', new_callable=AsyncMock)
async def test_gemini_client_429_default_retry(mock_sleep, mock_limiter):
    """
    Test that GeminiClient falls back to 60s sleep if it cannot parse retryDelay.
    """
    client = GeminiClient(model_name="gemini-2.5-flash")
    
    call_count = 0
    async def mock_execute(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # First call raises 429 without retryDelay
            err = APIError(429, {})
            err.__str__ = lambda self: "No details"
            raise err
        elif call_count == 2:
            return DummySchema(message="success")
            
    client._execute_with_transient_retry = AsyncMock(side_effect=mock_execute)
    
    result = await client.extract_structured("Test prompt", "Test text", DummySchema)
    
    assert result.message == "success"
    mock_sleep.assert_called_once_with(60.0)
