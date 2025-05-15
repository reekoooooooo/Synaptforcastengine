import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    print("[DEBUG] API Key Loaded:", api_key)

    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
    )

    print(f"[World Input] Fetching live weather for {city}...")
    response = requests.get(url)

    if response.status_code != 200:
        return f"Error fetching weather: {response.status_code}"

    data = response.json()

    desc = data['weather'][0]['description']
    temp = data['main']['temp']

    return f"Weather in {city}: {desc.capitalize()} with {temp}°F"
