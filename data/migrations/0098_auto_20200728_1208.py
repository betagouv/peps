# Generated by Django 3.0.7 on 2020-07-28 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0097_auto_20200724_1157'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Culture',
            new_name='SimulatorCulture',
        ),
    ]