from aiogram.utils.exceptions import ChatAdminRequired
from aiogram import Bot, types

from data import texts


bot = Bot.get_current()


async def kick_user(message: types.Message):

    user_id = message.from_user.id
    chat_type = message.chat.type
    chat_id = message.chat.id

    if chat_type not in ('group', 'supergroup'):
        return await message.answer(texts.CAN_NOT_USE)

    try:
        await bot.kick_chat_member(chat_id, user_id, 60)
    except ChatAdminRequired:
        await bot.send_message(chat_id, texts.DELETION_ERROR)
