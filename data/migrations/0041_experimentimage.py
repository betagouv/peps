# Generated by Django 3.0.3 on 2020-03-17 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0040_experiment_xp_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExperimentImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('experiment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='data.Experiment')),
            ],
        ),
    ]
