# Generated by Django 3.1.1 on 2020-11-10 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0112_theme_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='copyright',
            field=models.TextField(blank=True, null=True),
        ),
    ]