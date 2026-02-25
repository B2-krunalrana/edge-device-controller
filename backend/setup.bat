@echo off
REM ========================================
REM Edge Device Controller - Setup Script
REM ========================================

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   Edge Device Controller - Automated Setup         ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please download Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python detected:
python --version
echo.

REM Install pip packages
echo 📦 Installing Python dependencies...
echo.

pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install Python packages
    pause
    exit /b 1
)

echo ✅ Python packages installed successfully!
echo.

REM Check if cloudflared is installed
cloudflared --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Cloudflared is not installed
    echo.
    echo 📥 Downloading Cloudflared...
    echo Please choose your Windows version:
    echo 1) 64-bit (Recommended)
    echo 2) 32-bit
    set /p choice="Enter choice [1-2]: "
    
    if "%choice%"=="1" (
        REM Download 64-bit version
        powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile 'cloudflared.exe'"
    ) else if "%choice%"=="2" (
        REM Download 32-bit version
        powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-386.exe' -OutFile 'cloudflared.exe'"
    ) else (
        echo Invalid choice
        pause
        exit /b 1
    )
    
    REM Move to System32
    move cloudflared.exe C:\Windows\System32\
    echo ✅ Cloudflared installed to C:\Windows\System32\
) else (
    echo ✅ Cloudflared is already installed:
    cloudflared --version
)

echo.
echo ════════════════════════════════════════════════════
echo ✅ Setup Complete!
echo ════════════════════════════════════════════════════
echo.
echo 📖 NEXT STEPS:
echo.
echo Option 1 - Run with Cloudflare Tunnel (Internet Access):
echo   python main.py
echo.
echo Option 2 - Run Local Server Only (LAN Access):
echo   python other-scripts/server.py
echo.
echo 🌐 For more information, see README.md
echo.
pause
