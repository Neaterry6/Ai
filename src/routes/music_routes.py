import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

bp = Blueprint("music_routes", __name__)

# Genius API Access Token from .env
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

# Mood-Based Songs
@bp.route("/mood", methods=["POST"])
def get_mood_songs():
    data = request.json
    mood = data.get("mood", "happy")  # Default mood is 'happy'

    # Suggestions based on mood
    songs = {
        "happy": ["Happy by Pharrell Williams", "Can't Stop the Feeling by Justin Timberlake"],
        "sad": ["Someone Like You by Adele", "The Scientist by Coldplay"],
        "energetic": ["Eye of the Tiger by Survivor", "Stronger by Kanye West"],
        "relaxed": ["Thinking Out Loud by Ed Sheeran", "Gravity by John Mayer"],
    }

    # If the mood doesn't match predefined ones, return a default suggestion
    return jsonify({"songs": songs.get(mood.lower(), ["Mood not recognized, try again!"])})

# Lyrics Retrieval
@bp.route("/lyrics", methods=["POST"])
def get_lyrics():
    data = request.json
    song = data.get("song")
    artist = data.get("artist", "")

    if not song:
        return jsonify({"error": "Song name is required"}), 400

    try:
        # Search for the song on Genius
        url = f"https://api.genius.com/search?q={song} {artist}"
        headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
        response = requests.get(url, headers=headers).json()

        # Extract song details
        hits = response.get("response", {}).get("hits", [])
        if not hits:
            return jsonify({"error": "Lyrics not found for the requested song"}), 404

        # Get the URL of the first result
        song_url = hits[0]["result"]["url"]

        return jsonify({"song_url": song_url, "message": "Lyrics found, visit the link to view them!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
