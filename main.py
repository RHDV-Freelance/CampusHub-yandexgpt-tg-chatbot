import asyncio
from datetime import datetime, timedelta
from telebot.asyncio_filters import ForwardFilter, IsDigitFilter, IsReplyFilter, StateFilter
from config import bot
from config import basedir
from controller import UserController
from filters import forward_filter, reply_filter, content_types_filter
from handlers import text_handler, start

from scheduler import scheduled_tasks


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
        self.scheduled_tasks = scheduled_tasks

    async def polling(self):
        task1 = asyncio.create_task(bot.infinity_polling())
        self.scheduled_tasks.run()
        await task1


if __name__ == "__main__":
    b = Bot()
    asyncio.run(b.polling())
    asyncio.get_event_loop().run_forever()
