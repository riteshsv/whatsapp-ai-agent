import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings and environment variable validation."""
    
    # Meta WhatsApp API Credentials
    meta_verify_token: str
    meta_access_token: str
    whatsapp_phone_number_id: str

    # OpenAI Credentials & Models
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    #google api key and model
    google_api_key: str
    google_model: str = "google_genai:gemini-3.7-flash"

    # App Settings
    app_env: str = "development"
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()