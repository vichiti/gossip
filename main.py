import os
import asyncio
from fastapi import FastAPI
from pyrogram import Client, filters
import uvicorn

# Load environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))  # Render assigns a dynamic port

# Initialize Pyrogram bot
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize FastAPI for Render
server = FastAPI()

@server.get("/")
def home():
    return {"status": "Bot is Running on Render"}

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Hello! I'm running on Render Free Tier 🚀")

@bot.on_message(filters.text)
async def echo(client, message):
    await message.reply_text(f"You said: {message.text}")

async def run_pyrogram():
    """Start the Pyrogram bot"""
    async with bot:
        print("Bot is running on Render...")
        await asyncio.Event().wait()  # Keeps the bot running

def start():
    """Run both Pyrogram bot and FastAPI together"""
    loop = asyncio.get_event_loop()
    loop.create_task(run_pyrogram())  # ✅ Runs Pyrogram in the event loop
    uvicorn.run(server, host="0.0.0.0", port=PORT)  # ✅ Starts FastAPI server

if __name__ == "__main__":
    start()
