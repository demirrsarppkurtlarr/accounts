from flask import Flask, request, jsonify
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

# Environment variable olarak Render'da tanımlayacaksın
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.route("/")
def home():
    return "Central Log Server Running"

@app.route("/log", methods=["POST"])
def receive_log():
    try:
        data = request.json

        if not data:
            return jsonify({"status": "no data"}), 400

        # Zaman ekle (sunucu zamanı)
        data["server_received_time"] = datetime.now().isoformat()

        # Eğer webhook varsa Discord'a gönder
        if DISCORD_WEBHOOK_URL:
            full_json_text = json.dumps(data, indent=4)

            # Discord 2000 karakter limit
            if len(full_json_text) > 1900:
                full_json_text = full_json_text[:1900] + "\n...TRUNCATED..."

            payload = {
                "content": f"```json\n{full_json_text}\n```"
            }

            requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
