import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
from dotenv import load_dotenv
load_dotenv()
url = os.getenv("URL")


def web_kb(text: str):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, web_app=WebAppInfo(url=url))
        ]

    ])

    return markup
