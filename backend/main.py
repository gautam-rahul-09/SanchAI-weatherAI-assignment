from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
import httpx
import json
import re

# Load environment variables
load_dotenv()

app = FastAPI(title="Weather App API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class WeatherQuery(BaseModel):
    message: str

class WeatherResponse(BaseModel):
    response: str

# Weather function using OpenWeatherMap API
def get_weather(city: str) -> str:
    """Get current weather information for a given city."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Weather API key not configured"
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = httpx.get(url)
        
        if response.status_code == 200:
            data = response.json()
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            
            return f"Weather in {city}: {weather.title()}, Temperature: {temp}°C (feels like {feels_like}°C), Humidity: {humidity}%"
        else:
            return f"Could not find weather information for {city}"
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"

# Initialize Azure OpenAI
def get_llm():
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    if not all([endpoint, api_key, deployment]):
        raise ValueError("Missing Azure OpenAI configuration. Please check your .env file.")
    
    return AzureChatOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version="2024-02-15-preview",
        deployment_name=deployment,
        temperature=0.1
    )

# Extract city from user message
def extract_city_from_message(message: str) -> str:
    """Extract city name from user message using simple patterns."""
    # Common patterns for weather queries
    patterns = [
        r"weather (?:in|of|for) ([a-zA-Z\s]+)",
        r"(?:in|of) ([a-zA-Z\s]+) weather",
        r"([a-zA-Z\s]+) weather",
        r"weather ([a-zA-Z\s]+)"
    ]
    
    message_lower = message.lower()
    for pattern in patterns:
        match = re.search(pattern, message_lower)
        if match:
            city = match.group(1).strip()
            # Clean up common words
            city = re.sub(r'\b(today|tomorrow|now|current|the)\b', '', city).strip()
            if city:
                return city.title()
    
    # If no pattern matches, try to find city names (simple approach)
    words = message.split()
    for word in words:
        if len(word) > 2 and word.isalpha():
            return word.title()
    
    return "Mumbai"  # Default city

# Process weather query with LLM
async def process_weather_query(message: str) -> str:
    """Process weather query using Azure OpenAI and weather API."""
    try:
        # Extract city from message
        city = extract_city_from_message(message)
        
        # Get weather data
        weather_info = get_weather(city)
        
        # Use LLM to generate a natural response
        llm = get_llm()
        
        prompt = f"""
        User asked: "{message}"
        
        Weather information: {weather_info}
        
        Please provide a natural, conversational response about the weather. Be friendly and helpful.
        """
        
        response = llm.invoke(prompt)
        return response.content
        
    except Exception as e:
        return f"I'm sorry, I couldn't get the weather information right now. Error: {str(e)}"

@app.get("/")
async def root():
    return {"message": "Weather App API is running"}

@app.post("/weather", response_model=WeatherResponse)
async def get_weather_response(query: WeatherQuery):
    try:
        result = await process_weather_query(query.message)
        return WeatherResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)