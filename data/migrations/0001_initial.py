# Generated by Django 2.2.3 on 2019-08-13 13:35

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirtableRecords',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pratiques', django.contrib.postgres.fields.jsonb.JSONField()),
                ('marges', django.contrib.postgres.fields.jsonb.JSONField()),
                ('soil_types', django.contrib.postgres.fields.jsonb.JSONField()),
                ('soil_pratiques', django.contrib.postgres.fields.jsonb.JSONField()),
                ('cultures', django.contrib.postgres.fields.jsonb.JSONField()),
                ('culture_types', django.contrib.postgres.fields.jsonb.JSONField()),
                ('departments', django.contrib.postgres.fields.jsonb.JSONField()),
                ('departments_pratiques', django.contrib.postgres.fields.jsonb.JSONField()),
                ('weeds', django.contrib.postgres.fields.jsonb.JSONField()),
                ('pests', django.contrib.postgres.fields.jsonb.JSONField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_fetch_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Mechanism',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_id', models.CharField(max_length=100)),
                ('modification_date', models.DateTimeField()),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('airtable_json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('airtable_url', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PracticeGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_id', models.CharField(max_length=100)),
                ('modification_date', models.DateTimeField()),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('airtable_json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_id', models.CharField(max_length=100)),
                ('modification_date', models.DateTimeField()),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('airtable_json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('airtable_url', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('resource_type', models.IntegerField(blank=True, null=True)),
                ('url', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Practice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_id', models.CharField(max_length=100)),
                ('modification_date', models.DateTimeField()),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('airtable_json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('airtable_url', models.TextField(blank=True, null=True)),
                ('title', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('equipment', models.TextField(blank=True, null=True)),
                ('schedule', models.TextField(blank=True, null=True)),
                ('impact', models.TextField(blank=True, null=True)),
                ('additional_benefits', models.TextField(blank=True, null=True)),
                ('success_factors', models.TextField(blank=True, null=True)),
                ('image_url', models.TextField(blank=True, null=True)),
                ('main_resource_label', models.TextField(blank=True, null=True)),
                ('needs_tillage', models.BooleanField(null=True)),
                ('livestock_multiplier', models.DecimalField(decimal_places=6, max_digits=7, null=True)),
                ('direct_sale_multiplier', models.DecimalField(decimal_places=6, max_digits=7, null=True)),
                ('precision', models.DecimalField(decimal_places=6, max_digits=7, null=True)),
                ('difficulty', models.DecimalField(decimal_places=6, max_digits=7, null=True)),
                ('added_cultures', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
                ('target_cultures', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
                ('problems_addressed', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
                ('weeds', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
                ('pests', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
                ('types', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
                ('department_multipliers', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), blank=True, null=True, size=None)),
                ('soil_type_multipliers', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), blank=True, null=True, size=None)),
                ('main_resource', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_practices', related_query_name='main_practice', to='data.Resource')),
                ('mechanism', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.Mechanism')),
                ('practice_groups', models.ManyToManyField(to='data.PracticeGroup')),
                ('secondary_resources', models.ManyToManyField(to='data.Resource')),
            ],
        ),
    ]
