@echo off
echo Starting SanchAI Analytics Weather App...
echo.

echo Installing backend dependencies...
cd backend
pip install -r ../requirements.txt
if errorlevel 1 (
    echo Error installing Python dependencies
    pause
    exit /b 1
)

echo.
echo Installing frontend dependencies...
cd ../frontend
call npm install
if errorlevel 1 (
    echo Error installing Node.js dependencies
    pause
    exit /b 1
)

echo.
echo Setup complete! 
echo.
echo Please:
echo 1. Copy backend/.env.example to backend/.env
echo 2. Add your API keys to backend/.env
echo 3. Run 'npm run dev' from root directory
echo.
pause