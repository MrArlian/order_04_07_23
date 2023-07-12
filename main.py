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


def main() -> None:
    from handlers.middleware import CheckPrivilege, CheckAdminRole

    dispatcher.setup_middleware(CheckAdminRole(('owner', 'super_user', 'user')))
    dispatcher.setup_middleware(CheckPrivilege())

    loop.create_task(
        bot.set_my_commands([
            types.BotCommand('/start', 'Начать использование бота.'),
            types.BotCommand('/help', 'Помощь и доступные команды.'),
            types.BotCommand('/bay', 'Приобретение подписок.'),
            types.BotCommand('/time', 'Текущее время.'),
            types.BotCommand('/date', 'Текущая дата.'),
        ])
    )

    try:
        executor.start_polling(dispatcher, loop=loop)
    finally:
        loop.run_until_complete(dispatcher.storage.close())


if __name__ == '__main__':
    main()
