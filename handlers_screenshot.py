# handlers_screenshot.py
from pyrogram import Client, filters
from bot_config import DEMO_TEXT
from utils_video import take_screenshots
import os

users = {}

@Client.on_callback_query(filters.regex("screenshot"))
def screenshot_callback(client, callback_query):
    users[callback_query.from_user.id] = {"mode": "wait_video"}
    callback_query.message.reply_text(
        DEMO_TEXT["screenshot"] + "Send your video file.")

@Client.on_message(filters.video)
def ss_video_handler(client, message):
    if users.get(message.from_user.id, {}).get("mode") == "wait_video":
        video_path = f"{message.video.file_id}_ss.mp4"
        message.download(video_path)
        users[message.from_user.id] = {"mode": "wait_times", "video": video_path}
        message.reply_text("Send screenshot times (comma-separated mm:ss).")

@Client.on_message(filters.text & filters.create(lambda m: users.get(m.from_user.id, {}).get("mode") == "wait_times"))
def ss_time_handler(client, message):
    times = [x.strip() for x in message.text.split(",")]
    video_path = users[message.from_user.id]["video"]
    files = take_screenshots(video_path, times)
    for f in files:
        message.reply_photo(f)
    users.pop(message.from_user.id, None)
