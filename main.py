import os
import requests
from fastapi import FastAPI, Request
from pyrogram import Client, filters
from pyrogram.types import Update, Message
import uvicorn
from dotenv import load_dotenv
import pyrogram

print(pyrogram.__version__) 

# Load environment variables
load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize FastAPI app
app = FastAPI()

# Initialize Pyrogram bot
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Webhook URL
WEBHOOK_URL = "https://gossip-bbzn.onrender.com/webhook"  # Replace with your actual URL

@app.on_event("startup")
async def startup():
    await bot.start()
    # Set webhook for the bot using Telegram's setWebhook API
    set_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}"
    response = requests.get(set_webhook_url)
    if response.status_code == 200:
        print(f"Webhook set to {WEBHOOK_URL}")
    else:
        print(f"Failed to set webhook: {response.text}")

@app.on_event("shutdown")
async def shutdown():
    await bot.stop()
    print("Bot stopped successfully!")


@app.post("/webhook")
async def webhook(request: Request):
    """Handle incoming updates from Telegram."""
    try:
        # Parse the incoming JSON data
        data = await request.json()
        print("📩 Webhook received:", data)  # Debugging

        # Convert the raw data to an Update object
        # update = pyrogram.raw.types.Updates.read(data)  # Use Update.read to parse the data
        await bot.handle_update(data)  # Process the update using Pyrogram

        return {"status": "OK"}
    except Exception as e:
        print("❌ Webhook Error:", e)  # Debugging
        return {"error": str(e)}

# Simple endpoint to keep Glitch running
@app.get("/")
def read_root():
    return {"status": "gossip net is running 16"}

# Define a handler to process messages
@bot.on_message(filters.text)
async def echo(client, message):
    """Simple echo handler: Responds to 'hi' and 'hello'"""
    text = message.text.lower()
    if text in ['hi', 'hello']:
        await message.reply_text("Hello! How can I help you today?")
    else:
        await message.reply_text("I received your message: " + message.text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port)
