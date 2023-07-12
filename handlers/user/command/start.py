from aiogram import Bot, types

from database import DataBase, models
from modules import Config
from data import texts


db = DataBase(Config.DATABASE_URL)
bot = Bot.get_current()


async def starting(message: types.Message):

    username = message.from_user.username or ''
    full_name = message.from_user.full_name
    user_id = message.from_user.id

    bot_me = await bot.get_me()

    db.add(models.User, 'id', id=user_id, username=username.lower())
    await message.answer(texts.START_MESSAGE.format(full_name, bot_me.full_name))
