import random
from flask import Blueprint, request, jsonify

bp = Blueprint("weather_routes", __name__)

@bp.route("/", methods=["POST"])
def get_weather():
    simulated_weather = {
        "New York": {"temperature": random.randint(15, 25), "description": "Partly cloudy"},
        "London": {"temperature": random.randint(5, 15), "description": "Rainy"},
        "Tokyo": {"temperature": random.randint(10, 20), "description": "Sunny"},
    }

    city = request.json.get("city", "New York")
    weather = simulated_weather.get(city, {"temperature": 22, "description": "Sunny"})

    return jsonify({
        "location": city,
        "temperature": weather["temperature"],
        "description": weather["description"]
    })
