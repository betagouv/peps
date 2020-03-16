# Generated by Django 3.0.3 on 2020-03-16 09:44

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0032_experiment_farmer'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='control_presence',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='equipment',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='execution',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='farmer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='data.Farmer'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='links',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='method',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='name',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='experiment',
            name='objectives',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='ongoing',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='photos',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.ImageField(upload_to=''), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='experiment',
            name='results',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='results_details',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='surface',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='temporality',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='airtable_url',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='contact_possible',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='farmer',
            name='cultures',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='installation_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='lat',
            field=models.DecimalField(decimal_places=6, default=47.1807, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='farmer',
            name='livestock_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='livestock_type',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='lon',
            field=models.DecimalField(decimal_places=6, default=1.494141, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='farmer',
            name='name',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='output',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='personnel',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='postal_code',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='profession',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='profile_image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='farmer',
            name='soil_type',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='specificities',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='surface',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='surface_cultures',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='surface_meadows',
            field=models.FloatField(null=True),
        ),
    ]