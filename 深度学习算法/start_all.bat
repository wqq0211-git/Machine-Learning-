@echo off
cd /d "%~dp0"
start "CIFAR10 Backend" cmd /k start_backend.bat
start "CIFAR10 Frontend" cmd /k start_frontend.bat

