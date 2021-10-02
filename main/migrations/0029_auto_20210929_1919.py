# Generated by Django 3.2.4 on 2021-09-29 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_alter_game_priority_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Имя юзера')),
                ('user_id', models.TextField(unique=True, verbose_name='UserId')),
            ],
            options={
                'verbose_name': 'Телеграм Аккаунт',
                'verbose_name_plural': 'Телеграм Аккаунты',
            },
        ),
        migrations.RenameModel(
            old_name='Telegram',
            new_name='TelegramBot',
        ),
        migrations.AlterModelOptions(
            name='telegrambot',
            options={'verbose_name': 'Телеграм бот', 'verbose_name_plural': 'Телеграм боты'},
        ),
    ]
