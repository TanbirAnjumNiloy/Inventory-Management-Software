# Generated by Django 4.1.6 on 2023-02-17 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0005_delete_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('size', models.CharField(max_length=20)),
                ('commission', models.DecimalField(decimal_places=2, max_digits=10)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.brand')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.supplier')),
            ],
        ),
    ]