from aiogram.dispatcher import Dispatcher
from aiogram.types import ContentType

from . import group


dispatcher = Dispatcher.get_current()

#group.py
dispatcher.register_message_handler(group.add_group, content_types=ContentType.NEW_CHAT_MEMBERS)
