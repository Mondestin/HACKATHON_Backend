"""
Application settings and configuration for Campus Access Management System.
Uses Pydantic settings for environment variable management.
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Application settings
    app_name: str = "Campus Access Management System"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS settings
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]
    
    # Database settings
    database_url: str = "mysql+pymysql://root:@localhost/estiamAccess"
    database_host: str = "localhost"
    database_port: int = 3306
    database_name: str = "estiamAccess"
    database_user: str = "root"
    database_password: str = ""
    
    # Security settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Logging settings
    log_level: str = "INFO"
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Create global settings instance
settings = Settings()

# Environment-specific settings
def get_settings() -> Settings:
    """
    Get application settings based on environment.
    
    Returns:
        Settings instance configured for current environment
    """
    return settings 