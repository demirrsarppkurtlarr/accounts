from flask import Flask, request, jsonify
import requests
import os
import json
from datetime import datetime
import traceback

app = Flask(__name__)

# ================================
# CONFIG
# ================================

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
LOG_FILE = "server_internal_log.json"

print("=== SERVER STARTED ===")
print("DISCORD_WEBHOOK_URL:", DISCORD_WEBHOOK_URL)
print("======================")

# ================================
# INTERNAL FILE LOGGER
# ================================

def write_internal_log(entry):
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)

        logs.append(entry)

        temp_file = LOG_FILE + ".tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4)

        os.replace(temp_file, LOG_FILE)

    except Exception as e:
        print("Internal log write error:", str(e))


# ================================
# DISCORD SENDER
# ================================

def send_to_discord(data):
    if not DISCORD_WEBHOOK_URL:
        print("Webhook not set.")
        return

    try:
        full_json_text = json.dumps(data, indent=4)

        # Discord limit 2000 char
        chunks = []
        while len(full_json_text) > 1900:
            chunks.append(full_json_text[:1900])
            full_json_text = full_json_text[1900:]
        chunks.append(full_json_text)

        for index, chunk in enumerate(chunks):
            payload = {
                "content": f"```json\n{chunk}\n```"
            }

            response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)

            print("Discord status:", response.status_code)
            print("Discord response:", response.text)

            # Rate limit kontrol
            if response.status_code == 429:
                retry_after = response.json().get("retry_after", 1)
                print("Rate limited. Waiting:", retry_after)
            
            # Hata kodları
            if response.status_code not in [200, 204]:
                write_internal_log({
                    "type": "discord_error",
                    "status_code": response.status_code,
                    "response": response.text,
                    "time": datetime.now().isoformat()
                })

    except Exception as e:
        print("Discord send error:", str(e))
        write_internal_log({
            "type": "discord_exception",
            "error": str(e),
            "trace": traceback.format_exc(),
            "time": datetime.now().isoformat()
        })


# ================================
# ROUTES
# ================================

@app.route("/")
def home():
    return "Central Log Server Running - Advanced Mode"

@app.route("/log", methods=["POST"])
def receive_log():
    try:
        data = request.json

        if not data:
            return jsonify({"status": "no data"}), 400

        # Server time ekle
        data["server_received_time"] = datetime.now().isoformat()

        # Internal log
        write_internal_log({
            "type": "incoming_log",
            "data": data,
            "time": datetime.now().isoformat()
        })

        # Discord'a gönder
        send_to_discord(data)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        error_data = {
            "type": "server_error",
            "error": str(e),
            "trace": traceback.format_exc(),
            "time": datetime.now().isoformat()
        }

        print("SERVER ERROR:", str(e))
        write_internal_log(error_data)

        return jsonify({"error": str(e)}), 500


# ================================
# START
# ================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
