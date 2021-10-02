import json
import requests


def getInventory(steamid):
    data = requests.get(
        "https://steamcommunity.com/id/{}/inventory/json/730/2?l=english&count=5000".format(steamid))
    print(data.text)
    json_data = json.loads(data.text)
    print(json_data)
    descriptions = json_data["rgDescriptions"]
    print([(descriptions[item]["name"], getItemAmount(descriptions[item]["classid"], json_data)) for item in descriptions])

print(getInventory('76561198843199462'))

def getItemAmount(classid, json_data):
    inventory = json_data["rgInventory"]
    count = 0
    for item in inventory:
        if inventory[item]["classid"] == classid:
            count += 1
    return count