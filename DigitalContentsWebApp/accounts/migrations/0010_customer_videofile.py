# Generated by Django 3.0.8 on 2020-10-17 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20201017_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='videofile',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
