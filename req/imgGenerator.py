import json
import requests
from dotenv import load_dotenv
from os import getenv
import time


def image_generator(text: str):
    load_dotenv()
    headers = {"Authorization": f"Bearer {getenv('TOKEN')}"}

    url = "https://api.edenai.run/v2/image/generation"
    payload = {
        "providers": "openai",
        "text": F"{text}",
        "resolution": "512x512"
    }
    unx_time = int(time.time())
    try:

        response = requests.post(url, json=payload, headers=headers)
        result = json.loads(response.text)
    except Exception as errpr:
        return errpr
    '''with open('too.json', 'w') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)'''
    try:

        image_url1 = result['openai']['items'][0]['image_resource_url']
        r = requests.get(image_url1)
        print()

        with open(f'{unx_time}.jpg', 'wb', ) as file:
            file.write(r.content)
        return unx_time
    except Exception as e:
        print('get error',e)
 
def main():
    image_generator(text='утро программиста мужчины')


if __name__ == '__main__':
    main()

