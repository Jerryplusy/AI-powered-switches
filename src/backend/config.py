from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "Network Automation API"
    redis_url: str = Field("redis://localhost:6379", env="REDIS_URL")
    ai_api_key: str = Field(..., env="AI_API_KEY")
    max_connections: int = Field(50, env="MAX_CONNECTIONS")
    default_timeout: int = Field(30, env="DEFAULT_TIMEOUT")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()