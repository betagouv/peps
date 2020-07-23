# Generated by Django 3.0.7 on 2020-07-23 13:20

from django.db import migrations, models

def migrate_email_allowed(apps, schema_editor):
    Farmer = apps.get_model('data', 'Farmer')
    for farmer in Farmer.objects.all():
        farmer.email_for_messages_allowed = True
        farmer.save()


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0093_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='email_for_messages_allowed',
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(migrate_email_allowed),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['sent_at'], name='data_messag_sent_at_dec768_idx'),
        ),
    ]
