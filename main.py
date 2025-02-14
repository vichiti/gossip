import os
from fastapi import FastAPI, Request
from pyrogram import Client
from dotenv import load_dotenv
import uvicorn

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8000))  # Render assigns a port dynamically

# Ensure the correct timezone
os.environ["TZ"] = "UTC"

# Initialize Pyrogram bot client
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize FastAPI app
app = FastAPI()

@bot.on_message()
def handle_message(client, message):
    """Handles incoming messages."""
    message.reply(f"You said: {message.text}")

@app.post("/webhook")
async def webhook(request: Request):
    """Receives updates from Telegram and processes them."""
    data = await request.json()
    # bot.process_update(data)
    return {"status": "OK"}

@app.get("/")
async def home():
    """Health check endpoint."""
    return {"message": "Bot is running successfully"}

# Start bot and FastAPI together
if __name__ == "__main__":
    bot.start()
    uvicorn.run(app, host="0.0.0.0", port=PORT)
