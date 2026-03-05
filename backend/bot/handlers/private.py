from aiogram import Bot,Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import Command,CommandStart
from  keyboard.inl_kbds import web_kb
private_router = Router()

@private_router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Hello {message.from_user.first_name}!",reply_markup= web_kb(f"Hello {message.from_user.first_name}!"))

@private_router.message(F.web_app_data)
async def web_app(message: Message):
    await message.answer(message.web_app_data.data)