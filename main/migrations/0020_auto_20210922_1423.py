# Generated by Django 3.2.4 on 2021-09-22 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20210922_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='country',
        ),
        migrations.AlterField(
            model_name='game',
            name='sub_id',
            field=models.PositiveIntegerField(verbose_name='SubID'),
        ),
    ]
