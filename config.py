import os
from dotenv import load_dotenv

from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
bot = AsyncTeleBot(os.getenv("TG_BOT_TOKEN"), state_storage=StateMemoryStorage())
catalog_id_yandex_cloud = os.getenv("CATALOG_ID_YANDEX_CLOUD")
api_key_yandex_cloud = os.getenv("API_KEY_YANDEX_CLOUD")
