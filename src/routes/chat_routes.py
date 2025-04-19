from flask import Blueprint, request, jsonify

bp = Blueprint("chat_routes", __name__)

@bp.route("/respond", methods=["POST"])
def chat_respond():
    data = request.json
    message = data.get("message")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    # Placeholder Gemini AI logic
    response = {
        "response": f"Gemini says: '{message}' has been processed!"
    }
    return jsonify(response)
