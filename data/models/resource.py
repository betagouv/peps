import uuid
from enum import Enum
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

class ResourceType(Enum):
    SITE_WEB = 1
    PDF = 2
    VIDEO = 3

class Resource(models.Model):
    """
    PDFs, web sites or videos that provide more information and
    context to practices.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100)
    modification_date = models.DateTimeField()
    creation_date = models.DateTimeField(default=timezone.now)

    airtable_json = JSONField(null=True, blank=True)
    airtable_url = models.TextField(null=True, blank=True)

    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    resource_type = models.IntegerField(blank=True, null=True)
    url = models.TextField()

    def get_type_name(self):
        if not self.resource_type:
            return None
        return ResourceType(self.resource_type).name
