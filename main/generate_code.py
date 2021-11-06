from steam.guard import SteamAuthenticator


def generate(shared_secret):
    dict_secret = {'shared_secret': shared_secret}
    secrets = dict_secret
    sa = SteamAuthenticator(secrets)
    return str(sa.get_code())


# print(generate('+DXndp7GbTTJce1Ru75b6dZEt/g='))
