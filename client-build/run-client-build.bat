@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo === Poetic Layer Client Build ===

REM Prefer python3 if present; otherwise fall back to python
where python3 >nul 2>nul
if %ERRORLEVEL%==0 (set PYTHON=python3) else (set PYTHON=python)

%PYTHON% --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
  echo ❌ Python not found. Please install Python 3.11+ from https://www.python.org/downloads/
  pause
  exit /b 1
)

REM Ensure pip exists (Windows Store python sometimes needs this)
%PYTHON% -m ensurepip --upgrade >nul 2>nul

REM Create venv if missing
if not exist venv (
  echo Creating virtual environment…
  %PYTHON% -m venv venv || (
    echo ❌ Failed to create venv.
    pause
    exit /b 1
  )
)

call venv\Scripts\activate

echo Upgrading pip…
python -m pip install --upgrade pip

echo Installing backend requirements…
pip install -r requirements.txt || (
  echo ❌ pip install failed.
  pause
  exit /b 1
)

REM Make sure Python can import "packages" from client-build root
set PYTHONPATH=%CD%

echo Starting Mapping Service on http://127.0.0.1:8000 …
REM If your app.py has a __main__ that starts uvicorn, this works. Otherwise switch to:
REM python -m uvicorn mapping-service.app:app --host 127.0.0.1 --port 8000
start "" cmd /c "python mapping-service/app.py"

REM Give server a moment, then open the frontend
timeout /t 2 >nul
start "" "%CD%\frontend\build\index.html"

echo All set. Press any key to stop (this does not stop the server window)…
pause
