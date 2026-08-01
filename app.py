# NEXORA V2 — Python AI Backend
# Save this as app.py
#
# Install:
#   pip install flask openai
#
# Set your API key as an environment variable.
# NEVER put the API key inside index.html.

from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
import os

app = Flask(__name__, static_folder=".")

API_KEY = os.environ.get("OPENAI_API_KEY")

if not API_KEY:
    print("WARNING: OPENAI_API_KEY is not set.")

client = OpenAI(api_key=API_KEY) if API_KEY else None


@app.get("/api/health")
def health():
    return jsonify({
        "ok": bool(client),
        "message": "NEXORA backend is online."
    })


@app.post("/api/ai")
def ai():
    if client is None:
        return jsonify({
            "error": "OPENAI_API_KEY is not configured on the server."
        }), 500

    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Message is required."}), 400

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            instructions=(
                "You are NEXORA, a helpful, intelligent and friendly AI assistant. "
                "Answer clearly and naturally. If the user speaks Bangla, answer in Bangla."
            ),
            input=message
        )

        return jsonify({
            "reply": response.output_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.get("/")
def home():
    return send_from_directory(".", "NEXORA_V2_REAL_AI_READY.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

