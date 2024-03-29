# Generated by Django 4.1.6 on 2023-04-08 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0030_discountsetup'),
        ('account', '0033_delete_dailycost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dailycost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('carcost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dsrbill', models.DecimalField(decimal_places=2, max_digits=10)),
                ('toll', models.DecimalField(decimal_places=2, max_digits=10)),
                ('othercost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dsr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.dsr')),
            ],
        ),
    ]
