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

    db.add(models.Replenishment, order_id=payment.id, user_id=user_id, amount=amount)

    await message.answer(texts.PAYMENT_INFO.format(amount, payment.id), reply_markup=reply.remove)
    await message.answer(texts.PAYMENT, reply_markup=markup)
    await state.finish()

async def check_replenishment(callback: types.CallbackQuery, callback_data: dict):

    payment_id = callback_data.get('id')
    user_id = callback.from_user.id

    payment = Payment.find_one(payment_id=payment_id)
    data = tools.get_privilege(Config.PRODUCTS_FILE)
    markup = types.InlineKeyboardMarkup()


    if payment.status == 'pending':
        return await callback.answer(texts.NO_PAID)
    if payment.status == 'canceled':
        await callback.message.delete_reply_markup()
        return await callback.message.answer(texts.CANCELED_PAYMENT)

    markup.add(types.InlineKeyboardButton(
        text='Пополнить баланс',
        callback_data=callbacks.replenishment.new()
    ))
    markup.inline_keyboard.append([])

    for key, value in data.items():
        if key == 'default':
            continue

        markup.insert(types.InlineKeyboardButton(
            text=value.get('name'),
            callback_data=callbacks.privilege.new(key, user_id)
        ))

    db.update(models.Replenishment, models.Replenishment.order_id == payment_id, status='replenishment')
    db.update_by_id(models.User, user_id, balance=models.User.balance + payment.amount.value)

    await callback.message.delete_reply_markup()
    await callback.message.answer(texts.PAID.format(payment.amount.value), reply_markup=markup)

async def cancel(message: types.Message, state: FSMContext):
    await message.answer(texts.ACTION_CANCELED, reply_markup=reply.remove)
    await state.finish()
