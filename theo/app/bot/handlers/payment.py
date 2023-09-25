from aiogram import Bot, types
from app.bot.dispatcher import dp, bot


@dp.message_handler(commands=["pay"])
async def order(message: types.Message):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Payment from telegram bot",
        description="Try to use telegram payloads",
        payload=f"{message.chat.username}",
        provider_token="381764678:TEST:65581",
        currency="rub",
        prices=[
            types.LabeledPrice(
                label="Покупка экскурсий",
                amount=99000,
            ),
            types.LabeledPrice(
                label="NDS",
                amount=20000,
            ),
            types.LabeledPrice(
                label="Discount",
                amount=-20000,
            ),
            types.LabeledPrice(label="Bonus", amount=-40000),
        ],
        max_tip_amount=5000,
        suggested_tip_amounts=[1000, 2000, 3000, 4000],
        start_parameter=f"{message.chat.username}",
        provider_data=None,
        need_name=True,
        need_email=True,
        need_phone_number=True,
        need_shipping_address=False,
        send_email_to_provider=False,
        send_phone_number_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        reply_markup=None,
        allow_sending_without_reply=True,
    )


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_ck_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_ck_query.id, ok=True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    msg = f"""Successful payment 
            {message.successful_payment.total_amount // 100} 
            {message.successful_payment.currency}.
            Our manager already get your order and just call you now.
            """
    await message.answer(msg)
