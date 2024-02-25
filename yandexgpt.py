import json
import requests

from pathlib import Path

from config import basedir
from config import api_key_yandex_cloud
from config import catalog_id_yandex_cloud


class YandexChatGPT:

    with open("config.json", "r", encoding="utf-8") as file:
        config_json = json.load(file)

    _tokens_per_day: int = config_json['TOKEN_PER_DAY_LIMIT']
    _chat_version: str = "gpt"
    _model: str = "yandexgpt-lite"
    _stream: bool = False
    _temperature: float = 0.6
    _max_tokens: int = 2000
    _url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    _headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {api_key_yandex_cloud}"
    }

    @classmethod
    def sync_prompt(cls, chat_id: str, prompt: str):
        chat_history_file = Path(f"{basedir}/chats/{chat_id}_history.json")
        if chat_history_file.exists():
            with open(chat_history_file, "r", encoding="utf-8") as file:
                messages_history = json.load(file)
        else:
            messages_history = []

        system_prompt = cls.load_system_prompt()
        messages_history.insert(0, system_prompt)

        user_prompt = {"role": "user", "text": prompt}
        messages_history.append(user_prompt)

        payload = {
            "modelUri": f"{cls._chat_version}://{catalog_id_yandex_cloud}/{cls._model}",
            "completionOptions": {
                "stream": cls._stream,
                "temperature": cls._temperature,
                "maxTokens": cls._max_tokens
            },
            "messages": messages_history
        }

        response = requests.post(cls._url, headers=cls._headers, json=payload)
        result = response.json()

        assistant_response = result["result"]["alternatives"][0]["message"]
        messages_history.append(assistant_response)

        with open(chat_history_file, "w", encoding="utf-8") as file:
            json.dump(messages_history, file, ensure_ascii=False, indent=2)

        return assistant_response['text']

    @staticmethod
    def load_system_prompt():
        system_prompt_file = "config.json"
        with open(system_prompt_file, "r", encoding="utf-8") as file:
            system_prompt = json.load(file)
        return {"role": "system", "text": system_prompt['PROMPT']}


if __name__ == "__main__":
    chat_id = "user123"
    user_prompt_text = "Напиши код на python для нахождения дискриминанта"
    response = YandexChatGPT.sync_prompt(chat_id, user_prompt_text)
    print(response)
