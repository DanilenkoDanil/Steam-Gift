# Generated by Django 3.2.4 on 2021-09-25 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20210925_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.TextField(default=1, verbose_name='Страна'),
            preserve_default=False,
        ),
    ]
