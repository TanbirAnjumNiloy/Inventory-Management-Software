# Generated by Django 4.1.6 on 2023-04-07 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0030_discountsetup'),
        ('account', '0030_delete_acdiccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acdiccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.brand')),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.discountsetup')),
                ('sr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.salesmanager')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.supplier')),
            ],
        ),
    ]
