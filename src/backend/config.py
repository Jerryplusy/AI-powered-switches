from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Network Config API"
    ai_api_key: str = "your-silicon-mobility-api-key"
    ai_api_url: str = "https://api.silicon-mobility.com/v1/parse"
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()