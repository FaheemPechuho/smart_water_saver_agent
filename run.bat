@echo off
REM Quick start script for Windows

echo Starting Smart Water Saver Agent...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please create a .env file with your API keys.
    echo See .env.example for reference.
    echo.
    pause
    exit /b 1
)

REM Install/update dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

echo.
echo Starting FastAPI server...
echo Access the API at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.

python main.py

