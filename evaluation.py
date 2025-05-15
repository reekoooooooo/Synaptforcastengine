import os
import json
from fetch_data import get_weather

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

    if "slower" in old_prediction.lower() and any(w in current_weather for w in keywords):
        print("SYNAPT: ✅ My prediction was correct.")
        update_accuracy(correct=True)
    elif "flow normally" in old_prediction.lower() and all(w not in current_weather for w in keywords):
        print("SYNAPT: ✅ My prediction was correct.")
        update_accuracy(correct=True)
    else:
        print("SYNAPT: ❌ My prediction was inaccurate.")
        update_accuracy(correct=False)

    print("[Evaluation] Real-world condition now:", current_weather)

def update_accuracy(correct):
    stats = {"correct": 0, "total": 0}
    if os.path.exists("accuracy.json"):
        with open("accuracy.json", "r") as f:
            stats = json.load(f)

    stats["total"] += 1
    if correct:
        stats["correct"] += 1

    with open("accuracy.json", "w") as f:
        json.dump(stats, f, indent=2)

def load_accuracy_stats():
    if os.path.exists("accuracy.json"):
        with open("accuracy.json", "r") as f:
            return json.load(f)
    return {"correct": 0, "total": 0}
