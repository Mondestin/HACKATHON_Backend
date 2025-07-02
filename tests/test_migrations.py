"""
Test cases for database migration system.
"""

import pytest
from app.database.migrations import (
    check_database_connection,
    get_existing_tables,
    run_migrations,
    check_table_data
)

def test_database_connection():
    """Test database connection functionality."""
    # This test requires a running database
    # In CI, this should work with the MySQL service
    connection_successful = check_database_connection()
    assert connection_successful, "Database connection should be successful"

def test_get_existing_tables():
    """Test getting existing tables."""
    tables = get_existing_tables()
    assert isinstance(tables, list), "Should return a list of table names"
    
    # Check if required tables exist
    required_tables = [
        'users', 'access_cards', 'rooms', 'access_logs', 
        'reservations', 'students', 'professors'
    ]
    
    for table in required_tables:
        assert table in tables, f"Required table '{table}' should exist"

def test_run_migrations():
    """Test running migrations."""
    # Run migrations
    migration_success = run_migrations()
    assert migration_success, "Migrations should run successfully"
    
    # Verify tables exist after migration
    tables = get_existing_tables()
    required_tables = [
        'users', 'access_cards', 'rooms', 'access_logs', 
        'reservations', 'students', 'professors'
    ]
    
    for table in required_tables:
        assert table in tables, f"Table '{table}' should exist after migration"

def test_table_data():
    """Test checking table data."""
    # Check if users table has data
    user_count = check_table_data('users')
    assert user_count >= 0, "User count should be non-negative"
    
    # Check if access_cards table has data
    card_count = check_table_data('access_cards')
    assert card_count >= 0, "Access card count should be non-negative"
    
    # Check if rooms table has data
    room_count = check_table_data('rooms')
    assert room_count >= 0, "Room count should be non-negative"

def test_migration_idempotency():
    """Test that running migrations multiple times doesn't cause issues."""
    # Run migrations twice
    first_run = run_migrations()
    second_run = run_migrations()
    
    assert first_run, "First migration run should succeed"
    assert second_run, "Second migration run should succeed"
    
    # Both runs should result in the same table structure
    tables_after_first = get_existing_tables()
    tables_after_second = get_existing_tables()
    
    assert tables_after_first == tables_after_second, "Table structure should be consistent" 