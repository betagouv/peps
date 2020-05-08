import uuid
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import JSONField
from django_better_admin_arrayfield.models.fields import ArrayField
from data.models import Farmer
from data.utils import optimize_image
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

    tags = ChoiceArrayField(models.CharField(max_length=255, choices=TAGS), default=list, blank=True, null=True)
    name = models.TextField(unique=True)
    objectives = models.TextField(null=True, blank=True)
    method = models.TextField(null=True, blank=True)
    temporality = models.TextField(null=True, blank=True)
    equipment = models.TextField(null=True, blank=True)
    origin = models.TextField(null=True, blank=True)
    execution = models.TextField(null=True, blank=True)
    additional_details = models.TextField(null=True, blank=True)
    control_presence = models.BooleanField(null=True, blank=True)
    ongoing = models.BooleanField(null=True, blank=True)
    results = models.TextField(null=True, blank=True, choices=RESULTS)
    results_details = models.TextField(null=True, blank=True)
    links = ArrayField(models.TextField(), default=list, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    investment = models.TextField(null=True, blank=True)
    xp_type = models.TextField(null=True, blank=True, choices=XP_TYPE)

    surface = models.TextField(null=True, blank=True)
    surface_type = ChoiceArrayField(models.TextField(choices=SURFACE_TYPE), default=list, blank=True, null=True)

    def __str__(self):
        return self.name


# This is sadly necessary because we can't use an ArrayField of ImageFields
# https://code.djangoproject.com/ticket/25756#no1
class ExperimentImage(models.Model):
    experiment = models.ForeignKey(Experiment, related_name='images', on_delete=models.CASCADE, null=True)
    image = models.ImageField()
    label = models.TextField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.image = optimize_image(self.image, self.image.name)
        super(ExperimentImage, self).save(force_insert, force_update, using, update_fields)


# This is sadly necessary because we can't use an ArrayField of ImageFields
# https://code.djangoproject.com/ticket/25756#no1
class ExperimentVideo(models.Model):
    experiment = models.ForeignKey(Experiment, related_name='videos', on_delete=models.CASCADE, null=True)
    video = models.FileField(upload_to='videos/')
    label = models.TextField(null=True, blank=True)
