"""
Students router for Campus Access Management System.
Handles student profile CRUD operations and management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.base import get_db
from app.models.database_models import Student, User
from app.models.schemas import (
    StudentCreate, StudentUpdate, StudentResponse,
    PaginationParams, PaginatedResponse, ErrorResponse
)

router = APIRouter()

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new student profile.
    
    Args:
        student_data: Student creation data
        db: Database session
        
    Returns:
        Created student information
        
    Raises:
        HTTPException: If user not found or email/student_card_id already exists
    """
    # Check if user exists
    user = db.query(User).filter(User.id == student_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user already has a student profile
    existing_student = db.query(Student).filter(Student.user_id == student_data.user_id).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a student profile"
        )
    
    # Check if email already exists
    existing_email = db.query(Student).filter(Student.email == student_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student with this email already exists"
        )
    
    # Check if student card ID already exists
    existing_card = db.query(Student).filter(Student.student_card_id == student_data.student_card_id).first()
    if existing_card:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student with this card ID already exists"
        )
    
    # Create new student profile
    db_student = Student(
        user_id=student_data.user_id,
        full_name=student_data.full_name,
        student_card_id=student_data.student_card_id,
        email=student_data.email,
        class_name=student_data.class_name,
        phone_number=student_data.phone_number
    )
    
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    return db_student

@router.get("/", response_model=List[StudentResponse])
async def get_students(
    db: Session = Depends(get_db)
):
    """
    Get all students.
    
    Args:
        db: Database session
        
    Returns:
        List of all students
    """
    # Get all students
    students = db.query(Student).all()
    
    return students

@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific student by ID.
    
    Args:
        student_id: Student ID
        db: Database session
        
    Returns:
        Student information
        
    Raises:
        HTTPException: If student not found
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return student

@router.get("/user/{user_id}", response_model=StudentResponse)
async def get_student_by_user_id(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get student profile by user ID.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        Student information
        
    Raises:
        HTTPException: If student not found
    """
    student = db.query(Student).filter(Student.user_id == user_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found for this user"
        )
    
    return student

@router.get("/class/{class_name}", response_model=List[StudentResponse])
async def get_students_by_class(
    class_name: str,
    db: Session = Depends(get_db)
):
    """
    Get all students in a specific class.
    
    Args:
        class_name: Class name
        db: Database session
        
    Returns:
        List of students in the class
    """
    students = db.query(Student).filter(Student.class_name == class_name).all()
    return students

@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: str,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a student profile.
    
    Args:
        student_id: Student ID
        student_data: Student update data
        db: Database session
        
    Returns:
        Updated student information
        
    Raises:
        HTTPException: If student not found or email/student_card_id already exists
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Check if email is being updated and if it already exists
    if student_data.email and student_data.email != student.email:
        existing_email = db.query(Student).filter(Student.email == student_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student with this email already exists"
            )
    
    # Check if student card ID is being updated and if it already exists
    if student_data.student_card_id and student_data.student_card_id != student.student_card_id:
        existing_card = db.query(Student).filter(Student.student_card_id == student_data.student_card_id).first()
        if existing_card:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student with this card ID already exists"
            )
    
    # Update student fields
    update_data = student_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    
    db.commit()
    db.refresh(student)
    
    return student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a student profile.
    
    Args:
        student_id: Student ID
        db: Database session
        
    Raises:
        HTTPException: If student not found
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    db.delete(student)
    db.commit()
    
    return None

@router.get("/stats/summary")
async def get_student_stats(
    db: Session = Depends(get_db)
):
    """
    Get student statistics summary.
    
    Args:
        db: Database session
        
    Returns:
        Student statistics summary
    """
    # Get total students
    total_students = db.query(Student).count()
    
    # Get unique classes
    unique_classes = db.query(Student.class_name).distinct().count()
    
    # Get students by class
    class_counts = db.query(
        Student.class_name,
        db.func.count(Student.id).label('count')
    ).group_by(Student.class_name).all()
    
    # Get students with phone numbers
    students_with_phone = db.query(Student).filter(Student.phone_number.isnot(None)).count()
    
    return {
        "total_students": total_students,
        "unique_classes": unique_classes,
        "students_with_phone": students_with_phone,
        "class_distribution": [
            {"class_name": class_name, "count": count}
            for class_name, count in class_counts
        ]
    } 