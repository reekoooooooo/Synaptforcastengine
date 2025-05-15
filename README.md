# Synaptforcastengine
A predictive machine learning ai forecasting thing by Tyrek Long
# SYNAPT Weather Core ☁️🧠

A terminal-based weather intelligence module that fetches real-time forecasts and hourly breakdowns for any city using the Open-Meteo API and geolocation services.

> 🔧 Part of **SYNAPT** — a modular AI system for environmental forecasting and real-world simulation.

---

## 🌍 Features

- 🔍 Search any city by name
- 📆 Get a **7-day weather forecast** (max/min temperature, wind, cloud coverage, rain)
- ⏰ View **hour-by-hour weather breakdown** for the current day
- 📦 Clean, styled terminal UI using [Rich](https://github.com/Textualize/rich)
- ✅ Built in Python with modern APIs
- 🧠 Machine Learning extension in development for intelligent weather prediction

---

## 📸 Preview

> Screenshots coming soon — you can add these after launching it in your terminal.

- `screenshots/forecast.png` — Daily Forecast
- `screenshots/hourly.png` — Hourly Forecast
- `screenshots/input.png` — Terminal UI Prompt

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/synapt-weather-core.git
cd synapt-weather-core
2. Install Dependencies
Install required Python packages:


pip install -r requirements.txt
Or manually:


pip install requests pandas geopy rich
3. Run the Program

python ui.py
🧠 Behind the Scenes
This module uses:

Tool	Purpose
Open-Meteo	Free weather forecast API
Geopy	Convert city name → lat/lon
Pandas	Process weather data
Rich	Styled terminal interface
Python 3.9+	Core language
🧠 Coming Soon (Full SYNAPT System)
Module	Status
🌦️ Weather Forecast	✅ Complete
⏱ Hourly Forecast	✅ Complete
🧠 AI Rain Prediction	🔄 In Progress
📈 Forecast vs AI Compare	🔜 Coming Soon
🗃️ Memory + Trend Storage	✅ Prototype
🌐 Multi-City Awareness	🔜 Coming Soon
🖥️ Web UI (Streamlit?)	🔜 Long-Term
📦 Project Structure

synapt-weather-core/
├── ui.py                 ← Main terminal interface
├── forecast.py           ← Daily + hourly weather logic
├── fetch_data.py         ← Raw weather text puller
├── memory.py             ← Simple in-session memory
├── predict.py            ← AI prediction engine (basic)
├── train_real_model.py   ← ML model trainer
├── requirements.txt      ← Python dependencies
├── README.md             ← You're here
└── screenshots/          ← UI previews
✨ Author
Tyrek Long
Computer Information Systems Major
South Carolina National Guard | Cybersecurity & AI Enthusiast
🔗 GitHub @reekoooooooo
📜 License
MIT License — free to build on, fork, or remix. Give credit where due.
