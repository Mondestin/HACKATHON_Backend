"""
Access Cards router for Campus Access Management System.
Handles access card CRUD operations and status management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.base import get_db
from app.models.database_models import AccessCard, User
from app.models.schemas import (
    AccessCardCreate, AccessCardUpdate, AccessCardResponse,
    PaginationParams, PaginatedResponse, ErrorResponse
)

router = APIRouter()

@router.post("/", response_model=AccessCardResponse, status_code=status.HTTP_201_CREATED)
async def create_access_card(
    card_data: AccessCardCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new access card.
    
    Args:
        card_data: Access card creation data
        db: Database session
        
    Returns:
        Created access card information
        
    Raises:
        HTTPException: If user not found or card number already exists
    """
    # Check if user exists
    user = db.query(User).filter(User.id == card_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if card number already exists
    existing_card = db.query(AccessCard).filter(AccessCard.card_number == card_data.card_number).first()
    if existing_card:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Access card with this number already exists"
        )
    
    # Create new access card
    db_card = AccessCard(
        user_id=card_data.user_id,
        card_number=card_data.card_number,
        status=card_data.status
    )
    
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    
    return db_card

@router.get("/", response_model=List[AccessCardResponse])
async def get_access_cards(
    db: Session = Depends(get_db)
):
    """
    Get all access cards.
    
    Args:
        db: Database session
        
    Returns:
        List of all access cards
    """
    # Get all access cards
    cards = db.query(AccessCard).all()
    
    return cards

@router.get("/{card_id}", response_model=AccessCardResponse)
async def get_access_card(
    card_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific access card by ID.
    
    Args:
        card_id: Access card ID
        db: Database session
        
    Returns:
        Access card information
        
    Raises:
        HTTPException: If access card not found
    """
    card = db.query(AccessCard).filter(AccessCard.id == card_id).first()
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access card not found"
        )
    
    return card

@router.get("/user/{user_id}", response_model=List[AccessCardResponse])
async def get_user_access_cards(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all access cards for a specific user.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        List of access cards for the user
        
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
    
    # Get access cards for the user
    cards = db.query(AccessCard).filter(AccessCard.user_id == user_id).all()
    
    return cards

@router.put("/{card_id}", response_model=AccessCardResponse)
async def update_access_card(
    card_id: str,
    card_data: AccessCardUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an access card.
    
    Args:
        card_id: Access card ID
        card_data: Access card update data
        db: Database session
        
    Returns:
        Updated access card information
        
    Raises:
        HTTPException: If access card not found
    """
    card = db.query(AccessCard).filter(AccessCard.id == card_id).first()
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access card not found"
        )
    
    # Update card fields
    update_data = card_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(card, field, value)
    
    db.commit()
    db.refresh(card)
    
    return card

@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_access_card(
    card_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete an access card.
    
    Args:
        card_id: Access card ID
        db: Database session
        
    Raises:
        HTTPException: If access card not found
    """
    card = db.query(AccessCard).filter(AccessCard.id == card_id).first()
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access card not found"
        )
    
    db.delete(card)
    db.commit()
    
    return None

@router.put("/{card_id}/status", response_model=AccessCardResponse)
async def update_card_status(
    card_id: str,
    status: str,
    db: Session = Depends(get_db)
):
    """
    Update the status of an access card.
    
    Args:
        card_id: Access card ID
        status: New status (active, lost, disabled)
        db: Database session
        
    Returns:
        Updated access card information
        
    Raises:
        HTTPException: If access card not found or invalid status
    """
    card = db.query(AccessCard).filter(AccessCard.id == card_id).first()
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access card not found"
        )
    
    # Validate status
    valid_statuses = ["active", "lost", "disabled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    # Update status
    card.status = status
    db.commit()
    db.refresh(card)
    
    return card 