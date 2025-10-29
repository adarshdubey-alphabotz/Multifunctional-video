# bot_main.py
from pyrogram import Client, filters
from bot_config import API_ID, API_HASH, BOT_TOKEN

app = Client("video_master_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

import handlers_start
import handlers_split
import handlers_merge
import handlers_screenshot
import handlers_watermark

if __name__ == "__main__":
    app.run()
