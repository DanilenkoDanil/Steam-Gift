import requests


def get_name(link):
    res = requests.get(link)
    name = str(res.content).replace('\\t', '').replace('\\r', '').replace('\\n', '').split('Steam Community :: ')[1].split('</title>')[0]
    return name
