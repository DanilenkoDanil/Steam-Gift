# Generated by Django 3.2.4 on 2021-10-23 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_auto_20211023_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='description',
        ),
        migrations.AddField(
            model_name='game',
            name='description_eng',
            field=models.TextField(default=1, verbose_name='Описание ENG'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='description_ru',
            field=models.TextField(default=1, verbose_name='Описание RU'),
            preserve_default=False,
        ),
    ]
