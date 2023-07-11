from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import Dispatcher

from .. import states

from . import command, grant_privilege, revoke_privilege, statistics


dispatcher = Dispatcher.get_current()

#grant_privilege.py
dispatcher.register_message_handler(grant_privilege.enter_user, Text('выдать', ignore_case=True))
dispatcher.register_message_handler(grant_privilege.cancel, Text('отмена', ignore_case=True), state=states.GrantPrivilege)
dispatcher.register_message_handler(grant_privilege.enter_privilege, state=states.GrantPrivilege.user)
dispatcher.register_message_handler(grant_privilege.grant, state=states.GrantPrivilege.privilege)

#revoke_privilege.py
dispatcher.register_message_handler(revoke_privilege.enter_user, Text('забрать', ignore_case=True))
dispatcher.register_message_handler(grant_privilege.cancel, Text('отмена', ignore_case=True), state=states.RevokePrivilege)
dispatcher.register_message_handler(revoke_privilege.revoke, state=states.RevokePrivilege.user)

#statistics.py
dispatcher.register_message_handler(statistics.bot_statistics, Text('статистика', ignore_case=True))
