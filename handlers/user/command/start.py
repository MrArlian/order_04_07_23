from aiogram import types

from database import DataBase, models
from modules import Config
from data import texts


db = DataBase(Config.DATABASE_URL)


async def starting(message: types.Message):

    username = message.from_user.username or ''
    user_id = message.from_user.id

    db.add(models.User, 'id', id=user_id, username=username.lower())
    await message.answer(texts.START_MESSAGE)
