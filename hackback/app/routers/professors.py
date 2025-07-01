"""
Professors router for Campus Access Management System.
Handles professor profile CRUD operations and management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.base import get_db
from app.models.database_models import Professor, User
from app.models.schemas import (
    ProfessorCreate, ProfessorUpdate, ProfessorResponse,
    PaginationParams, PaginatedResponse, ErrorResponse
)

router = APIRouter()

@router.post("/", response_model=ProfessorResponse, status_code=status.HTTP_201_CREATED)
async def create_professor(
    professor_data: ProfessorCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new professor profile.
    
    Args:
        professor_data: Professor creation data
        db: Database session
        
    Returns:
        Created professor information
        
    Raises:
        HTTPException: If user not found or email already exists
    """
    # Check if user exists
    user = db.query(User).filter(User.id == professor_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user already has a professor profile
    existing_professor = db.query(Professor).filter(Professor.user_id == professor_data.user_id).first()
    if existing_professor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a professor profile"
        )
    
    # Check if email already exists
    existing_email = db.query(Professor).filter(Professor.email == professor_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Professor with this email already exists"
        )
    
    # Create new professor profile
    db_professor = Professor(
        user_id=professor_data.user_id,
        full_name=professor_data.full_name,
        email=professor_data.email,
        department=professor_data.department,
        phone_number=professor_data.phone_number,
        office=professor_data.office
    )
    
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    
    return db_professor

@router.get("/", response_model=List[ProfessorResponse])
async def get_professors(
    db: Session = Depends(get_db)
):
    """
    Get all professors.
    
    Args:
        db: Database session
        
    Returns:
        List of all professors
    """
    # Get all professors
    professors = db.query(Professor).all()
    
    return professors

@router.get("/{professor_id}", response_model=ProfessorResponse)
async def get_professor(
    professor_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific professor by ID.
    
    Args:
        professor_id: Professor ID
        db: Database session
        
    Returns:
        Professor information
        
    Raises:
        HTTPException: If professor not found
    """
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )
    
    return professor

@router.get("/user/{user_id}", response_model=ProfessorResponse)
async def get_professor_by_user_id(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get professor profile by user ID.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        Professor information
        
    Raises:
        HTTPException: If professor not found
    """
    professor = db.query(Professor).filter(Professor.user_id == user_id).first()
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor profile not found for this user"
        )
    
    return professor

@router.get("/department/{department}", response_model=List[ProfessorResponse])
async def get_professors_by_department(
    department: str,
    db: Session = Depends(get_db)
):
    """
    Get all professors in a specific department.
    
    Args:
        department: Department name
        db: Database session
        
    Returns:
        List of professors in the department
    """
    professors = db.query(Professor).filter(Professor.department == department).all()
    return professors

@router.put("/{professor_id}", response_model=ProfessorResponse)
async def update_professor(
    professor_id: str,
    professor_data: ProfessorUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a professor profile.
    
    Args:
        professor_id: Professor ID
        professor_data: Professor update data
        db: Database session
        
    Returns:
        Updated professor information
        
    Raises:
        HTTPException: If professor not found or email already exists
    """
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )
    
    # Check if email is being updated and if it already exists
    if professor_data.email and professor_data.email != professor.email:
        existing_email = db.query(Professor).filter(Professor.email == professor_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Professor with this email already exists"
            )
    
    # Update professor fields
    update_data = professor_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(professor, field, value)
    
    db.commit()
    db.refresh(professor)
    
    return professor

@router.delete("/{professor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_professor(
    professor_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a professor profile.
    
    Args:
        professor_id: Professor ID
        db: Database session
        
    Raises:
        HTTPException: If professor not found
    """
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )
    
    db.delete(professor)
    db.commit()
    
    return None

@router.get("/stats/summary")
async def get_professor_stats(
    db: Session = Depends(get_db)
):
    """
    Get professor statistics summary.
    
    Args:
        db: Database session
        
    Returns:
        Professor statistics summary
    """
    # Get total professors
    total_professors = db.query(Professor).count()
    
    # Get unique departments
    unique_departments = db.query(Professor.department).distinct().count()
    
    # Get professors by department
    department_counts = db.query(
        Professor.department,
        db.func.count(Professor.id).label('count')
    ).group_by(Professor.department).all()
    
    # Get professors with phone numbers
    professors_with_phone = db.query(Professor).filter(Professor.phone_number.isnot(None)).count()
    
    # Get professors with offices
    professors_with_office = db.query(Professor).filter(Professor.office.isnot(None)).count()
    
    return {
        "total_professors": total_professors,
        "unique_departments": unique_departments,
        "professors_with_phone": professors_with_phone,
        "professors_with_office": professors_with_office,
        "department_distribution": [
            {"department": department, "count": count}
            for department, count in department_counts
        ]
    } 