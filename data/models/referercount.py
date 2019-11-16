import uuid
from enum import Enum
from django.db import models
from django.utils import timezone
from django.db.models import F

class RefererCount(models.Model):
    """
    This model stores referers (e.g., Facebook, workshops, etc) and their incidence.
    This allowsus to have statistic information on how we capture users.
    """

    class Referer(Enum):
        MOTEUR_RECHERCHE = 1
        RESEAUX_SOCIAUX = 2
        BOUCHE_A_OREILLE = 3
        PRESSE = 4
        COOPERATIVE_OU_NEGOCE = 5
        CHAMBRE_AGRICULTURE = 6
        AGRICULTEUR = 7
        ATELIER_TERRITOIRE = 8
        DDT = 9
        AUTRE = 10

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creation_date = models.DateTimeField(default=timezone.now)
    counter = models.IntegerField(default=0)

    # Must be part of the Referer enum
    referer = models.IntegerField(unique=True)

    @staticmethod
    def create_or_increment(referer):
        referer_count, _ = RefererCount.objects.get_or_create(referer=referer.value)
        referer_count.counter = F('counter') + 1
        referer_count.save()

    @property
    def referer_name(self):
        if not self.referer:
            return 'None'
        return RefererCount.Referer(self.referer).name.replace('_', ' ').capitalize()
