from telebot.asyncio_handler_backends import BaseMiddleware
from telebot.asyncio_handler_backends import CancelUpdate
from telebot.asyncio_handler_backends import ContinueHandling

from config import bot


class TokenMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()
        self.update_types = ["message"]

    async def pre_process(self, message, data):
        pass