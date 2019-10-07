import uuid
from enum import Enum
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField

class Culture(models.Model):

    class CulturesSowingPeriod(Enum):
        PRINTEMPS = 1
        AUTOMNE = 2
        ETE = 3
        FIN_ETE = 4

    class CulturesSowingMonth(Enum):
        JAN = 1
        FEV = 2
        MARS = 3
        AVR = 4
        MAI = 5
        JUIN = 6
        JUL = 7
        AOUT = 8
        SEP = 9
        OCT = 10
        NOV = 11
        DEC = 12

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100, db_index=True)
    modification_date = models.DateTimeField()
    creation_date = models.DateTimeField(default=timezone.now)

    airtable_json = JSONField(null=True, blank=True)
    airtable_url = models.TextField(null=True, blank=True)

    display_text = models.TextField(null=True, blank=True)

    # 1-12 (for January through December)
    sowing_months = ArrayField(models.IntegerField(), blank=True, null=True)

    # Must be part of the CulturePeriod enum
    sowing_period = models.IntegerField(null=True, blank=True)
