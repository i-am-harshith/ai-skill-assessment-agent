from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI-Powered Skill Assessment & Personalised Learning Plan Agent"
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./skill_assessment.db"
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"]
    )
    enable_openai: bool = False
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    max_assessment_skills: int = 6
    questions_per_skill: int = 1
    seed_on_start: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
