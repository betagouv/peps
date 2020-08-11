import uuid
from enum import Enum
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField

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
    modification_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)

    display_text = models.TextField(null=True, blank=True)

    airtable_json = JSONField(null=True, blank=True)
    airtable_url = models.TextField(null=True, blank=True)

    # 1-12 (for January through December)
    sowing_months = ArrayField(models.IntegerField(), blank=True, null=True)

    # Must be part of the CulturePeriod enum
    sowing_period = models.IntegerField(null=True, blank=True)

    @staticmethod
    def create_from_airtable(airtable_json):
        sowing_period = None
        periodes_de_semis = airtable_json['fields'].get('période de semis')
        if periodes_de_semis:
            try:
                sowing_period = Culture.CulturesSowingPeriod[periodes_de_semis[0]].value
            except KeyError as _:
                pass

        sowing_months = None
        mois_semis = airtable_json['fields'].get('mois semis')
        if mois_semis:
            sowing_months = []
            for mois in mois_semis:
                try:
                    sowing_months.append(Culture.CulturesSowingMonth[mois].value)
                except KeyError as _:
                    pass

        return Culture(
            external_id=airtable_json.get('id'),
            airtable_json=airtable_json,
            display_text=airtable_json['fields'].get('Name'),
            sowing_period=sowing_period,
            sowing_months=sowing_months
        )
