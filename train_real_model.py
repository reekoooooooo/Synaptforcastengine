import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_rain_model(csv_path):
    if not os.path.exists(csv_path):
        print("[ML] Data file not found.")
        return

    df = pd.read_csv(csv_path)

    # Create binary target: did it rain tomorrow?
    df["rain_tomorrow"] = df["precipitation_sum"].shift(-1).fillna(0)
    df["rain_tomorrow"] = (df["rain_tomorrow"] > 0.1).astype(int)

    # Drop last row (NaN label after shift)
    df = df[:-1]

    features = [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "windspeed_10m_max",
        "cloudcover_mean"
    ]

    X = df[features]
    y = df["rain_tomorrow"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"[ML] Accuracy: {acc:.2%}")
    print("[ML] Classification report:")
    print(classification_report(y_test, y_pred))

    # Save model
    joblib.dump(model, "rain_predictor.pkl")
    print("[ML] Model saved to rain_predictor.pkl")

def predict_rain_from_data(today_data):
    if not os.path.exists("rain_predictor.pkl"):
        return "No model found. Please train one first."

    model = joblib.load("rain_predictor.pkl")
    prediction = model.predict([today_data])[0]
    return "Rain likely tomorrow." if prediction == 1 else "No rain expected tomorrow."
