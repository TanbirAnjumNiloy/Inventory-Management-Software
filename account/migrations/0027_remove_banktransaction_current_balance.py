# Generated by Django 4.1.6 on 2023-03-29 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0026_banktransaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banktransaction',
            name='current_balance',
        ),
    ]
