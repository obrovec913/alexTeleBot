import json
import requests
from dotenv import load_dotenv
from os import getenv


def chat_generation(text: str, li=[]):
    load_dotenv()
    headers = {"Authorization": f"Bearer {getenv('TOKEN')}"}

    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": text,
        "chat_global_action": "Act as an assistant",
        "previous_history": li,
        "users":"ooo",
        "temperature": 0.0,
        "max_tokens": 3600,
    }
    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    return result['openai']['generated_text'], result['openai']['message']


def main():
    with open('too11.json', ) as file:
        op = json.load(file)

    chat_generation("напиши мне функцию калькулятор", op['openai']['message'])


if __name__ == '__main__':
    main()
