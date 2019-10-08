# Generated by Django 2.2.4 on 2019-10-05 08:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0013_auto_20191005_0759'),
    ]

    operations = [
        migrations.AddField(
            model_name='practice',
            name='pest_whitelist_external_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
        ),
        migrations.AddField(
            model_name='practice',
            name='weed_whitelist_external_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
        ),
    ]