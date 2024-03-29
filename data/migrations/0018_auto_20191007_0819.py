# Generated by Django 2.2.4 on 2019-10-07 08:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0017_culture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practice',
            name='added_cultures',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='practice',
            name='culture_whitelist',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None),
        ),
    ]
