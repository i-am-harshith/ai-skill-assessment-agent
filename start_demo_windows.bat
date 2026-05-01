@echo off
setlocal enabledelayedexpansion

set "PROJECT_ROOT=%~dp0"
set "BACKEND_DIR=%PROJECT_ROOT%backend"
set "FRONTEND_DIR=%PROJECT_ROOT%frontend"
set "PYTHON_CMD="

echo Checking Python...
where py >nul 2>nul
if not errorlevel 1 set "PYTHON_CMD=py"
if "%PYTHON_CMD%"=="" (
  where python >nul 2>nul
  if not errorlevel 1 set "PYTHON_CMD=python"
)
if "%PYTHON_CMD%"=="" (
  echo Python not found. Install Python 3.11+ from https://www.python.org/downloads/windows/
  pause
  exit /b 1
)

echo Checking Node.js...
where npm >nul 2>nul
if errorlevel 1 (
  echo npm not found. Install Node.js LTS from https://nodejs.org/
  pause
  exit /b 1
)

if not exist "%BACKEND_DIR%\.venv\Scripts\python.exe" (
  echo Creating backend virtual environment...
  if /i "%PYTHON_CMD%"=="py" (
    py -3.11 -m venv "%BACKEND_DIR%\.venv" >nul 2>nul
    if errorlevel 1 (
      py -3 -m venv "%BACKEND_DIR%\.venv"
    )
  ) else (
    python -m venv "%BACKEND_DIR%\.venv"
  )
  if errorlevel 1 (
      echo Failed to create the Python virtual environment.
      pause
      exit /b 1
  )
)

echo Installing backend dependencies if needed...
call "%BACKEND_DIR%\.venv\Scripts\python.exe" -m pip install -r "%BACKEND_DIR%\requirements.txt"
if errorlevel 1 (
  echo Failed to install backend requirements.
  pause
  exit /b 1
)

echo Installing frontend dependencies if needed...
pushd "%FRONTEND_DIR%"
call npm install
if errorlevel 1 (
  popd
  echo Failed to install frontend dependencies.
  pause
  exit /b 1
)
popd

echo Starting backend in a new window...
start "AI Skill Assessment Backend" cmd /k "cd /d \"%BACKEND_DIR%\" && call .venv\Scripts\activate && uvicorn app.main:app --reload"

echo Starting frontend in a new window...
start "AI Skill Assessment Frontend" cmd /k "cd /d \"%FRONTEND_DIR%\" && npm run dev"

echo Waiting for services to start...
timeout /t 10 /nobreak >nul

start "" "http://localhost:5173"

echo Demo app launch requested. If the browser opens too early, refresh after a few seconds.
exit /b 0
