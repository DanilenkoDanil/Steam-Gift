# Generated by Django 3.2.4 on 2021-10-15 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_auto_20211015_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='shop_link',
            field=models.TextField(default=1, verbose_name='Ссылка на магазин'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shop',
            name='skype_link',
            field=models.TextField(default=11, verbose_name='Ссылка на скайп'),
            preserve_default=False,
        ),
    ]
