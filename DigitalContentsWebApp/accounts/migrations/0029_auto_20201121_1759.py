# Generated by Django 3.0.8 on 2020-11-21 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_customer_subscribe_poster'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='subscribe_poster',
        ),
        migrations.AddField(
            model_name='customer',
            name='video_poster',
            field=models.ImageField(blank=True, default='poster_null.jpg', null=True, upload_to=''),
        ),
    ]
