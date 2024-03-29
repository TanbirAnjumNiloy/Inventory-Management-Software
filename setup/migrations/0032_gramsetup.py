# Generated by Django 4.1.6 on 2023-09-20 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0031_collectionsetup'),
    ]

    operations = [
        migrations.CreateModel(
            name='GramSetup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grams', models.FloatField()),
                ('current_grams', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gram_setups', to='setup.product')),
            ],
        ),
    ]
