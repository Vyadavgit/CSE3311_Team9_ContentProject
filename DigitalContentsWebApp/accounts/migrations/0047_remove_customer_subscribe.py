# Generated by Django 3.0.8 on 2020-11-29 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0046_auto_20201129_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='subscribe',
        ),
    ]
