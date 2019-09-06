# Generated by Django 2.2.4 on 2019-09-06 13:47

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_practice_weed_multipliers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='practice',
            old_name='target_cultures',
            new_name='cultures_whitelist',
        ),
        migrations.RenameField(
            model_name='practice',
            old_name='pests',
            new_name='pests_whitelist',
        ),
        migrations.RenameField(
            model_name='practice',
            old_name='weeds',
            new_name='weeds_whitelist',
        ),
        migrations.AddField(
            model_name='practice',
            name='culture_multipliers',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='practice',
            name='pest_multipliers',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), blank=True, null=True, size=None),
        ),
    ]
