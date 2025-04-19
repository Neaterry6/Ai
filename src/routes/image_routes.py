import cv2
import numpy as np
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

bp = Blueprint("image_routes", __name__)

# Unsplash API Key from .env file
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")  # Ensure this key exists in your .env file

# Image Sending Route
@bp.route("/send", methods=["POST"])
def send_image():
    data = request.json
    query = data.get("query", "nature")  # Default query is 'nature'
    count = data.get("count", 1)  # Default count is 1 image

    try:
        # Unsplash API request
        url = f"https://api.unsplash.com/search/photos?query={query}&per_page={count}&client_id={UNSPLASH_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()

        # Process results
        images = [
            {"url": img["urls"]["full"], "author": img["user"]["name"]}
            for img in response.json().get("results", [])
        ]
        if not images:
            return jsonify({"error": "No images found for the given query"}), 404

        return jsonify({"images": images})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Image Analysis Route
@bp.route("/analyze", methods=["POST"])
def analyze_image():
    data = request.json
    image_url = data.get("image_url")

    if not image_url:
        return jsonify({"error": "Image URL is required"}), 400

    try:
        # Fetch the image from the URL
        resp = requests.get(image_url, stream=True)
        resp.raw.decode_content = True
        np_image = np.asarray(bytearray(resp.raw.read()), dtype=np.uint8)
        img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

        # Convert to grayscale and detect edges
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # Count the number of edge pixels detected
        edge_count = np.count_nonzero(edges)

        # Detect contours in the image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_count = len(contours)

        return jsonify({
            "edges_detected": edge_count,
            "contours_detected": contour_count,
            "message": "Image analyzed successfully!"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
