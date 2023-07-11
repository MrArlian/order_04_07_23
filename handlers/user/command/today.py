from datetime import datetime

from aiogram import types


async def date(message: types.Message):
    await message.answer(datetime.now().date())

async def time(message: types.Message):
    await message.answer(datetime.now().time())
