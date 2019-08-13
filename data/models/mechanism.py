import uuid
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

class Mechanism(models.Model):
    """
    Refers to the means in which practices reach their goals.
    For example, one mechanism may be the disruption of the natural
    cycle of undesirable weeds. Many practices may employ this
    mechanism to reach their goal.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100)
    modification_date = models.DateTimeField()
    creation_date = models.DateTimeField(default=timezone.now)

    airtable_json = JSONField(null=True, blank=True)
    airtable_url = models.TextField(null=True, blank=True)

    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
