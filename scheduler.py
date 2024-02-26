from datetime import datetime, timezone, timedelta

from config import bot
from controller import UserController
from apscheduler.triggers.cron import CronTrigger


class ScheduledTasks:

    _instance = None

    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.existing_jobs = {}

    async def process(self):
        UserController.update_all_tokens()
        users_chatids = UserController.get_all_chat_ids()

        try:
            for chat_id in users_chatids:
                await bot.send_message(chat_id=chat_id, text="🔁 Токены обновлены!")

        except Exception:
            pass

    def run(self):
        moscow_tz = timezone(timedelta(hours=3))

        trigger = CronTrigger(hour=0, minute=0, second=0, timezone=moscow_tz)

        job_id = "daily_task"
        self.scheduler.add_job(
            self.process, trigger, id=job_id, misfire_grace_time=30, coalesce=True
        )
        self.scheduler.start()