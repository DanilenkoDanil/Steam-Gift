# Generated by Django 3.2.4 on 2021-10-24 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_alter_game_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.TextField(default=models.PositiveIntegerField(verbose_name='Код игры в стиме'), verbose_name='Название игры'),
        ),
    ]
