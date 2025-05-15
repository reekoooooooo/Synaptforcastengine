import json
import os

def analyze_city_trends(city):
    if not os.path.exists("memory.json"):
        print("[Trends] No memory data found.")
        return

    with open("memory.json", "r") as f:
        data = json.load(f)

    city_data = [entry for entry in data if entry["city"].lower() == city.lower()]
    if not city_data:
        print(f"[Trends] No past predictions for {city}.")
        return

    # Weather keyword categories
    categories = {
        "rain": 0,
        "clear": 0,
        "snow": 0,
        "cloud": 0,
        "fog": 0,
        "wind": 0,
        "other": 0
    }

    for entry in city_data:
        prediction = entry["prediction"].lower()
        matched = False
        for key in categories:
            if key in prediction:
                categories[key] += 1
                matched = True
                break
        if not matched:
            categories["other"] += 1

    total = len(city_data)
    print(f"\n📊 Weather Trend for {city.title()} (last {total} records):")
    for k, v in categories.items():
        if v > 0:
            percent = (v / total) * 100
            print(f" - {k.title()}: {v} times ({percent:.1f}%)")
