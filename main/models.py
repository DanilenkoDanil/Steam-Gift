from django.db import models
from . import get_name


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
    balance = models.TextField(
        verbose_name='Баланс'
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to='main/guard/'
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

    def __str__(self):
        return f'{self.sell_code} - {self.name}'

    def save(self, *args, **kwargs):
        if not self.pk:  # this will ensure that the object is new
            self.name = get_name.get_name_game(f'{self.app_code}')
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
        verbose_name='Код продажи'
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

    def __str__(self):
        return f'{self.sell_code} - {self.status}'

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = 'Заказы'


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
