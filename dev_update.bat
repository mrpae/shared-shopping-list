@echo off
chcp 65001 >nul
echo 🔄 Development Update Script
echo ============================
echo.

echo 🐳 Stopping existing containers...
docker-compose down

echo.
echo 🔨 Rebuilding containers with latest changes...
docker-compose up --build -d

echo.
echo ✅ Containers rebuilt and started!
echo.
echo 📱 Access your app at: http://localhost:8501
echo 🌐 Ngrok dashboard: http://localhost:4040
echo.
echo 💡 Changes will be automatically detected and reloaded.
echo.

pause 