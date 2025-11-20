from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Dummy prediction logic
    qoe = np.random.uniform(1,5)
    return jsonify({'qoe_score': qoe})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
