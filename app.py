from flask import Flask, render_template, request, jsonify
import pickle
import os

print("Current Working Directory:", os.getcwd())

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

if model is None or vectorizer is None:
    raise ValueError("Model or vectorizer is not loaded properly.")

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

    # Basic vectorization and prediction using loaded pickle model
    vect = vectorizer.transform([message]).toarray()
    pred = model.predict(vect)[0]
    prediction = "Spam" if pred == 1 else "Ham"

    # Support AJAX response (JSON) or standard form submit (HTML)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
        return jsonify({'prediction': prediction, 'message': message})
        
    return render_template('index.html', prediction=prediction, message=message)
    
# Run the application
if __name__ == "__main__":
    app.run(debug=True)