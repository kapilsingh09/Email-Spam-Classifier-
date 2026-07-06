from flask import Flask, render_template, request, jsonify
import pickle
import os
from pathlib import Path

print("Current Working Directory:", os.getcwd())

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"
VECTORIZER_PATH = BASE_DIR / "vectorizer.pkl"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

if not VECTORIZER_PATH.exists():
    raise FileNotFoundError(f"Vectorizer file not found: {VECTORIZER_PATH}")

with MODEL_PATH.open("rb") as model_file:
    model = pickle.load(model_file)

with VECTORIZER_PATH.open("rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

if model is None or vectorizer is None:
    raise ValueError("Model or vectorizer is not loaded properly.")

SPAM_KEYWORDS = [
    "free", "win", "winner", "claim", "prize", "cash", "reward",
    "urgent", "click", "bonus", "offer", "guaranteed", "congratulations",
    "reply", "txt", "call now", "limited time", "act now", "won"
]


def heuristic_prediction(message):
    text = (message or "").lower()
    if not text.strip():
        return "Ham"

    spam_hits = sum(1 for keyword in SPAM_KEYWORDS if keyword in text)
    return "Spam" if spam_hits >= 2 else "Ham"


def predict_text(message):
    try:
        if not message or not str(message).strip():
            return "Ham"

        vect = vectorizer.transform([message])
        pred = model.predict(vect)[0]
        return "Spam" if int(pred) == 1 else "Ham"
    except Exception:
        return heuristic_prediction(message)


# Create Flask application
app = Flask(__name__)

# Home Route serving the index page
@app.route('/')
def home():
    return render_template('index.html')

# About Route
@app.route('/about')
def about():
    return "<h2>This is the About Page</h2>"

@app.route('/predict', methods=['POST'])
def predict_message():
    message = ""
    # Support both JSON (AJAX) and Form Data requests
    if request.is_json:
        message = request.json.get('message', '')
    else:
        message = request.form.get('message', '')
        
    if not message:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            return jsonify({'error': 'No message provided', 'prediction': 'Ham', 'message': ''}), 400
        return render_template('index.html', prediction=None, message=None)

    prediction = predict_text(message)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
        return jsonify({'prediction': prediction, 'message': message})
        
    return render_template('index.html', prediction=prediction, message=message)
    
if __name__ == "__main__":
    app.run(debug=True)