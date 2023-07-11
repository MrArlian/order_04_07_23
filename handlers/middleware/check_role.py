import typing

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram import types

from database import DataBase, models
from modules import Config
from data import settings


db = DataBase(Config.DATABASE_URL)


class CheckAdminRole(BaseMiddleware):
    __cache_roles = {}

    def __init__(self, roles: typing.Iterable[str]):
        self.roles = roles
        super(CheckAdminRole, self).__init__()

    async def on_process_message(self, message: types.Message, *_) -> None:

        text = (message.text or message.caption or '').lower()
        chat_type = message.chat.type

        if text.startswith('/admin') or text in settings.ADMIN_KEYBOARD:
            if chat_type == 'private':
                await self._check_role(message.chat.id)
            else:
                raise CancelHandler

    async def _check_role(self, user_id: int) -> None:
        if user_id not in self.__cache_roles:
            self.__cache_roles[user_id] = db.get_data(
                table=models.User,
                columns=models.User.role,
                id=user_id
            )

        if not self.__cache_roles[user_id]:
            raise CancelHandler
        if self.__cache_roles[user_id] not in self.roles:
            raise CancelHandler
