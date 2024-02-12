# Generated by Django 4.1.6 on 2023-02-18 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0020_delete_dorate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dorate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(default=0)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.brand')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='setup.product')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.supplier')),
            ],
        ),
    ]
