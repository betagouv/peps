# Generated by Django 3.0.3 on 2020-03-24 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0049_remove_experiment_photos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='farmer',
            old_name='profession',
            new_name='production',
        ),
    ]