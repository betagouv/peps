import uuid
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import JSONField

class Farmer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100, db_index=True)
    modification_date = models.DateTimeField()
    creation_date = models.DateTimeField(default=timezone.now)
    airtable_json = JSONField(null=True, blank=True)

    @staticmethod
    def create_from_airtable(airtable_json):
        return Farmer(
            external_id=airtable_json.get('id'),
            airtable_json=airtable_json,
            modification_date=timezone.now(),
        )
