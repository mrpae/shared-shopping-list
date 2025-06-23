@echo off
chcp 65001 >nul
echo 🛒 Shopping List App - Docker Setup
echo ===================================

REM Check if Docker Desktop is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running or not installed.
    echo Please start Docker Desktop and try again.
    echo Download Docker Desktop from: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo ✅ Docker is running

REM Create data directory
if not exist "data" (
    mkdir data
    echo ✅ Created data directory
) else (
    echo ✅ Data directory already exists
)

REM Check if .env file exists and handle ngrok configuration
if not exist ".env" (
    echo 📝 Creating .env file...
    copy env.example .env
    echo.
    echo 🌐 Ngrok Configuration Required
    echo ===============================
    echo.
    echo To expose your app to the internet, you need an ngrok auth token.
    echo.
    echo 1. Go to: https://dashboard.ngrok.com/get-started/your-authtoken
    echo 2. Sign up/login and copy your auth token
    echo 3. Paste it below when prompted
    echo.
    set /p ngrok_token="Enter your ngrok auth token: "
    
    if not "%ngrok_token%"=="" (
        echo NGROK_AUTHTOKEN=%ngrok_token% > .env
        echo ✅ Ngrok token configured!
    ) else (
        echo ❌ Ngrok token is required for external access.
        echo Please run setup.bat again and provide your token.
        pause
        exit /b 1
    )
    echo.
) else (
    echo ✅ .env file already exists
    
    REM Check if ngrok token is configured
    findstr /C:"NGROK_AUTHTOKEN=your_ngrok_auth_token_here" .env >nul
    if %errorlevel% equ 0 (
        echo ⚠️  Ngrok token not configured in .env file
        echo.
        set /p ngrok_token="Enter your ngrok auth token: "
        
        if not "%ngrok_token%"=="" (
            echo NGROK_AUTHTOKEN=%ngrok_token% > .env
            echo ✅ Ngrok token configured!
        ) else (
            echo ❌ Ngrok token is required for external access.
            pause
            exit /b 1
        )
        echo.
    ) else (
        echo ✅ Ngrok token already configured
    )
)

echo.
echo 🚀 Starting Shopping List App with Docker and Ngrok...
echo.
echo 📱 Local access: http://localhost:8501
echo 🌐 Ngrok dashboard: http://localhost:4040
echo 🌐 Public URL: Check ngrok dashboard for the public URL
echo.
echo Press Ctrl+C to stop the application
echo.

docker-compose --profile ngrok up --build

pause 