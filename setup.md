# Setup Instructions for SanchAI Analytics Weather App

## Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- pip (Python package manager)

## Quick Setup

### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r ../requirements.txt

# Create environment file
copy .env.example .env
# Edit .env file with your credentials
```

### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

### 3. Environment Configuration
Edit `backend/.env` file with your credentials:
```
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
WEATHER_API_KEY=your_openweathermap_api_key
```

### 4. Get Weather API Key
1. Go to https://openweathermap.org/api
2. Sign up for free account
3. Get your API key
4. Add it to `.env` file

### 5. Run the Application

**Option 1: Run both services separately**
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm start
```

**Option 2: Run both services together**
```bash
# From root directory
npm install
npm run dev
```

### 6. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Testing the Application
Try these sample queries:
- "What's the weather in New York?"
- "How's the weather in London today?"
- "Tell me about the weather in Tokyo"
- "Weather in Mumbai"

## Project Structure
```
weather-app/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── .env.example         # Environment variables template
│   └── .env                 # Your environment variables (create this)
├── frontend/
│   ├── public/
│   │   └── index.html       # HTML template
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── App.css          # Styling
│   │   ├── index.js         # React entry point
│   │   └── index.css        # Global styles
│   └── package.json         # Frontend dependencies
├── requirements.txt         # Python dependencies
├── package.json            # Root package.json for scripts
└── README.md               # Project documentation
```