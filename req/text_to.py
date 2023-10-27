import json
import os
import time
import requests
from dotenv import load_dotenv



def text_to_speech(text: str) -> None:
    load_dotenv()
    headers = {"Authorization": f"Bearer {os.getenv('TOKEN')}"}
    url = 'https://api.edenai.run/v2/audio/text_to_speech'

    payload = {
        'providers': 'amazon',
        'language': 'ru-RU',
        # 'option': 'FEMALE',
        # 'lovoai': 'ru-RU_Anna Kravchuk',
        'option': 'MALE',
        'lovoai': 'ru-RU_Alexei Syomin',
        'text': f'{text}'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        result = json.loads(response.text)
        unx_time = int(time.time())
    except Exception:
       print('post error') 
    
    '''with open(f'{unx_time}.json', 'w') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)'''
    try:

        audio_url = result['amazon']['audio_resource_url']
        r = requests.get(audio_url)
        return r.content
    except Exception as e:
        print('get error',e)

def main():
    text_to_speech(text='написал не большой скрипт для перевода текста в голос, наверное этим голосом будут вести свой курс поо практики на питоне для новичков.. Оцените')


if __name__ == '__main__':
    main()
