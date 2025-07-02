"""
Tests for health check endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)

def test_health_check():
    """
    Test basic health check endpoint.
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["service"] == "FastAPI Project"
    assert data["version"] == "1.0.0"

def test_detailed_health_check():
    """
    Test detailed health check endpoint.
    """
    response = client.get("/api/v1/health/detailed")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "environment" in data
    
    # Check environment info
    environment = data["environment"]
    assert "python_version" in environment
    assert "platform" in environment

def test_readiness_check():
    """
    Test readiness check endpoint.
    """
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ready"
    assert "timestamp" in data

def test_root_endpoint():
    """
    Test root endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "docs" in data
    assert "redoc" in data
    assert "health" in data 