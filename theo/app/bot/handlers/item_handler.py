from aiogram import types, exceptions

from app.api import crud
from app.bot.dispatcher import dp
from app.database.session import db
from app.bot.utils.sanitize_message import sanitize_html
from app.core.s3_storage import create_presigned_url, bucket


@dp.callback_query_handler(lambda c: c.data.startswith("item_"))
async def item_handler(call: types.CallbackQuery):
    await call.answer()
    data = call.data.split("_")
    item_id = data[1]
    item = crud.item.get(db, id=item_id)

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(
            text="Back", callback_data=f"tech_{item.technology_id}"
        )
    )
    sanitized_html_text = sanitize_html(item.body)
    answer_text = f"<b>{item.name}</b>\n\n{sanitized_html_text}"

    # await call.message.edit_text(text=answer_text, reply_markup=markup)
    image_url = create_presigned_url(file_key=item.image)
    media = types.InputMediaPhoto(media=image_url, caption=answer_text)
    await call.message.edit_media(media=media, reply_markup=markup)
