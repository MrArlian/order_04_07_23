import os

from pydantic import BaseSettings


root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class _Config(BaseSettings):

    TELEGRAM_TOKEN: str

    DATABASE_URL: str

    YOOMONEY_SHOP_ID: str
    YOOMONEY_API_KEY: str

    CALLBACK_URL: str

    PRODUCTS_FILE: str = os.path.join(root_dir, 'data', 'products.json')
    ROOT_DIR: str = root_dir

    class Config:
        env_file = os.path.join(root_dir, '.config', 'dev.ini')
        env_file_encoding = 'utf-8'

config = _Config()
