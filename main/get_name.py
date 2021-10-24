import requests
import steamfront


def get_name(link):
    res = requests.get(link)
    name = str(res.content).replace('\\t', '').replace('\\r', '').replace('\\n', '').split('Steam Community :: ')[1].split('</title>')[0]
    return name


def get_name_game(app_code):
    client = steamfront.Client()
    game = client.getApp(appid=app_code)
    return game.name
