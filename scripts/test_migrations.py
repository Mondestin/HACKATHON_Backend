#!/usr/bin/env python3
"""
Test script for database migration system.
This script can be run independently to test migrations.
"""

import sys
import os
import logging

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.migrations import (
    check_database_connection,
    get_existing_tables,
    run_migrations,
    check_table_data,
    initialize_sample_data
)
from app.config.settings import DATABASE_URL

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_migration_system():
    """
    Test the complete migration system.
    """
    logger.info("Starting migration system test...")
    logger.info(f"Database URL: {DATABASE_URL}")
    
    # Test 1: Database connection
    logger.info("Test 1: Checking database connection...")
    if not check_database_connection():
        logger.error("❌ Database connection failed")
        return False
    logger.info("✅ Database connection successful")
    
    # Test 2: Get existing tables
    logger.info("Test 2: Getting existing tables...")
    tables = get_existing_tables()
    logger.info(f"Found {len(tables)} existing tables: {tables}")
    
    # Test 3: Run migrations
    logger.info("Test 3: Running migrations...")
    if not run_migrations():
        logger.error("❌ Migration failed")
        return False
    logger.info("✅ Migration completed successfully")
    
    # Test 4: Verify tables after migration
    logger.info("Test 4: Verifying tables after migration...")
    final_tables = get_existing_tables()
    required_tables = [
        'users', 'access_cards', 'rooms', 'access_logs', 
        'reservations', 'students', 'professors'
    ]
    
    missing_tables = [table for table in required_tables if table not in final_tables]
    if missing_tables:
        logger.error(f"❌ Missing required tables: {missing_tables}")
        return False
    logger.info("✅ All required tables exist")
    
    # Test 5: Check table data
    logger.info("Test 5: Checking table data...")
    for table in required_tables:
        count = check_table_data(table)
        logger.info(f"Table '{table}': {count} rows")
    
    # Test 6: Initialize sample data check
    logger.info("Test 6: Checking sample data...")
    initialize_sample_data()
    
    logger.info("🎉 All migration tests passed!")
    return True

def main():
    """
    Main function to run migration tests.
    """
    try:
        success = test_migration_system()
        if success:
            logger.info("Migration system test completed successfully!")
            sys.exit(0)
        else:
            logger.error("Migration system test failed!")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error during migration test: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 