# handlers_watermark.py
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_config import DEMO_TEXT, POSITIONS
from utils_video import add_watermark
from utils_image import remove_bg
import os

users = {}

@Client.on_callback_query(filters.regex("watermark"))
def wm_callback(client, callback_query):
    users[callback_query.from_user.id] = {"mode": "wait_video"}
    callback_query.message.reply_text(
        DEMO_TEXT["watermark"] + "Send your video file.")

@Client.on_message(filters.video)
def wm_video_handler(client, message):
    if users.get(message.from_user.id, {}).get("mode") == "wait_video":
        video_path = f"{message.video.file_id}_wm.mp4"
        message.download(video_path)
        users[message.from_user.id] = {"mode": "wait_image", "video": video_path}
        message.reply_text("Send watermark image or direct link.")

@Client.on_message(filters.photo)
def wm_image_handler(client, message):
    uid = message.from_user.id
    if users.get(uid, {}).get("mode") == "wait_image":
        image_path = f"{message.photo.file_id}_wm.png"
        message.download(image_path)
        with open(image_path, "rb") as f:
            new_img = remove_bg(f.read())
        bg_rm_path = f"{uid}_bg_rm.png"
        with open(bg_rm_path, "wb") as f:
            f.write(new_img)
        users[uid]["wm_img"] = bg_rm_path
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(pos.title(), callback_data=f"wmpos_{pos}")]
            for pos in POSITIONS
        ])
        message.reply_text("Choose watermark position:", reply_markup=kb)

@Client.on_message(filters.text & filters.create(lambda m: users.get(m.from_user.id, {}).get("mode") == "wait_image"))
def wm_image_link_handler(client, message):
    import requests
    uid = message.from_user.id
    img_data = requests.get(message.text).content
    with open(f"{uid}_wmimg.png", "wb") as f:
        f.write(img_data)
    new_img = remove_bg(img_data)
    bg_rm_path = f"{uid}_bg_rm.png"
    with open(bg_rm_path, "wb") as f:
        f.write(new_img)
    users[uid]["wm_img"] = bg_rm_path
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(pos.title(), callback_data=f"wmpos_{pos}")]
        for pos in POSITIONS
    ])
    message.reply_text("Choose watermark position:", reply_markup=kb)

@Client.on_callback_query(filters.regex(r"wmpos_"))
def wmpos_callback(client, callback_query):
    pos = callback_query.data.replace("wmpos_", "")
    uid = callback_query.from_user.id
    video = users[uid]["video"]
    watermark = users[uid]["wm_img"]
    out = add_watermark(video, watermark, pos)
    callback_query.message.reply_text("Here's your watermarked video.")
    callback_query.message.reply_video(out)
    users.pop(uid, None)
