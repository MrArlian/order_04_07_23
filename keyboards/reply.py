from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#User
cancel = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton('Отмена')
        ]
    ]
)

#Admin
admin_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton('Выдать'),
            KeyboardButton('Забрать')
        ],
        [
            KeyboardButton('Статистика')
        ]
    ]
)
