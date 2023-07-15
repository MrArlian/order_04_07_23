from datetime import datetime, timedelta

from aiogram import types

from database import DataBase, models
from modules import Config, tools
from keyboards import callbacks
from data import texts


PRIVILEGES = tools.get_privilege(Config.PRODUCTS_FILE)

db = DataBase(Config.DATABASE_URL)


async def view(callback: types.CallbackQuery, callback_data: dict):

    current_user = int(callback_data.get('current_user'))
    name = callback_data.get('name')

    chat_type = callback.message.chat.type
    user_id = callback.from_user.id

    balance = db.get_data(models.User, columns=models.User.balance, default=0, id=user_id)
    privilege = PRIVILEGES.get(name)


    if privilege is None:
        return await callback.answer(texts.PRIVILEGE_NOT_FOUND)
    if user_id != current_user:
        return await callback.answer(texts.ACTION_NOT_AVAILABLE, show_alert=True)

    if chat_type != 'private':
        item1_callback_data = callbacks.purchase_type.new(name, user_id)
    else:
        item1_callback_data = callbacks.bay_privilege.new(name, 'personal', user_id)

    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('Купить', callback_data=item1_callback_data)
    item2 = types.InlineKeyboardButton('Назад', callback_data=callbacks.back_bay.new(user_id))
    markup.add(item1, item2)

    msg = texts.PRIVILEGE_INFO.format(
        privilege.get('name'),
        '\n'.join(map(lambda x: f'/{x}', privilege.get('scope'))),
        privilege.get('price'),
        balance
    )
    await callback.message.edit_text(msg, reply_markup=markup)

async def purchase_type(callback: types.CallbackQuery, callback_data: dict):

    current_user = int(callback_data.get('current_user'))
    name = callback_data.get('name')

    user_id = callback.from_user.id

    balance = db.get_data(models.User, columns=models.User.balance, default=0, id=user_id)
    privilege = PRIVILEGES.get(name)


    if privilege is None:
        return await callback.answer(texts.PRIVILEGE_NOT_FOUND)
    if user_id != current_user:
        return await callback.answer(texts.ACTION_NOT_AVAILABLE, show_alert=True)
    if balance < privilege.get('price'):
        return await callback.answer(texts.INSUFFICIENT_FUNDS)

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(
            text='Для себя',
            callback_data=callbacks.bay_privilege.new(name, 'personal', user_id)
        ),
        types.InlineKeyboardButton(
            text='Для группы',
            callback_data=callbacks.bay_privilege.new(name, 'public', user_id)
        )
    )

    await callback.message.delete_reply_markup()
    await callback.message.answer(texts.PURCHASE_TYPE, reply_markup=markup)

async def purchase(callback: types.CallbackQuery, callback_data: dict):

    current_user = int(callback_data.get('current_user'))
    _type = callback_data.get('type')
    name = callback_data.get('name')

    chat_id = callback.message.chat.id
    user_id = callback.from_user.id

    balance = db.get_data(models.User, columns=models.User.balance, default=0, id=user_id)
    privilege = PRIVILEGES.get(name)
    now = datetime.now()


    if privilege is None:
        return
    if user_id != current_user:
        return await callback.answer(texts.ACTION_NOT_AVAILABLE, show_alert=True)
    if balance < privilege.get('price'):
        return await callback.answer(texts.INSUFFICIENT_FUNDS)

    expires_in = now + timedelta(seconds=privilege.get('expires_in'))

    db.update_by_id(models.User, user_id, balance=models.User.balance - privilege.get('price'))

    if _type == 'personal':
        db.update_by_id(models.User, user_id, privilege=name, expires_in=expires_in)
    else:
        db.update_by_id(models.Group, chat_id, privilege=name, expires_in=expires_in)

    await callback.message.delete_reply_markup()
    await callback.message.answer(texts.PRODUCT_PURCHASED)
