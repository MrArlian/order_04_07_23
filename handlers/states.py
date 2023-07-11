from aiogram.dispatcher.filters.state import State, StatesGroup


#User
class Replenishment(StatesGroup):
    amount = State()

#Admin
class GrantPrivilege(StatesGroup):
    user = State()
    privilege = State()

class RevokePrivilege(StatesGroup):
    user = State()
