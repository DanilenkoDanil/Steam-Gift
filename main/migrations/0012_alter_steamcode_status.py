# Generated by Django 3.2.4 on 2021-08-28 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_steamcode_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steamcode',
            name='status',
            field=models.BooleanField(null=True, verbose_name='Статус'),
        ),
    ]
