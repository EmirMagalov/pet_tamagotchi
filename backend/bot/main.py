import os

from aiogram import Bot, Dispatcher
import asyncio
from handlers.private import private_router
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("TOKEN")

bot = Bot(token=token)
dp = Dispatcher()

dp.include_router(private_router)

def start_bot():
    print("Bot_Online")

async def main():
    start_bot()
    await dp.start_polling(bot)


asyncio.run(main())