# Generated by Django 2.2.4 on 2019-09-10 13:00

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_auto_20190906_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='practice',
            name='glyphosate_multipliers',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), blank=True, null=True, size=None),
        ),
    ]
