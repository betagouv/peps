import uuid
from decimal import Decimal
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from data.utils import get_airtable_media_name, get_airtable_media_content_file

class Farmer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100, db_index=True, null=False, unique=True)
    modification_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)
    airtable_json = JSONField(null=True, blank=True)
    airtable_url = models.TextField(null=True)

    email = models.EmailField(db_index=True)

    name = models.TextField(null=True)
    production = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    groups = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    agriculture_types = ArrayField(models.TextField(), blank=True, null=True)
    profile_image = models.ImageField(null=True)
    postal_code = models.CharField(max_length=20, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    installation_date = models.DateField(null=True)
    personnel = models.TextField(null=True)
    livestock_type = models.CharField(max_length=120, null=True)
    livestock_number = models.TextField(null=True)
    cultures = models.TextField(null=True)
    soil_type = models.TextField(null=True)
    description = models.TextField(null=True)
    specificities = models.TextField(null=True)
    contact_possible = models.BooleanField(default=False)


    links = ArrayField(models.TextField(), blank=True, null=True)

    surface = models.TextField(null=True)
    surface_cultures = models.TextField(null=True)
    surface_meadows = models.TextField(null=True)

    output = models.TextField(null=True)


    def update_from_airtable(self, airtable_json):
        fields = airtable_json['fields']
        links = [fields.get(x) for x in ('Facebook', 'Twitter', 'Youtube', 'Site') if fields.get(x)]

        self.external_id = airtable_json.get('id')
        self.airtable_json = airtable_json
        self.name = fields.get('Prénom et Nom')
        self.production = fields.get('Productions')
        self.groups = fields.get('Groupes')
        self.agriculture_types = fields.get('Tag agriculture')
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
        self.email = fields.get('Adresse email')

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

    def create_user_if_needed(self):
        pass


# This is sadly necessary because we can't use an ArrayField of ImageFields
# https://code.djangoproject.com/ticket/25756#no1
class FarmImage(models.Model):
    farmer = models.ForeignKey(Farmer, related_name='images', on_delete=models.CASCADE, null=True)
    image = models.ImageField()
