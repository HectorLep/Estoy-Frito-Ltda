from flask import Flask, jsonify, request
from flask_cors import CORS
from generate_json import generate_sensor_data
import time
import threading
from datetime import datetime

app = Flask(__name__)
CORS(app)

data_history = []

def generate_data_loop():
    while True:
        data = generate_sensor_data()
        current_time = int(time.time() * 1000)
        
        data_history.append({
            'time': current_time,
            'temperature': data['dUMA']['environment']['temperature'],
            'humidity': data['dUMA']['environment']['humidity'],
            'iaq': data['dUMA']['air_quality']['iaq_index'],
            'pressure': data['dUMA']['environment']['air_pressure']
        })
        
        if len(data_history) > 100:
            data_history.pop(0)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Temp={data['dUMA']['environment']['temperature']}°C")
        time.sleep(5)

@app.route('/')
def index():
    return jsonify({'status': 'ok', 'message': 'Grafana Server Running', 'data_points': len(data_history)})

@app.route('/search', methods=['POST', 'GET'])
def search():
    return jsonify(['temperature', 'humidity', 'iaq', 'pressure'])

@app.route('/query', methods=['POST'])
def query():
    req = request.get_json()
    data = []
    
    for target in req.get('targets', []):
        metric = target.get('target', 'temperature')
        datapoints = [[d[metric], d['time']] for d in data_history if metric in d]
        data.append({'target': metric, 'datapoints': datapoints})
    
    return jsonify(data)

@app.route('/annotations', methods=['POST'])
def annotations():
    return jsonify([])

if __name__ == '__main__':
    print("Servidor Grafana iniciando...")
    thread = threading.Thread(target=generate_data_loop, daemon=True)
    thread.start()
    time.sleep(3)
    app.run(host='0.0.0.0', port=5000, debug=False)
