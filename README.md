# SanchAI Analytics Weather App

A minimal weather application with React frontend and FastAPI backend using LangChain and Azure OpenAI.

## Project Structure

```
weather-app/
├── frontend/          # React application
├── backend/           # FastAPI application
├── requirements.txt   # Python dependencies
├── package.json      # Node.js dependencies
└── README.md         # This file
```

## Setup Instructions

### Backend Setup
1. Navigate to backend directory
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables in `.env` file
4. Run: `uvicorn main:app --reload`

### Frontend Setup
1. Navigate to frontend directory
2. Install dependencies: `npm install`
3. Run: `npm start`

## Environment Variables Required
- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_ENDPOINT
- AZURE_OPENAI_DEPLOYMENT_NAME
- WEATHER_API_KEY (OpenWeatherMap)