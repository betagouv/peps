# Generated by Django 3.1.1 on 2020-09-07 07:31

from django.db import migrations, models

def populate_states(apps, schema_editor):
    Experiment = apps.get_model('data', 'Experiment')
    for experiment in Experiment.objects.all():
        if experiment.approved:
            experiment.state = "Validé"
            experiment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0104_auto_20200818_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='state',
            field=models.TextField(choices=[('Brouillon', 'Brouillon'), ('En attente de validation', 'En attente de validation'), ('Validé', 'Validé')], default='Brouillon'),
        ),
        migrations.RunPython(populate_states),
    ]
