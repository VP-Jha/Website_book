@echo off
setlocal

title V. P. Jha Website
cd /d "%~dp0"

echo.
echo ========================================
echo   V. P. Jha Website - Streamlit Setup
echo ========================================
echo.

if not exist "streamlit_app.py" (
    echo ERROR: streamlit_app.py was not found.
    echo Put this launcher in the same folder as streamlit_app.py.
    echo.
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ERROR: requirements.txt was not found.
    echo Put requirements.txt in this folder and try again.
    echo.
    pause
    exit /b 1
)

where py >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python was not found on this computer.
    echo Install Python from https://www.python.org/downloads/
    echo During installation, select "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

echo Installing the required package...
py -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (
    echo.
    echo ERROR: Installation did not complete.
    echo Please take a screenshot of the error above.
    echo.
    pause
    exit /b 1
)

echo.
echo Starting the website at http://localhost:8501
echo Keep this window open while using the website.
echo Press Ctrl+C to stop it.
echo.

py -m streamlit run "%~dp0streamlit_app.py"

echo.
echo The website has stopped.
pause
endlocal
