# Generated by Django 3.2.4 on 2021-08-11 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_proxy_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='status',
            field=models.BooleanField(null=True, verbose_name='Статус аккаунта'),
        ),
    ]
