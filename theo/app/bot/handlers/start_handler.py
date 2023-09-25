from aiogram.types import Message

# from pyrogram import Client, idle, types, filters

from app.bot.dispatcher import dp
from app.core.config import users_telegram_ids, settings


@dp.message_handler(commands=["start"])
async def start(message: Message):
    users_telegram_ids.append(message.chat.id)
    await message.answer(f"Hello, {message.chat.username}! Nice to meet you.")


# @dp.message_handler()
# async def get_id(message: Message):
#     await message.answer(
#         f"User id: {message.chat.id}\n"
#         f"Chat id: {message.chat.id}\n"
#         f"Forwarded msg: {message.forward_from_chat.id}"
#     )


# async def new_post(client: Client, message: types.Message):
#     await client.copy_message(
#         chat_id=settings.TECHNICAL_CHANNEL,
#         from_chat_id=message.chat.id,
#         message_id=message.id,
#     )
#

# async def copy_to_main_channel(client: Client, message: types.Message):
#     await client.copy_message(
#         chat_id=settings.BACKEND_MAIN_CHANNEL,
#         from_chat_id=message.chat.id,
#         message_id=message.reply_to_message_id,
#     )
#     await message.delete()
#     await message.reply_to_message.delete()


# async def fetch_data_to_channel():
#     user_bot = Client(
#         name="user_bot", api_id=settings.API_ID, api_hash=settings.APP_API_HASH
#     )
#     bot_content = Client(
#         name="bot_content",
#         api_id=settings.API_ID,
#         api_hash=settings.APP_API_HASH,
#         bot_token=settings.BOT_TOKEN,
#     )
#     user_bot.add_handler(
#         MessageHandler(new_post, filters=filters.chat(chats=settings.DONORS_LIST))
#     )
#     bot_content.add_handler(MessageHandler(copy_to_main_channel, filters=filters.reply))
#     await user_bot.start()
#     await bot_content.start()
#     await idle()
#     await user_bot.stop()
#     await bot_content.stop()
