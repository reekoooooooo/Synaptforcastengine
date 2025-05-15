import json
import os
from datetime import datetime
from fetch_data import get_weather

def make_prediction(weather):
    if "rain" in weather.lower():
        prediction = "Traffic will be slower than usual."
    else:
        prediction = "Traffic will flow normally."

    print("[Prediction] SYNAPT predicts:", prediction)
    return prediction

    with open("prediction_log.json", "a") as f:
        f.write(json.dumps(entry) + "\n")

    # Save to long-term memory
    memory = {"city": city, "timestamp": timestamp, "prediction": prediction}
    if os.path.exists("memory.json"):
        with open("memory.json", "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append(memory)

    with open("memory.json", "w") as f:
        json.dump(history, f, indent=2)

    print("[Log] Prediction logged.")

def evaluate_last_prediction(city):
    if not os.path.exists("prediction_log.json"):
        print("[Evaluation] No past predictions found.")
        return

    with open("prediction_log.json", "r") as f:
        lines = f.readlines()

    if not lines:
        print("[Evaluation] Log is empty.")
        return

    last_entry = json.loads(lines[-1].strip())
    old_prediction = last_entry["prediction"]
    timestamp = last_entry["timestamp"]

    print(f"[Evaluation] Checking if prediction from {timestamp} was accurate...")
    current_weather = get_weather(city).lower()

    keywords = ["rain", "snow", "storm", "sleet", "freezing", "drizzle", "thunder", "fog", "mist"]

    if "slower" in old_prediction.lower() and any(word in current_weather for word in keywords):
        print("SYNAPT: ✅ My prediction was correct.")
        update_accuracy_file(correct=True)
    elif "flow normally" in old_prediction.lower() and all(word not in current_weather for word in keywords):
        print("SYNAPT: ✅ My prediction was correct.")
        update_accuracy_file(correct=True)
    else:
        print("SYNAPT: ❌ My prediction was inaccurate.")
        update_accuracy_file(correct=False)

    print("[Evaluation] Real-world condition now:", current_weather)

def update_accuracy_file(correct):
    stats = {"correct": 0, "total": 0}
    if os.path.exists("accuracy.json"):
        with open("accuracy.json", "r") as f:
            stats = json.load(f)

    stats["total"] += 1
    if correct:
        stats["correct"] += 1

    with open("accuracy.json", "w") as f:
        json.dump(stats, f, indent=2)

def update_accuracy_stats(city, prediction, weather):
    # optional placeholder for future use if you want deeper analysis
    pass

def load_accuracy_stats():
    if os.path.exists("accuracy.json"):
        with open("accuracy.json", "r") as f:
            return json.load(f)
    return {"correct": 0, "total": 0}
