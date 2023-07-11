from aiogram import types

from data import texts


async def faq_group(message: types.Message):
    await message.answer(texts.FAQ_FOR_GROUP.format(message.chat.id))

async def faq_user(message: types.Message):
    await message.answer(texts.FAQ_FOR_USER)
