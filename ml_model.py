import json
import os
import re
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer

model_path = "synapt_model.pkl"
vector_path = "synapt_vectorizer.pkl"

def load_training_data():
    if not os.path.exists("memory.json"):
        return [], []

    with open("memory.json", "r") as f:
        memory = json.load(f)

    X = []
    y = []

    for entry in memory:
        prediction = entry.get("prediction", "").lower()
        label = 1 if "correct" in prediction or "flow normally" in prediction else 0  # crude label
        weather_text = prediction  # You can later swap to actual weather if you store it

        X.append(weather_text)
        y.append(label)

    return X, y

def train_model():
    X, y = load_training_data()
    if len(X) < 5:
        print("[ML] Not enough data to train a model.")
        return

    vectorizer = CountVectorizer()
    X_vect = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_vect, y)

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vector_path)

    print("[ML] Model trained and saved.")

def predict_with_model(text):
    if not os.path.exists(model_path) or not os.path.exists(vector_path):
        print("[ML] No trained model available.")
        return "Traffic condition unknown. Please train the model."

    model = joblib.load(model_path)
    vectorizer = joblib.load(vector_path)

    X_vect = vectorizer.transform([text])
    prediction = model.predict(X_vect)[0]

    return "Traffic will flow normally." if prediction == 1 else "Traffic will be slower than usual."
