# Generated by Django 3.2.4 on 2021-10-25 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0043_alter_game_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='file',
            field=models.ImageField(default=1, upload_to='main/guard/', verbose_name='Файл'),
            preserve_default=False,
        ),
    ]
