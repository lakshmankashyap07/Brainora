#!/bin/bash

# Brainora Learning Platform - Setup Script for macOS/Linux

echo ""
echo "========================================="
echo "  Brainora Learning Platform Setup"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python from https://www.python.org/"
    exit 1
fi

echo "[1/6] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "[2/6] Activating virtual environment..."
source venv/bin/activate

echo "[3/6] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "[4/6] Navigating to project directory..."
cd brainora_project

echo "[5/6] Running migrations..."
python manage.py makemigrations
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Error: Failed to run migrations"
    exit 1
fi

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Create superuser (admin account):"
echo "   python manage.py createsuperuser"
echo ""
echo "2. Run development server:"
echo "   python manage.py runserver"
echo ""
echo "3. Access the application:"
echo "   - Login: http://127.0.0.1:8000/auth/login/"
echo "   - Admin: http://127.0.0.1:8000/admin/"
echo ""
