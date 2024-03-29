# Generated by Django 4.1.6 on 2023-03-05 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0027_rename_price_doprice'),
        ('account', '0002_rename_purchase_price_lifting_doprice'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiftingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.product')),
            ],
        ),
    ]
