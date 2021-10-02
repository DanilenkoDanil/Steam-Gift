import requests
import time
from hashlib import sha256
import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gift_bot.settings")
import django
django.setup()


def check_code(code: str, guid: str = '778B993F62CB4D7BA7A88EC68FFBDD71', seller_id: int = 325919):
    timestamp = str(int(time.time()))

    api_guid = guid + timestamp

    sign = sha256(api_guid.encode('utf-8')).hexdigest()

    data = {
        'seller_id': seller_id,
        'timestamp': timestamp,
        'sign': sign

    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post('https://api.digiseller.ru/api/apilogin', json=data, headers=headers)
    token_json = json.loads(response.content.decode('utf8'))
    print(token_json)
    try:
        token = token_json['token']
    except KeyError:
        time.sleep(10)
        response = requests.post('https://api.digiseller.ru/api/apilogin', json=data, headers=headers)
        token_json = json.loads(response.content.decode('utf8'))
        token = token_json['token']

    response = requests.get(f'https://oplata.info/api/purchases/unique-code/{code}?token={token}')
    result_json = json.loads(response.content.decode('utf8'))
    return result_json


from background_task.models import Task

# print(len(Task.objects.filter(task_params__contains="001C3FA9AC664346")))
# print(check_code('001C3FA9AC664346'))
# print(check_code('9A673DFE426B4679'))
