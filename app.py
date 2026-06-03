from flask import Flask, jsonify, Request
from flask_cors import CORS
import pandas as pd

# Create Flask App 
app = Flask(__name__)
# Enable CORS for frontend connection 
CORS(app)

data = pd.read_csv("solar_panel_simulation_dataset.csv")

current_index = 0

#API Route
@app.route('/solar-data', methods=['GET'])
def solar_data():

    global current_index

    row = data.iloc[current_index]
    
    # JSON Response 
    result = {
        "timestamp": row["Timestamp"],
        "voltage": float(row["Voltage(V)"]),
        "current": float(row["Current(A)"]),
        "power": float(row["Power(W)"]),
        "temperature": float(row["Temperature(C)"]),
        "battery": float(row["Battery(%)"]),
        "status": row["System_Status"]
    }

    current_index += 1

    if current_index >= len(data):
        current_index = 0

    return jsonify(result)

# Prediction Route
@app.route('/predict', methods=['POST'])
def predict():

    data = Request.json

    voltage = float(data['voltage'])
    current = float(data['current'])
    temperature = float(data['temperature'])

    score = 0

    # Voltage Analysis
    if voltage < 20 or voltage > 32:
        score += 40
    elif voltage < 22 or voltage > 29:
        score += 20

    # Current Analysis
    if current < 2 or current > 11:
        score += 35
    elif current < 3 or current > 9:
        score += 15

    # Temperature Analysis
    if temperature > 65 or temperature < 0:
        score += 35
    elif temperature > 55:
        score += 15

    # Prediction Result
    if score <= 30:
        prediction = "System Normal"
    elif score <= 60:
        prediction = "Warning: Maintenance Recommended"
    else:
        prediction = "Critical Fault Predicted"

    return jsonify({
        "prediction": prediction,
        "fault_score": score
    })

# Run Server
if __name__ == '__main__':
    app.run(debug=True)