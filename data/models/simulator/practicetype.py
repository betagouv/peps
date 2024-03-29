import uuid
from enum import Enum
from django.utils import timezone
from django.db import models
from django.db.models import JSONField

class PracticeTypeCategory(Enum):
    REDUCTION_DOSES = 1
    ALLONGEMENT_ROTATION = 2
    NOUVELLES_CULTURES = 3
    TRAVAIL_DU_SOL = 4
    COUVERTS_VEGETAUX = 5
    FAUX_SEMIS = 6
    PLANTES_COMPAGNES = 7
    COUVERT_INTER_RANG = 8
    INSECTES_AUXILIAIRES = 9
    ALTERNER_PRINTEMPS_AUTOMNE = 10
    SEMIS_DIRECT = 11
    PLANTES_DE_SERVICE = 12
    PRODUIT_BIOCONTROLE = 13
    MELANGE_VARIETES = 14
    VARIETE_RESISTANTE = 15
    DATE_SEMIS = 16
    PROPHYLAXIE = 17
    DESHERBAGE_MECANIQUE = 18
    OAD = 19
    INFRASTRUCTURE = 20
    DESTRUCTION_COUVERT = 21
    TRAVAIL_PROFOND = 22
    ELEVAGE = 23
    BIOCONTROLE = 24
    VARIETES = 25
    CONVENTIONNEL = 26
    COMPETITIVITE = 27

class PracticeType(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100)
    modification_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)

    airtable_json = JSONField(null=True, blank=True)
    airtable_url = models.TextField(null=True, blank=True)

    display_text = models.TextField(null=True, blank=True)
    penalty = models.DecimalField(null=True, max_digits=7, decimal_places=6)

    # Must be part of the PracticeTypeEnum enum
    category = models.IntegerField()

    def get_category_name(self):
        if not self.category:
            return None
        return PracticeTypeCategory(self.category).name

    @staticmethod
    def create_from_airtable(airtable_json):
        return PracticeType(
            external_id=airtable_json.get('id'),
            airtable_json=airtable_json,
            airtable_url='https://airtable.com/tblTwpbVXTqbQAYfB/' + airtable_json.get('id') + '/',
            display_text=airtable_json['fields'].get('Name'),
            penalty=airtable_json['fields'].get('Malus'),
            category=PracticeType._get_practice_type_category(airtable_json),
        )


    @staticmethod
    def _get_practice_type_category(airtable_json):
        try:
            return PracticeTypeCategory[airtable_json['fields'].get('Enum code')].value
        except Exception as _:
            return None
