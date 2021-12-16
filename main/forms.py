from django import forms
from django.contrib import admin

from . import get_name
from .models import Account, Game, Order, Handmade


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = (
            'steam_login',
            'steam_password',
            'email',
            'email_password',
            'link',
            'country',
            'proxy',
            'shared_secret',
            'balance',

        )
        widgets = {
            'steam_login': forms.TextInput,
            'steam_password': forms.TextInput,
            'email': forms.EmailInput,
            'email_password': forms.TextInput,
            'link': forms.TextInput,
            'country': forms.TextInput,
            'proxy': forms.TextInput,
            'balance': forms.TextInput
        }


class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = (
            'name',
            'sell_code',
            'app_code',
            'description_ru',
            'description_eng',
            'sub_id',
            'priority_list',
            'price'
        )
        widgets = {
            'steam_password': forms.TextInput,
            'sub_id': forms.TextInput,
            'priority_list': forms.TextInput,
        }


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'sell_code',
            'game',
            'bot',
            'user_link',
            'country',
            'status',
            'skype_link',
            'shop_link',
        )
        widgets = {
            'sell_code': forms.TextInput,
            'user_link': forms.TextInput,
            'skype_link': forms.TextInput,
            'shop_link': forms.TextInput,
        }


class HandmadeForm(forms.ModelForm):

    class Meta:
        model = Handmade
        fields = (
            'code',
            'title',
            'text',
            'skype_link',
            'shop_link'
        )
        widgets = {
            'code': forms.TextInput,
            'title': forms.TextInput,
            'skype_link': forms.TextInput,
            'shop_link': forms.TextInput,
        }
