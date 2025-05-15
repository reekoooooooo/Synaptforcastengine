import json
import os

def get_region(city):
    if not os.path.exists("city_groups.json"):
        return None

    with open("city_groups.json", "r") as f:
        groups = json.load(f)

    for region, cities in groups.items():
        if city.lower() in [c.lower() for c in cities]:
            return region
    return None

def get_region_weather_trends(city):
    region = get_region(city)
    if not region:
        print(f"[Region] No region found for {city}")
        return

    with open("memory.json", "r") as f:
        memory = json.load(f)

    cities_in_region = []
    with open("city_groups.json", "r") as f:
        groups = json.load(f)
        cities_in_region = groups.get(region, [])

    trends = {}
    for c in cities_in_region:
        trends[c] = {
            "rain": 0,
            "clear": 0,
            "total": 0
        }

    for entry in memory:
        city_logged = entry["city"]
        if city_logged in cities_in_region:
            trends[city_logged]["total"] += 1
            pred = entry["prediction"].lower()
            if "rain" in pred:
                trends[city_logged]["rain"] += 1
            elif "clear" in pred:
                trends[city_logged]["clear"] += 1

    print(f"\n🌐 Regional Summary: {region}")
    for c, data in trends.items():
        if data["total"] > 0:
            rain_pct = (data["rain"] / data["total"]) * 100
            clear_pct = (data["clear"] / data["total"]) * 100
            print(f" - {c}: {data['rain']} rain ({rain_pct:.1f}%), {data['clear']} clear ({clear_pct:.1f}%)")
        else:
            print(f" - {c}: No data.")

