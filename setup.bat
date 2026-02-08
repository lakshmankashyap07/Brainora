@echo off
REM Brainora Learning Platform - Setup Script for Windows

echo.
echo =========================================
echo   Brainora Learning Platform Setup
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/6] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/6] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/6] Navigating to project directory...
cd brainora_project

echo [5/6] Running migrations...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo Error: Failed to run migrations
    pause
    exit /b 1
)

echo.
echo =========================================
echo   Setup Complete!
echo =========================================
echo.
echo Next steps:
echo 1. Create superuser (admin account):
echo    python manage.py createsuperuser
echo.
echo 2. Run development server:
echo    python manage.py runserver
echo.
echo 3. Access the application:
echo    - Login: http://127.0.0.1:8000/auth/login/
echo    - Admin: http://127.0.0.1:8000/admin/
echo.
pause
