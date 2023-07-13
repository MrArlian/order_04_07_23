from aiogram.dispatcher.filters import CommandStart, Command, ChatTypeFilter, Regexp
from aiogram.dispatcher import Dispatcher

from keyboards import callbacks

from . import about, start, today, bay, kick, default


dispatcher = Dispatcher.get_current()

#start.py
dispatcher.register_message_handler(start.starting, CommandStart(), ChatTypeFilter('private'))

#faq.py
dispatcher.register_message_handler(about.about_bot_group, Command('help'), ChatTypeFilter(('group', 'supergroup')))
dispatcher.register_message_handler(about.about_bot_user, Command('help'), ChatTypeFilter('private'))

#today.py
dispatcher.register_message_handler(today.date, Command('date'))
dispatcher.register_message_handler(today.time, Command('time'))

#bay.py
dispatcher.register_callback_query_handler(bay.bay_menu, callbacks.back_bay.filter())
dispatcher.register_message_handler(bay.bay_menu, Command('bay'))

#kick.py
dispatcher.register_message_handler(kick.kick_user, Command('kick'))

#default.py
dispatcher.register_message_handler(default.other_command, Regexp(r'^/(\w+)$'))
