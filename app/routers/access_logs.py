"""
Access Logs router for Campus Access Management System.
Handles access log CRUD operations and access simulation.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.models.base import get_db
from app.models.database_models import AccessLog, AccessCard, User
from app.models.schemas import (
    AccessLogCreate, AccessLogResponse,
    PaginationParams, PaginatedResponse, ErrorResponse
)

router = APIRouter()

@router.post("/", response_model=AccessLogResponse, status_code=status.HTTP_201_CREATED)
async def create_access_log(
    log_data: AccessLogCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new access log entry.
    
    Args:
        log_data: Access log creation data
        db: Database session
        
    Returns:
        Created access log information
        
    Raises:
        HTTPException: If access card not found
    """
    # Check if access card exists
    card = db.query(AccessCard).filter(AccessCard.id == log_data.card_id).first()
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access card not found"
        )
    
    # Create new access log
    granted = log_data.access_type != "denied"
    db_log = AccessLog(
        card_id=log_data.card_id,
        location=log_data.location,
        access_type=log_data.access_type,
        granted=granted
    )
    
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    
    return db_log

@router.post("/simulate-access", response_model=AccessLogResponse, status_code=status.HTTP_201_CREATED)
async def simulate_access(
    card_number: str,
    location: str,
    access_type: str,
    db: Session = Depends(get_db)
):
    """
    Simulate an access attempt using card number.
    
    Args:
        card_number: Access card number
        location: Access location
        access_type: Type of access (entry, exit, denied)
        db: Database session
        
    Returns:
        Created access log information
        
    Raises:
        HTTPException: If access card not found or invalid access type
    """
    # Validate access type
    valid_access_types = ["entry", "exit", "denied"]
    if access_type not in valid_access_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid access type. Must be one of: {', '.join(valid_access_types)}"
        )
    
    # Find access card by number
    card = db.query(AccessCard).filter(AccessCard.card_number == card_number).first()
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access card not found"
        )
    
    # Check if card is active
    if card.status != "active":
        access_type = "denied"  # Force denied if card is not active
    
    # Create access log
    granted = access_type != "denied"
    db_log = AccessLog(
        card_id=card.id,
        location=location,
        access_type=access_type,
        granted=granted
    )
    
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    
    return db_log

@router.get("/", response_model=List[AccessLogResponse])
async def get_access_logs(
    db: Session = Depends(get_db)
):
    """
    Get all access logs.
    
    Args:
        db: Database session
        
    Returns:
        List of all access logs
    """
    # Get all access logs
    logs = db.query(AccessLog).all()
    
    return logs

@router.get("/{log_id}", response_model=AccessLogResponse)
async def get_access_log(
    log_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific access log by ID.
    
    Args:
        log_id: Access log ID
        db: Database session
        
    Returns:
        Access log information
        
    Raises:
        HTTPException: If access log not found
    """
    log = db.query(AccessLog).filter(AccessLog.id == log_id).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access log not found"
        )
    
    return log

@router.get("/card/{card_id}", response_model=List[AccessLogResponse])
async def get_card_access_logs(
    card_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all access logs for a specific card.
    
    Args:
        card_id: Access card ID
        db: Database session
        
    Returns:
        List of access logs for the card
        
    Raises:
        HTTPException: If access card not found
    """
    # Check if access card exists
    card = db.query(AccessCard).filter(AccessCard.id == card_id).first()
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access card not found"
        )
    
    # Get access logs for the card
    logs = db.query(AccessLog).filter(AccessLog.card_id == card_id).all()
    
    return logs

@router.get("/user/{user_id}", response_model=List[AccessLogResponse])
async def get_user_access_logs(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all access logs for a specific user.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        List of access logs for the user
        
    Raises:
        HTTPException: If user not found
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get access logs for all user's cards
    logs = db.query(AccessLog).join(AccessCard).filter(AccessCard.user_id == user_id).all()
    
    return logs

@router.get("/location/{location}", response_model=List[AccessLogResponse])
async def get_location_access_logs(
    location: str,
    db: Session = Depends(get_db)
):
    """
    Get all access logs for a specific location.
    
    Args:
        location: Access location
        db: Database session
        
    Returns:
        List of access logs for the location
    """
    # Get access logs for the location
    logs = db.query(AccessLog).filter(AccessLog.location == location).all()
    
    return logs

@router.get("/stats/summary")
async def get_access_stats(
    db: Session = Depends(get_db)
):
    """
    Get access statistics summary.
    
    Args:
        db: Database session
        
    Returns:
        Access statistics summary
    """
    # Get total access attempts
    total_attempts = db.query(AccessLog).count()
    
    # Get successful entries
    successful_entries = db.query(AccessLog).filter(AccessLog.access_type == "entry").count()
    
    # Get exits
    exits = db.query(AccessLog).filter(AccessLog.access_type == "exit").count()
    
    # Get denied attempts
    denied_attempts = db.query(AccessLog).filter(AccessLog.access_type == "denied").count()
    
    # Get unique locations
    unique_locations = db.query(AccessLog.location).distinct().count()
    
    # Get unique cards used
    unique_cards = db.query(AccessLog.card_id).distinct().count()
    
    return {
        "total_attempts": total_attempts,
        "successful_entries": successful_entries,
        "exits": exits,
        "denied_attempts": denied_attempts,
        "success_rate": round((successful_entries + exits) / total_attempts * 100, 2) if total_attempts > 0 else 0,
        "unique_locations": unique_locations,
        "unique_cards_used": unique_cards
    } 