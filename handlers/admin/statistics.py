from datetime import datetime, timedelta

from aiogram import types

from sqlalchemy import func, case

from database import DataBase, models
from modules import Config
from data import texts


db = DataBase(Config.DATABASE_URL)


async def bot_statistics(message: types.Message):

    group_count = db.counter(models.Group)
    user_count = db.counter(models.User)

    week = datetime.now() + timedelta(days=7)

    replenishments = db.session.query(
        func.coalesce(func.sum(models.Replenishment.amount), 0),
        func.coalesce(func.sum(case(
            [(
                models.Replenishment.created_at.between(week, datetime.now()),
                models.Replenishment.amount
            )],
            else_=0
        )), 0)
    ).filter(
        models.Replenishment.status == 'replenishment'
    ).first()

    await message.answer(texts.BOT_STATISTICS.format(*replenishments, user_count, group_count))
