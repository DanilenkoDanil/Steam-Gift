from django import forms
from django.contrib import admin

from .models import Account, Game, Order


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
            'status',
            'balance'
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
            'sell_code',
            'name',
            'app_code',
            'sub_id',
            'priority_list'
        )
        widgets = {
            'name': forms.TextInput,
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
        )
        widgets = {
            'sell_code': forms.TextInput,
            'user_link': forms.TextInput,
            'status': forms.TextInput,
        }









