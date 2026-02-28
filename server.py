from flask import Flask, request, jsonify
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

# ==============================
# ENVIRONMENT VARIABLES
# ==============================

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

print("=== SERVER STARTED ===")
print("DISCORD_WEBHOOK_URL:", DISCORD_WEBHOOK_URL)
print("======================")

# ==============================
# ROOT
# ==============================

@app.route("/")
def home():
    return "Central Log Server Running"

# ==============================
# LOG ENDPOINT
# ==============================

@app.route("/log", methods=["POST"])
def receive_log():
    try:
        data = request.json

        print("\n--- LOG RECEIVED ---")
        print("Incoming Data:", data)
        print("Webhook ENV:", DISCORD_WEBHOOK_URL)

        if not data:
            print("No data received.")
            return jsonify({"status": "no data"}), 400

        # Server timestamp ekle
        data["server_received_time"] = datetime.now().isoformat()

        # Discord gönderim
        if DISCORD_WEBHOOK_URL:

            full_json_text = json.dumps(data, indent=4)

            # Discord 2000 karakter limit
            if len(full_json_text) > 1900:
                full_json_text = full_json_text[:1900] + "\n...TRUNCATED..."

            payload = {
                "content": f"```json\n{full_json_text}\n```"
            }

            try:
                resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)

                print("DISCORD STATUS:", resp.status_code)
                print("DISCORD RESPONSE:", resp.text)

            except Exception as discord_error:
                print("DISCORD SEND ERROR:", discord_error)

        else:
            print("WEBHOOK ENV IS EMPTY!")

        print("--- LOG PROCESSED ---\n")

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("SERVER ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ==============================
# RUN (Render compatible)
# ==============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
