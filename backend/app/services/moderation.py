from typing import Optional
import httpx
from app.core.config import settings


class ModerationService:
    """Content moderation service using OpenAI moderation API"""
    
    def __init__(self):
        self.enabled = settings.MODERATION_ENABLED
        self.api_key = settings.OPENAI_API_KEY
    
    async def moderate_text(self, text: str) -> dict:
        """
        Moderate text content for inappropriate content
        
        Returns:
            dict with 'flagged' (bool) and 'categories' (dict)
        """
        if not self.enabled or not self.api_key:
            return {"flagged": False, "categories": {}, "warning": "Moderation disabled"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/moderations",
                    json={"input": text},
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                result = response.json()
                
                if result.get("results"):
                    moderation_result = result["results"][0]
                    return {
                        "flagged": moderation_result.get("flagged", False),
                        "categories": moderation_result.get("categories", {}),
                        "category_scores": moderation_result.get("category_scores", {})
                    }
        except Exception as e:
            # Log error but don't block the request
            print(f"Moderation API error: {e}")
            return {"flagged": False, "categories": {}, "error": str(e)}
        
        return {"flagged": False, "categories": {}}


moderation_service = ModerationService()
