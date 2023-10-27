import json
import requests
from dotenv import load_dotenv
from os import getenv

def speech_recognition(fileame="", fi=''):
    load_dotenv()
    headers = {"Authorization": f"Bearer {getenv('TOKEN')}"}

    url="https://api.edenai.run/v2/audio/speech_to_text_async"
    data={"providers": "openai","language": "ru-RU"}

    files = {'file': open(f"{fileame}",'rb')}

    response = requests.post(url, data=data, files=files, headers=headers)
    result = json.loads(response.text)
    url_get = f'https://api.edenai.run/v2/audio/speech_to_text_async/{result["public_id"]}'
    res = requests.get(url_get, headers=headers)
    sn = json.loads(res.text)    
    res_text = sn["results"]['openai']['text']
    
    with open(f'{fi}.txt', 'w', encoding='utf-8') as file:
        file.write(res_text)
        



def main():
    print('Запущен процесс транскрибации, пожалуйста ожидайте...')
    speech_recognition()


if __name__ == '__main__':
    main()
