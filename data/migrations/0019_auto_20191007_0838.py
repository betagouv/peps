# Generated by Django 2.2.4 on 2019-10-07 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0018_auto_20191007_0819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='culture',
            old_name='period',
            new_name='sowing_period',
        ),
    ]
