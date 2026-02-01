import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # App
    APP_NAME: str = "DPG Project Management System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("FASTAPI_DEBUG", "false").lower() == "true"
    API_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./dpg_pms.db"
    )
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    DATABASE_POOL_RECYCLE: int = int(os.getenv("DATABASE_POOL_RECYCLE", "3600"))

    # Security
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-super-secret-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRY_HOURS: int = int(os.getenv("JWT_EXPIRY_HOURS", "24"))

    # OTP
    OTP_EXPIRY_MINUTES: int = int(os.getenv("OTP_EXPIRY_MINUTES", "5"))
    OTP_LENGTH: int = int(os.getenv("OTP_LENGTH", "6"))

    # SMTP Email Configuration
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "noreply@dpg-itm.com")
    SMTP_FROM_NAME: str = os.getenv("SMTP_FROM_NAME", "DPG PMS")

    # OneDrive/Azure
    ONEDRIVE_CLIENT_ID: str = os.getenv("ONEDRIVE_CLIENT_ID", "")
    ONEDRIVE_CLIENT_SECRET: str = os.getenv("ONEDRIVE_CLIENT_SECRET", "")
    ONEDRIVE_TENANT_ID: str = os.getenv("ONEDRIVE_TENANT_ID", "")
    ONEDRIVE_FOLDER_ID: str = os.getenv("ONEDRIVE_FOLDER_ID", "")

    # Groq LLM
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL_NAME: str = os.getenv("GROQ_MODEL_NAME", "mixtral-8x7b-32768")

    # RAG
    RAG_MODEL_NAME: str = os.getenv("RAG_MODEL_NAME", "ollama")
    RAG_EMBEDDING_MODEL: str = os.getenv(
        "RAG_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
    ]

    # Security
    ALLOWED_DOMAINS: str = os.getenv("ALLOWED_DOMAINS", ".dpg-itm.edu.in")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))

    # Notifications
    ENABLE_EMAIL_NOTIFICATIONS: bool = (
        os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "true").lower() == "true"
    )
    ENABLE_IN_APP_NOTIFICATIONS: bool = (
        os.getenv("ENABLE_IN_APP_NOTIFICATIONS", "true").lower() == "true"
    )

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    LOG_FILE_PATH: str = os.getenv("LOG_FILE_PATH", "/var/log/dpg-pms/app.log")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
