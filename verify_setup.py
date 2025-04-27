#!/usr/bin/env python
"""
Verification script for Plant Disease Detection Application
This script checks the environment, dependencies, and file structure
"""

import os
import sys
import importlib
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from flask import Flask
import sqlite3

# Set base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def check_python_version():
    """Check if Python version is compatible"""
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python version should be 3.8 or higher")
        return False
    print("✅ Python version OK")
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        "flask", "flask_sqlalchemy", "pillow", "torch", "torchvision", 
        "pandas", "numpy", "python-dotenv"
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            # Normalize package name for import
            import_name = package.replace("-", "_")
            importlib.import_module(import_name)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is not installed")
            all_installed = False
    
    return all_installed

def check_file_structure():
    """Check if all required files and directories exist"""
    required_files = [
        "run.py",
        "requirements.txt",
        ".env",
        "app/models.py",
        "app/routes.py",
        "app/__init__.py",
        "data/disease_info.csv",
        "data/supplement_info.csv",
        "models/plant_disease_model_1_latest (1).pt"
    ]
    
    required_dirs = [
        "app",
        "data",
        "models",
        "static",
        "static/css",
        "static/js",
        "static/uploads",
        "templates"
    ]
    
    all_files_exist = True
    all_dirs_exist = True
    
    # Check files
    for file_path in required_files:
        full_path = os.path.join(BASE_DIR, file_path)
        if not os.path.isfile(full_path):
            print(f"❌ File missing: {file_path}")
            all_files_exist = False
        else:
            print(f"✅ File exists: {file_path}")
    
    # Check directories
    for dir_path in required_dirs:
        full_path = os.path.join(BASE_DIR, dir_path)
        if not os.path.isdir(full_path):
            print(f"❌ Directory missing: {dir_path}")
            all_dirs_exist = False
        else:
            print(f"✅ Directory exists: {dir_path}")
    
    return all_files_exist and all_dirs_exist

def check_model_compatibility():
    """Check if the model file is compatible with installed torch version"""
    model_path = os.path.join(BASE_DIR, "models/plant_disease_model_1_latest (1).pt")
    if not os.path.isfile(model_path):
        print("❌ Model file is missing")
        return False
        
    try:
        import torch
        # Attempt to load model - this will fail if incompatible
        print("Testing model loading...")
        model = torch.load(model_path, map_location=torch.device('cpu'))
        print(f"✅ Model can be loaded with torch {torch.__version__}")
        return True
    except Exception as e:
        print(f"❌ Model loading failed: {str(e)}")
        return False

def test_env_variables():
    print("\nTesting Environment Variables:")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv(os.path.join(BASE_DIR, ".env"))
    
    # Test Flask Configuration
    print("\n1. Flask Configuration:")
    print("-" * 30)
    secret_key = os.getenv('SECRET_KEY')
    flask_app = os.getenv('FLASK_APP')
    flask_env = os.getenv('FLASK_ENV')
    
    print(f"SECRET_KEY: {'✓ Set' if secret_key else '✗ Not set'}")
    print(f"FLASK_APP: {'✓ Set' if flask_app else '✗ Not set'}")
    print(f"FLASK_ENV: {'✓ Set' if flask_env else '✗ Not set'}")
    
    # Test Groq API Configuration
    print("\n2. Groq API Configuration:")
    print("-" * 30)
    groq_key = os.getenv('GROQ_API_KEY')
    print(f"GROQ_API_KEY: {'✓ Set' if groq_key else '✗ Not set'}")
    
    if groq_key:
        try:
            client = Groq(api_key=groq_key)
            print("✓ Groq API Key is valid")
        except Exception as e:
            print(f"✗ Groq API Key validation failed: {str(e)}")
    
    # Test Database Configuration
    print("\n3. Database Configuration:")
    print("-" * 30)
    db_url = os.getenv('DATABASE_URL')
    print(f"DATABASE_URL: {'✓ Set' if db_url else '✗ Not set'}")
    
    if db_url:
        try:
            # Extract database path from SQLite URL
            db_path = os.path.join(BASE_DIR, db_url.replace('sqlite:///', ''))
            if os.path.exists(db_path):
                print(f"✓ Database file exists at: {db_path}")
            else:
                print(f"✗ Database file not found at: {db_path}")
        except Exception as e:
            print(f"✗ Database configuration error: {str(e)}")
    
    # Test Application Settings
    print("\n4. Application Settings:")
    print("-" * 30)
    upload_folder = os.getenv('UPLOAD_FOLDER')
    max_content_length = os.getenv('MAX_CONTENT_LENGTH')
    
    print(f"UPLOAD_FOLDER: {'✓ Set' if upload_folder else '✗ Not set'}")
    print(f"MAX_CONTENT_LENGTH: {'✓ Set' if max_content_length else '✗ Not set'}")
    
    if upload_folder:
        full_upload_path = os.path.join(BASE_DIR, upload_folder)
        if os.path.exists(full_upload_path):
            print(f"✓ Upload folder exists at: {upload_folder}")
        else:
            print(f"✗ Upload folder not found at: {upload_folder}")
    
    # Test Flask Application
    print("\n5. Flask Application Test:")
    print("-" * 30)
    try:
        app = Flask(__name__)
        app.config['SECRET_KEY'] = secret_key
        print("✓ Flask application created successfully")
    except Exception as e:
        print(f"✗ Flask application creation failed: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Environment Variables Test Complete")
    print("=" * 50)

def main():
    """Main verification function"""
    print("\n" + "="*50)
    print("Plant Disease Detection Application - Verification")
    print("="*50 + "\n")
    
    # Path checks
    print("Base directory:", BASE_DIR)
    print("\n" + "-"*50)
    print("CHECKING PYTHON ENVIRONMENT")
    print("-"*50)
    python_ok = check_python_version()
    
    print("\n" + "-"*50)
    print("CHECKING DEPENDENCIES")
    print("-"*50)
    deps_ok = check_dependencies()
    
    print("\n" + "-"*50)
    print("CHECKING FILE STRUCTURE")
    print("-"*50)
    files_ok = check_file_structure()
    
    print("\n" + "-"*50)
    print("CHECKING MODEL COMPATIBILITY")
    print("-"*50)
    model_ok = check_model_compatibility()
    
    # Summary
    print("\n" + "="*50)
    print("VERIFICATION SUMMARY")
    print("="*50)
    print(f"Python environment: {'✅ OK' if python_ok else '❌ Issues found'}")
    print(f"Dependencies: {'✅ OK' if deps_ok else '❌ Issues found'}")
    print(f"File structure: {'✅ OK' if files_ok else '❌ Issues found'}")
    print(f"Model compatibility: {'✅ OK' if model_ok else '❌ Issues found'}")
    
    if all([python_ok, deps_ok, files_ok, model_ok]):
        print("\n✅ All checks passed! The application should run correctly.")
        print("Run 'python run.py' to start the application.")
    else:
        print("\n❌ Some checks failed. Please fix the issues before running the application.")
        print("See the HELP.md file for troubleshooting information.")
    
    test_env_variables()

if __name__ == "__main__":
    main() 