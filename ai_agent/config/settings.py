import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # gemini, openai, anthropic

    # Model configurations
    # Gemini models
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    # OpenAI models
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

    # Anthropic models
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")

    # Memory Configuration
    MEMORY_TYPE = os.getenv("MEMORY_TYPE", "buffer")  # buffer or buffer_window
    MEMORY_WINDOW_SIZE = int(os.getenv("MEMORY_WINDOW_SIZE", "5"))
    USE_MEMORY = os.getenv("USE_MEMORY", "True").lower() == "true"

    # Database Configuration
    DB_URI = os.getenv("DB_URI", "")
    DB_NAME = os.getenv("DB_NAME", "blog_writer")

    # SerpAPI Configuration
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
    SERPAPI_LANGUAGE = os.getenv("SERPAPI_LANGUAGE", "en")
    SERPAPI_GEO_LOCATION = os.getenv("SERPAPI_GEO_LOCATION", "us")

    # Application Settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # GOOGLE Drive Settings
    GOOGLE_SERVICE_ACCOUNT = os.getenv("GOOGLE_SERVICE_ACCOUNT", "")
    GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
    GOOGLE_EMAIL = os.getenv("GOOGLE_EMAIL", "")
    GOOGLE_SCOPES = os.getenv("GOOGLE_SCOPES", "").split(",")


settings = Settings()
