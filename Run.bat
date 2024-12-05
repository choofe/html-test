@echo off
REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not added to PATH. Please install Python from https://www.python.org and try again.
    pause
    exit /b
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing required dependencies...
pip install -r requirements.txt

REM Run the FastAPI server
echo Starting the FastAPI server...
uvicorn main:app --host 127.0.0.1 --port 8000 --reload

REM Deactivate virtual environment after server stops
echo Deactivating virtual environment...
deactivate

pause
