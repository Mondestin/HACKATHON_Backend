"""
Database initialization script for Campus Access Management System.
Creates all tables and inserts default data.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.database_models import Role, User
from app.config.settings import settings
import bcrypt

# —– Configuration du moteur et de la session au niveau module —–
engine = create_engine(settings["database_url"], pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_database():
    """
    Initialize the database by creating all tables and inserting default data.
    """
    # Création de toutes les tables
    Base.metadata.create_all(bind=engine)

    # Ouverture d'une session
    db = SessionLocal()
    try:
        # Vérifier et insérer les rôles par défaut
        if db.query(Role).count() == 0:
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

        # Vérifier et créer l'utilisateur admin
        if not db.query(User).filter(User.email == "admin@campus.com").first():
            hashed_password = bcrypt.hashpw(
                "admin123".encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')
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
