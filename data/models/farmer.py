import uuid
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import JSONField
from django_better_admin_arrayfield.models.fields import ArrayField
from data.utils import get_airtable_media_name, get_airtable_media_content_file
from data.forms import ChoiceArrayField

PRODUCTIONS = (
    ('Grandes cultures', 'Grandes cultures'),
    ('Cultures industrielles', 'Cultures industrielles'),
    ('Élevage allaitant', 'Élevage allaitant'),
    ('Élevage laitier', 'Élevage laitier'),
    ('Élevage engraissement', 'Élevage engraissement'),
    ('Élevage poule pondeuses', 'Élevage poule pondeuses'),
    ('Cultures légumières', 'Cultures légumières'),
    ('Vigne', 'Vigne'),
    ('Autre', 'Autre'),
)

GROUPS = (
    ('DEPHY', 'DEPHY'),
    ('GIEE', 'GIEE'),
    ('30000', '30000'),
    ('CETA', 'CETA'),
    ('Groupe de coopérative', 'Groupe de coopérative'),
    ('Groupe de négoce', 'Groupe de négoce'),
    ('Groupe de chambre d\'agriculture', 'Groupe de chambre d\'agriculture'),
    ('Groupe de voisins', 'Groupe de voisins'),
    ('CUMA', 'CUMA'),
    ('Autre', 'Autre'),
)

TYPE_AGRICULTURE = (
    ('Agriculture Biologique', 'Agriculture Biologique'),
    ('Agriculture de Conservation des Sols', 'Agriculture de Conservation des Sols'),
    ('Techniques Culturales Simplifiées', 'Techniques Culturales Simplifiées'),
    ('Labour occasionnel', 'Labour occasionnel'),
    ('Agroforesterie', 'Agroforesterie'),
    ('Conventionnel', 'Conventionnel'),
    ('Cahier des charges industriel', 'Cahier des charges industriel'),
    ('Label qualité', 'Label qualité'),
    ('Autre', 'Autre'),
)

class Farmer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100, db_index=True, null=True)

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=True)

    approved = models.BooleanField(default=False, db_index=True)

    modification_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)
    airtable_json = JSONField(null=True, blank=True)
    airtable_url = models.TextField(null=True)

    name = models.TextField(null=True, blank=True)
    email = models.EmailField(db_index=True, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    installation_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)

    production = ChoiceArrayField(models.CharField(max_length=100, choices=PRODUCTIONS), default=list, null=True, blank=True)
    groups = ChoiceArrayField(models.CharField(max_length=200, choices=GROUPS), default=list, null=True, blank=True)
    agriculture_types = ChoiceArrayField(models.TextField(choices=TYPE_AGRICULTURE), default=list, null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    personnel = models.TextField(null=True, blank=True)
    livestock_type = models.CharField(max_length=120, null=True, blank=True)
    livestock_number = models.TextField(null=True, blank=True)
    cultures = models.TextField(null=True, blank=True)
    soil_type = models.TextField(null=True, blank=True)
    specificities = models.TextField(null=True, blank=True)
    contact_possible = models.BooleanField(default=False)

    links = ArrayField(models.TextField(), default=list, blank=True, null=True)

    surface = models.TextField(null=True, blank=True)
    surface_cultures = models.TextField(null=True, blank=True)
    surface_meadows = models.TextField(null=True, blank=True)

    output = models.TextField(null=True, blank=True)


    def update_from_airtable(self, airtable_json):
        fields = airtable_json['fields']
        links = [fields.get(x) for x in ('Facebook', 'Twitter', 'Youtube', 'Site') if fields.get(x)]

        self.approved = fields.get('Validation', False)
        self.external_id = airtable_json.get('id')
        self.airtable_json = airtable_json
        self.name = fields.get('Prénom et Nom')
        self.production = fields.get('Productions', [])
        self.groups = fields.get('Groupes', [])
        self.agriculture_types = fields.get('Tag agriculture', [])
        self.postal_code = fields.get('Code postal')
        self.lat = Decimal(fields.get('Latitude'))
        self.lon = Decimal(fields.get('Longitude'))
        self.installation_date = fields.get('Date d\'installation')
        self.personnel = str(fields.get('Main d\'oeuvre')) if fields.get('Main d\'oeuvre') else None
        self.livestock_type = ' ,'.join(fields.get('Type d\'élevage')) if fields.get('Type d\'élevage') else None
        self.livestock_number = str(fields.get('Nombre animaux')) if fields.get('Nombre animaux') else None
        self.cultures = fields.get('Cultures')
        self.soil_type = fields.get('Types sols')
        self.description = fields.get('Description exploitation')
        self.specificities = fields.get('Spécificités')
        self.contact_possible = fields.get('Contact possible') == 'Oui'
        self.links = links
        self.surface = str(fields.get('Surface'))
        self.surface_cultures = str(fields.get('Surface cultures')) if fields.get('Surface cultures') else None
        self.surface_meadows = str(fields.get('Surface prairie')) if fields.get('Surface prairie') else None
        self.output = str(fields.get('Rendement moyen')) if fields.get('Rendement moyen') else None
        self.email = fields.get('Adresse email').strip().lower() if fields.get('Adresse email') else None
        self.phone_number = fields.get('Numéro de téléphone')

        self.assign_main_image_from_airtable()
        self.assign_additional_images_from_airtable()

    def assign_media_from_airtable(self):
        self.assign_main_image_from_airtable()
        self.assign_additional_images_from_airtable()

    def assign_main_image_from_airtable(self):
        airtable_json = self.airtable_json
        image_name = get_airtable_media_name(airtable_json, 'Photo')
        image_content_file = get_airtable_media_content_file(airtable_json, 'Photo')
        if image_name and image_content_file:
            self.profile_image.save(image_name, image_content_file, save=True)

    def assign_additional_images_from_airtable(self):
        self.images.all().delete()
        fields = self.airtable_json['fields']
        for media in fields.get('Photos additionnelles', []):
            is_image = 'image' in media.get('type')
            if not is_image:
                continue

            media_name = get_airtable_media_name(media)
            media_content_file = get_airtable_media_content_file(media)

            if media_name and media_content_file:
                farm_image = FarmImage()
                farm_image.farmer = self
                farm_image.image.save(media_name, media_content_file, save=True)

    @property
    def approved_experiments(self):
        return self.experiments.filter(approved=True)

    @property
    def pending_experiments(self):
        return self.experiments.filter(approved=False)

    def __str__(self):
        return self.name


# This is sadly necessary because we can't use an ArrayField of ImageFields
# https://code.djangoproject.com/ticket/25756#no1
class FarmImage(models.Model):
    farmer = models.ForeignKey(Farmer, related_name='images', on_delete=models.CASCADE, null=True)
    image = models.ImageField()
    label = models.TextField(null=True, blank=True)
