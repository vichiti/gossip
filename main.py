import os
import requests
from fastapi import FastAPI, Request
from pyrogram import Client, filters, types
import pyrogram

print(pyrogram.__version__)

# Load environment variables
bot_token = os.environ.get("bot_token")
api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")

# Initialize FastAPI app
app = FastAPI()

# Initialize Pyrogram bot
bot = Client("gossip_render", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Webhook URL (Replace with your Glitch project URL)
WEBHOOK_URL = "https://gossip-bbzn.onrender.com/webhook"  # Replace this with your actual Glitch URL

@app.on_event("startup")
async def startup():
    print("Starting bot...")
    await bot.start()

    # Set webhook for the bot using Telegram's setWebhook API
    set_webhook_url = f"https://api.telegram.org/bot{bot_token}/setWebhook?url={WEBHOOK_URL}"
    response = requests.get(set_webhook_url)
    if response.status_code == 200:
        print(f"Webhook set to {WEBHOOK_URL}")
    else:
        print(f"Failed to set webhook: {response.text}")


@app.on_event("shutdown")
async def shutdown():
    """Remove the webhook when the FastAPI app shuts down"""
    print("Stopping bot...")
    await bot.remove_webhook()  # Remove the webhook
    print("Webhook removed successfully!")

@app.post("/webhook")
async def webhook(request: Request):
    """Handle incoming updates from Telegram"""
    json_data = await request.json()  # Get the incoming webhook data
    
    update = types.Update.de_json(json_data)  # Convert it to a Pyrogram Update object
    print(update)
    await bot.process_update(update)  # Process the update with Pyrogram
    return {"status": "ok"}

# Simple endpoint to keep Glitch running
@app.get("/")
def read_root():
    return {"status": "@gossipsnet is running"}

# Define a handler to process messages
@bot.on_message(filters.text)
async def echo(client, message):
    """Simple echo handler: Responds to 'hi' and 'hello'"""
    text = message.text.lower()
    if text in ['hi', 'hello']:
        await message.reply_text("Hello! How can I help you today?")
    else:
        await message.reply_text("I received your message: " + message.text)



# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8000))  # Default to 8000 if PORT is not set
#     uvicorn.run(app, host="0.0.0.0", port=port)
