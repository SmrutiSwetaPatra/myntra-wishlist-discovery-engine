import httpx
from typing import Dict, Any, Optional

class YouTubeAPIClient:
    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient()

    async def search_videos(
        self,
        query: str,
        region_code: str = "IN",
        relevance_language: str = "en",
        max_results: int = 50,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "regionCode": region_code,
            "relevanceLanguage": relevance_language,
            "maxResults": min(max_results, 50),
            "key": self.api_key
        }
        if page_token:
            params["pageToken"] = page_token

        response = await self.client.get(f"{self.BASE_URL}/search", params=params)
        response.raise_for_status()
        return response.json()

    async def get_comment_threads(
        self,
        video_id: str,
        max_results: int = 100,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        params = {
            "part": "snippet,replies",
            "videoId": video_id,
            "maxResults": min(max_results, 100),
            "key": self.api_key,
            "textFormat": "plainText"
        }
        if page_token:
            params["pageToken"] = page_token
            
        response = await self.client.get(f"{self.BASE_URL}/commentThreads", params=params)
        response.raise_for_status()
        return response.json()
        
    async def close(self):
        await self.client.aclose()
