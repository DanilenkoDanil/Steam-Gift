# Generated by Django 3.2.4 on 2021-08-11 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_account_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sell_code', models.PositiveIntegerField(verbose_name='Код продажи')),
                ('name', models.BooleanField(verbose_name='Название игры')),
                ('app_code', models.TextField(verbose_name='Код игры в стиме')),
            ],
            options={
                'verbose_name': 'Игра',
                'verbose_name_plural': 'Игры',
            },
        ),
        migrations.RemoveField(
            model_name='key',
            name='game_link',
        ),
        migrations.AddField(
            model_name='key',
            name='game',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='main.game', verbose_name='Игра'),
            preserve_default=False,
        ),
    ]
