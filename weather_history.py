import requests
from geopy.geocoders import Nominatim
import pandas as pd
import os

def get_lat_lon(city):
    geolocator = Nominatim(user_agent="synapt")
    location = geolocator.geocode(city)
    if not location:
        print(f"[Geo] Couldn't find coordinates for {city}")
        return None, None
    return location.latitude, location.longitude

def fetch_historical_weather(city, start_date="2023-01-01", end_date="2023-12-31"):
    lat, lon = get_lat_lon(city)
    if lat is None or lon is None:
        return None

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
        f"windspeed_10m_max,cloudcover_mean&timezone=auto"
    )

    print(f"[Weather] Fetching history for {city} ({lat}, {lon})...")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"[Weather] API error: {response.status_code}")
        return None

    data = response.json()["daily"]
    df = pd.DataFrame(data)
    df["city"] = city.lower().replace(" ", "")
    save_path = f"weather_data_{df['city'][0]}.csv"
    df.to_csv(save_path, index=False)
    print(f"[Weather] Saved historical data to {save_path}")
    return df
