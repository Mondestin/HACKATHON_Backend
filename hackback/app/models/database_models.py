"""
Database models for Campus Access Management System.
Based on the provided SQL schema.
"""

from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import SQLAlchemyBaseModel
import enum

# Enum classes for status fields
class UserRole(enum.Enum):
    """User role enumeration."""
    admin = "admin"
    student = "student"
    professor = "professor"

class CardStatus(enum.Enum):
    """Access card status enumeration."""
    active = "active"
    lost = "lost"
    disabled = "disabled"

class AccessType(enum.Enum):
    """Access type enumeration."""
    entry = "entry"
    exit = "exit"
    denied = "denied"

class User(SQLAlchemyBaseModel):
    """
    Users table - Base user accounts with authentication.
    """
    __tablename__ = "users"
    
    # User fields
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    
    # Relationships
    access_cards = relationship("AccessCard", back_populates="user", cascade="all, delete-orphan")
    room_reservations = relationship("RoomReservation", back_populates="reserved_by_user", cascade="all, delete-orphan")
    student_profile = relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    professor_profile = relationship("Professor", back_populates="user", uselist=False, cascade="all, delete-orphan")
    user_roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")

class Role(SQLAlchemyBaseModel):
    """
    Roles table - Available roles in the system.
    """
    __tablename__ = "roles"
    
    # Role fields
    name = Column(String(50), unique=True, nullable=False)
    
    # Relationships
    user_roles = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")

class UserRole(SQLAlchemyBaseModel):
    """
    User roles table - Many-to-many relationship between users and roles.
    """
    __tablename__ = "user_roles"
    
    # Foreign keys
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")

class AccessCard(SQLAlchemyBaseModel):
    """
    Access cards table - Physical cards for building access.
    """
    __tablename__ = "access_cards"
    
    # Card fields
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    card_number = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(Enum(CardStatus), default=CardStatus.active)
    issued_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="access_cards")
    access_logs = relationship("AccessLog", back_populates="card", cascade="all, delete-orphan")

class AccessLog(SQLAlchemyBaseModel):
    """
    Access logs table - Audit trail of all access attempts.
    """
    __tablename__ = "access_logs"
    
    # Log fields
    card_id = Column(String(36), ForeignKey("access_cards.id", ondelete="SET NULL"), nullable=True)
    accessed_at = Column(DateTime, default=func.now())
    location = Column(String(100), nullable=False)
    access_type = Column(Enum(AccessType), nullable=False)
    
    # Relationships
    card = relationship("AccessCard", back_populates="access_logs")

class Room(SQLAlchemyBaseModel):
    """
    Rooms table - Physical spaces that can be reserved.
    """
    __tablename__ = "rooms"
    
    # Room fields
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    
    # Add check constraint for capacity
    __table_args__ = (
        CheckConstraint('capacity > 0', name='check_capacity_positive'),
    )
    
    # Relationships
    reservations = relationship("RoomReservation", back_populates="room", cascade="all, delete-orphan")

class RoomReservation(SQLAlchemyBaseModel):
    """
    Room reservations table - Booking system for rooms.
    """
    __tablename__ = "room_reservations"
    
    # Reservation fields
    room_id = Column(String(36), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    reserved_by = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    expected_occupants = Column(Integer, nullable=False)
    
    # Add check constraint for expected occupants
    __table_args__ = (
        CheckConstraint('expected_occupants > 0', name='check_occupants_positive'),
    )
    
    # Relationships
    room = relationship("Room", back_populates="reservations")
    reserved_by_user = relationship("User", back_populates="room_reservations")

class Student(SQLAlchemyBaseModel):
    """
    Students table - Extended user profile for students.
    """
    __tablename__ = "students"
    
    # Student fields
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    student_card_id = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False)
    class_name = Column(String(50), nullable=False)  # Using class_name to avoid Python keyword conflict
    phone_number = Column(String(20), nullable=True)
    registered_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="student_profile")

class Professor(SQLAlchemyBaseModel):
    """
    Professors table - Extended user profile for faculty.
    """
    __tablename__ = "professors"
    
    # Professor fields
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    department = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    office = Column(String(100), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="professor_profile") 