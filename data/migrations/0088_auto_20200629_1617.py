# Generated by Django 3.0.7 on 2020-06-29 16:17
from django.db import migrations, models
from data.models.farmer import get_next_increment as get_next_farmer_increment
from data.models.experiment import get_next_increment as get_next_experiment_increment

def assign_sequential_number_farmer(apps, schema_editor):
    Farmer = apps.get_model('data', 'Farmer')
    for farmer in Farmer.objects.all():
        farmer.sequence_number = get_next_farmer_increment()
        farmer.save()

def assign_sequential_number_experiment(apps, schema_editor):
    Experiment = apps.get_model('data', 'Experiment')
    for experiment in Experiment.objects.all():
        experiment.sequence_number = get_next_experiment_increment()
        experiment.save()

class Migration(migrations.Migration):

    dependencies = [
        ('data', '0087_auto_20200629_1614'),
    ]

    operations = [
        migrations.RunPython(assign_sequential_number_farmer),
        migrations.RunPython(assign_sequential_number_experiment),
    ]
