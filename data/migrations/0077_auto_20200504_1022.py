# Generated by Django 3.0.3 on 2020-05-04 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0076_auto_20200502_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='approved',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='farmer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
