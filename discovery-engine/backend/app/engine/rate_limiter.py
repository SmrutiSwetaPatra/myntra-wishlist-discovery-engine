import asyncio
import time
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    A simple asynchronous rate limiter that guarantees a minimum interval
    between successful acquisitions.
    """
    def __init__(self, interval_seconds: float):
        self.interval = interval_seconds
        self.last_call = 0.0
        self._locks = {}
        
    async def acquire(self):
        """
        Acquires the rate limiter, sleeping if the interval has not yet elapsed
        since the last acquisition.
        """
        loop = asyncio.get_running_loop()
        if loop not in self._locks:
            self._locks[loop] = asyncio.Lock()
            
        async with self._locks[loop]:
            now = time.monotonic()
            elapsed = now - self.last_call
            if elapsed < self.interval:
                sleep_time = self.interval - elapsed
                logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
                await asyncio.sleep(sleep_time)
            
            self.last_call = time.monotonic()

# Global rate limiter instance: 1 request every 5 seconds (12 RPM)
# We place this here so it can be shared across GeminiClient instances or tasks if needed.
global_limiter = RateLimiter(5.0)
