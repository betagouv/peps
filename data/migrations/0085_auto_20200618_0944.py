# Generated by Django 3.0.7 on 2020-06-18 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0084_farmer_onboarding_shown'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='farmer',
            options={'ordering': ['name']},
        ),
    ]