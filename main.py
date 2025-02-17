import os
import asyncio
from fastapi import FastAPI
from pyrogram import Client, filters
import uvicorn

# Get credentials from environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))  # Render assigns a dynamic port

# Initialize Pyrogram bot
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize FastAPI for Render
server = FastAPI()

@server.get("/")
def home():
    return {"status": "Bot is Running on Render"}

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Hello! I'm running on Render Free Tier 🚀")

@app.on_message(filters.text)
async def echo(client, message):
    await message.reply_text(f"You said: {message.text}")

async def run_pyrogram():
    async with app:
        print("Bot is running on Render...")
        await asyncio.Event().wait()  # Keeps the bot running

async def run():
    # Run both FastAPI (fake web server) and Pyrogram bot together
    await asyncio.gather(
        run_pyrogram(),
        uvicorn.run(server, host="0.0.0.0", port=PORT, loop="asyncio")
    )

if __name__ == "__main__":
    asyncio.run(run())
