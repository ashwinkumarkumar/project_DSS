@echo off
REM Batch script to run the Flask app for the Drone Decision Support System

REM Activate virtual environment if exists (optional)
IF EXIST venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Run the Flask app
python backend\app.py

REM Pause to keep the window open after the server stops
pause
