# Generated by Django 4.1.6 on 2023-02-17 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0010_rename_supplier_product_supplier'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]
