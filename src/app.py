from flask import Flask
from routes import chat_routes, image_routes, weather_routes, jokes_routes, music_routes

app = Flask(__name__)

# Registering routes for each feature
app.register_blueprint(chat_routes.bp, url_prefix="/chat")
app.register_blueprint(image_routes.bp, url_prefix="/image")
app.register_blueprint(weather_routes.bp, url_prefix="/weather")
app.register_blueprint(jokes_routes.bp, url_prefix="/jokes")
app.register_blueprint(music_routes.bp, url_prefix="/music")

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
