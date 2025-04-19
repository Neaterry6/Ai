from flask import Blueprint, request, jsonify
import requests

bp = Blueprint("image_routes", __name__)

UNSPLASH_API_KEY = "R6_-bAjOS06I89QrCoZ4zgVLEoLjjA3MdltvKuf2uD0"

@bp.route("/send", methods=["POST"])
def send_image():
    data = request.json
    query = data.get("query", "nature")
    count = data.get("count", 1)

    url = f"https://api.unsplash.com/search/photos?query={query}&per_page={count}&client_id={UNSPLASH_API_KEY}"
    response = requests.get(url).json()

    images = [{"url": img["urls"]["full"], "author": img["user"]["name"]} for img in response["results"]]
    return jsonify({"images": images})

@bp.route("/analyze", methods=["POST"])
def analyze_image():
    data = request.json
    image_url = data.get("image_url")

    if not image_url:
        return jsonify({"error": "Image URL is required"}), 400

    detected_objects = ["cat", "dog", "tree"]  # Placeholder logic
    return jsonify({"detected_objects": detected_objects})
