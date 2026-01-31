from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_TITLE: str = "Inferra Chatbot Backend"
    API_VERSION: str = "1.0.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    ANTHROPIC_API_KEY: str = ""
    DEFAULT_MODEL: str = "claude-sonnet-4-5-20250929"
    API_PROVIDER: Literal["claude", "grok", "gemini"] = "claude"

    DOCKER_IMAGE: str = "inferra:latest"

    MAX_CONCURRENT_SESSIONS: int = 10
    SESSION_TIMEOUT_MINUTES: int = 60

    BASE_DIR: Path = Path(__file__).parent.parent

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
