# Generated by Django 3.2.4 on 2021-09-29 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20210929_0256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='priority_list',
            field=models.TextField(null=True, verbose_name='Приоритеты'),
        ),
    ]
