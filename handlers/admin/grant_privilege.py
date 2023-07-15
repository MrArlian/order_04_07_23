from aiogram.dispatcher.storage import FSMContext
from aiogram import types

from database import DataBase, models
from modules import Config, tools
from keyboards import reply
from data import texts

from .. import states


PRIVILEGES = tools.get_privilege()

db = DataBase(Config.DATABASE_URL)


async def enter_user(message: types.Message):
    await message.answer(texts.INPUT_ENTITY, reply_markup=reply.cancel)
    await states.GrantPrivilege.user.set()

async def enter_privilege(message: types.Message, state: FSMContext):

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
        return await message.answer(texts.ERROR_INPUT_ENTITY)

    if entity is None:
        return await message.answer(texts.ENTITY_NOT_FOUND)

    await state.update_data(entity=entity[0])
    await message.answer(texts.INPUT_PRIVILEGE_NAME, reply_markup=reply.cancel)
    await states.GrantPrivilege.next()

async def grant(message: types.Message, state: FSMContext):

    text = message.text

    data = await state.get_data(default={})
    entity = data.get('entity', 0)


    if text not in PRIVILEGES:
        return await message.answer(texts.ADMIN_PRIVILEGE_NOT_FOUND)

    if entity > 0:
        db.update_by_id(models.User, entity, privilege=text)
    else:
        db.update_by_id(models.Group, entity, privilege=text)

    await message.answer(texts.PRIVILEGE_GRANTED, reply_markup=reply.admin_menu)
    await state.finish()

async def cancel(message: types.Message, state: FSMContext):
    await message.answer(texts.ACTION_CANCELED, reply_markup=reply.admin_menu)
    await state.finish()
