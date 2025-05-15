# Core libraries
import os
import pandas as pd
import requests

# Rich terminal formatting
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Geo tools
from geopy.geocoders import Nominatim

# SYNAPT modules
from forecast import get_daily_forecast, get_hourly_forecast_today
from fetch_data import get_weather
from memory import Memory
from predict import make_prediction, evaluate_last_prediction, load_accuracy_stats
from prepare_city import prepare_city
from train_real_model import predict_rain_from_data  # This is your ML prediction function



console = Console()

def print_header(city):
    console.print(Panel.fit(f"[bold cyan]SYNAPT v1[/bold cyan]\nCity: [bold green]{city.title()}[/bold green]", title="🌐 AI Weather Terminal"))

def show_forecast_table(data):
    table = Table(title="📆 7-Day Forecast")

    table.add_column("Date", style="cyan")
    table.add_column("High/Low", style="yellow")
    table.add_column("Cloud", justify="right")
    table.add_column("Wind", justify="right")
    table.add_column("Rain", justify="right")

    for i in range(len(data)):
        table.add_row(
            data["time"][i],
            f"{data['temperature_2m_max'][i]}°F / {data['temperature_2m_min'][i]}°F",
            f"{data['cloudcover_mean'][i]}%",
            f"{data['windspeed_10m_max'][i]} mph",
            f"{data['precipitation_sum'][i]} mm"
        )
    console.print(table)

def show_today_ai_prediction():
    today_data = [82, 68, 0.0, 10, 65]  # placeholder or pull from live forecast
    result = predict_rain_from_data(today_data)
    console.print(Panel.fit(f"[bold magenta]AI Prediction for Tomorrow:[/bold magenta] {result}", title="🧠 SYNAPT AI"))

def launch_synapt_ui(city):
    print_header(city)
    lat, lon = get_lat_lon(city)
    if lat is None:
        return

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
        f"windspeed_10m_max,weathercode,cloudcover_mean"
        f"&timezone=auto"
        f"&temperature_unit=fahrenheit"
        f"&windspeed_unit=mph"
        f"&forecast_days=7"
    )
    response = requests.get(url)
    data = pd.DataFrame(response.json()["daily"])
    show_forecast_table(data)
    show_today_ai_prediction()
