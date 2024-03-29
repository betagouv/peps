# Generated by Django 2.2.4 on 2019-10-07 08:17

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0016_auto_20191005_0847'),
    ]

    operations = [
        migrations.CreateModel(
            name='Culture',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_id', models.CharField(db_index=True, max_length=100)),
                ('modification_date', models.DateTimeField()),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('airtable_json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('airtable_url', models.TextField(blank=True, null=True)),
                ('display_text', models.TextField(blank=True, null=True)),
                ('sowing_month', models.IntegerField(blank=True, null=True)),
                ('period', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
