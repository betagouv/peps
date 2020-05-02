import uuid
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import JSONField
from django_better_admin_arrayfield.models.fields import ArrayField
from data.models import Farmer
from data.utils import get_airtable_media_name, get_airtable_media_content_file
from data.forms import ChoiceArrayField

MAPPINGS = {
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

# (Stored in db, seen in drop-down)
XP_TYPE = (
    ('Changement important de l\'exploitation', 'Changement important de l\'exploitation'),
    ('Amélioration de l\'existant', 'Amélioration de l\'existant'),
)

TAGS = (
    ("Changement important de l'exploitation", "Changement important de l'exploitation"),
    ("Amélioration de l'existant", "Amélioration de l'existant"),
    ("Maladies", "Maladies"),
    ("Insectes et ravageurs", "Insectes et ravageurs"),
    ("Adventices", "Adventices"),
    ("Environnement & biodiversité", "Environnement & biodiversité"),
    ("Diversification", "Diversification"),
    ("Autonomie fourragère", "Autonomie fourragère"),
    ("Productivité", "Productivité"),
    ("Organisation du travail", "Organisation du travail"),
    ("Réduction des charges", "Réduction des charges"),
    ("Autre", "Autre"),
)

RESULTS = (
    ("XP qui fonctionne, elle est intégrée à l'exploitation", "XP qui fonctionne, elle est intégrée à l'exploitation"),
    ("XP prometteuse, en cours d'amélioration", "XP prometteuse, en cours d'amélioration"),
    ("XP abandonnée, les résultats ne sont pas satisfaisants", "XP abandonnée, les résultats ne sont pas satisfaisants"),
    ("XP en suspens, les conditions ne sont plus réunies", "XP en suspens, les conditions ne sont plus réunies"),
    ("XP qui commence, les premiers résultats sont à venir", "XP qui commence, les premiers résultats sont à venir"),
)

SURFACE_TYPE = (
    ("Toutes les surfaces", "Toutes les surfaces"),
    ("Plusieurs parcelles", "Plusieurs parcelles"),
    ("Une parcelle", "Une parcelle"),
    ("Des bandes", "Des bandes"),
    ("Des carrés", "Des carrés"),
)

class Experiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100, db_index=True, null=True)
    modification_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)
    airtable_json = JSONField(null=True, blank=True)

    farmer = models.ForeignKey(Farmer, related_name='experiments', on_delete=models.CASCADE, null=True)

    approved = models.BooleanField(default=False, db_index=True)

    tags = ChoiceArrayField(models.CharField(max_length=255, choices=TAGS), default=list)
    name = models.TextField(unique=True)
    objectives = models.TextField(null=True)
    method = models.TextField(null=True)
    temporality = models.TextField(null=True)
    equipment = models.TextField(null=True)
    origin = models.TextField(null=True)
    execution = models.TextField(null=True)
    additional_details = models.TextField(null=True)
    control_presence = models.BooleanField(null=True)
    ongoing = models.BooleanField(null=True)
    results = models.TextField(null=True, choices=RESULTS)
    results_details = models.TextField(null=True)
    links = ArrayField(models.TextField(), default=list)
    description = models.TextField(null=True)
    investment = models.TextField(null=True)
    xp_type = models.TextField(null=True, choices=XP_TYPE)

    surface = models.TextField(null=True)
    surface_type = ChoiceArrayField(models.TextField(choices=SURFACE_TYPE), default=list)

    def update_from_airtable(self, airtable_json):
        fields = airtable_json['fields']
        links = [fields.get(x) for x in ('Lien 1', 'Lien 2', 'Lien 3', 'Lien 4') if fields.get(x)]

        setattr(self, 'airtable_json', airtable_json)
        setattr(self, 'external_id', airtable_json.get('id'))
        setattr(self, 'links', links)

        setattr(self, 'control_presence', fields.get(MAPPINGS.get('control_presence')) == 'Oui')
        setattr(self, 'ongoing', fields.get(MAPPINGS.get('ongoing')) == 'Oui')
        setattr(self, 'surface', str(fields.get(MAPPINGS.get('surface'))) if fields.get(MAPPINGS.get('surface')) else None)

        # These fields can be fetched directly into this model's properties, no further treatment is needed
        direct_fields = [
            'name',
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
            value = fields.get(MAPPINGS.get(direct_field))
            setattr(self, direct_field, value)

        array_fields = [
            'tags',
            'surface_type',
        ]
        for array_field in array_fields:
            value = fields.get(MAPPINGS.get(array_field), [])
            setattr(self, array_field, value)

        self.assign_media_from_airtable()


    def assign_media_from_airtable(self):
        fields = self.airtable_json['fields']
        self.images.all().delete()
        self.videos.all().delete()
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

    @staticmethod
    def get_airtable_payload(changes, external_id=None):
        payload = {
            'fields': {}
        }

        if external_id:
            payload['id'] = external_id

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
            'surface_type',
        ]
        for direct_field in direct_fields:
            if direct_field in changes:
                payload['fields'][MAPPINGS.get(direct_field)] = changes[direct_field]

        if 'control_presence' in changes:
            payload['fields'][MAPPINGS.get('control_presence')] = 'Oui' if changes['control_presence'] else 'Non'

        if 'ongoing' in changes:
            payload['fields'][MAPPINGS.get('ongoing')] = 'Oui' if changes['ongoing'] else 'Non'

        # TODO: missing fields
        # links
        # photos
        # videos

        return payload

    def __str__(self):
        return self.name


# This is sadly necessary because we can't use an ArrayField of ImageFields
# https://code.djangoproject.com/ticket/25756#no1
class ExperimentImage(models.Model):
    experiment = models.ForeignKey(Experiment, related_name='images', on_delete=models.CASCADE, null=True)
    image = models.ImageField()
    label = models.TextField(null=True)


# This is sadly necessary because we can't use an ArrayField of ImageFields
# https://code.djangoproject.com/ticket/25756#no1
class ExperimentVideo(models.Model):
    experiment = models.ForeignKey(Experiment, related_name='videos', on_delete=models.CASCADE, null=True)
    video = models.FileField(upload_to='videos/')
    label = models.TextField(null=True)
