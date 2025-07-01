"""
Database initialization script for Campus Access Management System.
Creates all tables and inserts default data.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.database_models import Role, User, UserRole
from app.config.settings import settings
import bcrypt

def init_database():
    """
    Initialize the database by creating all tables and inserting default data.
    """
    # Create database engine
    engine = create_engine(settings.database_url)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if default roles already exist
        existing_roles = db.query(Role).count()
        if existing_roles == 0:
            # Insert default roles
            default_roles = [
                Role(name="admin"),
                Role(name="student"),
                Role(name="professor")
            ]
            db.add_all(default_roles)
            db.commit()
            print("Default roles created successfully")
        else:
            print("Default roles already exist")
        
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.email == "admin@campus.com").first()
        if not admin_user:
            # Create admin user
            hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin_user = User(
                email="admin@campus.com",
                password_hash=hashed_password,
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print("Admin user created successfully")
        else:
            print("Admin user already exists")
        
        print("Database initialization completed successfully")
        
    except Exception as e:
        print(f"Error during database initialization: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database() 