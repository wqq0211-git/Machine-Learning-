@echo off
cd /d "%~dp0frontend"
if not exist node_modules (
  echo Missing node_modules. Please run:
  echo npm install
  pause
  exit /b 1
)
npm run dev

