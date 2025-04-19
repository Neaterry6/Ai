from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup

bp = Blueprint("music_routes", __name__)

GENIUS_API_KEY = "YOUR_GENIUS_API_KEY_HERE"  # Replace with your Genius API key

@bp.route("/mood", methods=["POST"])
def get_mood_songs():
    data = request.json
    mood = data.get("mood", "happy")

    songs = {
        "happy": ["Happy by Pharrell Williams", "Can't Stop the Feeling by Justin Timberlake"],
        "sad": ["Someone Like You by Adele", "The Scientist by Coldplay"],
    }
    return jsonify({"songs": songs.get(mood, ["No suggestions available"])})

@bp.route("/lyrics", methods=["POST"])
def get_lyrics():
    data = request.json
    song = data.get("song")
    artist = data.get("artist", "")

    if not song:
        return jsonify({"error": "Song name is required"}), 400

    try:
        url = f"https://api.genius.com/search?q={song} {artist}"
        headers = {"Authorization": f"Bearer {GENIUS_API_KEY}"}
        response = requests.get(url, headers=headers).json()

        hits = response.get("response", {}).get("hits", [])
        if not hits:
            return jsonify({"error": "Lyrics not found"}), 404

        song_url = hits[0]["result"]["url"]
        page = requests.get(song_url)
        soup = BeautifulSoup(page.text, "html.parser")
        lyrics = soup.find("div", class_="lyrics").get_text(strip=True)

        return jsonify({"lyrics": lyrics})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
