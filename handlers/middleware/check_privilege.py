import itertools
import re

from datetime import datetime

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram import Bot, types

from database import DataBase, models
from modules import Config, tools
from data import settings, texts


PRIVILEGE = tools.get_privilege()
CHECK_COMMANDS = set(itertools.chain.from_iterable(
    _privilege.get('scope') for _privilege in PRIVILEGE.values()
))

db = DataBase(Config.DATABASE_URL)
bot = Bot.get_current()


class CheckPrivilege(BaseMiddleware):

    async def on_process_message(self, message: types.Message, *_) -> None:

        text = (message.text or message.caption or '')
        user_id = message.from_user.id
        chat_type = message.chat.type
        chat_id = message.chat.id

        match_command = re.search(r'(?<=\/)(\w*?)(?=@|$)', text, re.IGNORECASE)
        command = match_command.group() if match_command is not None else None

        if command in CHECK_COMMANDS and command not in settings.EXCLUDED_COMMANDS:
            if chat_type in ('group', 'supergroup'):
                await self._check_group_privilege(chat_id, user_id, command)
            elif chat_type == 'private':
                await self._check_user_privilege(user_id, command)

    async def _check_user_privilege(self, user_id: int, command: str) -> None:
        user = db.get_data(models.User, id=user_id)

        now = datetime.now()

        if user.expires_in <= now:
            await bot.send_message(user_id, texts.COMMAND_NOT_AVAILABLE)
            raise CancelHandler
        if not self._check_command_privilege(user.privilege, command):
            await bot.send_message(user_id, texts.COMMAND_NOT_AVAILABLE)
            raise CancelHandler

    async def _check_group_privilege(self, group_id: int, user_id: int, command: str) -> None:
        group = db.get_data(models.Group, id=group_id)
        user = db.get_data(models.User, id=user_id)

        now = datetime.now()

        if user is None:
            await bot.send_message(group_id, texts.START_BOT)
            raise CancelHandler
        if group.expires_in <= now and user.expires_in <= now:
            await bot.send_message(group_id, texts.COMMAND_NOT_AVAILABLE)
            raise CancelHandler
        if (
            not self._check_command_privilege(user.privilege, command) and
            not self._check_command_privilege(group.privilege, command)
        ):
            await bot.send_message(group_id, texts.COMMAND_NOT_AVAILABLE)
            raise CancelHandler

    def _check_command_privilege(self, privilege: str, command: str) -> bool:
        data = PRIVILEGE.get(privilege)

        if data and command in data['scope']:
            return True
        return False
