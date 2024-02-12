# Generated by Django 4.1.6 on 2023-03-27 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0028_product_qty'),
        ('account', '0018_alter_sales_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Damage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('total_product_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_sum', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(null=True)),
                ('mem_number', models.PositiveIntegerField(unique=True)),
                ('Purchase_Price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.doprice')),
                ('dsr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.dsr')),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.market')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.product')),
            ],
        ),
    ]
