# Generated by Django 3.2.4 on 2021-11-06 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_auto_20211028_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='shared_secret',
            field=models.TextField(default=1, verbose_name='Shared Secret'),
            preserve_default=False,
        ),
    ]
