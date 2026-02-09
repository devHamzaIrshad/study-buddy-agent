from groq import Groq
from backend.config import settings

def get_groq_client() -> Groq:
    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")
    return Groq(api_key=settings.groq_api_key)