from flask import Flask
from flask_smorest import Api
from core import main_bp
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Scraper"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"

api = Api(app)
api.register_blueprint(main_bp)