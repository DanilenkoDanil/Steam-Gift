# Generated by Django 3.2.4 on 2021-10-15 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='lang',
            field=models.TextField(choices=[('eng', 'English'), ('ru', 'Russian')], default=1, verbose_name='Язык'),
            preserve_default=False,
        ),
    ]