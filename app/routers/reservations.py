"""
Room Reservations router for Campus Access Management System.
Handles room reservation CRUD operations and availability checking.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.models.base import get_db
from app.models.database_models import RoomReservation, Room, User
from app.models.schemas import (
    RoomReservationCreate, RoomReservationUpdate, RoomReservationResponse,
    PaginationParams, PaginatedResponse, ErrorResponse
)

router = APIRouter()

@router.post("/", response_model=RoomReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation_data: RoomReservationCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new room reservation.
    
    Args:
        reservation_data: Reservation creation data
        db: Database session
        
    Returns:
        Created reservation information
        
    Raises:
        HTTPException: If room/user not found or time conflict exists
    """
    # Check if room exists
    room = db.query(Room).filter(Room.id == reservation_data.room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Check if user exists
    user = db.query(User).filter(User.id == reservation_data.reserved_by).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if expected occupants exceed room capacity
    if reservation_data.expected_occupants > room.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Expected occupants ({reservation_data.expected_occupants}) exceed room capacity ({room.capacity})"
        )
    
    # Check for time conflicts
    conflicting_reservations = db.query(RoomReservation).filter(
        RoomReservation.room_id == reservation_data.room_id,
        RoomReservation.start_time < reservation_data.end_time,
        RoomReservation.end_time > reservation_data.start_time
    ).first()
    
    if conflicting_reservations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Time conflict: Room is already reserved for this time period"
        )
    
    # Create new reservation
    db_reservation = RoomReservation(
        room_id=reservation_data.room_id,
        reserved_by=reservation_data.reserved_by,
        start_time=reservation_data.start_time,
        end_time=reservation_data.end_time,
        expected_occupants=reservation_data.expected_occupants
    )
    
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    
    return db_reservation

@router.get("/", response_model=List[RoomReservationResponse])
async def get_reservations(
    db: Session = Depends(get_db)
):
    """
    Get all reservations.
    
    Args:
        db: Database session
        
    Returns:
        List of all reservations
    """
    # Get all reservations
    reservations = db.query(RoomReservation).all()
    
    return reservations

@router.get("/{reservation_id}", response_model=RoomReservationResponse)
async def get_reservation(
    reservation_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific reservation by ID.
    
    Args:
        reservation_id: Reservation ID
        db: Database session
        
    Returns:
        Reservation information
        
    Raises:
        HTTPException: If reservation not found
    """
    reservation = db.query(RoomReservation).filter(RoomReservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    
    return reservation

@router.get("/room/{room_id}", response_model=List[RoomReservationResponse])
async def get_room_reservations(
    room_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all reservations for a specific room.
    
    Args:
        room_id: Room ID
        db: Database session
        
    Returns:
        List of reservations for the room
        
    Raises:
        HTTPException: If room not found
    """
    # Check if room exists
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Get reservations for the room
    reservations = db.query(RoomReservation).filter(RoomReservation.room_id == room_id).all()
    
    return reservations

@router.get("/user/{user_id}", response_model=List[RoomReservationResponse])
async def get_user_reservations(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all reservations made by a specific user.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        List of reservations made by the user
        
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
    
    # Get reservations made by the user
    reservations = db.query(RoomReservation).filter(RoomReservation.reserved_by == user_id).all()
    
    return reservations

@router.get("/room/{room_id}/availability")
async def check_room_availability(
    room_id: str,
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db)
):
    """
    Check if a room is available for a specific time period.
    
    Args:
        room_id: Room ID
        start_time: Start time to check
        end_time: End time to check
        db: Database session
        
    Returns:
        Availability information
        
    Raises:
        HTTPException: If room not found or invalid time range
    """
    # Validate time range
    if start_time >= end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be before end time"
        )
    
    # Check if room exists
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Check for conflicting reservations
    conflicting_reservations = db.query(RoomReservation).filter(
        RoomReservation.room_id == room_id,
        RoomReservation.start_time < end_time,
        RoomReservation.end_time > start_time
    ).all()
    
    is_available = len(conflicting_reservations) == 0
    
    return {
        "room_id": room_id,
        "room_name": room.name,
        "start_time": start_time,
        "end_time": end_time,
        "is_available": is_available,
        "conflicting_reservations": [
            {
                "id": res.id,
                "start_time": res.start_time,
                "end_time": res.end_time,
                "reserved_by": res.reserved_by
            }
            for res in conflicting_reservations
        ]
    }

@router.put("/{reservation_id}", response_model=RoomReservationResponse)
async def update_reservation(
    reservation_id: str,
    reservation_data: RoomReservationUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a reservation.
    
    Args:
        reservation_id: Reservation ID
        reservation_data: Reservation update data
        db: Database session
        
    Returns:
        Updated reservation information
        
    Raises:
        HTTPException: If reservation not found or time conflict exists
    """
    reservation = db.query(RoomReservation).filter(RoomReservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    
    # Check for time conflicts if time is being updated
    if reservation_data.start_time or reservation_data.end_time:
        start_time = reservation_data.start_time or reservation.start_time
        end_time = reservation_data.end_time or reservation.end_time
        
        if start_time >= end_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start time must be before end time"
            )
        
        conflicting_reservations = db.query(RoomReservation).filter(
            RoomReservation.room_id == reservation.room_id,
            RoomReservation.id != reservation_id,
            RoomReservation.start_time < end_time,
            RoomReservation.end_time > start_time
        ).first()
        
        if conflicting_reservations:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Time conflict: Room is already reserved for this time period"
            )
    
    # Update reservation fields
    update_data = reservation_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(reservation, field, value)
    
    db.commit()
    db.refresh(reservation)
    
    return reservation

@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    reservation_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a reservation.
    
    Args:
        reservation_id: Reservation ID
        db: Database session
        
    Raises:
        HTTPException: If reservation not found
    """
    reservation = db.query(RoomReservation).filter(RoomReservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    
    db.delete(reservation)
    db.commit()
    
    return None

@router.get("/stats/summary")
async def get_reservation_stats(
    db: Session = Depends(get_db)
):
    """
    Get reservation statistics summary.
    
    Args:
        db: Database session
        
    Returns:
        Reservation statistics summary
    """
    # Get total reservations
    total_reservations = db.query(RoomReservation).count()
    
    # Get active reservations (future reservations)
    now = datetime.utcnow()
    active_reservations = db.query(RoomReservation).filter(
        RoomReservation.start_time > now
    ).count()
    
    # Get past reservations
    past_reservations = db.query(RoomReservation).filter(
        RoomReservation.end_time < now
    ).count()
    
    # Get current reservations
    current_reservations = db.query(RoomReservation).filter(
        RoomReservation.start_time <= now,
        RoomReservation.end_time >= now
    ).count()
    
    # Get total expected occupants
    total_occupants = db.query(RoomReservation).with_entities(
        db.func.sum(RoomReservation.expected_occupants)
    ).scalar() or 0
    
    return {
        "total_reservations": total_reservations,
        "active_reservations": active_reservations,
        "past_reservations": past_reservations,
        "current_reservations": current_reservations,
        "total_expected_occupants": total_occupants
    } 