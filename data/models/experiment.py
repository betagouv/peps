import uuid
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from data.models import Farmer
from data.utils import get_airtable_image_name, get_airtable_image_content_file

class Experiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100, db_index=True)
    modification_date = models.DateTimeField()
    creation_date = models.DateTimeField(default=timezone.now)
    airtable_json = JSONField(null=True, blank=True)

    farmer = models.ForeignKey(Farmer, related_name='experiments', on_delete=models.CASCADE, null=True)

    name = models.TextField()
    objectives = models.TextField(null=True)
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
    links = ArrayField(models.TextField(), blank=True, null=True)
    description = models.TextField(null=True)
    investment = models.TextField(null=True)
    xp_type = models.TextField(null=True)

    surface = models.TextField(null=True)
    surface_type = models.TextField(null=True)

    @staticmethod
    def create_from_airtable(airtable_json):
        fields = airtable_json['fields']
        links = [fields.get(x) for x in ('Site', 'Liens contenu') if fields.get(x)]
        experiment = Experiment(
            external_id=airtable_json.get('id'),
            airtable_json=airtable_json,
            modification_date=timezone.now(),
            name=fields.get('Titre de l\'XP'),
            objectives=fields.get('Objectifs'),
            method=fields.get('Méthode XP'),
            temporality=fields.get('Temporalité'),
            equipment=fields.get('Matériel'),
            execution=fields.get('Déroulé'),
            origin=fields.get('Origine'),
            additional_details=fields.get('Détails supplémentaires'),
            control_presence=fields.get('Présence d\'un témoin') == 'Oui',
            ongoing=fields.get('XP en cours') == 'Oui',
            results=fields.get('Résultats'),
            results_details=fields.get('Plus d\'information résultats'),
            links=links,
            surface=str(fields.get('Surface')) if fields.get('Surface') else None,
            surface_type=' ,'.join(fields.get('Type surface')) if fields.get('Type surface') else None,
            description=fields.get('Description'),
            investment=fields.get('Investissement'),
            xp_type=fields.get('Type d\'XP'),
        )

        return experiment


    def assign_images_from_airtable(self):
        fields = self.airtable_json['fields']
        for image in fields.get('Photos / vidéo', []):
            image_name = get_airtable_image_name(image)
            image_content_file = get_airtable_image_content_file(image)
            if image_name and image_content_file:
                experiment_image = ExperimentImage()
                experiment_image.experiment = self
                experiment_image.image.save(image_name, image_content_file, save=True)

# This is sadly necessary because we can't use an ArrayField of ImageFields
# https://code.djangoproject.com/ticket/25756#no1
class ExperimentImage(models.Model):
    experiment = models.ForeignKey(Experiment, related_name='images', on_delete=models.CASCADE, null=True)
    image = models.ImageField()
