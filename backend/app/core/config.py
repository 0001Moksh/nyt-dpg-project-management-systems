from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    # App
    APP_NAME: str = "DPG Project Management System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    DATABASE_ECHO: bool = False
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = 24
    
    # OTP
    OTP_LENGTH: int = 6
    OTP_EXPIRY_MINUTES: int = 5
    
    # Email/SMTP
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str
    SMTP_FROM_NAME: str = "DPG Project Management System"
    
    # File Storage
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_FILE_TYPES: List[str] = ["pdf"]
    
    # OneDrive
    ONEDRIVE_TENANT_ID: str
    ONEDRIVE_CLIENT_ID: str
    ONEDRIVE_CLIENT_SECRET: str
    ONEDRIVE_FOLDER_ID: str
    
    # Groq LLM
    GROQ_API_KEY: str
    GROQ_MODEL_NAME: str = "mixtral-8x7b-32768"
    
    # RAG
    RAG_MODEL_NAME: str = "ollama"
    RAG_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    ALLOWED_DOMAINS: List[str] = [".dpg-itm.edu.in"]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_MINUTES: int = 1
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
