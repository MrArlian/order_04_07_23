import random

from aiogram.dispatcher.storage import FSMContext
from aiogram import types

from yookassa import Configuration, Payment

from database import DataBase, models
from modules import Config, tools
from keyboards import reply
from data import texts

from .. import states


Configuration.configure(Config.YOOMONEY_SHOP_ID, Config.YOOMONEY_API_KEY)
db = DataBase(Config.DATABASE_URL)


async def enter_amount(callback: types.CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.message.answer(texts.ENTER_REPLENISHMENT_AMOUNT, reply_markup=reply.cancel)
    await states.Replenishment.amount.set()

async def replenishment(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    text = message.text

    order_id = random.getrandbits(32)


    if not tools.is_digit(text):
        return await message.answer(texts.INPUT_ERROR)

    payment = Payment.create({
        'amount': {
            'value': str(text),
            'currency': 'RUB'
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': Config.CALLBACK_URL
        }
    })

    markup = types.InlineKeyboardMarkup()
    item = types.InlineKeyboardButton('Оплатить', url=payment.confirmation.confirmation_url)
    markup.add(item)

    db.add(models.Replenishment, order_id=order_id, user_id=user_id, amount=float(text))

    await message.answer(texts.PAYMENT_INFO.format(float(text), order_id), reply_markup=reply.remove)
    await message.answer(texts.PAYMENT, reply_markup=markup)
    await state.finish()

async def cancel(message: types.Message, state: FSMContext):
    await message.answer(texts.ACTION_CANCELED, reply_markup=reply.remove)
    await state.finish()
