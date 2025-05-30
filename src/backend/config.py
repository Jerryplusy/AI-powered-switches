from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

import os
class Settings(BaseSettings):
    APP_NAME: str = "AI Network Configurator"
    DEBUG: bool = True
    API_PREFIX: str = "/api"

    # 硅基流动API配置
    SILICONFLOW_API_KEY: str = os.getenv("SILICON_API_KEY", "")
    SILICONFLOW_API_URL: str = os.getenv("SILICONFLOW_API_URL", "https://api.siliconflow.ai/v1")

    # 交换机配置
    SWITCH_USERNAME: str = os.getenv("SWITCH_USERNAME", "admin")
    SWITCH_PASSWORD: str = os.getenv("SWITCH_PASSWORD", "admin")
    SWITCH_TIMEOUT: int = os.getenv("SWITCH_TIMEOUT", 10)

    class Config:
        env_file = ".env"


settings = Settings()