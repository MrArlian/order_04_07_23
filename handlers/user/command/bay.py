from aiogram import types

from database import DataBase, models
from modules import Config, tools
from keyboards import generated
from data import texts


PRIVILEGE = tools.get_privilege()

db = DataBase(Config.DATABASE_URL)


async def bay_menu(message: types.Message):

    user_id = message.from_user.id
    chat_type = message.chat.type
    chat_id = message.chat.id

    if chat_type == 'private':
        entity = db.get_data(models.User, id=user_id)
    else:
        entity = db.get_data(models.Group, id=chat_id)

    if entity.privilege != 'default':
        await message.answer(
            text=texts.DETAILS_PRIVILEGE.format(
                PRIVILEGE[entity.privilege]['name'],
                entity.expires_in.strftime('%Y-%m-%d %H:%M:%S')
            ),
            reply_markup=generated.buy_menu_keyboard(user_id, PRIVILEGE)
        )
    else:
        await message.answer(
            text=texts.CHOOSE_PRIVILEGE,
            reply_markup=generated.buy_menu_keyboard(user_id, PRIVILEGE)
        )
