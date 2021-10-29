import requests
import json


def get_price(app_id):
    url = "http://store.steampowered.com/api/appdetails/?appids={}".format(app_id)
    response = requests.get(url)
    j = response.json()
    pre_final_price = j["{}".format(app_id)]["data"]["price_overview"]["final"]
    final_price = float(pre_final_price) / 100

    return final_price


# print(get_price(644560))
