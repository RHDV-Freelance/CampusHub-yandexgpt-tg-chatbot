from datetime import datetime, timezone, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import bot
from controller import UserController
from apscheduler.triggers.cron import CronTrigger
from telebot import types


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

    async def add_async_task1(self, user_id):
        job_id1 = f"async_task1_{user_id}"
        trigger_time_1 = datetime.now() + timedelta(hours=1)

        self.scheduler.add_job(
            self.task1,
            'date',
            run_date=trigger_time_1,
            id=job_id1,
            misfire_grace_time=30,
            kwargs={'user_id': user_id}
        )

    async def add_async_task2(self, user_id):
        job_id2 = f"async_task2_{user_id}"
        trigger_time_2 = datetime.now() + timedelta(hours=25)

        self.scheduler.add_job(
            self.task2,
            'date',
            run_date=trigger_time_2,
            id=job_id2,
            misfire_grace_time=30,
            kwargs={'user_id': user_id}
        )

    async def add_async_task3(self, user_id):
        job_id3 = f"async_task3_{user_id}"
        trigger_time_3 = datetime.now() + timedelta(hours=73)

        self.scheduler.add_job(
            self.task3,
            'date',
            run_date=trigger_time_3,
            id=job_id3,
            misfire_grace_time=30,
            kwargs={'user_id': user_id}
        )

    async def task1(self, user_id):
        await bot.send_photo(
            chat_id=user_id,
            photo=open(r'banners/3.png', 'rb'),
            caption='''
Как тебе наш искусственный интеллект? Отличная современная шпаргалка для студентов, да? 😀

<b>Хочешь, чтобы он всегда был у тебя под рукой? 📲</b>

Оформи подписку на экосистему Кампус и получи:

🔹<b>10 токенов на использование Искусственного интеллекта Кампус:</b>
Он уже знает ответ на любой твой вопрос по учебе, а еще поможет решить задачу или составить текст для работы 🤖

🔹 <b>2 запроса в Кампус Библиотеку:</b>
Больше не нужно решать скучные или сложные задания самостоятельно или тратить время на поиск решения – просто открой нашу Библиотеку, там уже все есть! 📚
 
🔹 <b>299 бонусных рублей на Кампус Эксперт:</b>
Ты можешь попросить помощи с любой студенческой работой у профессионала в этой области и потратить бонусные рубли на его услуги.

Ну что, начнем учиться без проблем? 😉
Тебе понравится Кампус! 👇
        ''',
            parse_mode='html',
            reply_markup=types.InlineKeyboardMarkup(
                row_width=2,
                keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text="Оформить подписку 🔥",
                            url="https://kampus.ai/ecosystem/subscription/?entry=codbot_2 ",
                        )
                    ]
                ]
            )
        )

    async def task2(self, user_id):
        await bot.send_photo(
            chat_id=user_id,
            photo=open(r'banners/5.png', 'rb'),
            caption='''
Кампус – твой помощник в учебе 🤖

Он создан специально для студентов, так что <b>если ты учишься – Кампус создан специально для тебя! ❤️</b>

<b>С Кампус ты сможешь:</b>

<b>➕ Решать верно даже самые сложные тесты</b>, придуманные твоим преподавателем лично, всего за считанные минуты;
<b>➕ Сдавать без проблем все тесты</b>, зачеты и контрольные, даже если не успел подготовиться или переволновался перед экзаменом 😉
<b>➕ Делегировать дела по учебе</b>, которые отнимают слишком много времени или нервов 😀
<b>➕ Экономить время на скучных или непрофильных предметах</b>, чтобы погрузиться в то, что тебе действительно интересно. 

<b>Месячная подписка на Кампус стоит как шаурма около твоего универа, а пользы в подписке горааааздо больше! Убедись сам 🔥</b>
''',
            parse_mode='html',
            reply_markup=types.InlineKeyboardMarkup(
                row_width=2,
                keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text="Хочу подписку на Кампус!",
                            url="https://kampus.ai/ecosystem/subscription/?entry=codbot_2 ",
                        )
                    ]
                ]
            )
        )

    async def task3(self, user_id):
        await bot.send_photo(
            chat_id=user_id,
            photo=open(r'banners/6.png', 'rb'),
            caption='''
Может, Кампус не для тебя? 😱 Если… 👇

❌ Ты уже <b>закончил университет;</b>
❌ <b>Тебя мало волнует</b> наличие свободного времени;

Это не про тебя? Хочешь:

✅ <b>Учиться легко и без стресса</b>, получая хорошие оценки? 😎 
✅ <b>Иметь под рукой правильные ответы</b> и готовые решения? 
✅ <b>Отдать задания на выполнение Кампусу</b>, освободив свое время для важных дел или долгожданного сна? 

Оформляй месячную подписку на Кампус <b> всего за 299 руб 👌</b>


👍Ты получишь Искусственный интеллект, <b>который найдет ответы на тест, напишет текст или решит задачу за тебя. </b>

👍<b>Кампус Библиотеку</b>, где собраны готовые решения и материал для учебы. 


👍<b>И бонусные 299 рублей на Кампус Эксперт</b>, который поможет с любой студенческой работой! 


Ну что, начнем учиться без проблем? 😉

                        ''',
            parse_mode='html',
            reply_markup=types.InlineKeyboardMarkup(
                row_width=2,
                keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text="Беру подписку 🎉",
                            url="https://kampus.ai/ecosystem/subscription/?entry=codbot_2 ",
                        )
                    ]
                ]
            )
        )


scheduler = AsyncIOScheduler()
scheduled_tasks = ScheduledTasks(scheduler)
