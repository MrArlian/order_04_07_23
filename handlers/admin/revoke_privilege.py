from aiogram.dispatcher.storage import FSMContext
from aiogram import types

from database import DataBase, models
from modules import Config, tools
from keyboards import reply
from data import texts

from .. import states


db = DataBase(Config.DATABASE_URL)


async def enter_user(message: types.Message):
    await message.answer(texts.INPUT_USER, reply_markup=reply.cancel)
    await states.RevokePrivilege.user.set()

async def revoke(message: types.Message, state: FSMContext):

    text = message.text.lower()

    if tools.is_digit(text, only_integer=True):
        entity = (
            db.session.query(models.User.id).filter_by(id=int(text)).union(
                db.session.query(models.Group.id).filter_by(id=int(text))
            )
        ).first()
    elif tools.is_username(text):
        entity = (
            db.session.query(models.User.id).filter_by(username=text.split('@')[-1]).union(
                db.session.query(models.Group.id).filter_by(username=text.split('@')[-1])
            )
        ).first()
    else:
        return await message.answer(texts.ERROR_INPUT_USER)

    if entity is None:
        return await message.answer(texts.USER_NOT_FOUND)

    if entity[0] < 0:
        db.update_by_id(models.User, entity[0], privilege='default')
    else:
        db.update_by_id(models.Group, entity[0], privilege='default')

    await message.answer(texts.PRIVILEGE_REVOKED, reply_markup=reply.admin_menu)
    await state.finish()

async def cancel(message: types.Message, state: FSMContext):
    await message.answer(texts.ACTION_CANCELED, reply_markup=reply.admin_menu)
    await state.finish()
