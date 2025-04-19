import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

bp = Blueprint("chat_routes", __name__)

# Fetch Gemini API Key from .env file
GEMINI_API_KEY = os.getenv("")  # Make sure to set this in your .env file

@bp.route("/respond", methods=["POST"])
def chat_respond():
    data = request.json
    message = data.get("message")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    try:
        # Send the message to Gemini AI
        url = "https://api.gemini.ai/v1/chat/respond"  # Replace with the correct endpoint if needed
        headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
        payload = {"message": message}
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            reply = response.json().get("response", "No response from Gemini AI.")
            return jsonify({"response": reply})
        else:
            return jsonify({"error": f"Gemini AI error: {response.status_code}"}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
