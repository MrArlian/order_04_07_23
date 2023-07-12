#User
START_MESSAGE = (
    'Добро пожаловать, {:s}!\n\n'
    '{:s} - это чат-бот-менеджер для ваших групп/бесед.\n'
    'Список доступных команд доступен по: /help'
)

ABOUT_BOT_FOR_GROUP = (
    'Доступные команды:\n\n'
    'Стартовые команды.\n'
    '/help - Помощь и доступные команды.\n'
    '/bay - Приобретение подписок.\n'
    '/time - Текущее время.\n'
    '/date - Текущая дата.\n'
    '/kick - Выйти из группы.\n\n'
    'Id группы: {:d}'
)

ABOUT_BOT_FOR_USER = (
    'Доступные команды:\n\n'
    'Стартовые команды.\n'
    '/start - Начать использование бота.\n'
    '/help - Помощь и доступные команды.\n'
    '/bay - Приобретение подписок.\n'
    '/time - Текущее время.\n'
    '/date - Текущая дата.\n'
    '/kick - Выйти из группы.'
)

CHOOSE_PRIVILEGE = 'Выберите подписку.'

PRIVILEGE_NOT_FOUND = 'Оооупс. Подписка не найдена.'

PRIVILEGE_INFO = 'Название: {:s}\n\nДоступные команды:\n{:s}\n\nЦена: {:.2f} руб.'

PURCHASE_TYPE = 'Для кого подписка?'

INSUFFICIENT_FUNDS = 'Недостаточно средств для покупки.'

PRODUCT_PURCHASED = 'Спасибо за покупку.'

ENTER_REPLENISHMENT_AMOUNT = 'Введите сумму пополнения.'

INPUT_ERROR = 'Ошибка ввода! Попробуйте ввести число или используйте точку вместо запятой.'

PAYMENT_INFO = 'Сумма пополнения: {:.2f} руб.\nId заказа: {:d}'

PAYMENT = 'Нажмите на кнопку для оплаты. /bay чтобы вернутся к подпискам.'

ACTION_NOT_AVAILABLE = 'Вы не можете использовать эту кнопку.'

COMMAND_NOT_AVAILABLE = 'Эта команда недоступна для вас!'

START_BOT = 'Напишите /start в боте, чтобы использовать эту команду!'

CAN_NOT_USE = 'Эту команду можно использовать только в группе!'

DELETION_ERROR = 'Бот не может удалить администратора!'


#Admin
HELLO_ADMIN = 'Добро пожаловать в админ панель.'

INPUT_ENTITY = 'Введите ID/username пользователя.'

ERROR_INPUT_ENTITY = 'Неверный ID или username.'

ENTITY_NOT_FOUND = 'Пользователь или группа не найдены.'

INPUT_PRIVILEGE_NAME = 'Введите имя подписки.'

ADMIN_PRIVILEGE_NOT_FOUND = 'Подписка не найдена.'

PRIVILEGE_GRANTED = 'Подписка выдана'

PRIVILEGE_REVOKED = 'Подписка отозвана.'

ACTION_CANCELED = 'Действие отменено.'

BOT_STATISTICS = (
    'Доход за все время: {:.2f}\n'
    'Доход за неделю: {:.2f}\n\n'
    'Кол-во пользователей: {:d}\n'
    'кол-во бесед: {:d}'
)
