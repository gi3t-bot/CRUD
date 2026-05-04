@echo off
echo ===================================
echo  Team Task Manager - Project Setup
echo ===================================

:: Step 1: Create virtual environment
echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (echo ERROR: Failed to create venv & pause & exit /b)

:: Step 2: Activate and install dependencies
echo [2/5] Installing Python dependencies...
call venv\Scripts\activate.bat
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers python-dotenv dj-database-url psycopg2-binary whitenoise

:: Step 3: Create migrations and apply them
echo [3/5] Creating database tables...
cd backend
python manage.py makemigrations users projects tasks
python manage.py migrate
python manage.py collectstatic --noinput 2>nul

echo [4/5] Done!
echo.
echo ===================================
echo  NEXT: Run the dev server
echo  cd backend
echo  ..\venv\Scripts\activate
echo  python manage.py runserver
echo ===================================
pause
