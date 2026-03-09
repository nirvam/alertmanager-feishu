from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    feishu_webhook_url: str
    feishu_secret: Optional[str] = None
    message_type: str = "interactive"  # "text" or "interactive"
    app_host: str = "0.0.0.0"
    app_port: int = 8080

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
