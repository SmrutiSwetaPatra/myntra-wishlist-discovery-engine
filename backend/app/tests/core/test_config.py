from app.core.config import settings

def test_gemini_api_key_configured():
    """
    Safely verifies that the GEMINI_API_KEY is loaded by the application configuration.
    Does NOT print or assert the actual value, only its presence.
    """
    has_key = bool(settings.GEMINI_API_KEY)
    assert has_key is True, "GEMINI_API_KEY is not configured or could not be loaded from .env"
