from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
import random

app = Flask(__name__)
CORS(app)

# Single in-memory scenario state for demo
scenario = {
    "step": 0,
    "steps": [],
    "session": {
        "id": 1,
        "customer": "Customer_JHB",
        "location": "JOHANNESBURG",
        "start_time": None,
        "qoe_score": 5.0,
        "status": "idle"
    },
    "ticket": None,
    "notifications": []
}

def run_simulation():
    # Sequence of steps matching the user's scenario
    global scenario
    s = scenario
    s['steps'] = [
        {"id": 1, "name": "Detection", "desc": "Device handoff 4G->5G, latency spike 300ms", "duration": 2},
        {"id": 2, "name": "Prediction", "desc": "ML predicts poor QoE (2.1/5) with 89% confidence", "duration": 2},
        {"id": 3, "name": "Ticket Creation", "desc": "Auto-generate high-priority ticket for Network Ops", "duration": 1},
        {"id": 4, "name": "Customer Notification", "desc": "Send SMS/App alert to customer", "duration": 1},
        {"id": 5, "name": "Resolution", "desc": "Network Ops adjust load balancing; latency back to 85ms", "duration": 2},
        {"id": 6, "name": "Follow-up & Feedback", "desc": "Notify customer issue resolved + quick NPS survey", "duration": 1}
    ]

    # go through steps
    for step in s['steps']:
        s['step'] = step['id']
        name = step['name']
        # simulate effects per step
        if name == 'Detection':
            s['session']['status'] = 'degraded'
            s['session']['qoe_score'] = 3.5  # initial detect
            s['detection'] = {
                'latency_ms': 300,
                'handoff': '4G->5G'
            }
        elif name == 'Prediction':
            # ML prediction
            s['session']['qoe_score'] = 2.1
            s['prediction'] = {
                'qoe_score': 2.1,
                'confidence': 0.89,
                'root_cause': ['network_latency', 'app_retry_loops']
            }
        elif name == 'Ticket Creation':
            s['ticket'] = {
                'id': f"TKT-{random.randint(1000,9999)}",
                'title': 'Network latency issue in JHB region, customer streaming video',
                'priority': 'HIGH',
                'assigned_to': 'NETWORK OPS TEAM'
            }
        elif name == 'Customer Notification':
            notif = {
                'type': 'sms_app',
                'message': "We detected an issue with your video service. Our network team is working on it. ETA: 5 minutes.",
                'sent': True
            }
            s['notifications'].append(notif)
        elif name == 'Resolution':
            # simulate resolution
            s['detection']['latency_ms'] = 85
            s['session']['qoe_score'] = 3.8
            s['session']['status'] = 'ok'
        elif name == 'Follow-up & Feedback':
            notif = {
                'type': 'sms_app',
                'message': "Issue resolved. Your service is back to normal. Please rate us.",
                'sent': True
            }
            s['notifications'].append(notif)

        # wait for the duration to simulate time passing
        time.sleep(step['duration'])

    # mark completed
    s['step'] = len(s['steps'])


@app.route('/api/sessions/', methods=['GET'])
def get_sessions():
    return jsonify([scenario['session']])


@app.route('/api/scenario/start', methods=['POST'])
def start_scenario():
    # start the simulation in a background thread
    t = threading.Thread(target=run_simulation, daemon=True)
    t.start()
    scenario['session']['start_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
    scenario['session']['status'] = 'running'
    return jsonify({'started': True})


@app.route('/api/scenario/state', methods=['GET'])
def scenario_state():
    return jsonify({
        'current_step': scenario.get('step'),
        'steps': scenario.get('steps'),
        'session': scenario.get('session'),
        'ticket': scenario.get('ticket'),
        'notifications': scenario.get('notifications'),
        'prediction': scenario.get('prediction', None),
        'detection': scenario.get('detection', None)
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
