# Generated by Django 3.2.4 on 2021-08-28 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_steamcode_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='steamcode',
            name='status',
        ),
    ]
