@echo off
title Automobile Service Diagnosis Assistant
echo ========================================================
echo   Automobile Service Diagnosis Assistant - 1-Credit Project
echo ========================================================
echo.
echo Starting FastAPI Backend and Streamlit Frontend...
echo.

REM Start FastAPI Backend in a new terminal window
start "FastAPI Backend (Port 8000)" cmd /k "python -m uvicorn backend.main:app --reload --port 8000"

echo FastAPI Backend started at http://127.0.0.1:8000
echo Swagger API Docs available at http://127.0.0.1:8000/docs
echo.

REM Wait 2 seconds for backend to initialize
timeout /t 2 /nobreak >nul

REM Start Streamlit Frontend
echo Starting Streamlit Frontend at http://localhost:8501 ...
python -m streamlit run frontend/app.py --server.port 8501

pause
