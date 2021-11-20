from django.db import models
from model_utils import FieldTracker
from background_task import background
from . import get_name
from . import game_price_check
from . import get_friends
from . import send_gift


class Account(models.Model):
    steam_login = models.TextField(
        verbose_name="Логин пользователя в Steam",
        unique=True
    )
    steam_password = models.TextField(
        verbose_name="Пароль от Steam"
    )
    email = models.TextField(
        verbose_name='Почта к которой привязан аккаунт'
    )
    email_password = models.TextField(
        verbose_name='Пароль от почты'
    )
    link = models.TextField(
        verbose_name='Ссылка'
    )
    country = models.TextField(
        verbose_name='Страна'
    )
    proxy = models.TextField(
        verbose_name='Прокси'
    )
    shared_secret = models.TextField(
        verbose_name="Shared Secret"
    )
    balance = models.TextField(
        verbose_name='Баланс'
    )

    def __str__(self):
        return f'#{self.steam_login}'

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'


class Game(models.Model):
    sell_code = models.PositiveIntegerField(
        verbose_name='Код продажи'
    )

    app_code = models.PositiveIntegerField(
        verbose_name='Код игры в стиме'
    )
    sub_id = models.PositiveIntegerField(
        verbose_name='SubID'
    )
    description_ru = models.TextField(
        verbose_name='Описание RU'
    )
    description_eng = models.TextField(
        verbose_name='Описание ENG'
    )
    priority_list = models.TextField(
        verbose_name='Приоритеты',
        blank=True
    )
    name = models.TextField(
        verbose_name='Название игры',
        blank=True
    )
    price = models.FloatField(
        verbose_name='Цена',
        blank=True
    )

    def __str__(self):
        return f'{self.sell_code} - {self.name}'

    def save(self, *args, **kwargs):
        if not self.pk:  # this will ensure that the object is new
            self.name = get_name.get_name_game(self.sub_id)
            try:
                self.price = game_price_check.get_price(self.sub_id)
            except Exception as e:
                print(e)
                self.price = 0
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = 'Игры'


class Order(models.Model):
    STATUS_CHOICES = (
        ('Add to Friends', 'Add to Friends'),
        ('Sending Gift', 'Sending Gift'),
        ('Check Error', 'Check Error'),
        ('Send Gift Error', 'Send Gift Error'),
        ('Add Friend Error', 'Add Friend Error'),
        ('Add to Friends', 'Add to Friends'),
        ('Gift Rejected', 'Gift Rejected'),
        ('Gift Received', 'Gift Received'),
        ('Gift Sent', 'Gift Sent'),
        ('Accept Request', 'Accept Request'),
    )

    sell_code = models.TextField(
        verbose_name='Код продажи',
        unique=True
    )
    game = models.ForeignKey(
        to='main.Game',
        verbose_name='Игра',
        on_delete=models.PROTECT,
    )
    bot = models.ForeignKey(
        to='main.Account',
        verbose_name='Аккаунт',
        on_delete=models.PROTECT,
    )
    user_link = models.TextField(
        verbose_name='Аккаунт покупателя'
    )
    country = models.TextField(
        verbose_name='Страна'
    )
    status = models.TextField(
        verbose_name='Status',
        choices=STATUS_CHOICES
    )
    created_at = models.DateTimeField(
        verbose_name='Время получения',
        auto_now_add=True,
    )
    skype_link = models.TextField(
        verbose_name='Ссылка на скайп'
    )
    shop_link = models.TextField(
        verbose_name='Ссылка на магазин'
    )
    check_count = models.PositiveIntegerField(
        verbose_name='Кол-во проверок'
    )

    tracker = FieldTracker()

    def __str__(self):
        return f'{self.sell_code} - {self.status}'

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
        if self.tracker.has_changed('status'):
            print(self.status)
            if self.status == 'Add to Friends':
                add_friend(self.bot.steam_login, self.user_link, self.sell_code, "Add Friend")
            elif self.status == 'Sending Gift':
                send_gift_to_user(self.bot.steam_login, self.sell_code, "Sending Gift")
            elif self.status == 'Add to Friends':
                check_gift_status(self.bot.steam_login, get_name.get_name(self.user_link), self.sell_code,
                                  "Check Gift Status")
        super().save(*args, **kwargs)


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


class TelegramBot(models.Model):
    name = models.TextField(
        verbose_name='Имя бота',
    )
    key = models.TextField(
        verbose_name='Ключ',
        unique=True
    )
    link = models.TextField(
        verbose_name='Ссылка'
    )

    def __str__(self):
        return f'Бот - {self.name} - {self.key}'

    class Meta:
        verbose_name = "Телеграм бот"
        verbose_name_plural = 'Телеграм боты'


class TelegramAccount(models.Model):
    name = models.TextField(
        verbose_name='Имя юзера',
    )
    user_id = models.TextField(
        verbose_name='UserId',
        unique=True
    )

    def __str__(self):
        return f'Бот - {self.name} - {self.user_id}'

    class Meta:
        verbose_name = "Телеграм Аккаунт"
        verbose_name_plural = 'Телеграм Аккаунты'


class Shop(models.Model):
    name = models.TextField(
        verbose_name='Название магазина',
    )
    guid = models.TextField(
        verbose_name='API Guid',
    )
    seller_id = models.TextField(
        verbose_name='Seller ID'
    )
    skype_link = models.TextField(
        verbose_name='Ссылка на скайп'
    )
    shop_link = models.TextField(
        verbose_name='Ссылка на магазин'
    )

    def __str__(self):
        return f'Магазин - {self.name}'

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = 'Магазины'


class Handmade(models.Model):
    code = models.TextField(
        verbose_name='Код',
        unique=True
    )
    title = models.TextField(
        verbose_name='Тема',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    skype_link = models.TextField(
        verbose_name='Ссылка на скайп'
    )
    shop_link = models.TextField(
        verbose_name='Ссылка на магазин'
    )

    def __str__(self):
        return f'Код - {self.title}'

    class Meta:
        verbose_name = "Ручная страница"
        verbose_name_plural = 'Ручные страницы'


class Status(models.Model):

    YESNO_CHOICES = (
        ('eng', 'English'),
        ('ru', 'Russian'),
    )
    status_type = models.TextField(
        verbose_name='Тип Статуса',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    lang = models.TextField(
        verbose_name='Язык',
        choices=YESNO_CHOICES
    )

    def __str__(self):
        return f'Статус - {self.status_type}'

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = 'Статусы'


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

def get_shops() -> Shop:
    return Shop.objects.all()
