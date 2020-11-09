from django.db import models, connection
from django.utils import timezone
from .experiment import Experiment

class Theme(models.Model):

    modification_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)

    active = models.BooleanField(default=False, db_index=True)

    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    experiments = models.ManyToManyField(Experiment)

    def __str__(self):
        return self.name
