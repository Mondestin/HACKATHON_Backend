"""
Rooms router for Campus Access Management System.
Handles room CRUD operations and management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.base import get_db
from app.models.database_models import Room
from app.models.schemas import (
    RoomCreate, RoomUpdate, RoomResponse,
    PaginationParams, PaginatedResponse, ErrorResponse
)

router = APIRouter()

@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(
    room_data: RoomCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new room.
    
    Args:
        room_data: Room creation data
        db: Database session
        
    Returns:
        Created room information
    """
    # Create new room
    db_room = Room(
        name=room_data.name,
        location=room_data.location,
        capacity=room_data.capacity
    )
    
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    
    return db_room

@router.get("/", response_model=List[RoomResponse])
async def get_rooms(
    db: Session = Depends(get_db)
):
    """
    Get all rooms.
    
    Args:
        db: Database session
        
    Returns:
        List of all rooms
    """
    # Get all rooms
    rooms = db.query(Room).all()
    
    return rooms

@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific room by ID.
    
    Args:
        room_id: Room ID
        db: Database session
        
    Returns:
        Room information
        
    Raises:
        HTTPException: If room not found
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    return room

@router.get("/location/{location}", response_model=List[RoomResponse])
async def get_rooms_by_location(
    location: str,
    db: Session = Depends(get_db)
):
    """
    Get all rooms in a specific location.
    
    Args:
        location: Room location
        db: Database session
        
    Returns:
        List of rooms in the location
    """
    rooms = db.query(Room).filter(Room.location == location).all()
    return rooms

@router.get("/capacity/{min_capacity}", response_model=List[RoomResponse])
async def get_rooms_by_min_capacity(
    min_capacity: int,
    db: Session = Depends(get_db)
):
    """
    Get all rooms with minimum capacity.
    
    Args:
        min_capacity: Minimum room capacity
        db: Database session
        
    Returns:
        List of rooms with minimum capacity
        
    Raises:
        HTTPException: If minimum capacity is negative
    """
    if min_capacity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Minimum capacity must be non-negative"
        )
    
    rooms = db.query(Room).filter(Room.capacity >= min_capacity).all()
    return rooms

@router.put("/{room_id}", response_model=RoomResponse)
async def update_room(
    room_id: str,
    room_data: RoomUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a room.
    
    Args:
        room_id: Room ID
        room_data: Room update data
        db: Database session
        
    Returns:
        Updated room information
        
    Raises:
        HTTPException: If room not found
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Update room fields
    update_data = room_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(room, field, value)
    
    db.commit()
    db.refresh(room)
    
    return room

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a room.
    
    Args:
        room_id: Room ID
        db: Database session
        
    Raises:
        HTTPException: If room not found
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    db.delete(room)
    db.commit()
    
    return None

@router.get("/stats/summary")
async def get_room_stats(
    db: Session = Depends(get_db)
):
    """
    Get room statistics summary.
    
    Args:
        db: Database session
        
    Returns:
        Room statistics summary
    """
    # Get total rooms
    total_rooms = db.query(Room).count()
    
    # Get total capacity
    total_capacity = db.query(Room).with_entities(
        db.func.sum(Room.capacity)
    ).scalar() or 0
    
    # Get average capacity
    avg_capacity = db.query(Room).with_entities(
        db.func.avg(Room.capacity)
    ).scalar() or 0
    
    # Get unique locations
    unique_locations = db.query(Room.location).distinct().count()
    
    # Get rooms by capacity range
    small_rooms = db.query(Room).filter(Room.capacity < 20).count()
    medium_rooms = db.query(Room).filter(Room.capacity >= 20, Room.capacity < 50).count()
    large_rooms = db.query(Room).filter(Room.capacity >= 50).count()
    
    return {
        "total_rooms": total_rooms,
        "total_capacity": total_capacity,
        "average_capacity": round(avg_capacity, 2),
        "unique_locations": unique_locations,
        "capacity_distribution": {
            "small_rooms_less_than_20": small_rooms,
            "medium_rooms_20_to_50": medium_rooms,
            "large_rooms_50_plus": large_rooms
        }
    } 