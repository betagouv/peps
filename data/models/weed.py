import uuid
from enum import Enum
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import JSONField


class Weed(models.Model):

    class WeedNature(Enum):
        VIVACE = 1
        ANNUELLE = 2

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100, db_index=True)
    modification_date = models.DateTimeField()
    creation_date = models.DateTimeField(default=timezone.now)

    airtable_json = JSONField(null=True, blank=True)
    airtable_url = models.TextField(null=True, blank=True)

    display_text = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    # Must be part of the WeedNature enum
    nature = models.IntegerField(null=True, blank=True)
