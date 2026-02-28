from flask import Flask, request, jsonify
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

print("=== SERVER STARTED ===")
print("DISCORD_WEBHOOK_URL:", DISCORD_WEBHOOK_URL)
print("======================")

# ---------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------

@app.route("/")
def home():
    return "Central Log Server Running"

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "webhook_set": bool(DISCORD_WEBHOOK_URL)
    })

# ---------------------------------------------------
# TEST WEBHOOK
# ---------------------------------------------------

@app.route("/test-webhook")
def test_webhook():
    if not DISCORD_WEBHOOK_URL:
        return "Webhook not set", 500

    try:
        r = requests.post(DISCORD_WEBHOOK_URL, json={
            "content": "🔥 WEBHOOK TEST SUCCESS 🔥"
        }, timeout=10)

        return f"Discord response: {r.status_code} - {r.text}"

    except Exception as e:
        return f"Error: {str(e)}", 500

# ---------------------------------------------------
# LOG RECEIVER
# ---------------------------------------------------

@app.route("/log", methods=["POST"])
def receive_log():
    try:
        data = request.json

        if not data:
            return jsonify({"status": "no data"}), 400

        data["server_received_time"] = datetime.now().isoformat()

        if DISCORD_WEBHOOK_URL:

            full_json_text = json.dumps(data, indent=4)

            if len(full_json_text) > 1900:
                full_json_text = full_json_text[:1900] + "\n...TRUNCATED..."

            payload = {
                "content": f"```json\n{full_json_text}\n```"
            }

            try:
                response = requests.post(
                    DISCORD_WEBHOOK_URL,
                    json=payload,
                    timeout=10
                )

                print("Discord Status:", response.status_code)
                print("Discord Response:", response.text)

            except Exception as e:
                print("Discord ERROR:", str(e))

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("SERVER ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
