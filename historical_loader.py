import os
import requests
import pandas as pd
from geopy.geocoders import Nominatim

def get_lat_lon(city):
    geolocator = Nominatim(user_agent="synapt-historical")
    location = geolocator.geocode(city)
    if not location:
        print(f"[Geo] Could not find coordinates for {city}")
        return None, None
    return location.latitude, location.longitude

def fetch_historical_weather(city, years_back=2):
    city_clean = city.lower().replace(",", "").replace(" ", "_")
    file_name = f"weather_data_{city_clean}.csv"

    if os.path.exists(file_name):
        print(f"[✓] Historical weather file already exists: {file_name}")
        return file_name

    lat, lon = get_lat_lon(city)
    if not lat or not lon:
        print(f"[X] Invalid location: {city}")
        return None

    start = f"{pd.Timestamp.now().year - years_back}-01-01"
    end = f"{pd.Timestamp.now().year - 1}-12-31"

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start}&end_date={end}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
        f"windspeed_10m_max,cloudcover_mean"
        f"&temperature_unit=fahrenheit"
        f"&windspeed_unit=mph"
        f"&timezone=auto"
    )

    print(f"[Weather] Fetching history for {city.title()} ({lat}, {lon})...")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"[X] Failed to fetch historical data: {response.status_code}")
        return None

    data = response.json()["daily"]
    df = pd.DataFrame(data)
    df["city"] = city_clean
    df.to_csv(file_name, index=False)

    print(f"[✓] Saved historical data to {file_name}")
    train_model_from_csv(file_name)
    return file_name

from auto_train import train_model_from_csv
