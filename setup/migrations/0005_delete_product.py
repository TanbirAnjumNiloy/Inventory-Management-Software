# Generated by Django 4.1.6 on 2023-02-17 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0004_product'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]