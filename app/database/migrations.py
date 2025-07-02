"""
Database migration system for Campus Access Management System.
Handles table creation and schema updates on application startup.
"""

import logging
from sqlalchemy import text, inspect
from sqlalchemy.exc import OperationalError
from app.models.base import engine, Base

logger = logging.getLogger(__name__)

def check_database_connection():
    """
    Check if database connection is available.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return True
    except OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during database connection: {e}")
        return False

def get_existing_tables():
    """
    Get list of existing tables in the database.
    
    Returns:
        list: List of table names
    """
    try:
        inspector = inspect(engine)
        return inspector.get_table_names()
    except Exception as e:
        logger.error(f"Error getting existing tables: {e}")
        return []

def create_all_tables():
    """
    Create all tables defined in the models.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("All tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        return False

def add_granted_column_to_access_logs():
    """
    Add granted column to access_logs table if it doesn't exist.
    """
    try:
        with engine.connect() as connection:
            # Check if granted column exists
            result = connection.execute(text("SHOW COLUMNS FROM access_logs LIKE 'granted'"))
            if not result.fetchone():
                # Add granted column
                connection.execute(text("""
                    ALTER TABLE access_logs 
                    ADD COLUMN granted BOOLEAN NOT NULL DEFAULT TRUE
                """))
                connection.commit()
                logger.info("Added 'granted' column to access_logs table")
                
                # Update existing records based on access_type
                connection.execute(text("""
                    UPDATE access_logs 
                    SET granted = (access_type != 'denied')
                    WHERE granted = TRUE
                """))
                connection.commit()
                logger.info("Updated existing access_logs records with granted status")
            else:
                logger.info("'granted' column already exists in access_logs table")
    except Exception as e:
        logger.error(f"Error adding granted column: {e}")
        return False
    return True

def run_migrations():
    """
    Run database migrations and setup.
    
    Returns:
        bool: True if migrations successful, False otherwise
    """
    try:
        # Check database connection first
        if not check_database_connection():
            logger.error("Cannot run migrations: Database connection failed")
            return False
        
        # Get existing tables
        existing_tables = get_existing_tables()
        logger.info(f"Existing tables: {existing_tables}")
        
        # Create all tables (SQLAlchemy will handle IF NOT EXISTS)
        if not create_all_tables():
            logger.error("Failed to create tables")
            return False
        
        # Add granted column to access_logs
        success = add_granted_column_to_access_logs()
        if not success:
            return False
        
        # Verify tables were created
        final_tables = get_existing_tables()
        logger.info(f"Final tables: {final_tables}")
        
        # Check if all required tables exist
        required_tables = [
            'users', 'access_cards', 'rooms', 'access_logs', 
            'room_reservations', 'students', 'professors', 'roles', 'user_roles'
        ]
        
        missing_tables = [table for table in required_tables if table not in final_tables]
        if missing_tables:
            logger.error(f"Missing required tables: {missing_tables}")
            return False
        
        logger.info("Database migration completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error during migration: {e}")
        return False

def check_table_data(table_name):
    """
    Check if a table has data.
    
    Args:
        table_name (str): Name of the table to check
        
    Returns:
        int: Number of rows in the table
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            logger.info(f"Table {table_name} has {count} rows")
            return count
    except Exception as e:
        logger.error(f"Error checking data in table {table_name}: {e}")
        return 0

def initialize_sample_data():
    """
    Initialize sample data if tables are empty.
    This will be handled by the database_setup.sql file in CI/CD.
    """
    try:
        # Check if users table has data
        user_count = check_table_data('users')
        if user_count == 0:
            logger.info("Tables appear to be empty. Sample data should be loaded from database_setup.sql")
        else:
            logger.info(f"Database already contains {user_count} users")
        
        return True
    except Exception as e:
        logger.error(f"Error checking sample data: {e}")
        return False 