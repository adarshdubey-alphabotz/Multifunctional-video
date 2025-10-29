# bot_main.py
from pyrogram import Client
from bot_config import API_ID, API_HASH, BOT_TOKEN

# Create the single Client instance used by the whole bot.
app = Client("video_master_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Import handler modules (they only define functions, no registration side-effects).
import handlers_start
import handlers_split
import handlers_merge
import handlers_screenshot
import handlers_watermark

# Register handlers onto the one `app` instance.
handlers_start.register_handlers(app)
handlers_split.register_handlers(app)
handlers_merge.register_handlers(app)
handlers_screenshot.register_handlers(app)
handlers_watermark.register_handlers(app)

if __name__ == "__main__":
    app.run()
