# calendarTelegramBot

Telegram bot with OpenAI and Google Calendar integration.

## Description

Send an event description to the bot, a new event will appear in your google calendar. Description, time and location will be taken from the text by the OpenAI.

## How to start

1. Create a project in [Google Console](https://console.cloud.google.com/workspace-api?project=calendar-api-440912)
2. Create a OAuth 2.0 Client, select Web Client ([Follow this link for the entire Oauth setup procedure](https://support.google.com/cloud/answer/6158849?hl=en))
3. Put your redirect URLs
4. Download Client secrets, rename the file to credentials.json and put to the project root
5. In Google Console go to Enabled APIs & Servises
	- Press + ENABLE APIS & SERVICES
	- Search for Calendar
	- Add Calendar Scopes (https://www.googleapis.com/auth/calendar.app.created,https://www.googleapis.com/auth/calendar.events.owned)

Create `.env` file in the project root:
```
BOT_TOKEN="<put yout bot token from @BotFather>"
OPENAI_API_KEY="<put your OpenAI token>"
```

Launch with `python3 calendarbot.py`