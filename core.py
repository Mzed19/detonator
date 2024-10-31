from flask import request, jsonify, render_template
from flask_smorest import Blueprint
from flask_socketio import send, SocketIO
import requests

main_bp = Blueprint("test", __name__, description="Initial test")

socketio = None

def init_socketio(app_socketio):
    global socketio
    socketio = app_socketio
    register_events() 

def register_events():
    @socketio.on('message')
    def handle_message(msg):
        send({'status': 'success', 'message': f'Gem: {msg}'}, broadcast=True)

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

@main_bp.route('/')
def index():
    return render_template('index.html')

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
    made_requests = 0

    
    while int(informationsOfTarget.requests_per_consumer) > made_requests:
        try:
            response = requests.get(informationsOfTarget.endpoint)
            elapsed_time = response.elapsed.total_seconds()
            
            socketio.emit('message', {
                'status': 'Success',
                'content': {
                    'requestTime': elapsed_time
                }
            }, namespace='/')
            
            socketio.sleep(0.1)
            
        except:
            socketio.emit('message', {
                'status': 'Error',
                'content': {
                    'requestTime': elapsed_time
                }
            }, namespace='/')
            
            socketio.sleep(0.1)
            
        made_requests += 1
        
        
    return jsonify('Finished')
    
    
