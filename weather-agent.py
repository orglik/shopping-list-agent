# weather-agent.py — Daily Weather Briefing Agent

from unittest import result

from flask import Flask, request, jsonify
import anthropic
import os
import traceback
import requests
from twilio.rest import Client

app = Flask(__name__)

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

@app.route("/weather-briefing", methods=["POST"])
def weather_briefing():
    try:
        # 1. Call OpenWeatherMap API
        api_key = os.environ["OPENWEATHER_API_KEY"]
        city = "Tel Aviv"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        weather_response = requests.get(url)
        weather_data = weather_response.json()

        # 2. Pass data to Claude
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system="You are a weather helper. Your job is to receive valid information about the daily weather. Start with Good morning Or! Describe the weather today in Tel Aviv with the precise temperature in celsius. Add weather description (sunny/rainy/windy etc.) and recommend what to wear (short sleeve/jacket/coat etc.). Format: up to 3 sentences.Use WhatsApp-friendly formatting with emojis. You will receive raw JSON data from a weather API. Extract the relevant fields and present them in a friendly, human-readable format.",
            messages=[
                {
                    "role": "user",
                    "content": f"{weather_data}"
                }
            ],
        )

        # 3. Extract text from Claude's response
        result = message.content[0].text
        print(f"Claude response: {result}")

        
        # 4. Send via Telegram
telegram_token = os.environ["TELEGRAM_BOT_TOKEN"]
telegram_chat_id = os.environ["TELEGRAM_CHAT_ID"]
telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"

requests.post(telegram_url, json={
    "chat_id": telegram_chat_id,
    "text": result
})

return "Message sent", 200
    
    except Exception as e:
    print(f"ERROR: {traceback.format_exc()}")
return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def health():
    return "Weather Agent is running! ✅"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)