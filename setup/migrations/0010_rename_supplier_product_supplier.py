# Generated by Django 4.1.6 on 2023-02-17 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0009_rename_supplier_product_supplier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Supplier',
            new_name='supplier',
        ),
    ]
