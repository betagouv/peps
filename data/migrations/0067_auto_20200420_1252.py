# Generated by Django 3.0.3 on 2020-04-20 12:52

import data.forms
from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0066_auto_20200419_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='links',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.TextField(), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='results',
            field=models.TextField(choices=[("XP qui fonctionne, elle est intégrée à l'exploitation", "XP qui fonctionne, elle est intégrée à l'exploitation"), ("XP prometteuse, en cours d'amélioration", "XP prometteuse, en cours d'amélioration"), ('XP abandonnée, les résultats ne sont pas satisfaisants', 'XP abandonnée, les résultats ne sont pas satisfaisants'), ('XP en suspens, les conditions ne sont plus réunies', 'XP en suspens, les conditions ne sont plus réunies'), ('XP qui commence, les premiers résultats sont à venir', 'XP qui commence, les premiers résultats sont à venir')], null=True),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='surface_type',
            field=data.forms.ChoiceArrayField(base_field=models.TextField(choices=[('Toutes les surfaces', 'Toutes les surfaces'), ('Plusieurs parcelles', 'Plusieurs parcelles'), ('Une parcelle', 'Une parcelle'), ('Des bandes', 'Des bandes'), ('Des carrés', 'Des carrés')]), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='tags',
            field=data.forms.ChoiceArrayField(base_field=models.CharField(choices=[("Changement important de l'exploitation", "Changement important de l'exploitation"), ("Amélioration de l'existant", "Amélioration de l'existant"), ('Maladies', 'Maladies'), ('Insectes et ravageurs', 'Insectes et ravageurs'), ('Adventices', 'Adventices'), ('Environnement & biodiversité', 'Environnement & biodiversité'), ('Diversification', 'Diversification'), ('Autonomie fourragère', 'Autonomie fourragère'), ('Productivité', 'Productivité'), ('Organisation du travail', 'Organisation du travail'), ('Réduction des charges', 'Réduction des charges'), ('Autre', 'Autre')], max_length=255), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='agriculture_types',
            field=data.forms.ChoiceArrayField(base_field=models.TextField(choices=[('Agriculture Biologique', 'Agriculture Biologique'), ('Agriculture de Conservation des Sols', 'Agriculture de Conservation des Sols'), ('Techniques Culturales Simplifiées', 'Techniques Culturales Simplifiées'), ('Labour occasionnel', 'Labour occasionnel'), ('Agroforesterie', 'Agroforesterie'), ('Conventionnel', 'Conventionnel'), ('Cahier des charges industriel', 'Cahier des charges industriel'), ('Label qualité', 'Label qualité'), ('Autre', 'Autre')]), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='groups',
            field=data.forms.ChoiceArrayField(base_field=models.CharField(choices=[('DEPHY', 'DEPHY'), ('GIEE', 'GIEE'), ('30000', '30000'), ('CETA', 'CETA'), ('Groupe de coopérative', 'Groupe de coopérative'), ('Groupe de négoce', 'Groupe de négoce'), ("Groupe de chambre d'agriculture", "Groupe de chambre d'agriculture"), ('Groupe de voisins', 'Groupe de voisins'), ('CUMA', 'CUMA'), ('Autre', 'Autre')], max_length=200), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='links',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.TextField(), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='production',
            field=data.forms.ChoiceArrayField(base_field=models.CharField(choices=[('Grandes cultures', 'Grandes cultures'), ('Cultures industrielles', 'Cultures industrielles'), ('Élevage allaitant', 'Élevage allaitant'), ('Élevage laitier', 'Élevage laitier'), ('Cultures légumières', 'Cultures légumières'), ('Vigne', 'Vigne'), ('Autre', 'Autre')], max_length=100), default=list, size=None),
        ),
    ]