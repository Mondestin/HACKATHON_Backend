#!/usr/bin/env python3
"""
Database initialization script for Campus Access Management System.
This script can be run manually to set up the database and create tables.
"""

import sys
import os
import logging

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.migrations import run_migrations, initialize_sample_data, check_database_connection
from app.config.settings import DATABASE_URL

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    Main function to initialize the database.
    """
    logger.info("Starting database initialization...")
    logger.info(f"Database URL: {DATABASE_URL}")
    
    # Check database connection
    if not check_database_connection():
        logger.error("Cannot connect to database. Please check your configuration.")
        sys.exit(1)
    
    # Run migrations
    logger.info("Running database migrations...")
    if run_migrations():
        logger.info("Database migrations completed successfully!")
        
        # Check sample data
        logger.info("Checking sample data...")
        initialize_sample_data()
        
        logger.info("Database initialization completed successfully!")
        logger.info("You can now start the application.")
    else:
        logger.error("Database migrations failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 