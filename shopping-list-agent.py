# server.py — Shopping List Agent
# This server receives a voice transcription from Tasker,
# sends it to Claude, and returns a clean shopping list.

from flask import Flask, request, jsonify
import anthropic
import os
import traceback

app = Flask(__name__)

# -------------------------------------------------------
# Claude client — reads your API key from the environment
# -------------------------------------------------------
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


@app.route("/shopping-list", methods=["POST"])
def shopping_list():
    try:
        # 1. Get the transcribed text from Tasker
        # Support both JSON body and raw text
        if request.is_json:
            data = request.get_json(force=True)
            user_text = data.get("text", "")
        else:
            user_text = request.data.decode("utf-8")

        if not user_text:
            return jsonify({"error": "Missing text"}), 400

        print(f"Received text: {user_text}")

        # 2. Ask Claude to extract a clean shopping list
        message = client.messages.create(
            model="claude-sonnet-4-5",
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
        print(f"Claude response: {result}")

        # 4. Send it back to Tasker
        return result, 200, {'Content-Type': 'text/plain; charset=utf-8'}

    except Exception as e:
        print(f"ERROR: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500


@app.route("/joke", methods=["POST"])
def joke():
    try:
        # 1. Get the joke topic 
        # Support both JSON body and raw text
        if request.is_json:
            data = request.get_json(force=True)
            joke_topic_text = data.get("text", "")
        else:
            joke_topic_text = request.data.decode("utf-8")

        if not joke_topic_text:
            return jsonify({"error": "Missing joke topic"}), 400

        print(f"Received joke topic: {joke_topic_text}")

        # 2. Ask Claude to generate a joke
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Generate a joke about the following topic: "
                        "add emojis to make it more fun!"
                        f"{joke_topic_text}" 
                    ),
                }
            ],
        )

        # 3. Pull the text out of Claude's response
        result = message.content[0].text
        print(f"Claude response: {result}")

        # 4. Send it back to Tasker
        return result, 200, {'Content-Type': 'text/plain; charset=utf-8'}

    except Exception as e:
        print(f"ERROR: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route("/joke-kids", methods=["POST"])
def joke_kids():
    try:
        # 1. Get the joke topic 
        # Support both JSON body and raw text
        if request.is_json:
            data = request.get_json(force=True)
            joke_topic_text = data.get("text", "")
        else:
            joke_topic_text = request.data.decode("utf-8")

        if not joke_topic_text:
            return jsonify({"error": "Missing joke topic"}), 400

        print(f"Received joke topic: {joke_topic_text}")

        # 2. Ask Claude to generate a joke
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system="You are a kids comedian . Your job is to create jokes that make kids laugh. Use simple words a 6 year old understands. Always use a setup and punchline structure. Always be polite. Never make any racial or gender or sexual jokes. Format: one sentence.",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"{joke_topic_text}" 
                    ),
                }
            ],
        )

        # 3. Pull the text out of Claude's response
        result = message.content[0].text
        print(f"Claude response: {result}")

        # 4. Send it back to Tasker
        return result, 200, {'Content-Type': 'text/plain; charset=utf-8'}

    except Exception as e:
        print(f"ERROR: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500


@app.route("/joke-dev", methods=["POST"])
def joke_dev():
    try:
        # 1. Get the joke topic 
        # Support both JSON body and raw text
        if request.is_json:
            data = request.get_json(force=True)
            joke_topic_text = data.get("text", "")
        else:
            joke_topic_text = request.data.decode("utf-8")

        if not joke_topic_text:
            return jsonify({"error": "Missing joke topic"}), 400

        print(f"Received joke topic: {joke_topic_text}")

        # 2. Ask Claude to generate a joke
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system="You are comedian who is also expert developer. Your job is to create jokes that make developers laugh. the joke should relates to technology and code developing.Reference real things developers experience: bugs, deadlines, Stack Overflow, coffee, Git. Never make any racial or gender or sexual jokes. Format: any length under 10 sentences.",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"{joke_topic_text}" 
                    ),
                }
            ],
        )
        # 3. Pull the text out of Claude's response
        result = message.content[0].text
        print(f"Claude response: {result}")

        # 4. Send it back to Tasker
        return result, 200, {'Content-Type': 'text/plain; charset=utf-8'}

    except Exception as e:
        print(f"ERROR: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route("/joke-fashion", methods=["POST"])
def joke_fashion():
    try:
        # 1. Get the joke topic 
        # Support both JSON body and raw text
        if request.is_json:
            data = request.get_json(force=True)
            joke_topic_text = data.get("text", "")
        else:
            joke_topic_text = request.data.decode("utf-8")

        if not joke_topic_text:
            return jsonify({"error": "Missing joke topic"}), 400

        print(f"Received joke topic: {joke_topic_text}")

        # 2. Ask Claude to generate a joke
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system= "You are comedian who is also an fashion leader/influencer. Your job is to create jokes that make fashion enthusiastic laugh. the joke should relates to lead fashion brand and designers and celebrities. Reference real events, designers, and moments — like the Met Gala, Balenciaga, or Fashion Week. Never make any racial or gender or sexual jokes. Format: any length under 10 sentences.",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"{joke_topic_text}" 
                    ),
                }
            ],
        )

        # 3. Pull the text out of Claude's response
        result = message.content[0].text
        print(f"Claude response: {result}")

        # 4. Send it back to Tasker
        return result, 200, {'Content-Type': 'text/plain; charset=utf-8'}

    except Exception as e:
        print(f"ERROR: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500


# -------------------------------------------------------
# Health-check endpoint
# -------------------------------------------------------
@app.route("/", methods=["GET"])
def health():
    return "Shopping List Agent is running! ✅"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


