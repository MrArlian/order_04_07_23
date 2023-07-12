from aiogram import types

from data import texts


async def about_bot_group(message: types.Message):
    await message.answer(texts.ABOUT_BOT_FOR_GROUP.format(message.chat.id))

async def about_bot_user(message: types.Message):
    await message.answer(texts.ABOUT_BOT_FOR_USER)
