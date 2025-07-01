#!/usr/bin/env python3
"""
Setup script for Campus Access Management System.
This script helps users set up the environment and initialize the database.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"SUCCESS: {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        return False
    print(f"SUCCESS: Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_file = Path(".env")
    if env_file.exists():
        print("SUCCESS: .env file already exists")
        return True
    
    env_content = """# Campus Access Management System Environment Variables

# Database Configuration
DATABASE_URL=mysql+pymysql://campus_user:campus_password@localhost/campus_access_db
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=campus_access_db
DATABASE_USER=campus_user
DATABASE_PASSWORD=campus_password

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true
LOG_LEVEL=INFO
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("SUCCESS: .env file created")
        print("NOTE: Please update the database credentials in .env file")
        return True
    except Exception as e:
        print(f"ERROR: Failed to create .env file: {e}")
        return False

def main():
    """Main setup function."""
    print("Campus Access Management System Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment if it doesn't exist
    venv_path = Path(".venv")
    if not venv_path.exists():
        print("\nCreating virtual environment...")
        if not run_command("python -m venv .venv", "Creating virtual environment"):
            sys.exit(1)
    else:
        print("SUCCESS: Virtual environment already exists")
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        pip_cmd = ".venv\\Scripts\\pip"
        python_cmd = ".venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        pip_cmd = ".venv/bin/pip"
        python_cmd = ".venv/bin/python"
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("SUCCESS: Setup completed")
    print("\nNext steps:")
    print("1. Set up your MySQL database:")
    print("   - Run the database_setup.sql script in MySQL")
    print("   - Or create database manually and update .env file")
    print("\n2. Initialize the database:")
    print(f"   {python_cmd} -m app.database.init_db")
    print("\n3. Start the application:")
    print(f"   {python_cmd} -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("\n4. Access the API:")
    print("   - Interactive docs: http://localhost:8000/docs")
    print("   - Health check: http://localhost:8000/api/v1/health")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main() 