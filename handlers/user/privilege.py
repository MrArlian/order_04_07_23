from datetime import datetime, timedelta

from aiogram import Bot, types

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import JobLookupError

from keyboards import callbacks, generated
from database import DataBase, models
from modules import Config, tools
from data import texts


PRIVILEGE = tools.get_privilege()

db = DataBase(Config.DATABASE_URL)
bot = Bot.get_current()

scheduler = AsyncIOScheduler()
scheduler.start()


async def view(callback: types.CallbackQuery, callback_data: dict):

    current_user = int(callback_data.get('current_user'))
    name = callback_data.get('name')

    chat_type = callback.message.chat.type
    user_id = callback.from_user.id

    balance = db.get_data(models.User, columns=models.User.balance, default=0, id=user_id)


    if user_id != current_user:
        return await callback.answer(texts.ACTION_NOT_AVAILABLE, show_alert=True)

    if chat_type == 'private':
        item1_callback_data = callbacks.bay_privilege.new(name, 'personal', user_id)
    else:
        item1_callback_data = callbacks.purchase_type.new(name, user_id)

    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('Купить', callback_data=item1_callback_data)
    item2 = types.InlineKeyboardButton('Назад', callback_data=callbacks.back_bay.new(user_id))
    markup.add(item1, item2)

    msg = texts.PRIVILEGE_INFO.format(
        PRIVILEGE[name]['name'],
        '\n'.join(map(lambda x: f'/{x}', PRIVILEGE[name]['scope'])),
        PRIVILEGE[name]['price'],
        balance
    )
    await callback.message.edit_text(msg, reply_markup=markup)

async def purchase_type(callback: types.CallbackQuery, callback_data: dict):

    current_user = int(callback_data.get('current_user'))
    name = callback_data.get('name')

    user_id = callback.from_user.id

    balance = db.get_data(models.User, columns=models.User.balance, default=0, id=user_id)


    if user_id != current_user:
        return await callback.answer(texts.ACTION_NOT_AVAILABLE, show_alert=True)
    if balance < PRIVILEGE[name]['price']:
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

    expires_in = datetime.now() + timedelta(seconds=PRIVILEGE[name]['expires_in'])

    balance = db.get_data(models.User, columns=models.User.balance, default=0, id=user_id)


    if user_id != current_user:
        return await callback.answer(texts.ACTION_NOT_AVAILABLE, show_alert=True)
    if balance < PRIVILEGE[name]['price']:
        return await callback.answer(texts.INSUFFICIENT_FUNDS)

    db.update_by_id(models.User, user_id, balance=models.User.balance - PRIVILEGE[name]['price'])

    if _type == 'personal':
        kwargs = {'chat_id': str(user_id), 'text': texts.USER_PRIVILEGE_TIME_EXPIRED}
        db.update_by_id(models.User, user_id, privilege=name, expires_in=expires_in)
    else:
        kwargs = {'chat_id': str(chat_id), 'text': texts.GROUP_PRIVILEGE_TIME_EXPIRED}
        db.update_by_id(models.Group, chat_id, privilege=name, expires_in=expires_in)

    try:
        scheduler.remove_job(kwargs['chat_id'])
    except JobLookupError:
        pass

    scheduler.add_job(
        id=kwargs['chat_id'],
        func=bot.send_message,
        kwargs=kwargs,
        trigger='date',
        run_date=expires_in,
    )

    await callback.message.delete_reply_markup()
    await callback.message.answer(texts.PRODUCT_PURCHASED)

async def back_bay_menu(callback: types.CallbackQuery, callback_data: dict):

    current_user = int(callback_data.get('current_user'))

    chat_type = callback.message.chat.type
    chat_id = callback.message.chat.id
    user_id = callback.from_user.id


    if chat_type == 'private':
        entity = db.get_data(models.User, id=user_id)
    else:
        entity = db.get_data(models.Group, id=chat_id)

    if user_id != current_user:
        return await callback.answer(texts.ACTION_NOT_AVAILABLE, show_alert=True)

    if entity.privilege != 'default':
        await callback.message.edit_text(
            text=texts.DETAILS_PRIVILEGE.format(
                PRIVILEGE[entity.privilege]['name'],
                entity.expires_in.strftime('%Y-%m-%d %H:%M:%S')
            ),
            reply_markup=generated.buy_menu_keyboard(user_id, PRIVILEGE)
        )
    else:
        await callback.message.edit_text(
            text=texts.CHOOSE_PRIVILEGE,
            reply_markup=generated.buy_menu_keyboard(user_id, PRIVILEGE)
        )
