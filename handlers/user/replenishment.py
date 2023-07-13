import random

from aiogram.dispatcher.storage import FSMContext
from aiogram import types

from yookassa import Configuration, Payment

from keyboards import callbacks, reply
from database import DataBase, models
from modules import Config, tools
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

    amount = float(text)
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

    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('Оплатить', url=payment.confirmation.confirmation_url)
    item2 = types.InlineKeyboardButton('Проверить', callback_data=callbacks.check_replenishment.new(payment.id))
    markup.add(item1, item2)

    db.add(models.Replenishment, order_id=order_id, user_id=user_id, amount=amount)

    await message.answer(texts.PAYMENT_INFO.format(amount, order_id), reply_markup=reply.remove)
    await message.answer(texts.PAYMENT, reply_markup=markup)
    await state.finish()

async def check_replenishment(callback: types.CallbackQuery, callback_data: dict):

    payment_id = callback_data.get('id')
    user_id = callback.from_user.id

    payment = Payment.find_one(payment_id=payment_id)


    if payment.status == 'pending':
        return await callback.answer(texts.NO_PAID)
    if payment.status == 'canceled':
        await callback.message.delete_reply_markup()
        return await callback.message.answer(texts.CANCELED_PAYMENT)
    
    amount = float(payment.amount.value)

    db.update_by_id(models.User, user_id, balance=models.User.balance + amount)
    await callback.message.delete_reply_markup()
    await callback.message.answer(texts.PAID.format(amount))

async def cancel(message: types.Message, state: FSMContext):
    await message.answer(texts.ACTION_CANCELED, reply_markup=reply.remove)
    await state.finish()
