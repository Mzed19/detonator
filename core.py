from flask import request, jsonify
from flask_smorest import Blueprint

main_bp = Blueprint("test", __name__, description="Initial test")

informationsOfTarget = {}

@main_bp.route('/save', methods=['POST'])
def test():
    global informationsOfTarget
    informationsOfTarget = request.get_json()
    return jsonify(informationsOfTarget)

@main_bp.route('/test2', methods=['GET'])
def test2():
    return jsonify(informationsOfTarget)