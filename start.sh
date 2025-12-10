#!/bin/bash

echo "Starting SanchAI Analytics Weather App..."
echo

echo "Installing backend dependencies..."
cd backend
pip install -r ../requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing Python dependencies"
    exit 1
fi

echo
echo "Installing frontend dependencies..."
cd ../frontend
npm install
if [ $? -ne 0 ]; then
    echo "Error installing Node.js dependencies"
    exit 1
fi

echo
echo "Setup complete!"
echo
echo "Please:"
echo "1. Copy backend/.env.example to backend/.env"
echo "2. Add your API keys to backend/.env"
echo "3. Run 'npm run dev' from root directory"
echo