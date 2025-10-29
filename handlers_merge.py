# handlers_merge.py
from pyrogram import Client, filters
from bot_config import DEMO_TEXT
from utils_video import merge_videos
import os

users = {}

@Client.on_callback_query(filters.regex("merge"))
def merge_callback(client, callback_query):
    users[callback_query.from_user.id] = {"mode": "wait_base"}
    callback_query.message.reply_text(
        DEMO_TEXT["merge"] + "
Send base video first.")

@Client.on_message(filters.video)
def merge_video_handler(client, message):
    uid = message.from_user.id
    if users.get(uid, {}).get("mode") == "wait_base":
        base_path = f"{message.video.file_id}_base.mp4"
        message.download(base_path)
        users[uid].update({"mode": "wait_next", "base": base_path})
        message.reply_text("Now send the video to be joined.")
    elif users.get(uid, {}).get("mode") == "wait_next":
        next_path = f"{message.video.file_id}_merge.mp4"
        message.download(next_path)
        merged = merge_videos(users[uid]["base"], next_path)
        message.reply_text("Here's your merged video.")
        message.reply_video(merged)
        users.pop(uid, None)
