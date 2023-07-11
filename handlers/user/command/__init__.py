from aiogram.dispatcher.filters import CommandStart, Command, ChatTypeFilter
from aiogram.dispatcher import Dispatcher

from keyboards import callbacks

from . import start, faq, today, bay


dispatcher = Dispatcher.get_current()

#start.py
dispatcher.register_message_handler(start.starting, CommandStart())

#faq.py
dispatcher.register_message_handler(faq.faq_group, Command('help'), ChatTypeFilter(('group', 'supergroup')))
dispatcher.register_message_handler(faq.faq_user, Command('help'), ChatTypeFilter('private'))

#today.py
dispatcher.register_message_handler(today.date, Command('date'))
dispatcher.register_message_handler(today.time, Command('time'))

#bay.py
dispatcher.register_message_handler(bay.bay_menu, callbacks.back_bay.filter())
dispatcher.register_message_handler(bay.bay_menu, Command('bay'))
