from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.database_models import User, Student, Professor
from app.models.schemas import LoginResponse, UserResponse, ExtendedLoginResponse
from app.config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == username).first()
    if not user:
        return None
    if not pwd_context.verify(password, user.password_hash):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les informations d'identification",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == username).first()
    if user is None:
        raise credentials_exception
    return user

def get_user_profile(user: User, db: Session) -> Optional[dict]:
    """
    Get full user profile information based on user role.
    
    Args:
        user: User object
        db: Database session
        
    Returns:
        Dictionary containing full profile information or None for admin users
    """
    if user.role.value == "student":
        # Get student profile
        student = db.query(Student).filter(Student.user_id == user.id).first()
        if student:
            return {
                "type": "student",
                "id": student.id,
                "full_name": student.full_name,
                "student_card_id": student.student_card_id,
                "email": student.email,
                "class_name": student.class_name,
                "phone_number": student.phone_number,
                "registered_at": student.registered_at.isoformat() if student.registered_at else None
            }
    elif user.role.value == "professor":
        # Get professor profile
        professor = db.query(Professor).filter(Professor.user_id == user.id).first()
        if professor:
            return {
                "type": "professor",
                "id": professor.id,
                "full_name": professor.full_name,
                "email": professor.email,
                "department": professor.department,
                "phone_number": professor.phone_number,
                "office": professor.office
            }
    elif user.role.value == "admin":
        # For admin users, return basic admin info
        return {
            "type": "admin",
            "id": user.id,
            "email": user.email,
            "role": user.role.value
        }
    
    return None

@router.post("/login", response_model=ExtendedLoginResponse, summary="Connexion utilisateur")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return access token with user information and full profile details.
    
    Args:
        form_data: Login form data (username/email and password)
        db: Database session
        
    Returns:
        Extended login response with access token, user information, and full profile details
        
    Raises:
        HTTPException: If authentication fails
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    # Get full profile information
    profile = get_user_profile(user, db)
    
    # Return token, user information, and profile details
    return ExtendedLoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES,
        user=user,
        profile=profile
    )

@router.post("/logout", summary="Déconnexion utilisateur")
async def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Déconnexion réussie"}

@router.get("/me", response_model=UserResponse, summary="Obtenir les informations de l'utilisateur actuel")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information using the authentication token.
    
    Args:
        current_user: Current authenticated user (from token)
        
    Returns:
        Current user information
    """
    return current_user
