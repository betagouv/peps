import uuid
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from data.models import Farmer
from data.utils import get_airtable_media_name, get_airtable_media_content_file

class Experiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100, db_index=True, null=False, unique=True)
    modification_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)
    airtable_json = JSONField(null=True, blank=True)

    farmer = models.ForeignKey(Farmer, related_name='experiments', on_delete=models.CASCADE, null=True)

    tags = ArrayField(models.TextField(), blank=True, null=True)
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

    mapping = {
        'name': 'Titre de l\'XP',
        'tags': 'Tags',
        'objectives': 'Objectifs',
        'method': 'Méthode XP',
        'temporality': 'Temporalité',
        'equipment': 'Matériel',
        'execution': 'Déroulé',
        'origin': 'Origine',
        'additional_details': 'Détails supplémentaires',
        'control_presence': 'Présence d\'un témoin',
        'ongoing': 'XP en cours',
        'results': 'Résultats',
        'results_details': 'Plus d\'information résultats',
        'surface': 'Surface',
        'surface_type': 'Type surface',
        'description': 'Description',
        'investment': 'Investissement',
        'xp_type': 'Type d\'XP',
    }

    def update_from_airtable(self, airtable_json):
        fields = airtable_json['fields']
        links = [fields.get(x) for x in ('Lien 1', 'Lien 2', 'Lien 3', 'Lien 4') if fields.get(x)]

        setattr(self, 'airtable_json', airtable_json)
        setattr(self, 'external_id', airtable_json.get('id'))
        setattr(self, 'links', links)

        setattr(self, 'control_presence', fields.get(self.mapping.get('control_presence') == 'Oui'))
        setattr(self, 'ongoing', fields.get(self.mapping.get('ongoing')) == 'Oui')
        setattr(self, 'surface', str(fields.get(self.mapping.get('surface'))) if fields.get(self.mapping.get('surface')) else None)
        setattr(self, 'surface_type', ' ,'.join(fields.get(self.mapping.get('surface_type'))) if fields.get(self.mapping.get('surface_type')) else None)

        # These fields can be fetched directly into this model's properties, no further treatment is needed
        direct_fields = [
            'name',
            'tags',
            'objectives',
            'method',
            'temporality',
            'equipment',
            'execution',
            'origin',
            'additional_details',
            'description',
            'investment',
            'xp_type',
            'results',
            'results_details',
        ]
        for direct_field in direct_fields:
            setattr(self, direct_field, fields.get(self.mapping.get(direct_field)))

        self.assign_media_from_airtable()


    def assign_media_from_airtable(self):
        fields = self.airtable_json['fields']
        for media in fields.get('Photos / vidéo', []):
            is_video = 'video' in media.get('type')
            is_image = 'image' in media.get('type')
            if not is_video and not is_image:
                continue
            media_name = get_airtable_media_name(media)
            media_content_file = get_airtable_media_content_file(media)
            if not media_name or not media_content_file:
                continue
            if is_image:
                experiment_image = ExperimentImage()
                experiment_image.experiment = self
                experiment_image.image.save(media_name, media_content_file, save=True)
            if is_video:
                experiment_video = ExperimentVideo()
                experiment_video.experiment = self
                experiment_video.video.save(media_name, media_content_file, save=True)


    def get_airtable_patch_payload(self, changes):
        payload = {
            'id': self.external_id,
            'fields': {}
        }

        # These fields can be fetched serialized directly into the payload, no further treatment is needed
        direct_fields = [
            'name',
            'tags',
            'objectives',
            'method',
            'temporality',
            'equipment',
            'execution',
            'origin',
            'additional_details',
            'description',
            'investment',
            'xp_type',
            'results',
            'results_details',
            'surface',
        ]
        for direct_field in direct_fields:
            if direct_field in changes:
                payload['fields'][self.mapping.get(direct_field)] = changes[direct_field]

        if 'control_presence' in direct_fields:
            payload['fields'][self.mapping.get('control_presence')] = 'Oui' if changes['control_presence'] else 'Non'

        if 'ongoing' in direct_fields:
            payload['fields'][self.mapping.get('ongoing')] = 'Oui' if changes['ongoing'] else 'Non'

        # TODO: missing fields
        # links
        # surface_type

        return payload


# This is sadly necessary because we can't use an ArrayField of ImageFields
# https://code.djangoproject.com/ticket/25756#no1
class ExperimentImage(models.Model):
    experiment = models.ForeignKey(Experiment, related_name='images', on_delete=models.CASCADE, null=True)
    image = models.ImageField()

# This is sadly necessary because we can't use an ArrayField of ImageFields
# https://code.djangoproject.com/ticket/25756#no1
class ExperimentVideo(models.Model):
    experiment = models.ForeignKey(Experiment, related_name='videos', on_delete=models.CASCADE, null=True)
    video = models.FileField(upload_to='videos/')
