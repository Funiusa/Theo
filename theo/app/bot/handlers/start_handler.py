from aiogram import types

from app.bot.dispatcher import dp
from app.core.config import users_telegram_ids


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    users_telegram_ids.append(message.chat.id)
    await message.answer(f"Hello, {message.chat.username}! Nice to meet you.")

