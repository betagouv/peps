# Generated by Django 3.0.7 on 2020-08-10 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0101_auto_20200803_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='experimentimage',
            name='copyright',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='experimentvideo',
            name='copyright',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='farmimage',
            name='copyright',
            field=models.TextField(blank=True, null=True),
        ),
    ]