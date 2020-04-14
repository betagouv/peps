# Generated by Django 3.0.3 on 2020-04-14 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0059_auto_20200414_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='external_id',
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='external_id',
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
    ]
