# Shopping List Agent (and friends)

A collection of small Flask + Claude API agents built during a learning program, each automating a different everyday task via Telegram or Tasker.

## Agents

**research-agent.py** — Weekly Israeli AI job market briefing. Triggered by cron, runs Claude with web search across layoffs, in-demand skills, junior vs. senior hiring trends, and the week's top story, then sends a formatted summary to Telegram.

**weather-agent.py** — Daily weather and news briefings. One endpoint fetches Tel Aviv weather from OpenWeatherMap and has Claude turn it into a friendly morning message; another pulls top headlines from the Jerusalem Post RSS feed and summarizes them — both delivered via Telegram.

**shopping-list-agent.py** — Voice-to-shopping-list assistant via Tasker. Takes a voice transcription, has Claude extract a clean bulleted shopping list, and also includes a few joke-generator endpoints (general, kids, dev, fashion) for fun.

## Tech Stack

- Python (Flask)
- Anthropic Claude API (with web search for the research agent)
- Telegram Bot API
- Tasker (Android automation, for shopping list input)
- OpenWeatherMap API + RSS (feedparser)
- Hosted on Render, scheduled via cron-job.org + UptimeRobot

## Live

- Research briefing: delivered weekly to Telegram, Sundays 8:00 AM IL time
- Weather briefing: delivered daily to Telegram
- News briefing: delivered daily to Telegram
