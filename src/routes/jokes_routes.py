import pyjokes
from flask import Blueprint, jsonify

bp = Blueprint("jokes_routes", __name__)

@bp.route("/", methods=["GET"])
def get_joke():
    joke = pyjokes.get_joke()
    return jsonify({"joke": joke})
