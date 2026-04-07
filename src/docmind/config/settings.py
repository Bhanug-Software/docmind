from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # LLM
    anthropic_api_key: str = Field(..., description="Anthropic API key")
    openai_api_key: str = Field(..., description="OpenAI API key")

    # Vector DB
    qdrant_url: str = Field(default="http://localhost:6333")
    qdrant_api_key: str = Field(default="")

    # Observability
    langsmith_api_key: str = Field(default="")
    langsmith_project: str = Field(default="docmind")

    # App
    app_env: str = Field(default="development")
    log_level: str = Field(default="DEBUG")


settings = Settings()
