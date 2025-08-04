from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import sqlite3
import os

app = Flask(__name__)

# Load model
model = joblib.load('model.pkl')

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            destination TEXT,
            time_slot TEXT,
            crowd TEXT,
            stand_time INTEGER,
            sit_from TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Predict API
@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.get_json()
    source = input_data['source']
    destination = input_data['destination']
    time = input_data['time']

    # Format input for model
    row = pd.DataFrame([[source, destination, time]], columns=['Source', 'Destination', 'Time_Slot'])
    row_encoded = pd.get_dummies(row)

    # Align with model columns
    model_columns = model.feature_names_in_
    for col in model_columns:
        if col not in row_encoded.columns:
            row_encoded[col] = 0
    row_encoded = row_encoded[model_columns]

    # Predict
    prediction = model.predict(row_encoded)[0]
    stand_time = 30 if prediction == 'High' else 15
    sit_from = "Next Major Station" if prediction == 'High' else "Mid Route"

    # Save to database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (source, destination, time_slot, crowd, stand_time, sit_from)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (source, destination, time, prediction, stand_time, sit_from))
    conn.commit()
    conn.close()

    return jsonify({
        'train': 'Example Express',
        'crowd': prediction,
        'stand_time': stand_time,
        'sit_from': sit_from
    })

# History page
@app.route('/history')
def history():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return render_template('history.html', records=rows)

if __name__ == '__main__':
    app.run(debug=True)
