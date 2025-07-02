"""
Pydantic schemas for Campus Access Management System API.
These schemas define the structure of request and response data.
"""

from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enum classes for API schemas
class UserRoleEnum(str, Enum):
    """User role enumeration for API."""
    admin = "admin"
    student = "student"
    professor = "professor"

class CardStatusEnum(str, Enum):
    """Access card status enumeration for API."""
    active = "active"
    lost = "lost"
    disabled = "disabled"

class AccessTypeEnum(str, Enum):
    """Access type enumeration for API."""
    entry = "entry"
    exit = "exit"
    denied = "denied"

# Base schemas
class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# User schemas
class UserBase(BaseSchema):
    """Base user schema."""
    email: EmailStr = Field(..., description="User email address")
    role: UserRoleEnum = Field(..., description="User role")

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")

class UserUpdate(BaseSchema):
    """Schema for updating a user."""
    email: Optional[EmailStr] = Field(None, description="User email address")
    role: Optional[UserRoleEnum] = Field(None, description="User role")

class UserResponse(UserBase):
    """Schema for user response."""
    id: str = Field(..., description="User ID")

# Access Card schemas
class AccessCardBase(BaseSchema):
    """Base access card schema."""
    card_number: str = Field(..., description="Unique card number")
    status: CardStatusEnum = Field(CardStatusEnum.active, description="Card status")

class AccessCardCreate(AccessCardBase):
    """Schema for creating a new access card."""
    user_id: str = Field(..., description="User ID who owns the card")

class AccessCardUpdate(BaseSchema):
    """Schema for updating an access card."""
    status: Optional[CardStatusEnum] = Field(None, description="Card status")

class AccessCardResponse(AccessCardBase):
    """Schema for access card response."""
    id: str = Field(..., description="Card ID")
    user_id: str = Field(..., description="User ID who owns the card")
    issued_at: datetime = Field(..., description="Card issuance timestamp")

# Access Log schemas
class AccessLogBase(BaseSchema):
    """Base access log schema."""
    location: str = Field(..., description="Access location")
    access_type: AccessTypeEnum = Field(..., description="Type of access")
    granted: bool = Field(..., description="Whether access was granted or not")

class AccessLogCreate(AccessLogBase):
    """Schema for creating a new access log."""
    card_id: str = Field(..., description="Access card ID")

class AccessLogResponse(AccessLogBase):
    """Schema for access log response."""
    id: str = Field(..., description="Log ID")
    card_id: Optional[str] = Field(None, description="Access card ID")
    accessed_at: datetime = Field(..., description="Access timestamp")

# Room schemas
class RoomBase(BaseSchema):
    """Base room schema."""
    name: str = Field(..., description="Room name")
    location: str = Field(..., description="Room location")
    capacity: int = Field(..., gt=0, description="Room capacity (must be positive)")

class RoomCreate(RoomBase):
    """Schema for creating a new room."""
    pass

class RoomUpdate(BaseSchema):
    """Schema for updating a room."""
    name: Optional[str] = Field(None, description="Room name")
    location: Optional[str] = Field(None, description="Room location")
    capacity: Optional[int] = Field(None, gt=0, description="Room capacity (must be positive)")

class RoomResponse(RoomBase):
    """Schema for room response."""
    id: str = Field(..., description="Room ID")

# Room Reservation schemas
class RoomReservationBase(BaseSchema):
    """Base room reservation schema."""
    room_id: str = Field(..., description="Room ID")
    start_time: datetime = Field(..., description="Reservation start time")
    end_time: datetime = Field(..., description="Reservation end time")
    expected_occupants: int = Field(..., gt=0, description="Expected number of occupants")

class RoomReservationCreate(RoomReservationBase):
    """Schema for creating a new room reservation."""
    reserved_by: str = Field(..., description="User ID making the reservation")

    @validator('end_time')
    def end_time_must_be_after_start_time(cls, v, values):
        """Validate that end time is after start time."""
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('End time must be after start time')
        return v

class RoomReservationUpdate(BaseSchema):
    """Schema for updating a room reservation."""
    start_time: Optional[datetime] = Field(None, description="Reservation start time")
    end_time: Optional[datetime] = Field(None, description="Reservation end time")
    expected_occupants: Optional[int] = Field(None, gt=0, description="Expected number of occupants")

class RoomReservationResponse(RoomReservationBase):
    """Schema for room reservation response."""
    id: str = Field(..., description="Reservation ID")
    reserved_by: str = Field(..., description="User ID making the reservation")

# Student schemas
class StudentBase(BaseSchema):
    """Base student schema."""
    full_name: str = Field(..., description="Student full name")
    student_card_id: str = Field(..., description="Student card ID")
    email: EmailStr = Field(..., description="Student email")
    class_name: str = Field(..., description="Student class")
    phone_number: Optional[str] = Field(None, description="Student phone number")

class StudentCreate(StudentBase):
    """Schema for creating a new student."""
    user_id: str = Field(..., description="Associated user ID")

class StudentUpdate(BaseSchema):
    """Schema for updating a student."""
    full_name: Optional[str] = Field(None, description="Student full name")
    student_card_id: Optional[str] = Field(None, description="Student card ID")
    email: Optional[EmailStr] = Field(None, description="Student email")
    class_name: Optional[str] = Field(None, description="Student class")
    phone_number: Optional[str] = Field(None, description="Student phone number")

class StudentResponse(StudentBase):
    """Schema for student response."""
    id: str = Field(..., description="Student ID")
    user_id: str = Field(..., description="Associated user ID")
    registered_at: datetime = Field(..., description="Registration timestamp")

# Professor schemas
class ProfessorBase(BaseSchema):
    """Base professor schema."""
    full_name: str = Field(..., description="Professor full name")
    email: EmailStr = Field(..., description="Professor email")
    department: Optional[str] = Field(None, description="Department")
    phone_number: Optional[str] = Field(None, description="Professor phone number")
    office: Optional[str] = Field(None, description="Office location")

class ProfessorCreate(ProfessorBase):
    """Schema for creating a new professor."""
    user_id: str = Field(..., description="Associated user ID")

class ProfessorUpdate(BaseSchema):
    """Schema for updating a professor."""
    full_name: Optional[str] = Field(None, description="Professor full name")
    email: Optional[EmailStr] = Field(None, description="Professor email")
    department: Optional[str] = Field(None, description="Department")
    phone_number: Optional[str] = Field(None, description="Professor phone number")
    office: Optional[str] = Field(None, description="Office location")

class ProfessorResponse(ProfessorBase):
    """Schema for professor response."""
    id: str = Field(..., description="Professor ID")
    user_id: str = Field(..., description="Associated user ID")

# Pagination schemas
class PaginationParams(BaseModel):
    """Pagination parameters."""
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(100, ge=1, le=1000, description="Number of records to return")

class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    items: List[BaseModel] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Number of records returned")

# Error schemas
class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information") 