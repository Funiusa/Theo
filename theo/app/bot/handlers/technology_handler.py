from aiogram import types, exceptions
from app.api import crud
from app.bot.dispatcher import dp, bot
from app.database.session import db
from app.bot.keyboards.ikb import ikb_back_main
from app.bot.utils.sanitize_message import sanitize_html
from app.core.s3_storage import create_presigned_url, bucket

title_image = "theo_images/title_image.jpeg"


@dp.message_handler(commands=["technologies"])
async def all_technologies(message: types.Message) -> None:
    main_markup = types.InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text=t.title, callback_data=f"tech_{t.id}")
                for t in crud.technology.get_multi(db)
            ]
        ],
    )
    answer_text = "<b>List of technologies</b>\n\n\n"
    image_url = create_presigned_url(file_key=title_image)
    await message.answer_photo(
        photo=image_url, caption=answer_text, reply_markup=main_markup
    )


@dp.callback_query_handler(lambda c: c.data.startswith("back_main"))
async def main_menu_technologies(call: types.CallbackQuery):
    await call.answer()
    main_markup = types.InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text=t.title, callback_data=f"tech_{t.id}")
                for t in crud.technology.get_multi(db)
            ]
        ],
    )
    answer_text = "<b>List of technologies</b>\n\n"
    image_url = create_presigned_url(file_key=title_image)
    media = types.InputMediaPhoto(media=image_url, caption=answer_text)
    await call.message.edit_media(media=media, reply_markup=main_markup)


@dp.callback_query_handler(lambda c: c.data.startswith("tech_"))
async def technology_main(call: types.CallbackQuery):
    await call.answer()
    ikb_markup = types.InlineKeyboardMarkup(row_width=2)
    data = call.data.split("_")
    technology_id = data[1]
    technology = crud.technology.get(db, id=technology_id)

    items = crud.item.get_multi_by_technology(db, technology_id=technology_id)
    if items:
        ikb = [
            types.InlineKeyboardButton(text=i.name, callback_data=f"item_{i.id}")
            for i in items
        ]
        ikb_markup.add(*ikb)
    ikb_markup.add(ikb_back_main)

    sanitized_html_text = sanitize_html(technology.description)
    answer_text = f"<b>{technology.title}</b>\n\n{sanitized_html_text}"

    image_url = create_presigned_url(file_key=technology.image)
    media = types.InputMediaPhoto(media=image_url, caption=answer_text)
    await call.message.edit_media(media=media, reply_markup=ikb_markup)
