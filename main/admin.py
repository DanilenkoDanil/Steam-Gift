from django.contrib import admin

from .forms import AccountForm, GameForm, OrderForm, HandmadeForm
from .models import Account, Game, Shop, Order, TelegramBot, TelegramAccount, Handmade, Status


@admin.register(Account)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'steam_login', 'steam_password', 'email', 'email_password', 'link', 'country', 'proxy', 'balance'
    )
    form = AccountForm
    search_fields = ['steam_login']


@admin.register(Order)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('sell_code', 'game', 'bot', 'user_link', 'country', 'status', 'created_at')
    search_fields = ['sell_code', 'game', 'bot', 'user_link', 'country', 'status', 'created_at']
    form = OrderForm


@admin.register(Game)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('sell_code', 'name', 'app_code', 'sub_id', 'priority_list', 'price')
    search_fields = ['name', 'sell_code', 'app_code', 'sub_id']
    form = GameForm


@admin.register(Shop)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'guid', 'seller_id', 'skype_link', 'shop_link')


@admin.register(TelegramBot)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'link')


@admin.register(TelegramAccount)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id')


@admin.register(Handmade)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'skype_link', 'shop_link')
    form = HandmadeForm


@admin.register(Status)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('status_type', 'text', 'lang')
