"""
Practice groups refer to practices that are "the same" but
with different levels of specificity. For example, a practice
suggesting to add a "culture étouffate" and another one suggesting
to add "Chanvre" (which is a culture étouffante) are the same, so
we should avoid suggesting both at the same time.
"""
import uuid
from django.db import models
from django.utils import timezone
from django.db.models import JSONField

class PracticeGroup(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100)
    modification_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)

    airtable_json = JSONField(null=True, blank=True)

    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    @staticmethod
    def create_from_airtable(airtable_json):
        return PracticeGroup(
            external_id=airtable_json.get('id'),
            airtable_json=airtable_json,
            name=airtable_json['fields'].get('Nom'),
            description=airtable_json['fields'].get('Description'),
        )
