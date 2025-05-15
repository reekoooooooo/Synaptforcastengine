import random

blurbs = {
    "rain": [
        "Grab an umbrella… or stay inside and chill you know?",
        "Rain’s coming. SYNAPT recommends canceling all your plans and watching the sky drip.",
        "Scattered rain and deeply scattered thoughts. Coincidence?",
    ],
    "clear": [
        "Clear skies. SYNAPT recommends driving with the windows down like it’s 2003.",
        "Not a cloud in sight — go touch some grass. Literally.",
        "Perfect weather for regretting not doing laundry earlier.",
    ],
    "cloud": [
        "Cloudy with a 98% chance of moodiness.",
        "Skies look overcast — like your ex’s attitude.",
        "Not quite gloomy, not quite bright. Just like your playlist.",
    ],
    "snow": [
        "Snow incoming. Engage cozy mode.",
        "Do not eat yellow snow. That is all.",
        "Snow: nature’s excuse to ghost all obligations.",
    ],
    "wind": [
        "Windy vibes today. Try not to get slapped by a rogue trash bin.",
        "Wind detected. SYNAPT suggests strong hair gel.",
        "Perfect day for flying — if you’re a plastic bag.",
    ],
    "hot": [
        "Scorching. SYNAPT recommends: ice, shade, and to DRINK YOUR WATER.",
        "It’s giving… dehydration.",
        "So hot, SYNAPT is sweating circuits.",
    ],
    "cold": [
        "Cold enough to question life choices.",
        "Bundle up. It’s disrespectfully chilly.",
        "Your breath’s visible. Cold...",
    ],
    "default": [
        "Just another day in the simulation.",
        "Weather seems normal. SYNAPT is suspicious.",
        "Undefined conditions detected. Reality may be glitching.",
    ]
}

def classify_weather_condition(temp_max, cloud, rain):
    if rain > 0.2:
        return "rain"
    elif cloud > 70:
        return "cloud"
    elif temp_max < 45:
        return "cold"
    elif temp_max > 85:
        return "hot"
    elif cloud < 30:
        return "clear"
    else:
        return "default"

def get_weather_blurb_for_day(temp_max, cloud, rain):
    category = classify_weather_condition(temp_max, cloud, rain)
    return random.choice(blurbs.get(category, blurbs["default"]))
