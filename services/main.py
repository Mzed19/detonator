from flask import request, jsonify
from flask_smorest import Blueprint

main_bp = Blueprint("test", __name__, description="Initial test")

@main_bp.route('/test', methods=['GET'])
def extract_text():
    return jsonify('Working!')
