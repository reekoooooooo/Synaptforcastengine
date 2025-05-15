print("SYNAPT online.")
from predict import make_prediction
from log import log_prediction
from evaluation import evaluate_last_prediction, load_accuracy_stats
from memory import Memory
from fetch_data import get_weather
from region import get_region_weather_trends
from trend import analyze_city_trends
from ml_model import train_model, predict_with_model
from rich.console import Console
from forecast import get_daily_forecast
from weather_blurbs import get_weather_blurb_for_day

console = Console()

def main():
    # main.py (top of your input loop)
city = input("Enter a city (e.g., Charlotte): ").strip()

# Try to auto-fix missing comma
if ',' not in city and len(city.split()) == 2:
    city = city.replace(' ', ', ')

    synapt = Memory()
    from prepare_city import prepare_city

    city = console.input("\n[bold cyan]Enter a city[/] (e.g., Charlotte): ").strip()
    prepare_city(city)

    weather = get_weather(city)
    if "error" in weather.lower() or "not found" in weather.lower():
        print("SYNAPT: Could not fetch weather data. Please check the city name.")
        return

    lower_weather = weather.lower()
    synapt.store("latest_weather", weather)

    print("\n[Output] SYNAPT Observation:")
    print(weather)

    prediction = make_prediction(weather)
    log_prediction(city, prediction)
    evaluate_last_prediction(city)

    stats = load_accuracy_stats()
    if stats["total"] > 0:
        accuracy = (stats["correct"] / stats["total"]) * 100
        print(f"\n📊 Prediction Accuracy: {stats['correct']} out of {stats['total']} correct ({accuracy:.2f}%)")
    else:
        print("\n📊 No accuracy stats available yet.")

    # Detailed weather logic
    if any(term in lower_weather for term in ["blizzard", "heavy snow", "snowstorm"]):
        print("SYNAPT: Severe blizzard detected. High risk of closures and loss of visibility.")
    elif any(term in lower_weather for term in ["freezing rain", "icy mix", "sleet", "freezing drizzle"]):
        print("SYNAPT: Icy conditions detected. Roads may be treacherous.")
    elif any(term in lower_weather for term in ["light snow", "flurries"]):
        print("SYNAPT: Light snow present. Drive with caution.")
    elif any(term in lower_weather for term in ["rain", "heavy rain", "showers", "downpour"]):
        print("SYNAPT: Rain detected. Possible flooding or slowed traffic.")
    elif "drizzle" in lower_weather:
        print("SYNAPT: Drizzle present. Minimal disruption expected.")
    elif "thunderstorm" in lower_weather:
        print("SYNAPT: Thunderstorm in area. Stay indoors if possible.")
    elif any(term in lower_weather for term in ["fog", "haze", "mist"]):
        print("SYNAPT: Low visibility conditions. Travel with extreme caution.")
    elif any(term in lower_weather for term in ["wind", "gusts", "strong breeze"]):
        print("SYNAPT: Windy conditions may affect driving and flight paths.")
    elif any(term in lower_weather for term in ["hot", "heat", "heatwave", "very hot"]):
        print("SYNAPT: Extreme heat detected. Risk of overheating and health issues.")
    elif any(term in lower_weather for term in ["cold", "very cold", "bitter cold", "chilly"]):
        print("SYNAPT: Low temperatures may affect systems and travel.")
    elif any(term in lower_weather for term in ["scattered clouds", "broken clouds"]):
        print("SYNAPT: Intermittent cloud cover. Monitoring visibility.")
    elif any(term in lower_weather for term in ["overcast", "cloudy"]):
        print("SYNAPT: Overcast skies. Light disruption possible.")
    elif any(term in lower_weather for term in ["clear", "sunny", "mostly sunny"]):
        print("SYNAPT: Conditions clear. All systems nominal.")
    else:
        print("SYNAPT: Unknown weather condition. Manual assessment recommended.")

    analyze_city_trends(city)
    get_region_weather_trends(city)

    # FORECAST + AI BLURB PROMPT
    ask = console.input("\n[bold cyan]Would you like SYNAPT’s AI-powered forecast? (Y/N): ").strip().lower()
    if ask == "y":
        try:
            days = int(console.input("How many days ahead? (1–14): ").strip())
            print(f"\n🧠 SYNAPT Forecasting {days} Days Ahead...\n")
            get_daily_forecast(city, days=days)
            for i in range(days):
                print("💬 SYNAPT says:", get_weather_blurb_for_day(city, day_offset=i))
        except:
            print("SYNAPT: Invalid number. Forecast canceled.")
    else:
        print("SYNAPT: Maybe next time. Stay alert, stay synced.")

if __name__ == "__main__":
    main()
