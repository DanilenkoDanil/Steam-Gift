import random
import telebot

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from background_task import background

from main.models import Account, Game, Shop, Order, TelegramAccount, TelegramBot, Handmade, Status

from . import get_name
from . import get_friends
from . import send_gift
from . import api
from . import priority_list


def get_shops() -> Shop:
    return Shop.objects.all()


def send_message(message, token, users):
    bot = telebot.TeleBot(token.replace(" ", ""))
    for i in users:
        print(f"{i.user_id} - send")
        bot.send_message(i.user_id, message)
        print("Yes")

@background
def add_friend(login, target_link, order_id, task_name):
    print(task_name)
    order = get_order_by_sell_code(order_id)
    bot = get_user_by_login(login)
    try:
        send_gift.main_friend_add(bot.steam_login, bot.steam_password, bot.shared_secret, bot.proxy, target_link)
        order.status = 'Accept Request'
        order.save()
        check_friends_list(login, order_id, bot.link, target_link, 'Check friends')
    except Exception as e:
        print(e)
        order.status = 'Add Friend Error'
        order.save()


@background
def remove_friend(login, target_link, order_id, task_name):
    print(task_name)
    order = get_order_by_sell_code(order_id)
    bot = get_user_by_login(login)
    try:
        send_gift.main_friend_add(bot.steam_login, bot.steam_password, bot.shared_secret, bot.proxy, target_link)
        order.status = 'Accept Request'
        order.save()
        check_friends_list(login, order_id, bot.link, target_link, 'Check friends')
    except Exception as e:
        print(e)
        order.status = 'Add Friend Error'
        order.save()


@background
def check_gift_status(login, target_name, order_id, task_name):
    print(task_name)
    order = get_order_by_sell_code(order_id)
    order.check_count += 1
    order.save()
    bot = get_user_by_login(login)
    game_name = order.game.name
    try:
        if order.check_count < 6:
            status = send_gift.check_gift_status(bot.steam_login, bot.steam_password, bot.shared_secret, bot.proxy, target_name, game_name)
            if status == 'Submitted':
                order.status = 'Gift Sent'
                order.save()
                check_gift_status(login, target_name, order_id, task_name, schedule=1200)
            elif status == 'Received':
                order.status = 'Gift Received'
                order.save()

                message = f"""Гифт принят!
                Код - {order_id}
                {order.game.name} - {target_name}"""

                token = get_telegram_token('info').key
                users = get_telegram_users()

                send_message(message, token, users)

            elif status == 'Rejected':
                order.status = 'Gift Rejected'
                order.save()

                message = f"""Гифт Отклонён!
                Код - {order_id}
                {order.game.name} - {target_name}"""

                token = get_telegram_token('info').key
                users = get_telegram_users()

                send_message(message, token, users)
        else:
            print('Слишком много проверок, статус больше не обновляеться')
    except Exception as e:
        print(e)
        order.status = 'Check Error'
        order.save()


@background
def send_gift_to_user(login, order_code, task_name):
    print(task_name)
    bot = get_user_by_login(login)
    order = get_order_by_sell_code(order_code)
    target_name = get_name.get_name(order.user_link)
    game_link = f'https://store.steampowered.com/app/{order.game.app_code}'
    try:
        send_gift.main(bot.steam_login, bot.steam_password, bot.shared_secret, target_name, game_link, order.game.sub_id, bot.proxy)
        order.status = 'Gift Sent'
        order.save()
        check_gift_status(login, target_name, order_code, 'Check Gift Status', schedule=120)
    except Exception as e:
        print(e)

        order.status = 'Send Gift Error'
        order.save()

        message = f"""Произошёл сбой в отправке гифта!
Код - {order_code}
{order.game.name} - {target_name}"""

        token = get_telegram_token('info').key
        users = get_telegram_users()

        send_message(message, token, users)


@background(schedule=30)
def check_friends_list(bot_login, order_code, bot_link, user_link, task_name):
    print(task_name)
    print('!!!!!!!!!!!!!!!!!!!!!1111111111111111111111111111')
    print(order_code)
    print(bot_link)
    print(user_link)
    order = get_order_by_sell_code(order_code)
    print('!!!!!!!!!!!!!!!!!!!!!')
    try:
        result = get_friends.check_friends(bot_link, user_link)
        if result:
            print("Бот в друзьях")
            order.status = 'Sending Gift'
            order.save()
            send_gift_to_user(bot_login, order_code, 'Send Gift')
        else:
            check_friends_list(bot_login, order_code, bot_link, user_link, task_name)
    except Exception as e:
        print(e)
        check_friends_list(bot_login, order_code, bot_link, user_link, task_name)


@background(schedule=2)
def check_friends_list_first(bot_login, order_code, bot_link, user_link, task_name):
    print(task_name)
    print('!!!!!!!!!!!!!!!!!!!!!1111111111111111111111111111')
    print(order_code)
    print(bot_link)
    print(user_link)
    order = get_order_by_sell_code(order_code)
    print('!!!!!!!!!!!!!!!!!!!!!')
    try:
        result = get_friends.check_friends(bot_link, user_link)
        if result:
            print("Бот в друзьях")
            order.status = 'Sending Gift'
            order.save()
            send_gift_to_user(bot_login, order_code, 'Send Gift')
        else:
            add_friend(bot_login, user_link, order_code, 'Add to Friends')
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
    return Account.objects.filter(type=user_type)[0]


def get_telegram_token(name: str) -> TelegramBot:
    return TelegramBot.objects.filter(name=name)[0]


def get_telegram_users() -> TelegramAccount:
    return TelegramAccount.objects.all()


def get_user_by_login(login: str) -> Account:
    return Account.objects.filter(steam_login=login)[0]


def get_user_by_country(country: str) -> Account:
    return Account.objects.filter(country=country)[0]


def get_user_by_id(number: str) -> Account:
    return Account.objects.filter(id=number)[0]


def get_game(product_code: str) -> Game:
    return Game.objects.filter(sell_code=product_code)[0]


def get_status(status_type: str, lang: str):
    return Status.objects.filter(status_type=status_type, lang=lang)[0]


def get_order(key: str):
    try:
        return Order.objects.filter(sell_code=key)[0]
    except IndexError:
        return False


def get_handmade(key: str):
    try:
        return Handmade.objects.filter(code=key)[0]
    except IndexError:
        return False


def index(request):

    code = request.GET.get('uniquecode')
    order = get_order(code)
    if order is False:
        for i in get_shops():
            info = api.check_code(code, i.guid, i.seller_id)
            if info['retval'] == 0:

                add_to_friends_ru = get_status('Add to Friends', 'ru')
                add_to_friends_en = get_status('Add to Friends', 'eng')
                sending_gift_ru = get_status('Sending Gift', 'ru')
                sending_gift_en = get_status('Sending Gift', 'eng')
                check_error_ru = get_status('Check Error', 'ru')
                check_error_en = get_status('Check Error', 'eng')
                send_gift_error_ru = get_status('Send Gift Error', 'ru')
                send_gift_error_en = get_status('Send Gift Error', 'eng')
                add_friend_error_en = get_status('Add Friend Error', 'eng')
                add_friend_error_ru = get_status('Add Friend Error', 'ru')
                gift_rejected_en = get_status('Gift Rejected', 'eng')
                gift_rejected_ru = get_status('Gift Rejected', 'ru')
                gift_received_en = get_status('Gift Received', 'eng')
                gift_received_ru = get_status('Gift Received', 'ru')
                gift_sent_en = get_status('Gift Sent', 'eng')
                gift_sent_ru = get_status('Gift Sent', 'ru')
                accept_request_ru = get_status('Accept Request', 'ru')
                accept_request_en = get_status('Accept Request', 'eng')

                game = get_game(info['id_goods'])
                game_code = game.app_code
                print('!!!!!!!!!!!!!!!!!!!!!!')
                print(type(game.priority_list))
                print('!!!!!!!!!!!!!!!!!!!!!!')
                if game.priority_list != '' and game.priority_list is not None:
                    country = info['options'][1]['value']
                    bot_account_code = random.choice(priority_list.get_list(game.priority_list))
                    account = get_user_by_id(bot_account_code)
                else:
                    country = info['options'][1]['value']
                    account = get_user_by_country(country)

                image_link = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game_code}/header.jpg"
                game_link = f'https://store.steampowered.com/app/{game_code}'

                user_link = info['options'][0]['value']

                order = Order(sell_code=code, bot=account, game=game, user_link=user_link, status='Add to Friends',
                              country=country, skype_link=i.skype_link, shop_link=i.shop_link, check_count=0)
                order.save()

                check_friends_list_first(account.steam_login, code, account.link, user_link, 'First Check')

                message = f"""Новая покупка!
Код - {code}
{game} - {user_link}"""

                token = get_telegram_token('info').key
                users = get_telegram_users()

                send_message(message, token, users)

                return render(request, 'main/account.html',
                              {'game_name': game.name,
                               'game_link': game_link,
                               'description_ru': game.description_ru,
                               'description_eng': game.description_eng,
                               'image_link': image_link,
                               'code': code,
                               'user_link': user_link,
                               'bot_link': account.link,
                               'region': country,
                               'shop_link': order.shop_link,
                               'skype_link': order.skype_link,
                               'accept_request_ru': accept_request_ru.text,
                               'accept_request_en': accept_request_en.text,
                               'add_to_friends_ru': add_to_friends_ru.text,
                               'add_to_friends_en': add_to_friends_en.text,
                               'sending_gift_ru': sending_gift_ru.text,
                               'sending_gift_en': sending_gift_en.text,
                               'send_gift_error_ru': send_gift_error_ru.text,
                               'send_gift_error_en': send_gift_error_en.text,
                               'check_error_ru': check_error_ru.text,
                               'check_error_en': check_error_en.text,
                               'add_friend_error_ru': add_friend_error_ru.text,
                               'add_friend_error_en': add_friend_error_en.text,
                               'gift_rejected_en': gift_rejected_en.text,
                               'gift_rejected_ru': gift_rejected_ru.text,
                               'gift_received_en': gift_received_en.text,
                               'gift_received_ru': gift_received_ru.text,
                               'gift_sent_en': gift_sent_en.text,
                               'gift_sent_ru': gift_sent_ru.text,
                               })
            else:
                continue

        html = f"Код {code} не действителен!"
        return HttpResponse(html)
    else:

        add_to_friends_ru = get_status('Add to Friends', 'ru')
        add_to_friends_en = get_status('Add to Friends', 'eng')
        sending_gift_ru = get_status('Sending Gift', 'ru')
        sending_gift_en = get_status('Sending Gift', 'eng')
        check_error_ru = get_status('Check Error', 'ru')
        check_error_en = get_status('Check Error', 'eng')
        send_gift_error_ru = get_status('Send Gift Error', 'ru')
        send_gift_error_en = get_status('Send Gift Error', 'eng')
        add_friend_error_en = get_status('Add Friend Error', 'eng')
        add_friend_error_ru = get_status('Add Friend Error', 'ru')
        gift_rejected_en = get_status('Gift Rejected', 'eng')
        gift_rejected_ru = get_status('Gift Rejected', 'ru')
        gift_received_en = get_status('Gift Received', 'eng')
        gift_received_ru = get_status('Gift Received', 'ru')
        gift_sent_en = get_status('Gift Sent', 'eng')
        gift_sent_ru = get_status('Gift Sent', 'ru')
        accept_request_ru = get_status('Accept Request', 'ru')
        accept_request_en = get_status('Accept Request', 'eng')

        game_code = order.game.app_code
        image_link = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game_code}/header.jpg"
        game_link = f'https://store.steampowered.com/app/{game_code}'

        return render(request, 'main/account.html',
                      {'game_name': order.game.name,
                       'game_link': game_link,
                       'image_link': image_link,
                       'description_ru': order.game.description_ru,
                       'description_eng': order.game.description_eng,
                       'code': code,
                       'user_link': order.user_link,
                       'bot_link': order.bot.link,
                       'region': order.country,
                       'shop_link': order.shop_link,
                       'skype_link': order.skype_link,
                       'accept_request_ru': accept_request_ru.text,
                       'accept_request_en': accept_request_en.text,
                       'add_to_friends_ru': add_to_friends_ru.text,
                       'add_to_friends_en': add_to_friends_en.text,
                       'sending_gift_ru': sending_gift_ru.text,
                       'sending_gift_en': sending_gift_en.text,
                       'send_gift_error_ru': send_gift_error_ru.text,
                       'send_gift_error_en': send_gift_error_en.text,
                       'check_error_ru': check_error_ru.text,
                       'check_error_en': check_error_en.text,
                       'add_friend_error_ru': add_friend_error_ru.text,
                       'add_friend_error_en': add_friend_error_en.text,
                       'gift_rejected_en': gift_rejected_en.text,
                       'gift_rejected_ru': gift_rejected_ru.text,
                       'gift_received_en': gift_received_en.text,
                       'gift_received_ru': gift_received_ru.text,
                       'gift_sent_en': gift_sent_en.text,
                       'gift_sent_ru': gift_sent_ru.text,
                       })


def handmade(request):
    code = request.GET.get('uniquecode')

    for i in get_shops():
        info = api.check_code(code, i.guid, i.seller_id)
        if info['retval'] == 0:
            handmade = get_handmade(info['id_goods'])
            if handmade is not False:
                return render(request, 'main/handmade.html',
                              {'code': code,
                               'title': handmade.title,
                               'text': handmade.text,
                               'shop_link': handmade.shop_link,
                               'skype_link': handmade.skype_link,
                               })


def head(request):
    return render(request, 'main/head.html')
