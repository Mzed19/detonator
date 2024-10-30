from flask import Flask
from flask_smorest import Api
from flask_caching import Cache
from flask_cors import CORS
from flask_socketio import SocketIO
import core  # Importar o módulo core

app = Flask(__name__)
cache = Cache(app)
socketio_app = SocketIO(app, async_mode='eventlet', cors_allowed_origins='*')  # Inicialize o SocketIO aqui

CORS(app, resources={r"/*": {"origins": "*"}})

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Scraper"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['DEBUG'] = True
app.config["OPENAPI_URL_PREFIX"] = "/"

api = Api(app)
core.init_socketio(socketio_app)  # Passar o objeto SocketIO para o core

# Registre o blueprint no app
api.register_blueprint(core.main_bp)  

# Inicie o servidor usando `socketio.run`
if __name__ == "__main__":
    socketio_app.run(app, host="0.0.0.0", port=5000)
