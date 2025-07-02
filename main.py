"""
Main FastAPI application entry point for Campus Access Management System.
This file contains the FastAPI app instance and basic configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import routers
from app.routers import health, users, access_cards, access_logs, rooms, reservations, students, professors

# Create FastAPI app instance
app = FastAPI(
    title="Campus Access Management System",
    description="A comprehensive API for managing campus access control, room reservations, and user profiles",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(access_cards.router, prefix="/api/v1/access-cards", tags=["access-cards"])
app.include_router(access_logs.router, prefix="/api/v1/access-logs", tags=["access-logs"])
app.include_router(rooms.router, prefix="/api/v1/rooms", tags=["rooms"])
app.include_router(reservations.router, prefix="/api/v1/reservations", tags=["reservations"])
app.include_router(students.router, prefix="/api/v1/students", tags=["students"])
app.include_router(professors.router, prefix="/api/v1/professors", tags=["professors"])

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message and API information.
    """
    return JSONResponse(
        content={
            "message": "Welcome to Campus Access Management System!",
            "description": "A comprehensive API for managing campus access control, room reservations, and user profiles",
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/api/v1/health",
            "endpoints": {
                "users": "/api/v1/users",
                "access_cards": "/api/v1/access-cards",
                "access_logs": "/api/v1/access-logs",
                "rooms": "/api/v1/rooms",
                "reservations": "/api/v1/reservations",
                "students": "/api/v1/students",
                "professors": "/api/v1/professors"
            }
        },
        status_code=200
    )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled exceptions.
    """
    return JSONResponse(
        content={
            "error": "Internal server error",
            "message": str(exc)
        },
        status_code=500
    )

if __name__ == "__main__":
    import uvicorn
    from app.config.settings import settings
    
    # Print startup information
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Server will be available at: http://{settings.host}:{settings.port}")
    print(f"API Documentation: http://{settings.host}:{settings.port}/docs")
    print(f"Health Check: http://{settings.host}:{settings.port}/api/v1/health")
    print("-" * 50)
    
    # Run the application with uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,  # Enable auto-reload for development
        log_level=settings.log_level.lower(),
        access_log=True
    ) 