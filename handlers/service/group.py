from aiogram import Bot, types

from database import DataBase, models
from modules import Config


db = DataBase(Config.DATABASE_URL)
bot = Bot.get_current()


async def add_group(message: types.Message):

    if (
        message.new_chat_members[0].id == bot.id and
        message.chat.type in ('group', 'supergroup')
    ):
        db.add(
            table=models.Group,
            conflicts='id',
            id=message.chat.id,
            username=(message.chat.username or '').lower()
        )
