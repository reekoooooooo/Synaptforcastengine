from forecast import get_daily_forecast, get_hourly_forecast_today
from fetch_data import get_weather
from predict import make_prediction, evaluate_last_prediction, load_accuracy_stats
from memory import Memory
from train_real_model import predict_rain_from_data
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def display_synapt_ui():
    console.clear()
    console.rule("[bold magenta]🌐 SYNAPT: Predictive Weather AI", style="bold purple")

    city = console.input("\n[bold cyan]Enter a city[/] (e.g., Charlotte): ").strip()

    # --- Memory System ---
    memory = Memory()
    weather = get_weather(city)
    memory.store("latest_weather", weather)

    # --- Forecast Section ---
    console.rule("[green]📆 Forecast (7 Days)")
    get_daily_forecast(city, days=7)

    console.rule("[blue]⏰ Hour-by-Hour Forecast (Today)")
    get_hourly_forecast_today(city)

    # --- AI Model Section ---
    console.rule("[yellow]🧠 AI Weather Prediction")

    prediction = make_prediction(weather)
    features = [80, 65, 0.0, 9, 40]  # dummy input — we’ll replace later with real
    ml_prediction = predict_rain_from_data(features)

    console.print(f"[white]Text-based prediction: [bold green]{prediction}")
    console.print(f"[white]ML model prediction: [bold cyan]{ml_prediction}")

    # --- Evaluation Section ---
    evaluate_last_prediction(city)

    # --- Accuracy Stats ---
    stats = load_accuracy_stats()
    if stats["total"] > 0:
        acc = (stats["correct"] / stats["total"]) * 100
        console.print(f"\n[bold white]📊 Prediction Accuracy: {stats['correct']} of {stats['total']} correct "
                      f"([green]{acc:.2f}%[/green])")
    else:
        console.print("[dim]No predictions yet to evaluate.")

    console.rule("[bold magenta]End of SYNAPT Report", style="bold purple")

if __name__ == "__main__":
    display_synapt_ui()
