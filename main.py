import os
import asyncio

from telebot.asyncio_filters import ForwardFilter
from telebot.asyncio_filters import IsDigitFilter
from telebot.asyncio_filters import IsReplyFilter
from telebot.asyncio_filters import StateFilter

from config import bot
from config import basedir
from middleware import TokenMiddleware
from filters import forward_filter
from filters import reply_filter
from filters import content_types_filter


class Bot:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        bot.add_custom_filter(IsReplyFilter())
        bot.add_custom_filter(ForwardFilter())
        bot.add_custom_filter(StateFilter(bot))
        bot.add_custom_filter(IsDigitFilter())
        bot.setup_middleware(TokenMiddleware())

    @staticmethod
    async def polling():
        task1 = asyncio.create_task(bot.infinity_polling())
        await task1


if __name__ == "__main__":
    Bot.polling()