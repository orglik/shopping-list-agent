# server.py — Shopping List Agent
# This server receives a voice transcription from Tasker,
# sends it to Claude, and returns a clean shopping list.

from flask import Flask, request, jsonify
import anthropic
import os

app = Flask(__name__)

# -------------------------------------------------------
# Claude client — reads your API key from the environment
# -------------------------------------------------------
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


@app.route("/shopping-list", methods=["POST"])
def shopping_list():
    """
    Expects a JSON body like:
        { "text": "I need milk, two eggs and maybe some bread" }
    Returns:
        { "list": "🛒 Shopping List:\n• Milk\n• Eggs x2\n• Bread" }
    """

    # 1. Get the transcribed text from Tasker
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    user_text = data["text"]

    # 2. Ask Claude to extract a clean shopping list
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    "Extract a clean shopping list from the following voice transcription. "
                    "Format it as a WhatsApp-friendly message with bullet points (•). "
                    "Include quantities if mentioned. "
                    "Start with the emoji 🛒 and the title 'Shopping List:'.\n\n"
                    f"Transcription: {user_text}"
                ),
            }
        ],
    )

    # 3. Pull the text out of Claude's response
    result = message.content[0].text

    # 4. Send it back to Tasker
    return jsonify({"list": result})


# -------------------------------------------------------
# Health-check endpoint — useful to confirm the server is up
# -------------------------------------------------------
@app.route("/", methods=["GET"])
def health():
    return "Shopping List Agent is running! ✅"


if __name__ == "__main__":
    # Railway/Render set the PORT environment variable automatically
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
