"""
Base models and common database configurations.
Contains shared model functionality and database utilities.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import uuid
from app.config.settings import DATABASE_URL

# Database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all SQLAlchemy models
Base = declarative_base()

def get_db():
    """
    Database dependency for FastAPI.
    Yields a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SQLAlchemyBaseModel(Base):
    """
    Abstract base model with common fields for SQLAlchemy models.
    """
    __abstract__ = True
    
    # Common fields for all models
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

class BaseResponseModel(BaseModel):
    """
    Base response model with common configuration.
    All response models should inherit from this.
    """
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

class PaginationParams(BaseModel):
    """
    Common pagination parameters.
    """
    skip: int = Field(default=0, ge=0, description="Number of items to skip")
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum number of items to return")

class PaginatedResponse(BaseResponseModel):
    """
    Generic paginated response wrapper.
    """
    items: list
    total: int
    skip: int
    limit: int
    has_more: bool 