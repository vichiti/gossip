import os
import asyncio
import aiohttp
import requests
from fastapi import FastAPI
from pyrogram import Client, filters


# Load environment variables
bot_token = os.environ.get("BOT_TOKEN")
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
GLITCH_PROJECT_URL = "https://gossip-bbzn.onrender.com/"  # Add this to your .env file
PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY")  # Perplexity AI API Key

# Create FastAPI app
app = FastAPI()

# Initialize Pyrogram bot
bot = Client("GS_glitch", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Flag to track if the server is awake
server_awake = False

async def wake_up_server():
    global server_awake
    if not server_awake:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{GLITCH_PROJECT_URL}/") as response:
                    if response.status == 200:
                        print("Server is now awake")
                        server_awake = True
                    else:
                        print(f"Failed to wake up server. Status: {response.status}")
            except Exception as e:
                print(f"Error waking up server: {str(e)}")

@app.on_event("startup")
async def startup():
    print("Starting bot...")
    await bot.start()
    print("Bot started!")
    await wake_up_server()

@app.on_event("shutdown")
async def shutdown():
    print("Stopping bot...")
    await bot.stop()
    print("Bot stopped!")
    
def get_perplexity_response(user_input):
    """Fetch response from Perplexity AI."""
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": user_input},
        ],
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, I didn't understand that.")
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"API request failed: {str(e)}"
      
  

@bot.on_message(filters.text)
async def handle_message(client, message):
    """Handles incoming messages and replies using Perplexity AI."""
    await wake_up_server()
    user_message = message.text

    # Process message asynchronously
    asyncio.create_task(process_message(client, message, user_message))

async def process_message(client, message, user_input):
    """Fetches response from Perplexity AI and sends it back to the user."""
    response_text = get_perplexity_response(user_input)
    await message.reply_text(response_text)

# Keep Glitch running with a simple route
@app.get("/")
def read_root():
    global server_awake
    server_awake = True
    return {"status": "running @VyomCanvasBot with wake up mechanism on web 2"}

# Run with Uvicorn if needed (but not required on Glitch)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)








# from pyrogram import Client, filters, enums
# from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
# from pyrogram.types import BotCommand
# from pyrogram.raw import functions, types


# import os
# import asyncio


# # Replace 'API_ID' and 'API_HASH' with your actual values
# bot_token = os.environ.get("bot_token")
# api_id = int(os.environ.get("api_id"))
# api_hash = os.environ.get("api_hash")
# # Create the Pyrogram client
# bot = Client("vyomcanvabot_glitch", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


# # An echo handler that sends back the same message received
# @bot.on_message(filters.text)
# async def echo(client, message):
#     await client.send_message(chat_id=-1002367103149, text=(message))
    
# #     invite_link = message.text.split(" ")[-1].strip()  # Assuming the last part of the message is the link
# #     try:
# #         # Joining the group using the invite link
# #         client.join_chat(invite_link)
# #         await message.reply_text("Successfully joined the group!")
# #     except Exception as e:
# #         await message.reply_text(f"Failed to join the group: {str(e)}")

#     text = message.text.lower()
#     # print(text,message, message.chat)

#     # if message.chat.type == 'group':
#     #     # Process messages from the group
#     #     print(f"Received message from group: {message.chat.title}")
#     # elif message.chat.type == 'private':
#     #     # Process messages from private chats
#     #     print(f"Received message from private chat: {message.chat.username}")
#     if text in ['hi', 'hello']:
#         await message.reply_text("vyomcanva")
        
# try:
#     bot.run()
    
# except Exception as e:
#     print(f"An error occurred: {e}")


