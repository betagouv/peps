# Generated by Django 3.0.3 on 2020-05-02 15:14

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0075_auto_20200502_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='links',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.TextField(), blank=True, default=list, null=True, size=None),
        ),
    ]