# Generated by Django 3.1.1 on 2020-09-23 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0106_auto_20200907_0749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='contact_possible',
            field=models.BooleanField(default=True),
        ),
    ]
