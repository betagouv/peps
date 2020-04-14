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

    def update_from_airtable(self, airtable_json):
        fields = airtable_json['fields']
        links = [fields.get(x) for x in ('Lien 1', 'Lien 2', 'Lien 3', 'Lien 4') if fields.get(x)]

        self.external_id = airtable_json.get('id')
        self.airtable_json = airtable_json
        self.name = fields.get('Titre de l\'XP')
        self.tags = fields.get('Tags')
        self.objectives = fields.get('Objectifs')
        self.method = fields.get('Méthode XP')
        self.temporality = fields.get('Temporalité')
        self.equipment = fields.get('Matériel')
        self.execution = fields.get('Déroulé')
        self.origin = fields.get('Origine')
        self.additional_details = fields.get('Détails supplémentaires')
        self.control_presence = fields.get('Présence d\'un témoin') == 'Oui'
        self.ongoing = fields.get('XP en cours') == 'Oui'
        self.results = fields.get('Résultats')
        self.results_details = fields.get('Plus d\'information résultats')
        self.links = links
        self.surface = str(fields.get('Surface')) if fields.get('Surface') else None
        self.surface_type = ' ,'.join(fields.get('Type surface')) if fields.get('Type surface') else None
        self.description = fields.get('Description')
        self.investment = fields.get('Investissement')
        self.xp_type = fields.get('Type d\'XP')

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
