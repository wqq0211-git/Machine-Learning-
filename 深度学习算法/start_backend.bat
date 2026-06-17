@echo off
cd /d "%~dp0backend"
python -c "import fastapi,uvicorn,torch" 2>nul
if errorlevel 1 (
  echo Missing backend dependencies. Please run:
  echo python -m pip install -r requirements.txt
  pause
  exit /b 1
)
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
