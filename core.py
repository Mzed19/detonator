from flask import request, jsonify, render_template
from flask_smorest import Blueprint
from flask_socketio import send, SocketIO
import requests
from datetime import datetime

main_bp = Blueprint("test", __name__, description="Initial test")

socketio = None

def init_socketio(app_socketio):
    global socketio
    socketio = app_socketio


class TargetInformations:
    def __init__(self, endpoint, authorization, consumers_quantity, json_payload, requests_per_consumer):
        self.endpoint = endpoint
        self.authorization = authorization
        self.consumers_quantity = consumers_quantity
        self.json_payload = json_payload
        self.requests_per_consumer = requests_per_consumer

    def to_dict(self):
        return {
            'endpoint': self.endpoint,
            'authorization': self.authorization,
            'consumers_quantity': self.consumers_quantity,
            'json_payload': self.json_payload,
            'requests_per_consumer': self.requests_per_consumer
        }
        
    def camel_case(self):
        return {
            'endpoint': self.endpoint,
            'authorization': self.authorization,
            'consumersQuantity': self.consumers_quantity,
            'jsonPayload': self.json_payload,
            'requestsPerConsumer': self.requests_per_consumer
        }

informationsOfTarget = TargetInformations('yourApi', 'yourToken', 1, {}, 1)
requests_elapsed_time = []

@main_bp.route('/')
def index():
    return render_template('index.html', metrics={})

@main_bp.route('/', methods=['POST'])
def save_target_informations():
    global informationsOfTarget
    
    data = request.get_json()
    informationsOfTarget = TargetInformations(
        data.get('endpoint'),
        data.get('authorization'),
        data.get('consumersQuantity'),
        data.get('jsonPayload'),
        data.get('requestsPerConsumer')
    )

    return jsonify(informationsOfTarget.camel_case())

@main_bp.route('/target-infos', methods=['GET'])
def get_target_informations():
    return jsonify(informationsOfTarget.camel_case())

@main_bp.route('/detonate', methods=['GET'])
def detonate():
    global requests_elapsed_time
    for _ in range(int(informationsOfTarget.consumers_quantity)): 
        socketio.start_background_task(run_detonation)
    return jsonify('Started 5 detonation tasks')

def run_detonation():
    made_requests = 0

    while int(informationsOfTarget.requests_per_consumer) > made_requests:
        try:
            response = requests.get(informationsOfTarget.endpoint)
            elapsed_time = response.elapsed.total_seconds()
            
            socketio.emit('requests', {
                'status': 'Success',
                'content': {
                    'executionTime': elapsed_time,
                    'dateTime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'requestNumber': str(made_requests)
                }
            }, namespace='/')

            socketio.sleep(0.1)

            send_requisitions_metrics(elapsed_time)

        except Exception as e:
            socketio.emit('requests', {
                'status': 'Error',
                'content': {
                    'message': str(e),
                    'executionTime': elapsed_time if 'elapsed_time' in locals() else 0,
                    'dateTime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'requestNumber': str(made_requests)
                }
            }, namespace='/')

            socketio.sleep(0.1)

        made_requests += 1
    
    return jsonify('Finished detonation tasks')

def send_requisitions_metrics(elapsed_time):
    requests_elapsed_time.append(elapsed_time)
    
    
    if requests_elapsed_time:
        average_time = sum(requests_elapsed_time) / len(requests_elapsed_time)
        max_time = max(requests_elapsed_time) 

    else:
        average_time = 0
        max_time = 0

    socketio.emit('metrics', {
        'averageExecutionTime': average_time,
        'totalRequests': len(requests_elapsed_time),
        'maxExecutionTime': max_time, 
        'dateTime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }, namespace='/')

        
    

    
