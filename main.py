
from pyrogram import Client
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()
os.environ["TZ"] = "UTC"

# Get the credentials from .env
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
# WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Add webhook URL to .env


# Initialize the Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Define a message handler
@app.on_message()
def handle_message(client, message):
    if message.text == "/start":
        message.reply_text("Hello! I'm your Pyrogram bot.")

# Start the bot
if __name__ == "__main__":
    print("Bot is running...")
    app.run()