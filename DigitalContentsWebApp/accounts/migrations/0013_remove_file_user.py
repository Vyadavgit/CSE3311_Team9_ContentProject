# Generated by Django 3.0.8 on 2020-10-19 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='user',
        ),
    ]