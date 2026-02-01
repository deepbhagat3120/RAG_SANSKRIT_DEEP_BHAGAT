@echo off
setlocal
echo ===========================================
echo       Sanskrit RAG System Launcher
echo ===========================================

cd /d "%~dp0"

echo [1/5] Checking Python Version...

set PYTHON_CMD=python
%PYTHON_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 'python' command not found. Checking for 'py' launcher...
    set PYTHON_CMD=py
    %PYTHON_CMD% --version >nul 2>&1
)
if %errorlevel% neq 0 (
    echo 'py' command not found. Checking default install paths...
    if exist "C:\Users\HP\AppData\Local\Programs\Python\Python311\python.exe" (
        set PYTHON_CMD="C:\Users\HP\AppData\Local\Programs\Python\Python311\python.exe"
    ) else (
        set PYTHON_VER=Unknown
        goto :BAD_PYTHON
    )
)

for /f "tokens=2" %%I in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VER=%%I
echo Detected Python Version: %PYTHON_VER% using command: %PYTHON_CMD%

:: Check for 3.13 or 3.14 (Preview versions)
echo %PYTHON_VER% | findstr /C:"3.14" >nul
if %errorlevel%==0 goto :BAD_PYTHON
echo %PYTHON_VER% | findstr /C:"3.13" >nul
if %errorlevel%==0 goto :BAD_PYTHON

goto :GOOD_PYTHON

:BAD_PYTHON
echo.
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo CRITICAL ERROR: Incompatible or Missing Python Version (%PYTHON_VER%)
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo.
echo The libraries required for AI/RAG (llama-cpp, chromadb) DO NOT support
echo Python 3.13+ yet. They require C++ compilation which is failing.
echo.
echo === SOLUTION ===
echo 1. Ensure Python 3.11 is installed.
echo    Link: https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
echo 2. If already installed, ensure it is added to PATH or use the 'py' launcher.
echo.
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
pause
exit /b

:GOOD_PYTHON
echo Python version looks compatible. Proceeding...
timeout /t 2

if exist venv (
    venv\Scripts\python.exe --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [2/5] Cleaning broken virtual environment...
        rmdir /s /q venv
    )
)


if not exist venv (
    echo [2/5] Creating Python Virtual Environment...
    "%PYTHON_CMD%" -m venv venv
)

echo [3/5] Activating Virtual Environment...
:: We define the explicit path to the venv python to avoid PATH issues
set "VENV_PYTHON=%~dp0venv\Scripts\python.exe"

:: Verify venv python exists
if not exist "%VENV_PYTHON%" (
    echo ERROR: Virtual environment python not found at "%VENV_PYTHON%"
    echo Please run clean_install.bat
    pause
    exit /b
)

echo [4/5] Installing Dependencies...
"%VENV_PYTHON%" -m pip install --upgrade pip
:: Force install of CPU wheel
"%VENV_PYTHON%" -m pip install llama-cpp-python==0.2.90 --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
"%VENV_PYTHON%" -m pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Installation failed.
    echo Please ensure you are not using Python 3.13+.
    pause
    exit /b
)

if not exist "models\tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf" (
    echo [5/5] Downloading Model...
    "%VENV_PYTHON%" code\download_model.py
)

echo.
echo ===========================================
echo 1. Run Web App (Streamlit)
echo 2. Run CLI App (Command Line)
echo 3. Ingest New Data (Run this)
echo ===========================================
set /p choice="Enter choice (1/2/3): "

if "%choice%"=="1" (
    "%VENV_PYTHON%" -m streamlit run code\app.py
) else if "%choice%"=="2" (
    "%VENV_PYTHON%" code\main_cli.py
) else if "%choice%"=="3" (
    "%VENV_PYTHON%" code\ingest.py
    pause
) else (
    echo Invalid choice
    pause
)
endlocal
