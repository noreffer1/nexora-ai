# NEXORA V2 — Python AI Backend
# Flask + OpenAI + CORS
#
# requirements.txt:
# flask
# flask-cors
# openai
# gunicorn
#
# IMPORTANT:
# Never put your OpenAI API key in this file or in Blogger HTML.
# Add it to Render Environment Variables as:
# OPENAI_API_KEY = your_api_key


from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import os


# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__, static_folder=".")

# Allow requests from Blogger / frontend
CORS(app)


# =========================================================
# OPENAI CONFIGURATION
# =========================================================

API_KEY = os.environ.get("OPENAI_API_KEY")

if not API_KEY:
    print("WARNING: OPENAI_API_KEY is not set.")

client = OpenAI(api_key=API_KEY) if API_KEY else None


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/api/health")
def health():
    return jsonify({
        "ok": bool(client),
        "message": "NEXORA backend is online."
    })


# =========================================================
# AI CHAT API
# =========================================================

@app.post("/api/ai")
def ai():

    # Check API key / OpenAI client
    if client is None:
        return jsonify({
            "error": "OPENAI_API_KEY is not configured on the server."
        }), 500

    # Read JSON request
    data = request.get_json(silent=True) or {}

    message = str(data.get("message", "")).strip()

    # Check empty message
    if not message:
        return jsonify({
            "error": "Message is required."
        }), 400

    try:

        # Send request to OpenAI
        response = client.responses.create(
            model="gpt-5-mini",

            instructions=(
                "You are NEXORA, a helpful, intelligent and friendly AI assistant. "
                "Answer clearly, naturally and accurately. "
                "If the user speaks Bangla, answer in Bangla. "
                "If the user speaks English, answer in English. "
                "Do not unnecessarily mention that you are an AI."
            ),

            input=message
        )

        # Return AI response
        return jsonify({
            "reply": response.output_text
        })

    except Exception as e:

        print("OpenAI API Error:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# HOME / FRONTEND
# =========================================================

@app.get("/")
def home():
    return send_from_directory(
        app.static_folder,
        "NEXORA_V2_REAL_AI_READY.html"
    )


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
