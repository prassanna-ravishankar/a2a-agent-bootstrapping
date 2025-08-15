"""Configuration settings for A2A Agents."""

import os
from typing import Optional

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, continue without it
    pass


class Config:
    """Configuration class for A2A Agents."""
    
    # Model Configuration
    DEFAULT_MODEL = "gemini-2.5-flash-lite"  # Stable, fast, and cost-efficient model
    
    # Override with environment variable or use default
    MODEL_NAME: str = os.getenv("A2A_MODEL_NAME", DEFAULT_MODEL)
    
    # API Keys
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    
    # Server Configuration  
    HOST: str = os.getenv("A2A_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("A2A_PORT", "8000"))
    
    # Agent Configuration
    RETRIES: int = int(os.getenv("A2A_RETRIES", "2"))
    
    @classmethod
    def get_model_name(cls) -> str:
        """Get the configured model name."""
        return cls.MODEL_NAME
    
    @classmethod
    def set_model_name(cls, model_name: str) -> None:
        """Set the model name (useful for testing)."""
        cls.MODEL_NAME = model_name
    
    @classmethod
    def setup_api_keys(cls) -> None:
        """Set up API key compatibility between GEMINI_API_KEY and GOOGLE_API_KEY."""
        if cls.GEMINI_API_KEY and not cls.GOOGLE_API_KEY:
            os.environ["GOOGLE_API_KEY"] = cls.GEMINI_API_KEY
            cls.GOOGLE_API_KEY = cls.GEMINI_API_KEY
        elif cls.GOOGLE_API_KEY and not cls.GEMINI_API_KEY:
            os.environ["GEMINI_API_KEY"] = cls.GOOGLE_API_KEY
            cls.GEMINI_API_KEY = cls.GOOGLE_API_KEY


# Initialize configuration
config = Config()
config.setup_api_keys()

# Export commonly used values
MODEL_NAME = config.get_model_name()
