# Generated by Django 3.0.7 on 2020-07-24 11:55

import data.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0095_auto_20200724_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='agriculture_types',
            field=data.forms.ChoiceArrayField(base_field=models.TextField(choices=[('Agriculture Biologique', 'Agriculture Biologique'), ('Agriculture de Conservation des Sols', 'Agriculture de Conservation des Sols'), ('Techniques Culturales Simplifiées', 'Techniques Culturales Simplifiées'), ('Labour occasionnel', 'Labour occasionnel'), ('Agroforesterie', 'Agroforesterie'), ('Conventionnel', 'Conventionnel'), ('Cahier des charges industriel', 'Cahier des charges industriel'), ('Label qualité', 'Label qualité'), ('Cultures spécialisées', 'Cultures spécialisées'), ('Apiculture', 'Apiculture'), ('Label environnemental (HVE)', 'Label environnemental (HVE)'), ('Autre', 'Autre')]), blank=True, default=list, null=True, size=None),
        ),
    ]
