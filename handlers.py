import json
from controller import UserController
from config import bot
from yandexgpt import YandexChatGPT
from datetime import datetime, timedelta
from telebot import types
import re


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
        await bot.send_message(chat_id=message.chat.id, text=response_text, parse_mode="MARKDOWN")
        UserController.update_start_state(chat_id=message.chat.id, new_start_state=False)

        await sub_message(message)

    else:
        tokens_count = UserController.get_token_count(chat_id=message.chat.id)

        if tokens_count > 0:
            UserController.deduct_tokens(chat_id=message.chat.id, tokens_to_deduct=1)
            response_text = YandexChatGPT.sync_prompt(chat_id=message.chat.id, prompt=message.text)
            await bot.send_message(chat_id=message.chat.id, text=response_text, parse_mode="MARKDOWN")

            tokens_count = UserController.get_token_count(chat_id=message.chat.id)

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

    match = re.search(r'/([^/]+)$', data['advertising_chat_url'])

    if match:
        last_channel_name = match.group(1)

    await bot.send_message(
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
                        callback_data="subscribed"
                    )
                ]
            ]
        )
    )