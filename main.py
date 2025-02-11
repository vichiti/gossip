from fastapi import FastAPI, Request
from pyrogram import Client
from dotenv import load_dotenv
import os
import asyncio
import uvicorn

# Load environment variables from .env file
load_dotenv()

# Get the credentials from .env
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
# WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Add webhook URL to .env

# Initialize FastAPI app
app = FastAPI()

# Initialize the Pyrogram Client (Bot)
bot = Client("my_bot", bot_token=BOT_TOKEN)

@bot.on_message()
def handle_message(client, message):
    """
    This function is triggered when a message is received
    via webhook and processes the message using Pyrogram.
    """
    chat_id = message.chat.id
    text = message.text
    # Reply to the user message using message.reply()
    message.reply(f"You said: {text}")

@app.post("/webhook")
async def webhook(request: Request):
    """
    Endpoint for Telegram to send updates.
    """
    data = await request.json()
    bot.process_update(data)  # Process the update with Pyrogram
    return {"status": "OK"}

@app.get("/")
async def home():
    """
    Simple home endpoint for testing.
    """
    return {"message": "Bot is Running on site"}

# Run the bot in a separate thread to keep it running with FastAPI
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start())  # Start the Pyrogram bot

    # Start FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

