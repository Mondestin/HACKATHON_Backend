"""
Health check router.
Contains endpoints for monitoring application health and status.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import os
import logging

from app.database.migrations import check_database_connection, get_existing_tables, check_table_data

# Create router instance
router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health")
async def health_check():
    """
    Basic health check endpoint.
    Returns application status and basic information.
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "Campus Access Management System",
            "version": "1.0.0"
        },
        status_code=200
    )

@router.get("/health/detailed")
async def detailed_health_check():
    """
    Detailed health check endpoint.
    Returns comprehensive system information and application status.
    """
    try:
        # Check database connection
        db_connected = check_database_connection()
        tables = get_existing_tables() if db_connected else []
        
        return JSONResponse(
            content={
                "status": "healthy" if db_connected else "degraded",
                "timestamp": datetime.utcnow().isoformat(),
                "service": "Campus Access Management System",
                "version": "1.0.0",
                "database": {
                    "connected": db_connected,
                    "tables": tables,
                    "table_count": len(tables)
                },
                "environment": {
                    "python_version": os.sys.version,
                    "platform": os.sys.platform
                }
            },
            status_code=200
        )
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )

@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint.
    Used by load balancers and orchestration systems to determine if the service is ready to receive traffic.
    """
    try:
        # Check database connection
        db_connected = check_database_connection()
        
        if not db_connected:
            return JSONResponse(
                content={
                    "status": "not_ready",
                    "timestamp": datetime.utcnow().isoformat(),
                    "reason": "Database connection failed"
                },
                status_code=503
            )
        
        # Check if required tables exist
        tables = get_existing_tables()
        required_tables = ['users', 'access_cards', 'rooms', 'access_logs', 'room_reservations', 'students', 'professors', 'roles', 'user_roles']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            return JSONResponse(
                content={
                    "status": "not_ready",
                    "timestamp": datetime.utcnow().isoformat(),
                    "reason": f"Missing required tables: {missing_tables}"
                },
                status_code=503
            )
        
        return JSONResponse(
            content={
                "status": "ready",
                "timestamp": datetime.utcnow().isoformat(),
                "database": {
                    "connected": True,
                    "tables": tables
                }
            },
            status_code=200
        )
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return JSONResponse(
            content={
                "status": "not_ready",
                "timestamp": datetime.utcnow().isoformat(),
                "reason": f"Readiness check failed: {str(e)}"
            },
            status_code=503
        )

@router.get("/health/database")
async def database_health_check():
    """
    Database-specific health check endpoint.
    Returns detailed database status and table information.
    """
    try:
        # Check database connection
        db_connected = check_database_connection()
        
        if not db_connected:
            return JSONResponse(
                content={
                    "status": "unhealthy",
                    "timestamp": datetime.utcnow().isoformat(),
                    "database": {
                        "connected": False,
                        "error": "Database connection failed"
                    }
                },
                status_code=503
            )
        
        # Get table information
        tables = get_existing_tables()
        table_info = {}
        
        for table in tables:
            row_count = check_table_data(table)
            table_info[table] = {
                "exists": True,
                "row_count": row_count
            }
        
        return JSONResponse(
            content={
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "database": {
                    "connected": True,
                    "tables": table_info,
                    "total_tables": len(tables)
                }
            },
            status_code=200
        )
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return JSONResponse(
            content={
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "database": {
                    "connected": False,
                    "error": str(e)
                }
            },
            status_code=503
        ) 