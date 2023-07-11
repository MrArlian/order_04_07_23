import typing

from aiogram import types

from modules import Config, tools
from keyboards import callbacks
from data import texts


async def bay_menu(event: typing.Union[types.Message, types.CallbackQuery],
                   callback_data: typing.Optional[dict] = None):

    if isinstance(event, types.CallbackQuery):
        user_id = event.message.from_user.id
        chat_type = event.message.chat.type
    else:
        user_id = event.from_user.id
        chat_type = event.chat.type

    data = tools.get_privilege(Config.PRODUCTS_FILE)
    markup = types.InlineKeyboardMarkup()


    if chat_type == 'private':
        markup.add(types.InlineKeyboardButton(
            text='Пополнить баланс',
            callback_data=callbacks.replenishment.new()
        ))
        markup.inline_keyboard.append([])

    for key, value in data.items():
        if key == 'default':
            continue

        markup.insert(types.InlineKeyboardButton(
            text=value.get('name'),
            callback_data=callbacks.privilege.new(key, user_id)
        ))

    if isinstance(event, types.Message):
        await event.answer(texts.CHOOSE_PRIVILEGE, reply_markup=markup)
    else:
        if user_id != int(callback_data.get('current_user')):
            return await event.answer(texts.ACTION_NOT_AVAILABLE, show_alert=True)

        await event.message.edit_text(texts.CHOOSE_PRIVILEGE, reply_markup=markup)
