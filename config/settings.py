import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

    #LLM Configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash")

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
