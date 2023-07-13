from aiogram import types

from data import texts


async def other_command(message: types.Message):
    await message.answer(texts.COMMAND_NOT_FOUND)
