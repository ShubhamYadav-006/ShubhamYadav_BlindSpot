import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv(override=True)


class Settings:
    PROJECT_NAME: str = "Blind Spot API"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Gemini AI Configuration
    @property
    def GEMINI_API_KEY(self) -> str:
        load_dotenv(override=True)
        return os.getenv("GEMINI_API_KEY", "")

    @property
    def GEMINI_MODEL(self) -> str:
        load_dotenv(override=True)
        return os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")
    @property
    def GEMINI_TIMEOUT_SECONDS(self) -> float:
        load_dotenv(override=True)
        return float(os.getenv("GEMINI_TIMEOUT_SECONDS", "30.0"))
    GEMINI_MAX_OUTPUT_TOKENS: int = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "1024"))
    GEMINI_TEMPERATURE: float = float(os.getenv("GEMINI_TEMPERATURE", "0.2"))

    ALLOWED_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
        if origin.strip()
    ]


settings = Settings()
