# Generated by Django 3.0.8 on 2020-11-18 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_file_thumb_nail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='thumb_nail',
        ),
    ]
