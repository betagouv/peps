import uuid
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from data.models import Farmer

class Experiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100, db_index=True)
    modification_date = models.DateTimeField()
    creation_date = models.DateTimeField(default=timezone.now)
    airtable_json = JSONField(null=True, blank=True)

    farmer = models.ForeignKey(Farmer, related_name='experiments', on_delete=models.CASCADE, null=True)

    name = models.TextField()
    objectives = models.TextField(null=True)
    photos = ArrayField(models.ImageField(), blank=True, null=True)
    method = models.TextField(null=True)
    temporality = models.TextField(null=True)
    equipment = models.TextField(null=True)
    origin = models.TextField(null=True)
    execution = models.TextField(null=True)
    additional_details = models.TextField(null=True)
    control_presence = models.BooleanField(null=True)
    ongoing = models.BooleanField(null=True)
    results = models.TextField(null=True)
    results_details = models.TextField(null=True)
    links = models.TextField(null=True)

    surface = models.TextField(null=True)

    @staticmethod
    def create_from_airtable(airtable_json):
        fields = airtable_json['fields']
        return Experiment(
            external_id=airtable_json.get('id'),
            airtable_json=airtable_json,
            modification_date=timezone.now(),
            name=fields.get('Titre de l\'XP'),
            objectives=fields.get('Objectifs'),
            photos=None,
            method=fields.get('Méthode XP'),
            temporality=fields.get('Temporalité'),
            equipment=fields.get('Matériel'),
            execution=fields.get('Déroulé'),
            origin=fields.get('Origine'),
            additional_details=fields.get('Détails supplémentaires'),
            control_presence=fields.get('Présence d\'un témoin') == 'Oui',
            ongoing=fields.get('XP en cours') == 'Oui',
            results=fields.get('Résultats'),
            results_details=fields.get('Info résultats'),
            links=fields.get('Liens'),
            surface=str(fields.get('Surface')) if fields.get('Surface') else None,
        )
