import os
import asyncio
from pyrogram import Client, filters

# Get credentials from environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize the bot
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Hello! I'm running on Render 🚀")

@app.on_message(filters.text)
async def echo(client, message):
    await message.reply_text(f"You said: {message.text}")

# Run the bot
async def main():
    async with app:
        print("Bot is running on Render...")
        await idle()  # Keeps the bot running

if __name__ == "__main__":
    asyncio.run(main())
