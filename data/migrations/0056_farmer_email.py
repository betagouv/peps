# Generated by Django 3.0.3 on 2020-04-07 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0055_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='email',
            field=models.EmailField(db_index=True, default='test@email.com', max_length=254),
            preserve_default=False,
        ),
    ]
