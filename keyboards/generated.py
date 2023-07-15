import typing

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from . import callbacks


def buy_menu_keyboard(user_id: int, privilege: typing.List[dict]) -> InlineKeyboardMarkup:

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text='Пополнить баланс',
            callback_data=callbacks.replenishment.new(user_id)
        )
    )
    markup.inline_keyboard.append([])

    for key, value in privilege.items():
        if key == 'default':
            continue

        markup.insert(
            InlineKeyboardButton(
                text=value['name'],
                callback_data=callbacks.privilege.new(key, user_id)
            )
        )

    return markup
