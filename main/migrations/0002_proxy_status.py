# Generated by Django 3.2.4 on 2021-08-11 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proxy',
            name='status',
            field=models.BooleanField(default=1, verbose_name='Статус'),
            preserve_default=False,
        ),
    ]
