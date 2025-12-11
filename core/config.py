from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Database
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    APP_NAME: str = "PAPPI Calculator Auth API"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
