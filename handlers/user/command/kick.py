from aiogram.dispatcher.filters import Command
from aiogram.utils import exceptions
from aiogram import Bot, types

from modules import tools
from data import texts


bot = Bot.get_current()


async def kick_user(message: types.Message, command: Command.CommandObj):

    reply = message.reply_to_message
    chat_type = message.chat.type
    param = command.args or ''
    chat_id = message.chat.id


    if chat_type not in ('group', 'supergroup'):
        return await message.answer(texts.CAN_NOT_USE)
    if reply is None and not param:
        return await message.answer(texts.ERROR_KICK_PARAMS)
    if reply is None and not tools.is_digit(param, only_integer=True):
        return await message.answer(texts.ERROR_KICK_PARAM_ID)

    if reply:
        user_id = reply.from_user.id
    else:
        user_id = int(param)

    try:
        await bot.kick_chat_member(chat_id, user_id, 60)
    except exceptions.ChatAdminRequired:
        await message.answer(texts.DELETION_ERROR)
    except (exceptions.ChatNotFound, exceptions.InvalidUserId, exceptions.BadRequest):
        await message.answer(texts.USER_NOT_FOUND)
