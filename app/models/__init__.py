"""
Models package for Campus Access Management System.
"""

from .base import Base, SQLAlchemyBaseModel, get_db
from .database_models import (
    User, Role, UserRole, AccessCard, AccessLog, 
    Room, RoomReservation, Student, Professor,
    UserRole as UserRoleEnum, CardStatus, AccessType
)
from .schemas import (
    # User schemas
    UserCreate, UserUpdate, UserResponse,
    # Access card schemas
    AccessCardCreate, AccessCardUpdate, AccessCardResponse,
    # Access log schemas
    AccessLogCreate, AccessLogResponse,
    # Room schemas
    RoomCreate, RoomUpdate, RoomResponse,
    # Reservation schemas
    RoomReservationCreate, RoomReservationUpdate, RoomReservationResponse, ExtendedRoomReservationResponse,
    # Student schemas
    StudentCreate, StudentUpdate, StudentResponse,
    # Professor schemas
    ProfessorCreate, ProfessorUpdate, ProfessorResponse,
    # Authentication schemas
    LoginRequest, LoginResponse, ExtendedLoginResponse, TokenResponse,
    # Common schemas
    PaginationParams, PaginatedResponse, ErrorResponse,
    # Enums
    UserRoleEnum, CardStatusEnum, AccessTypeEnum
)

__all__ = [
    # Base models
    "Base", "SQLAlchemyBaseModel", "get_db",
    
    # Database models
    "User", "Role", "UserRole", "AccessCard", "AccessLog",
    "Room", "RoomReservation", "Student", "Professor",
    "UserRoleEnum", "CardStatus", "AccessType",
    
    # User schemas
    "UserCreate", "UserUpdate", "UserResponse",
    
    # Access card schemas
    "AccessCardCreate", "AccessCardUpdate", "AccessCardResponse",
    
    # Access log schemas
    "AccessLogCreate", "AccessLogResponse",
    
    # Room schemas
    "RoomCreate", "RoomUpdate", "RoomResponse",
    
    # Reservation schemas
    "RoomReservationCreate", "RoomReservationUpdate", "RoomReservationResponse", "ExtendedRoomReservationResponse",
    
    # Student schemas
    "StudentCreate", "StudentUpdate", "StudentResponse",
    
    # Professor schemas
    "ProfessorCreate", "ProfessorUpdate", "ProfessorResponse",
    
    # Authentication schemas
    "LoginRequest", "LoginResponse", "ExtendedLoginResponse", "TokenResponse",
    
    # Common schemas
    "PaginationParams", "PaginatedResponse", "ErrorResponse",
    
    # Enums
    "UserRoleEnum", "CardStatusEnum", "AccessTypeEnum"
] 