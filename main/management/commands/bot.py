from django.core.management.base import BaseCommand
from main.models import Game, TelegramAccount, TelegramBot, Account
import requests
import json
import time
import telebot
import codecs
from steampy.client import SteamClient, GameOptions
from steampy.market import Currency
from steampy.exceptions import ApiException


def get_balance(login, password, key):
    file = {'shared_secret': key}
    with SteamClient('E753335BD1F5A4BB0247D27C6D4A8A68', login, password,  json.dumps(file)) as steam_client:
        return steam_client.get_wallet_balance()


def get_telegram_token(name: str) -> TelegramBot:
    return TelegramBot.objects.filter(name=name)[0]


def get_telegram_users() -> TelegramAccount:
    return TelegramAccount.objects.all()


def send_message(message, token, users):
    bot = telebot.TeleBot(token)
    for i in users:
        print(f"{i.user_id} - send")
        try:
            bot.send_message(i.user_id, message)
        except Exception as e:
            print(e)


def get_price(sub_id):
    link = f'http://store.steampowered.com/api/packagedetails?packageids={sub_id}'
    res = requests.get(link)
    result_dict = json.loads(res.content.decode('utf-8'))
    try:
        return int(result_dict[str(sub_id)]['data']['price']['final'])/100
    except KeyError:
        return 0


def scan_all():
    counter = 1
    for i in list(Game.objects.all()):
        if counter % 100 == 0:
            time.sleep(300)
        counter += 1
        print(i.sub_id)
        time.sleep(2)
        base_price = i.price
        try:
            current_price = get_price(i.sub_id)
        except Exception as e:
            print(e)
            continue
        print(current_price)
        if float(current_price) != float(base_price):
            message = f"""Изменение цены!
Игра - {i.name}
Было {base_price} - стало {current_price}"""

            token = get_telegram_token('price').key
            users = get_telegram_users()

            send_message(message, token, users)
            i.price = current_price
            i.save()

    for i in list(Account.objects.all()):
        print(i.steam_login)
        try:
            balance = get_balance(i.steam_login, i.steam_password, i.shared_secret)
            i.balance = balance
            i.save()
        except Exception as e:
            print(e)


class Command(BaseCommand):
    help = 'Проверка цен'

    def handle(self, *args, **options):
        while True:
            scan_all()
            time.sleep(1800)
