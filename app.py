from flask import Flask ,render_template, request, jsonify
import pickle
import os

print("Current Working Directory:", os.getcwd())

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))


if model is None or vectorizer is None:
    raise ValueError("Model or vectorizer is not loaded properly.")

# Create Flask application
app = Flask(__name__)

# Home Route
@app.route('/')
def home():
    return "<h1>Hello, Flask!</h1>"

# About Route
@app.route('/about')
def about():
    return "<h2>This is the About Page</h2>"

@app.route('/predict', methods=['POST'])
def predict_message():
    return render_template('index.html')
    
# Run the application
if __name__ == "__main__":
    app.run(debug=True)