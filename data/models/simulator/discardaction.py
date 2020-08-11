import uuid
from django.db import models
from django.utils import timezone
from django.db.models import JSONField

class DiscardAction(models.Model):
    """
    This is a table meant to track the reasons why certain practices are
    discarded. There is no link between records and is meant solely to be
    used in the admin panel.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    practice_airtable_id = models.CharField(max_length=100)
    reason = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(default=timezone.now)
    answers = JSONField(null=True, blank=True)

    @property
    def airtable_url(self):
        return 'https://airtable.com/tblobpdQDxkzcllWo/viwIl6ySkIGCg2zPW/' + self.practice_airtable_id
