# YandexGPT-Telegram_chatBot

## Description
Telegram chat bot with YandexGPT integration. Subscription checker. Flexible configuration via config

## Roadmap:
![image](https://github.com/kde2podfreebsd/YandexGPT-Telegram-Bot/assets/39852259/4326fad6-ae62-41bf-b5c8-4c1a4d56b9e2)

## config.json
```json
{
  "token_per_day_limit": 5,
  "prompt": "Ты ассистент по математике",
  "advertising_chat_url": "https://t.me/test_spam_chat",
  "start_message": "Стартовое сообщение",
  "subscribe_message": "*Подпишись на канал!*",
  "after_sub": "Задайте свой вопрос!"
}
```

* token_per_day_limit - Кол-во токенов в день
* prompt - Промпт для гпт нейросети
* advertising_chat_url - Ссылка на канал для подписки. Обязательно бот должен быть админом канала, для проверки подписки
* start_message - Стартовое сообщение
* subscribe_message - Сообщение при просьбе подписаться
* after_sub - Сообщение после успешной подписки

## .env
```.dotenv
CATALOG_ID_YANDEX_CLOUD=<yandex_cloud_catalog>
API_KEY_YANDEX_CLOUD=<yandex_cloud_api_token>
TG_BOT_TOKEN=<telegram_bot_token>
```

## Build & Run
### Clone & cd in work dir
```shell
git clone <repo_url>
cd repo/
```

### Build docker
```shell
docker build -t yandexgptbot .

DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
            Install the buildx component to build images with BuildKit:
            https://docs.docker.com/go/buildx/

Sending build context to Docker daemon   42.2MB
Step 1/5 : FROM python:3.11
 ---> 22140cbb3b0c
Step 2/5 : WORKDIR /app
 ---> Using cache
 ---> 92cf939d3426
Step 3/5 : COPY . .
 ---> 776a5a6354f9
Step 4/5 : RUN pip install --no-cache-dir -r requirements.txt
 ---> Running in 791122adac69
Collecting aiohttp==3.9.3 (from -r requirements.txt (line 1))

Removing intermediate container 791122adac69
 ---> fcbe7e7fc548
Step 5/5 : CMD ["python", "main.py"]
 ---> Running in e46c234ae777
Removing intermediate container e46c234ae777
 ---> c98785ebd79b
Successfully built c98785ebd79b
Successfully tagged yandexgptbot:latest
```

### Run docker
```shell
docker run -it yandexgptbot
```

