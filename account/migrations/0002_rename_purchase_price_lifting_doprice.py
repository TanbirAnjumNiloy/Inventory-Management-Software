# Generated by Django 4.1.6 on 2023-03-05 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lifting',
            old_name='purchase_price',
            new_name='Doprice',
        ),
    ]
