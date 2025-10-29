# handlers_split.py
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_config import DEMO_TEXT
from utils_video import split_video
from utils_misc import parse_time_str
import os

users = {}

@Client.on_callback_query(filters.regex("split"))
def split_query_handler(client, callback_query):
    users[callback_query.from_user.id] = {"mode": "wait_video"}
    callback_query.message.reply_text(
        DEMO_TEXT["split"] + "
Send your video file.")

@Client.on_message(filters.video)
def split_video_handler(client, message):
    if users.get(message.from_user.id, {}).get("mode") == "wait_video":
        video_path = f"{message.video.file_id}.mp4"
        message.download(video_path)
        users[message.from_user.id]["video"] = video_path
        users[message.from_user.id]["mode"] = "choose_type"
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("Single Split", callback_data="single_split"),
             InlineKeyboardButton("Multiple Splits", callback_data="multi_split")]
        ])
        message.reply_text("Choose split type:", reply_markup=kb)
    elif users.get(message.from_user.id, {}).get("mode") == "multi_add":
        video_path = users[message.from_user.id]["video"]
        if "splits" not in users[message.from_user.id]:
            users[message.from_user.id]["splits"] = []
        ms = message.caption or message.text
        if ":" in ms:
            users[message.from_user.id]["splits"].append(ms)
            message.reply_text(
                f"Split at {ms} added. Send next time or type /done when finished.")

@Client.on_callback_query(filters.regex("single_split"))
def split_single_callback(client, callback_query):
    users[callback_query.from_user.id]["mode"] = "single_split"
    callback_query.message.reply_text(
        "Send split time in mm:ss, e.g., 1:10 for 1min 10sec.")

@Client.on_callback_query(filters.regex("multi_split"))
def split_multi_callback(client, callback_query):
    users[callback_query.from_user.id]["mode"] = "multi_add"
    callback_query.message.reply_text(
        "Send split points one by one in mm:ss. When finished, type /done.")

@Client.on_message(filters.text & filters.create(lambda m: users.get(m.from_user.id, {}).get("mode") == "single_split"))
def split_single_time_handler(client, message):
    video_path = users[message.from_user.id]["video"]
    sec = parse_time_str(message.text)
    out_files = split_video(video_path, [sec])
    for f in out_files:
        message.reply_video(f)
    users.pop(message.from_user.id, None)

@Client.on_message(filters.command("done"))
def split_multi_done_handler(client, message):
    splits = users.get(message.from_user.id, {}).get("splits", [])
    video_path = users.get(message.from_user.id, {}).get("video")
    out_files = split_video(video_path, [parse_time_str(s) for s in splits])
    for f in out_files:
        message.reply_video(f)
    users.pop(message.from_user.id, None)
