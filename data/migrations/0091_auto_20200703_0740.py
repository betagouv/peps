# Generated by Django 3.0.7 on 2020-07-03 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0090_experiment_short_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='short_name',
            field=models.TextField(blank=True, help_text="Si ce champs est présent, il sera utilisé pour l'URL", max_length=40, null=True),
        ),
    ]
