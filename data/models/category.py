import uuid
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField, ArrayField
from .practice import Practice

class Category(models.Model):
    """
    This model represents a category containing practices. Usually these are shown in
    the landing page.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100)
    modification_date = models.DateTimeField()
    creation_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(null=True)

    airtable_json = JSONField(null=True, blank=True)
    airtable_url = models.TextField(null=True, blank=True)

    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    practice_external_ids = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    practices = models.ManyToManyField(Practice)
