from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import Dispatcher

from keyboards import callbacks

from . import command, privilege, replenishment
from .. import states


dispatcher = Dispatcher.get_current()

#privilege.py
dispatcher.register_callback_query_handler(privilege.view, callbacks.privilege.filter())
dispatcher.register_callback_query_handler(privilege.purchase_type, callbacks.purchase_type.filter())
dispatcher.register_callback_query_handler(privilege.purchase, callbacks.bay_privilege.filter())

#privilege.py
dispatcher.register_callback_query_handler(replenishment.enter_amount, callbacks.replenishment.filter())
dispatcher.register_message_handler(replenishment.cancel, Text('отмена', ignore_case=True), state=states.Replenishment)
dispatcher.register_message_handler(replenishment.replenishment, state=states.Replenishment.amount)
