"""
Application settings and configuration for Campus Access Management System.
Uses python-dotenv for environment variable management.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "campus_access_db")
DB_USER = os.getenv("DB_USER", "campus_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "campus_password")

# Construct database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "hackaton-estiam-2025-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Application Settings
APP_NAME = os.getenv("APP_NAME", "Campus Access Management System")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "['*']").replace("'", '"')
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
CORS_ALLOW_METHODS = os.getenv("CORS_ALLOW_METHODS", "['*']").replace("'", '"')
CORS_ALLOW_HEADERS = os.getenv("CORS_ALLOW_HEADERS", "['*']").replace("'", '"')

# Import json for parsing CORS settings
import json

# Parse CORS settings from strings to lists
try:
    CORS_ORIGINS = json.loads(CORS_ORIGINS)
except json.JSONDecodeError:
    CORS_ORIGINS = ["*"]

try:
    CORS_ALLOW_METHODS = json.loads(CORS_ALLOW_METHODS)
except json.JSONDecodeError:
    CORS_ALLOW_METHODS = ["*"]

try:
    CORS_ALLOW_HEADERS = json.loads(CORS_ALLOW_HEADERS)
except json.JSONDecodeError:
    CORS_ALLOW_HEADERS = ["*"]

# Create global settings instance
settings = {
    "app_name": APP_NAME,
    "app_version": APP_VERSION,
    "debug": DEBUG,
    "host": HOST,
    "port": PORT,
    "cors_origins": CORS_ORIGINS,
    "cors_allow_credentials": CORS_ALLOW_CREDENTIALS,
    "cors_allow_methods": CORS_ALLOW_METHODS,
    "cors_allow_headers": CORS_ALLOW_HEADERS,
    "database_url": DATABASE_URL,
    "database_host": DB_HOST,
    "database_port": DB_PORT,
    "database_name": DB_NAME,
    "database_user": DB_USER,
    "database_password": DB_PASSWORD,
    "secret_key": SECRET_KEY,
    "algorithm": ALGORITHM,
    "access_token_expire_minutes": ACCESS_TOKEN_EXPIRE_MINUTES,
    "log_level": LOG_LEVEL
}

# Environment-specific settings
def get_settings():
    """
    Get application settings based on environment.
    
    Returns:
        Settings instance configured for current environment
    """
    return settings 