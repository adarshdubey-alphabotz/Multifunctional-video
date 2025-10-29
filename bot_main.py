# bot_main.py
from pyrogram import Client
from bot_config import API_ID, API_HASH, BOT_TOKEN

# Create the single Client instance used by the whole bot.
app = Client("video_master_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Import all handlers AFTER creating `app` so handler modules can import `app`
# and register their handlers on this exact Client instance.
import handlers_start
import handlers_split
import handlers_merge
import handlers_screenshot
import handlers_watermark

if __name__ == "__main__":
    app.run()
