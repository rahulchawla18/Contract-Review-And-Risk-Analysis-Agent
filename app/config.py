import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    # Groq API settings for contract analysis
    # Get your free API key from: https://console.groq.com/
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    # Groq model options (check https://console.groq.com/docs/models for latest):
    # - "llama-3.3-70b-versatile" (recommended, best quality - replacement for decommissioned llama-3.1-70b)
    # - "llama-3.1-8b-instant" (faster, smaller - default)
    # - "llama-3.2-90b-text-preview" (very high quality)
    # - "mixtral-8x7b-32768" (good balance)
    # - "gemma-7b-it" (fast, efficient)
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    # Port configuration (default: 7861)
    PORT = os.getenv("PORT", "7861")


settings = Settings()