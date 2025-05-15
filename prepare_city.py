import os
from historical_loader import fetch_historical_weather
from auto_train import train_model_from_csv

def prepare_city(city):
    city_id = city.lower().replace(",", "").replace(" ", "_")
    csv_file = f"weather_data_{city_id}.csv"
    model_file = f"rain_model_{city_id}.pkl"

    print(f"\n[🧠] Preparing SYNAPT for: {city.title()}")

    # Step 1: Check if historical data exists
    if not os.path.exists(csv_file):
        print(f"[📂] No historical data found for {city} — fetching now...")
        fetch_historical_weather(city)
    else:
        print(f"[✓] Historical data already exists for {city}")

    # Step 2: Check if model exists
    if not os.path.exists(model_file):
        print(f"[🧠] No trained model found for {city} — training now...")
        train_model_from_csv(csv_file)
    else:
        print(f"[✓] Model already exists for {city}")

    print(f"[✅] {city.title()} is ready.\n")
    return city_id  # or return paths if you want
