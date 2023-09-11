import random
from app.api import crud
from app.database.session import db
from app.bot.dispatcher import bot
from app.core.config import users_telegram_ids


async def send_item_cron():
    items = crud.item.get_multi(db)
    if items:
        item = random.choice(items)
        for chat_id in users_telegram_ids:
            await bot.send_message(chat_id=chat_id, text=item.body)


async def send_message_middleware():
    for chat_id in users_telegram_ids:
        await bot.send_message(chat_id, "Message from middleware")
