import requests
import json


def get_price(sub_id):
    link = f'http://store.steampowered.com/api/packagedetails?packageids={sub_id}'
    res = requests.get(link)
    result_dict = json.loads(res.content.decode('utf-8'))
    try:
        return int(result_dict[str(sub_id)]['data']['price']['final'])/100
    except KeyError:
        return 0


# +
