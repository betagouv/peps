# Generated by Django 3.0.3 on 2020-03-16 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0036_auto_20200316_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='surface',
            field=models.TextField(null=True),
        ),
    ]
