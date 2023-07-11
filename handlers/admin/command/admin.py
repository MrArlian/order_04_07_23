from aiogram import types

from keyboards import reply
from data import texts


async def admin_panel(message: types.Message):
    await message.answer(texts.HELLO_ADMIN, reply_markup=reply.admin_menu)
