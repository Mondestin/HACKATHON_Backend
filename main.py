"""
Main FastAPI application entry point for Campus Access Management System.
This file contains the FastAPI app instance and basic configuration.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import routers
from app.routers import health, users, access_cards, access_logs, rooms, reservations, students, professors, auth
from app.config.settings import APP_NAME, APP_VERSION, CORS_ORIGINS, CORS_ALLOW_CREDENTIALS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS

# Import database migration
from app.database.migrations import run_migrations, initialize_sample_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title=APP_NAME,
    description="Internal API for campus access control, room reservations, and user management",
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(access_cards.router, prefix="/api/v1/access-cards", tags=["access-cards"])
app.include_router(access_logs.router, prefix="/api/v1/access-logs", tags=["access-logs"])
app.include_router(rooms.router, prefix="/api/v1/rooms", tags=["rooms"])
app.include_router(reservations.router, prefix="/api/v1/reservations", tags=["reservations"])
app.include_router(students.router, prefix="/api/v1/students", tags=["students"])
app.include_router(professors.router, prefix="/api/v1/professors", tags=["professors"])

@app.on_event("startup")
async def startup_event():
    """
    Run database migrations and initialization on application startup.
    """
    logger.info("Starting Campus Access Management System...")
    
    # Run database migrations
    logger.info("Running database migrations...")
    migration_success = run_migrations()
    
    if migration_success:
        logger.info("Database migrations completed successfully")
        # Check sample data
        initialize_sample_data()
    else:
        logger.error("Database migrations failed. Application may not function correctly.")
        # Note: We don't exit here to allow the app to start even if migrations fail
        # This is useful for development and testing scenarios

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message and API information.
    """
    return JSONResponse(
        content={
            "message": f"Welcome to {APP_NAME}!",
            "description": "A comprehensive API for managing campus access control, room reservations, and user profiles",
            "version": APP_VERSION,
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
    from app.config.settings import HOST, PORT, DEBUG, LOG_LEVEL
    
    # Print startup information
    print(f"Starting {APP_NAME} v{APP_VERSION}")
    print(f"Server will be available at: http://{HOST}:{PORT}")
    print(f"API Documentation: http://{HOST}:{PORT}/docs")
    print(f"Health Check: http://{HOST}:{PORT}/api/v1/health")
    print("-" * 50)
    
    # Run the application with uvicorn
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,  # Enable auto-reload for development
        log_level=LOG_LEVEL.lower(),
        access_log=True
    ) 