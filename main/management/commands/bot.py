from django.core.management.base import BaseCommand
from main.models import Game, TelegramAccount, TelegramBot
import requests
import json
import time
import telebot


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


def get_price(app_id):
    url = "http://store.steampowered.com/api/appdetails/?appids={}".format(app_id)
    response = requests.get(url)
    j = response.json()

    pre_final_price = j["{}".format(app_id)]["data"]["price_overview"]["final"]
    final_price = float(pre_final_price) / 100

    return final_price


def scan_all():
    for i in list(Game.objects.all()):
        print(i.app_code)
        time.sleep(2)
        base_price = i.price
        try:
            current_price = get_price(i.app_code)
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


class Command(BaseCommand):
    help = 'Проверка цен'

    def handle(self, *args, **options):
        while True:
            scan_all()
            time.sleep(1800)
