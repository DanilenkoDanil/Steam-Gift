# Generated by Django 3.2.4 on 2021-09-29 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_alter_game_priority_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='priority_list',
            field=models.TextField(blank=True, default=1, verbose_name='Приоритеты'),
            preserve_default=False,
        ),
    ]
