import uuid
from enum import Enum
from django.db import models
from django.utils import timezone
from django.db.models import F

class GroupCount(models.Model):
    """
    This model stores agricultural groups and their incidence. This allows
    us to have statistic information on the users we have.
    """

    class AgriculturalGroup(Enum):
        DEPHY = 1
        GROUPE_30000 = 2
        GIEE = 3
        CHAMBRE = 4
        COOPERATIVE_OU_NEGOCE = 5
        AB_CONVERSION_AB = 6
        AUTRE = 7
        AUCUN = 8

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creation_date = models.DateTimeField(default=timezone.now)
    counter = models.IntegerField(default=0)

    # Must be part of the AgriculturalGroup enum
    group = models.IntegerField(unique=True)

    @staticmethod
    def create_or_increment(group):
        group_count, _ = GroupCount.objects.get_or_create(group=group.value)
        group_count.counter = F('counter') + 1
        group_count.save()

    @property
    def group_name(self):
        if not self.group:
            return 'None'
        return GroupCount.AgriculturalGroup(self.group).name.replace('_', ' ').capitalize()
