# Generated by Django 4.1.6 on 2023-04-07 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0029_salesmanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discountsetup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.brand')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.supplier')),
            ],
        ),
    ]
