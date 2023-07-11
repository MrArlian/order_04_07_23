from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import Dispatcher

from . import admin


dispatcher = Dispatcher.get_current()

#admin.py
dispatcher.register_message_handler(admin.admin_panel, Command('admin'))
