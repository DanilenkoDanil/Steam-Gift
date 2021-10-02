import os

ma = []
for i in os.listdir():
    if 'maFile' in i:
        ma.append(i)


for mafile in ma:
    with open(mafile, 'r', encoding='utf8') as file:
        text = file.read()
        shared_secret = text.split('"shared_secret":"')[1].split('"')[0]
        print(shared_secret)
        identity_secret = text.split('"identity_secret":"')[1].split('"')[0]
        print(identity_secret)
        steam_id = text.split('"SteamID":"')[1].split('"')[0]
        print(steam_id)

        print(ma)

        file = open(f"{mafile.replace('maFile', 'txt')}", "w")
        file.write(f"""{{
    "steamid": "{steam_id}",
    "shared_secret": "{shared_secret}",
    "identity_secret": "{identity_secret}"
}}
        """)
        file.close()