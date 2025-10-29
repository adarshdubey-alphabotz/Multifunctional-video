# handlers_start.py
from bot_main import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_config import DEMO_TEXT

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Split", callback_data="split"),
         InlineKeyboardButton("Merge", callback_data="merge")],
        [InlineKeyboardButton("Screenshot", callback_data="screenshot"),
         InlineKeyboardButton("Watermark", callback_data="watermark")]
    ])

@app.on_message(filters.command(["start", "help"]))
def start_handler(client, message):
    msg = ("👋 Welcome! Choose a tool below.\n"
           "Demo and examples at each step.")
    message.reply_text(msg, reply_markup=main_keyboard())
