import requests
import steam.steamid
import json

KEY = 'E753335BD1F5A4BB0247D27C6D4A8A68'


def check_friends(bot_link, user_link):
    steam_id_user = steam.steamid.from_url(user_link)
    steam_id_bot = steam.steamid.from_url(bot_link)
    print(steam_id_user)

    response = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'
                            f'?key={KEY}&steamid={steam_id_bot}&relationship=friend')
    json_data = json.loads(response.text)
    friends = json_data['friendslist']['friends']
    for i in friends:
        if i['steamid'] == str(steam_id_user):
            return True

    return False


# res = check_friends('https://steamcommunity.com/id/Elaine11199987125/', 'https://steamcommunity.com/profiles/76561198843199462')
# print(res)
