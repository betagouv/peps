import uuid
from urllib.parse import quote
from django.utils import timezone
from django.db import models, connection
from django.contrib.postgres.fields import JSONField
from django.utils.html import mark_safe
from django_better_admin_arrayfield.models.fields import ArrayField
from data.models import Farmer
from data.utils import optimize_image
from data.forms import ChoiceArrayField

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

def get_next_increment():
    with connection.cursor() as cursor:
        cursor.execute("SELECT nextval('experiment_sequence_number')")
        result = cursor.fetchone()
        return result[0]

class Experiment(models.Model):
    # These two are unique values. UUIDs were chosen initially as IDs as they
    # allow client ID generation, less issues when working with multiple DBs, etc.
    # However, they are cumbersome to use on some situations (e.g., URLs), so we
    # also benefit from a short sequential ID that uses a Postgres sequence.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sequence_number = models.IntegerField(default=get_next_increment, editable=False, unique=True)
    #############################################################################

    external_id = models.CharField(max_length=100, db_index=True, null=True)
    modification_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)
    airtable_json = JSONField(null=True, blank=True)

    farmer = models.ForeignKey(Farmer, related_name='experiments', on_delete=models.CASCADE, null=True)
    approved = models.BooleanField(default=False, db_index=True)
    tags = ChoiceArrayField(models.CharField(max_length=255, choices=TAGS), default=list, blank=True, null=True)
    name = models.TextField(max_length=70)
    short_name = models.TextField(max_length=40, null=True, blank=True, help_text='Si ce champ est présent, il sera utilisé pour l\'URL')
    objectives = models.TextField(null=True, blank=True)
    equipment = models.TextField(null=True, blank=True)
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

    @property
    def url_path(self):
        if not self.farmer:
            return ''
        url_name = quote(self.short_name or self.name)
        return f'{self.farmer.url_path}/{quote("expérience")}/{url_name}--{self.sequence_number or ""}'

    @property
    def html_link(self):
        if self.sequence_number and self.approved:
            unescaped_url = f'/exploitation/{self.farmer.farm_name or self.farmer.name}--{self.farmer.sequence_number}/expérience/{self.short_name or self.name}--{self.sequence_number}'
            return mark_safe(f'<a href="{self.url_path}" target="_blank">{unescaped_url}</a>')
        else:
            return 'Pas encore live'


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
