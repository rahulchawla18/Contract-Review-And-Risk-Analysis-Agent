"""Factory to create LLM instances using Groq"""
from app.config import settings
from langchain_groq import ChatGroq


def create_llm(temperature=0.1):
    """
    Create Groq LLM instance.
    
    Args:
        temperature: Temperature for LLM responses (0.0-1.0)
        
    Returns:
        ChatGroq LLM instance
        
    Raises:
        ValueError: If GROQ_API_KEY is missing
    """
    if not settings.GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not found. Set it in .env file or environment variables. "
            "Get your free API key from: https://console.groq.com/"
        )
    
    return ChatGroq(
        model=settings.GROQ_MODEL,
        groq_api_key=settings.GROQ_API_KEY,
        temperature=temperature,
    )

