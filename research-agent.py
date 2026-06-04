# research-agent.py — weekly AI research briefing

from flask import Flask, request, jsonify
import anthropic
import os
import traceback
import requests

app = Flask(__name__)

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

@app.route("/research-briefing", methods=["POST"])
def research_briefing():
    try:
        # 1. Call Claude with web search tool
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=3500,
            system="""You are a weekly research agent monitoring the Israeli AI job market.

Every run, you will:
1. Search the web for recent developments across 4 topics (see below)
2. Synthesize findings into a single Telegram message
3. Return ONLY the formatted output below — nothing else. No search summaries, no "Based on search results", no thinking out loud. Your entire response must be the final Telegram message and nothing else.
4. Do not include any text before the briefing. Start directly with the header line.

SEARCH TOPICS
Run one focused search per topic. Always include the current date/year in every query.

1. Israeli tech layoffs — recent company names, headcount numbers, stated reasons
2. AI skills and salaries in Israel — in-demand skills, salary data, hiring trends
3. Junior vs senior employment dynamics — who is being hired or cut, AI adoption rates
4. Top AI/tech labor market news this week in Israel — single biggest story

OUTPUT FORMAT
Return exactly this structure, plain text, no markdown:

🇮🇱 AI & the Israeli Job Market | {DD Month YYYY}

Layoffs: {company names, numbers, % cuts}. Drivers: {2-3 causes}.

Must-have skills: {3-5 skills}. AI specialists earn a {X}% salary premium.

Juniors vs Seniors: Juniors — {1 sentence}. Seniors — {1 sentence}.

This week's top story: {1-2 sentences. Name the company or event.}

RULES
- Only include figures with a named source. If no sourced number, omit it.
- If no new layoffs this week, use most recent data and add (prior week).
- Total message length: under 1,400 characters.
- Before writing the final output, summarize each search result in 2-3 sentences maximum. Keep search summaries brief to preserve tokens for the final output.
- No closing line or commentary after the message.
- CRITICAL: Your response must start with the 🇮🇱 emoji. If it does not start with 🇮🇱, you have failed the task.""",
            tools=[{"type": "web_search_20260209", "name": "web_search"}],
            messages=[{"role": "user", "content": "Run the weekly Israeli AI job market research briefing for today."}]
        )
        # DEBUG
        print(f"Content blocks: {[block.type for block in message.content]}")
        
        # 2. Extract text from Claude's response
        result = ""
        for block in message.content:
            if block.type == "text":
                result = block.text
                break
        result = result[:4000]

        # 3. Send via Telegram
        telegram_token = os.environ["TELEGRAM_BOT_TOKEN"]
        telegram_chat_id = os.environ["TELEGRAM_CHAT_ID"]
        telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"

        requests.post(telegram_url, json={
            "chat_id": telegram_chat_id,
            "text": result
        })

        return "", 204

    except Exception as e:
        print(f"ERROR: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def health():
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)