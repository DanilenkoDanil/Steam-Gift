# Generated by Django 3.2.4 on 2021-08-28 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210827_0349'),
    ]

    operations = [
        migrations.AddField(
            model_name='steamcode',
            name='status',
            field=models.BooleanField(default=None, verbose_name='Статус'),
            preserve_default=False,
        ),
    ]
