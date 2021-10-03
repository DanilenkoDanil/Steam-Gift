import random
import telebot

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from background_task import background

from main.models import Account, Game, Shop, Order, TelegramAccount, TelegramBot

from . import get_name
from . import get_friends
from . import send_gift
from . import api
from . import priority_list


def get_shops() -> Shop:
    return Shop.objects.all()


def send_message(message: str, token: str, users):
    bot = telebot.TeleBot(token, parse_mode=None)
    for i in users:
        print(f"{i.user_id} - send")
        try:
            bot.send_message(i.user_id, message)
        except Exception as e:
            print(e)
    bot.stop_bot()


@background
def add_friend(login, target_link, order_id, task_name):
    print(task_name)
    order = get_order_by_sell_code(order_id)
    bot = get_user_by_login(login)
    try:
        # send_gift.main_friend_add(bot.steam_login, bot.steam_password, bot.proxy, target_link)
        order.status = 'Accept the friend request from the bot'
        order.save()
        check_friends_list(login, order_id, bot.link, target_link, 'Check friends')
    except Exception as e:
        print(e)
        order.status = 'Add Friend Error!!!'
        order.save()


@background
def send_gift_to_user(login, order_code, task_name):
    print(task_name)
    bot = get_user_by_login(login)
    order = get_order_by_sell_code(order_code)
    target_name = get_name.get_name(order.user_link)
    game_link = f'https://store.steampowered.com/app/{order.game.app_code}'
    try:
        send_gift.main(bot.steam_login, bot.steam_password, target_name, game_link, bot.proxy)
        order.status = 'Gift sent'
        order.save()
    except Exception as e:
        print(e)
        order.status = 'Send Gift Error!!!'
        order.save()


# 5 СЕКУНД!
@background(schedule=5)
def check_friends_list(bot_login, order_code, bot_link, user_link, task_name):
    print(task_name)
    print('!!!!!!!!!!!!!!!!!!!!!1111111111111111111111111111')
    print(order_code)
    print(bot_link)
    print(user_link)
    print('!!!!!!!!!!!!!!!!!!!!!')
    try:
        result = get_friends.check_friends(bot_link, user_link)
        if result:
            print("Бот в друзьях")
            send_gift_to_user(bot_login, order_code, 'Send Gift')
        else:
            check_friends_list(bot_login, order_code, bot_link, user_link, task_name)
    except Exception as e:
        print(e)
        check_friends_list(bot_login, order_code, bot_link, user_link, task_name)


class DynamicStatusLoad(View):

    def get(self, request, *args, **kwargs):
        sell_code = request.GET.get('sell_code')
        order = get_order_by_sell_code(sell_code)
        obj = {
            'status': order.status
        }
        return JsonResponse({'data': obj})


def get_order_by_sell_code(code: str) -> Order:
    return Order.objects.filter(sell_code=code)[0]


def get_user(user_type: str) -> Account:
    return Account.objects.filter(type=user_type, status=None)[0]


def get_telegram_token(name: str) -> TelegramBot:
    return TelegramBot.objects.filter(name=name)[0]


def get_telegram_users() -> TelegramAccount:
    return TelegramAccount.objects.all()


def get_user_by_login(login: str) -> Account:
    return Account.objects.filter(steam_login=login, status=None)[0]


def get_user_by_country(country: str) -> Account:
    return Account.objects.filter(country=country, status=None)[0]


def get_user_by_id(number: str) -> Account:
    return Account.objects.filter(id=number, status=None)[0]


def get_game(product_code: str) -> Game:
    return Game.objects.filter(sell_code=product_code)[0]


def get_order(key: str):
    try:
        return Order.objects.filter(sell_code=key)[0]
    except IndexError:
        return False


def index(request):
    code = request.GET.get('uniquecode')
    order = get_order(code)
    if order is False:
        for i in get_shops():
            info = api.check_code(code, i.guid, i.seller_id)
            if info['retval'] == 0:

                game = get_game(info['id_goods'])
                game_code = game.app_code
                print('!!!!!!!!!!!!!!!!!!!!!!')
                print(type(game.priority_list))
                print('!!!!!!!!!!!!!!!!!!!!!!')
                if game.priority_list != '' and game.priority_list is not None:
                    country = info['options'][1]['value']
                    code = random.choice(priority_list.get_list(game.priority_list))
                    account = get_user_by_id(code)
                else:
                    country = info['options'][1]['value']
                    account = get_user_by_country(country)

                image_link = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game_code}/header.jpg"
                game_link = f'https://store.steampowered.com/app/{game_code}'

                user_link = info['options'][0]['value']

                order = Order(sell_code=code, bot=account, game=game, user_link=user_link, status='', country=country)
                order.save()

                add_friend(account.steam_login, user_link, code, 'Add to Friends')

                message = f"""Новая покупка!
Код - {code}
{game} - {user_link}"""

                token = get_telegram_token('info').key
                users = get_telegram_users()

                send_message(message, token, users)

                return render(request, 'main/account.html',
                              {'game_name': game.name,
                               'game_link': game_link,
                               'image_link': image_link,
                               'code': code,
                               'user_link': user_link,
                               'bot_link': account.link,
                               'region': country,
                               })
            else:
                continue

        html = f"Код {code} не действителен!"
        return HttpResponse(html)
    else:

        game_code = order.game.app_code
        image_link = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game_code}/header.jpg"
        game_link = f'https://store.steampowered.com/app/{game_code}'

        return render(request, 'main/account.html',
                      {'game_name': order.game.name,
                       'game_link': game_link,
                       'image_link': image_link,
                       'code': code,
                       'user_link': order.user_link,
                       'bot_link': order.bot.link,
                       'region': order.country,
                       })


def head(request):
    return render(request, 'main/head.html')
