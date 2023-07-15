from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.markdown import hlink
from aiogram import types

from yookassa import Configuration, Payment

from keyboards import callbacks, reply, generated
from database import DataBase, models
from modules import Config, tools
from data import texts

from .. import states


PRIVILEGE = tools.get_privilege()

Configuration.configure(Config.YOOMONEY_SHOP_ID, Config.YOOMONEY_API_KEY)
db = DataBase(Config.DATABASE_URL)


async def enter_amount(callback: types.CallbackQuery, callback_data: dict):

    current_user = int(callback_data.get('current_user'))
    first_name = callback.from_user.first_name
    username = callback.from_user.username
    user_id = callback.from_user.id


    if user_id != current_user:
        return await callback.answer(texts.ACTION_NOT_AVAILABLE, show_alert=True)

    if username is None:
        user_link = hlink(f'@{first_name}', f'tg://user?id={user_id}')
    else:
        user_link = f'@{username}'

    await callback.message.delete_reply_markup()
    await callback.message.answer(
        text=texts.ENTER_REPLENISHMENT_AMOUNT.format(user_link),
        reply_markup=reply.cancel
    )
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
            'return_url': Config.RETURN_URL
        }
    })

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(
            text='Оплатить',
            url=payment.confirmation.confirmation_url
        ),
        types.InlineKeyboardButton(
            text='Проверить',
            callback_data=callbacks.check_replenishment.new(payment.id, user_id)
        )
    )

    db.add(models.Replenishment, order_id=payment.id, user_id=user_id, amount=amount)

    await message.answer(texts.PAYMENT_INFO.format(amount, payment.id), reply_markup=reply.remove)
    await message.answer(texts.PAYMENT, reply_markup=markup)
    await state.finish()

async def check_replenishment(callback: types.CallbackQuery, callback_data: dict):

    current_user = int(callback_data.get('current_user'))
    payment_id = callback_data.get('id')
    user_id = callback.from_user.id

    payment = Payment.find_one(payment_id=payment_id)


    if user_id != current_user:
        return await callback.answer(texts.ACTION_NOT_AVAILABLE, show_alert=True)
    if payment.status == 'pending':
        return await callback.answer(texts.NO_PAID)
    if payment.status == 'canceled':
        await callback.message.delete_reply_markup()
        return await callback.message.answer(texts.CANCELED_PAYMENT)

    db.update(models.Replenishment, models.Replenishment.order_id == payment_id, status='replenishment')
    db.update_by_id(models.User, user_id, balance=models.User.balance + payment.amount.value)

    await callback.message.delete_reply_markup()
    await callback.message.answer(
        text=texts.PAID.format(payment.amount.value),
        reply_markup=generated.buy_menu_keyboard(user_id, PRIVILEGE)
    )

async def cancel(message: types.Message, state: FSMContext):
    await message.answer(texts.ACTION_CANCELED, reply_markup=reply.remove)
    await state.finish()
