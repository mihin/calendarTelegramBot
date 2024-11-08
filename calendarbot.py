#!/usr/bin/env python
# pylint: disable=unused-argument

import logging
import environs
import openai
from openai import OpenAI
import datetime
import json
from datetime import datetime, timedelta
from calendarutils import create_evnt_from_json
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

env = environs.Env()
env.read_env()
token = env.str("BOT_TOKEN")
openai_token = env.str("OPENAI_API_KEY")
chat_model = "gpt-4o-mini"


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


def chat(messages):
    response = openai.chat.completions.create(
        model=chat_model,
        messages=messages,
        max_tokens=200, 
        temperature=0.8,
        top_p=0.5
    )
    jdict = json.loads(response.choices[0].message.content)
    return create_evnt_from_json(jdict)


def reply(message):

    system_prompt = """
you are a bot. you will be given an event information. summarize the event inforamtion in a JSON object. respond only with the JSON of the following format:
{\"summary\":\"EVENT_TITLE\", \"description\": \"EVENT_DESCRIPTION\", \"start\": {\"dateTime\": \"EVENT_START\"}, \"end\": {\"dateTime\": \"EVENT_END\"}}
Replace EVENT_TITLE with the short event title, replace EVENT_DESCRIPTION with the event description (1-2 sentences, mention event location there), replace EVENT_START with a datetime string (formatted according to RFC3339) or date (in the format "yyyy-mm-dd") if time is not specified; use current 2024 year if not specified. Replace EVENT_END with the start date plus 1 hour. If the address is provided, add address string value to the JSON with the “location" key. You the same language as in provided event information.
"""

    prompt = f"""
Event information:
{message} 
"""

    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]

    return chat(messages)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    # await update.message.reply_text(update.message.text)
    if update.message and update.message.forward_origin:
        forwarded_text = update.message.text
        response = f"It was forwarded message: {forwarded_text}" # + f"{update.message.forward_origin}"
    #print(update.message)
    else:
        response = f"direct message: {update.message.text}"  # reply(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def echoFwd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    # await update.message.reply_text(update.message.text)
    # print(update.message)
    #response = reply(update.message.text)
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    print('FWD message txt: ' + str(update.message.text))
    print('FWD message: ' + str(update.message.forward_origin))
    await update.message.reply_text(update.message.forward_origin)


def main() -> None:
    # Set up OpenAI API key
    openai.api_key = openai_token
  #  openai.base_url = "https://api.proxyapi.ru/openai/v1"

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.FORWARDED, echoFwd))
    

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
