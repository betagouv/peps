# Generated by Django 3.0.3 on 2020-05-02 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0071_experiment_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='external_id',
            field=models.CharField(db_index=True, max_length=100, null=True),
        ),
    ]
