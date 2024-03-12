import json
from controller import UserController
from config import bot
from yandexgpt import YandexChatGPT
from datetime import datetime, timedelta
from telebot import types
import re
from scheduler import scheduled_tasks

uc = UserController()


@bot.message_handler(commands=["start"])
async def start(message):
    if UserController.CONFIG_FILE.exists():
        with open(UserController.CONFIG_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    UserController.create_user(chat_id=message.chat.id, prompt=data['prompt'], tokens=data['token_per_day_limit'])

    await bot.send_message(chat_id=message.chat.id, text=data['start_message'], parse_mode="MARKDOWN")


@bot.message_handler(content_types=['text'])
async def text_handler(message):
    if UserController.get_start_state(chat_id=message.chat.id):
        response_text = YandexChatGPT.sync_prompt(chat_id=message.chat.id, prompt=message.text)
        try:
            await bot.send_message(chat_id=message.chat.id, text=response_text, parse_mode="MARKDOWN")
        except Exception:
            response_text = YandexChatGPT.sync_prompt(chat_id=message.chat.id, prompt=message.text)
            await bot.send_message(chat_id=message.chat.id, text=response_text, parse_mode="MARKDOWN")

        UserController.clear_message_history(chat_id=message.chat.id)
        UserController.update_start_state(chat_id=message.chat.id, new_start_state=False)

        await _go_subscribe(chat_id=message.chat.id)

    else:

        if UserController.CONFIG_FILE.exists():
            with open(UserController.CONFIG_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

        match = re.search(r'/([^/]+)$', data['advertising_chat_url'])

        if match:
            last_channel_name = match.group(1)

        is_member = await bot.get_chat_member(f'@{last_channel_name}', message.chat.id)

        if is_member.status == 'left':
            await _go_subscribe(chat_id=message.chat.id)

        else:
            tokens_count = UserController.get_token_count(chat_id=message.chat.id)

            if tokens_count > 1:

                UserController.deduct_tokens(chat_id=message.chat.id, tokens_to_deduct=1)
                response_text = YandexChatGPT.sync_prompt(chat_id=message.chat.id, prompt=message.text)

                try:
                    await bot.send_message(chat_id=message.chat.id, text=response_text, parse_mode="MARKDOWN")
                except Exception:
                    response_text = YandexChatGPT.sync_prompt(chat_id=message.chat.id, prompt=message.text)
                    await bot.send_message(chat_id=message.chat.id, text=response_text, parse_mode="MARKDOWN")

                UserController.clear_message_history(chat_id=message.chat.id)

                tokens_count = UserController.get_token_count(chat_id=message.chat.id)

                if tokens_count > 0:

                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=f"❗️ У вас осталось {tokens_count} токенов.",
                        parse_mode="html"
                    )

                else:

                    if UserController.CONFIG_FILE.exists():
                        with open(UserController.CONFIG_FILE, "r", encoding="utf-8") as file:
                            data = json.load(file)

                    tomorrow = datetime.now() + timedelta(days=1)
                    tomorrow_at_midnight = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
                    formatted_date = tomorrow_at_midnight.strftime("%H:%M:%S %d.%m.%Y")

                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=f'''
❗️ У вас осталось {tokens_count} токенов.
 Токены обновятся *{formatted_date}* по Москве (GMT+3) и вы получите: *{data['token_per_day_limit']} токенов*.
❗️ 1 токен = 1 запрос
    ''',
                        parse_mode="MARKDOWN"
                    )

            elif tokens_count == 1:

                UserController.deduct_tokens(chat_id=message.chat.id, tokens_to_deduct=1)
                response_text = YandexChatGPT.sync_prompt(chat_id=message.chat.id, prompt=message.text)

                try:
                    await bot.send_message(chat_id=message.chat.id, text=response_text, parse_mode="MARKDOWN")
                except Exception:
                    response_text = YandexChatGPT.sync_prompt(chat_id=message.chat.id, prompt=message.text)
                    await bot.send_message(chat_id=message.chat.id, text=response_text, parse_mode="MARKDOWN")

                UserController.clear_message_history(chat_id=message.chat.id)

                tokens_count = UserController.get_token_count(chat_id=message.chat.id)

                if tokens_count > 0:

                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=f"❗️ У вас осталось {tokens_count} токенов.",
                        parse_mode="html"
                    )

                else:

                    if UserController.CONFIG_FILE.exists():
                        with open(UserController.CONFIG_FILE, "r", encoding="utf-8") as file:
                            data = json.load(file)

                    tomorrow = datetime.now() + timedelta(days=1)
                    tomorrow_at_midnight = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
                    formatted_date = tomorrow_at_midnight.strftime("%H:%M:%S %d.%m.%Y")

                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=f'''
❗️ У вас осталось {tokens_count} токенов.
Токены обновятся *{formatted_date}* по Москве (GMT+3) и вы получите: *{data['token_per_day_limit']} токенов*.
❗️ 1 токен = 1 запрос
''',
                        parse_mode="MARKDOWN"
                    )

                    await bot.send_photo(
                        chat_id=message.chat.id,
                        photo=open(r'banners/1.png', 'rb'),
                        caption='''
Ой-ой, кажется, все твои токены закончились! 

<b>Хочешь получить еще 2 токена? Тогда подпишись на Кампус Хаб 🤖 </b>

В нашем боте тебя встретит <b>искусственный интеллект, запрограммированный специально для помощи студентам и ученикам! 👇 </b>

Наш ИИ:

🔹 Поможет тебе решить любую задачу, тест или уравнение;

🔹 Напишет любую контрольную или учебную работу, а еще быстро найдет ответы;

🔹 Сделает любой текст лучше, проверит его на ошибки или даже составит его за тебя.


Переходи в бот, подписывайся и получай 2 токена прямо сейчас! ✅

''',
                        parse_mode='html',
                        reply_markup=types.InlineKeyboardMarkup(
                            row_width=2,
                            keyboard=[
                                [
                                    types.InlineKeyboardButton(
                                        text="Забрать 2 токена!",
                                        url="https://t.me/edu24_bot/kampus_ai/?entry=codbot_1",
                                    )
                                ]
                            ]
                        )
                    )

                    await scheduled_tasks.add_async_task1(user_id=message.chat.id)
                    await scheduled_tasks.add_async_task2(user_id=message.chat.id)
                    await scheduled_tasks.add_async_task3(user_id=message.chat.id)

            else:

                if UserController.CONFIG_FILE.exists():
                    with open(UserController.CONFIG_FILE, "r", encoding="utf-8") as file:
                        data = json.load(file)

                tomorrow = datetime.now() + timedelta(days=1)
                tomorrow_at_midnight = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
                formatted_date = tomorrow_at_midnight.strftime("%H:%M:%S %d.%m.%Y")

                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f'''
🚫 У вас {tokens_count} токенов.
🔁 Токены обновятся *{formatted_date}* по Москве (GMT+3) и вы получите: *{data['token_per_day_limit']} токенов*.
❗️ 1 токен = 1 запрос
    ''',
                    parse_mode="MARKDOWN"
                )


async def sub_message(message):
    if UserController.CONFIG_FILE.exists():
        with open(UserController.CONFIG_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    msg = await bot.send_message(
        chat_id=message.chat.id,
        text=data['subscribe_message'],
        parse_mode="MARKDOWN",
        reply_markup=types.InlineKeyboardMarkup(
            row_width=2,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        "➕ Подписаться",
                        url=data['advertising_chat_url'],
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "✅ Я уже подписан",
                        callback_data=f"sub:{message.chat.id}"
                    )
                ]
            ]
        )
    )

    uc.add_message_id(user_id=message.chat.id, message_id=msg.message_id)


async def _not_subbed(chat_id: int | str) -> None:
    if UserController.CONFIG_FILE.exists():
        with open(UserController.CONFIG_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    await uc.delete_message_id(user_id=chat_id)

    msg = await bot.send_message(
        chat_id=chat_id,
        text=data['subscribe_message'],
        reply_markup=types.InlineKeyboardMarkup(
            row_width=2,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        "➕ Подписаться",
                        url=data['advertising_chat_url'],
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "✅ Я уже подписан",
                        callback_data=f"sub:{chat_id}"
                    )
                ]
            ]
        ),
        parse_mode="MARKDOWN",
        disable_web_page_preview=False
    )

    uc.add_message_id(user_id=chat_id, message_id=msg.message_id)


async def _subbed(chat_id: int | str) -> None:
    await uc.delete_message_id(user_id=chat_id)

    if UserController.CONFIG_FILE.exists():
        with open(UserController.CONFIG_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    await bot.send_message(
        chat_id=chat_id,
        text=data['after_sub'],
        reply_markup=None,
        parse_mode="MARKDOWN",
    )


async def _go_subscribe(chat_id: int | str) -> None:
    if UserController.CONFIG_FILE.exists():
        with open(UserController.CONFIG_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    match = re.search(r'/([^/]+)$', data['advertising_chat_url'])

    if match:
        last_channel_name = match.group(1)

    is_member = await bot.get_chat_member(f'@{last_channel_name}', chat_id)

    await uc.delete_message_id(user_id=chat_id)

    if is_member.status != 'left':
        await _subbed(chat_id=chat_id)
    else:
        await _not_subbed(chat_id=chat_id)


@bot.callback_query_handler(func=lambda call: True)
async def callback_handler(call):
    if "sub" in call.data:
        response = call.data.split(':')
        user_id = int(response[1])

        await _go_subscribe(user_id)

    if "clear" in call.data:
        await bot.answer_callback_query(callback_query_id=call.id, text="♻️ История переписки очищена", show_alert=True)
