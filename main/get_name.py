import requests
import steamfront
import json


def get_name(link):
    res = requests.get(link)
    name = str(res.content).replace('\\t', '').replace('\\r', '').replace('\\n', '').split('Steam Community :: ')[1].split('</title>')[0]
    return name


def get_name_game(sub_id):
    link = f'http://store.steampowered.com/api/packagedetails?packageids={sub_id}'
    res = requests.get(link)
    result_dict = json.loads(res.content.decode('utf-8'))
    try:
        print(sub_id)
        print(result_dict)
        return result_dict[str(sub_id)]['data']['name']
    except KeyError:
        return "Не удалось получить имя"


# print(get_name_game('244390'))
