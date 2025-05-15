import json
import os
from datetime import datetime

def normalize_city(city):
    return city.strip().lower().replace(" ", "").replace(",", "")

def log_prediction(city, prediction):
    normalized_city = normalize_city(city)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "timestamp": timestamp,
        "city": normalized_city,
        "prediction": prediction
    }

    # Log to prediction_log.json
    with open("prediction_log.json", "a") as f:
        f.write(json.dumps(entry) + "\n")

    # Log to memory.json
    if os.path.exists("memory.json"):
        with open("memory.json", "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append(entry)
    with open("memory.json", "w") as f:
        json.dump(history, f, indent=2)

    print("[Log] Prediction logged.")
