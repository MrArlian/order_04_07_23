import itertools

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram import Bot, types

from database import DataBase, models
from modules import Config, tools
from data import settings, texts


PRIVILEGES = tools.get_privilege(Config.PRODUCTS_FILE)
CHECK_COMMANDS = set(itertools.chain.from_iterable(
    _privilege.get('scope') for _privilege in PRIVILEGES.values()
))

db = DataBase(Config.DATABASE_URL)
bot = Bot.get_current()


class CheckPrivilege(BaseMiddleware):

    async def on_process_message(self, message: types.Message, *_) -> None:

        text = (message.text or message.caption or '')
        user_id = message.from_user.id
        chat_type = message.chat.type
        chat_id = message.chat.id

        command = text.split('/', maxsplit=1)[-1]


        if command in CHECK_COMMANDS and command not in settings.EXCLUDED_COMMANDS:
            if chat_type in ('group', 'supergroup'):
                await self._check_group_privilege(chat_id, user_id, command)
            elif chat_type == 'private':
                await self._check_user_privilege(user_id, command)

    async def _check_user_privilege(self, user_id: int, command: str) -> None:
        user_privilege = db.get_data(models.User, columns=models.User.privilege, id=user_id)

        if self._check_command_privilege(user_privilege, command):
            return

        await bot.send_message(user_id, texts.COMMAND_NOT_AVAILABLE)
        raise CancelHandler

    async def _check_group_privilege(self, group_id: int, user_id: int, command: str) -> None:
        group_privilege = db.get_data(models.Group, columns=models.Group.privilege, id=group_id)
        user_privilege = db.get_data(models.User, columns=models.User.privilege, id=user_id)

        if (
            self._check_command_privilege(group_privilege, command) or
            self._check_command_privilege(user_privilege, command)
        ):
            return

        if user_privilege is None:
            await bot.send_message(group_id, texts.START_BOT)
        else:
            await bot.send_message(group_id, texts.COMMAND_NOT_AVAILABLE)
        raise CancelHandler

    def _check_command_privilege(self, privilege: str, command: str) -> bool:
        data = PRIVILEGES.get(privilege)

        if data and command in data['scope']:
            return True
        return False
