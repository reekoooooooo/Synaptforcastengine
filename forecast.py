import requests
from geopy.geocoders import Nominatim
import pandas as pd
from weather_blurbs import get_weather_blurb_for_day  # Intelligent blurbs

def get_lat_lon(city):
    geolocator = Nominatim(user_agent="synapt")
    location = geolocator.geocode(city)
    if not location:
        print(f"[Geo] Couldn't find coordinates for {city}")
        return None, None
    return location.latitude, location.longitude

def get_daily_forecast(city, days=7):
    lat, lon = get_lat_lon(city)
    if lat is None or lon is None:
        return

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
        f"windspeed_10m_max,weathercode,cloudcover_mean"
        f"&timezone=auto"
        f"&temperature_unit=fahrenheit"
        f"&windspeed_unit=mph"
        f"&forecast_days={days}"
    )

    print(f"[Forecast] Fetching {days}-day forecast for {city}...")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"[Forecast] API error: {response.status_code}")
        return

    data = response.json()["daily"]
    df = pd.DataFrame(data)
    print(f"\n📆 Forecast for {city.title()} (Next {days} Days):\n")
    for i in range(len(df)):
        temp_max = df["temperature_2m_max"][i]
        temp_min = df["temperature_2m_min"][i]
        cloud = df["cloudcover_mean"][i]
        rain = df["precipitation_sum"][i]
        wind = df["windspeed_10m_max"][i]
        date = df["time"][i]

        blurb = get_weather_blurb_for_day(temp_max, cloud, rain)

        print(
            f"{date} → {temp_max}°F / {temp_min}°F, "
            f"Cloud: {cloud}%, Wind: {wind} mph, Rain: {rain} mm"
        )
        print("💬 SYNAPT says:", blurb)

def get_hourly_forecast_today(city):
    lat, lon = get_lat_lon(city)
    if lat is None or lon is None:
        return

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,precipitation,cloudcover,windspeed_10m"
        f"&timezone=auto"
        f"&temperature_unit=fahrenheit"
        f"&windspeed_unit=mph"
    )

    print(f"[Hourly] Fetching hourly forecast for today in {city}...")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"[Hourly] API error: {response.status_code}")
        return

    data = pd.DataFrame(response.json()["hourly"])
    today = data[data["time"].str.startswith(pd.Timestamp.now().strftime("%Y-%m-%d"))]

    print(f"\n⏰ Hour-by-Hour Forecast for Today ({city.title()}):\n")
    for i in range(len(today)):
        print(
            f"{today['time'].iloc[i][-5:]} → {today['temperature_2m'].iloc[i]}°F, "
            f"Clouds: {today['cloudcover'].iloc[i]}%, Wind: {today['windspeed_10m'].iloc[i]} mph, "
            f"Rain: {today['precipitation'].iloc[i]} mm"
        )
