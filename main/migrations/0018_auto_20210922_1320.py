# Generated by Django 3.2.4 on 2021-09-22 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='proxy',
            field=models.TextField(default=0, verbose_name='Прокси'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='SteamCode',
        ),
    ]
