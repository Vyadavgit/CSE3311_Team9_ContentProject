# Generated by Django 3.0.8 on 2020-11-27 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0035_auto_20201121_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='saved_videos',
            field=models.ManyToManyField(related_name='_customer_saved_videos_+', to='accounts.File'),
        ),
    ]