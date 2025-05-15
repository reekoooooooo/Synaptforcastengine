from log import log_prediction
import json

def test_logging():
    test_city = "Testville"
    test_prediction = "Traffic will flow normally."
    
    log_prediction(test_city, test_prediction)

    # Confirm it's in the last entry of prediction_log.json
    with open("prediction_log.json", "r") as f:
        lines = f.readlines()
        last = json.loads(lines[-1])
        print("\n[✅] Last Logged Prediction:")
        print(json.dumps(last, indent=2))

if __name__ == "__main__":
    test_logging()
