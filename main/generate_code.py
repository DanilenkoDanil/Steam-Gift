from steam.guard import SteamAuthenticator
import json
import os


def generate(username):
    secrets = json.load(open(f'{os.getcwd()}/main/guard/{username}.txt'))

    sa = SteamAuthenticator(secrets)
    return sa.get_code()
