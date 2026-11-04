
import os
import uuid
from pathlib import Path

from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from openai import OpenAI

# --------------------------------
# 1. LOAD ENVIRONMENT VARIABLES
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE, override=True)

app = Flask(__name__)

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

print("--------------------------------")
print("SMARTCHAT AI STARTING...")
print("ENV FILE EXISTS:", ENV_FILE.exists())
print("GROQ API KEY FOUND:", bool(API_KEY))
print("MODEL:", MODEL)
print("--------------------------------")

# --------------------------------
# 2. GROQ API CONFIGURATION
# --------------------------------

client = None

if API_KEY:
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.groq.com/openai/v1",
        timeout=25
    )

# --------------------------------
# 3. CONVERSATION STORAGE
# --------------------------------

conversations = {}

MAX_HISTORY = 12

# --------------------------------
# 4. SYSTEM PROMPT
# --------------------------------

SYSTEM_PROMPT = """
You are SmartChat, a friendly and intelligent AI study assistant.

Your responsibilities:
1. Explain concepts in simple language.
2. Give examples whenever necessary.
3. Help students with programming and academics.
4. Answer questions clearly and accurately.
5. Maintain context from previous messages.
6. Be polite, helpful and concise.

Remember important details shared by the user
during the current conversation.
"""

# --------------------------------
# 5. HOME PAGE
# --------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------
# 6. CHAT API
# --------------------------------

@app.route("/chat", methods=["POST"])
def chat():

    if client is None:
        return jsonify({
            "error": "Groq API key is not configured. Check your .env file."
        }), 503

    data = request.get_json(silent=True) or {}

    message = str(data.get("message", "")).strip()

    conversation_id = (
        data.get("conversation_id") or str(uuid.uuid4())
    )

    if not message:
        return jsonify({
            "error": "Message cannot be empty."
        }), 400

    if len(message) > 4000:
        return jsonify({
            "error": "Message is too long. Maximum 4000 characters."
        }), 400

    # Get previous conversation history
    history = conversations.get(conversation_id, [])

    # Context window management
    history = history[-MAX_HISTORY:]

    # Add current user message
    messages = history + [
        {
            "role": "user",
            "content": message
        }
    ]

    try:

        # Send request to Groq
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                *messages
            ]
        )

        reply = response.choices[0].message.content

        if not reply:
            return jsonify({
                "error": "Empty response received from AI."
            }), 502

        # Save conversation history
        conversations[conversation_id] = (
            messages + [
                {
                    "role": "assistant",
                    "content": reply
                }
            ]
        )[-MAX_HISTORY:]

        return jsonify({
            "conversation_id": conversation_id,
            "reply": reply
        }), 200

    except Exception as e:

        app.logger.exception("Groq API error")

        error_message = "Unable to connect to AI. Please try again."

        if getattr(e, "status_code", None) == 429:
            error_message = "API rate limit reached. Please try again later."

        elif getattr(e, "status_code", None) in (401, 403):
            error_message = "Invalid or unauthorized Groq API key. Check your API key."

        elif getattr(e, "status_code", None) == 400:
            error_message = "Invalid API request or unsupported model."

        return jsonify({
            "error": error_message
        }), 500


# --------------------------------
# 7. RESET CONVERSATION
# --------------------------------

@app.route("/reset", methods=["POST"])
def reset():

    data = request.get_json(silent=True) or {}

    conversation_id = data.get("conversation_id")

    if conversation_id:
        conversations.pop(conversation_id, None)

    return jsonify({
        "message": "Conversation reset successfully."
    }), 200


# --------------------------------
# 8. HEALTH CHECK
# --------------------------------

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "running",
        "api_configured": client is not None,
        "model": MODEL
    })


# --------------------------------
# 9. RUN APPLICATION
# --------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
