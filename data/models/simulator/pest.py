import uuid
from django.utils import timezone
from django.db import models
from django.db.models import JSONField

class Pest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100, db_index=True)
    modification_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)

    airtable_json = JSONField(null=True, blank=True)
    airtable_url = models.TextField(null=True, blank=True)

    display_text = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    @staticmethod
    def create_from_airtable(airtable_json):
        return Pest(
            external_id=airtable_json.get('id'),
            airtable_json=airtable_json,
            display_text=airtable_json['fields'].get('Name'),
            description=airtable_json['fields'].get('Description'),
        )
