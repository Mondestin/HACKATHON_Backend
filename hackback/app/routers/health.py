"""
Health check router.
Contains endpoints for monitoring application health and status.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import os

# Create router instance
router = APIRouter()

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
            "service": "FastAPI Project",
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
        return JSONResponse(
            content={
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "service": "FastAPI Project",
                "version": "1.0.0",
                "environment": {
                    "python_version": os.sys.version,
                    "platform": os.sys.platform
                }
            },
            status_code=200
        )
    except Exception as e:
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
    # Add any readiness checks here (database connections, external services, etc.)
    return JSONResponse(
        content={
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat()
        },
        status_code=200
    ) 