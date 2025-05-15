import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_model_from_csv(csv_path):
    if not os.path.exists(csv_path):
        print(f"[X] File not found: {csv_path}")
        return None

    city_id = os.path.basename(csv_path).replace("weather_data_", "").replace(".csv", "")
    model_file = f"rain_model_{city_id}.pkl"

    df = pd.read_csv(csv_path)

    # Feature Engineering
    df["rain_tomorrow"] = df["precipitation_sum"].shift(-1).fillna(0)
    df["rain_tomorrow"] = (df["rain_tomorrow"] > 0.5).astype(int)

    X = df[["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "windspeed_10m_max", "cloudcover_mean"]]
    y = df["rain_tomorrow"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print(f"[🧠] Trained model for {city_id} — Accuracy: {acc*100:.2f}%")
    print("[ML] Classification report:")
    print(classification_report(y_test, preds))

    joblib.dump(model, model_file)
    print(f"[✓] Saved model to {model_file}")
    return model_file
