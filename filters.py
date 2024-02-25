from config import bot


@bot.message_handler(is_forwarded=True)
async def forward_filter(message):
    await bot.send_message(message.chat.id, "Бот не принимает пересланные сообщения!")


@bot.message_handler(is_reply=True)
async def reply_filter(message):
    await bot.send_message(message.chat.id, "Бот не принимает ответы на сообщения!")


@bot.message_handler(
    func=lambda message: True,
    content_types=[
        'audio',
        'photo',
        'voice',
        'video',
        'document',
        'location',
        'contact',
        'sticker'
    ])
async def content_types_filter(message):
    await bot.send_message(message.chat.id, "Бот не поддерживает данный тип сообщения!")