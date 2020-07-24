# Generated by Django 3.0.7 on 2020-07-24 11:54

import data.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0094_auto_20200723_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='agriculture_types',
            field=data.forms.ChoiceArrayField(base_field=models.TextField(choices=[('Agriculture Biologique', 'Agriculture Biologique'), ('Agriculture de Conservation des Sols', 'Agriculture de Conservation des Sols'), ('Techniques Culturales Simplifiées', 'Techniques Culturales Simplifiées'), ('Labour occasionnel', 'Labour occasionnel'), ('Agroforesterie', 'Agroforesterie'), ('Conventionnel', 'Conventionnel'), ('Cahier des charges industriel', 'Cahier des charges industriel'), ('Label qualité', 'Label qualité'), ('Cultures spécialisées', 'Cultures spécialisées'), ('Apiculture', 'Apiculture'), ('Autre', 'Autre')]), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='groups',
            field=data.forms.ChoiceArrayField(base_field=models.CharField(choices=[('DEPHY', 'DEPHY'), ('GIEE', 'GIEE'), ('30000', '30000'), ('CETA', 'CETA'), ('Groupe de coopérative', 'Groupe de coopérative'), ('Groupe de négoce', 'Groupe de négoce'), ("Groupe de chambre d'agriculture", "Groupe de chambre d'agriculture"), ('Groupe de voisins', 'Groupe de voisins'), ('CUMA', 'CUMA'), ('Civam', 'Civam'), ('Autre', 'Autre')], max_length=200), blank=True, default=list, null=True, size=None),
        ),
    ]
