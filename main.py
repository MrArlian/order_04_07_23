import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types, executor

from modules import Config


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

bot = Bot(Config.TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
dispatcher = Dispatcher(bot, storage=MemoryStorage())

Dispatcher.set_current(dispatcher)
Bot.set_current(bot)


from database import DataBase, models

db =DataBase(Config.DATABASE_URL)

entity = (
    db.session.query(models.User.id).filter_by(id=0).union(
        db.session.query(models.Group.id).filter_by(id=0)
    )
).first()

print(entity)


def main() -> None:
    from handlers.middleware import CheckPrivilege, CheckAdminRole

    dispatcher.setup_middleware(CheckAdminRole(('owner', 'super_user', 'user')))
    dispatcher.setup_middleware(CheckPrivilege())

    try:
        executor.start_polling(dispatcher, loop=loop)
    finally:
        loop.run_until_complete(dispatcher.storage.close())


if __name__ == '__main__':
    # main()
    pass
