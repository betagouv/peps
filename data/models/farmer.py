import uuid
from urllib.parse import quote
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models, connection
from django.db.models import JSONField
from django.utils.html import mark_safe
from django_better_admin_arrayfield.models.fields import ArrayField
from data.utils import optimize_image
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
    ('Cultures spécialisées', 'Cultures spécialisées'),
    ('Apiculture', 'Apiculture'),
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
    ('Civam', 'Civam'),
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
    ('Label environnemental (HVE)', 'Label environnemental (HVE)'),
    ('Autre', 'Autre'),
)

TYPE_LIVESTOCK = (
    ('Bovin', 'Bovin'),
    ('Ovin', 'Ovin'),
    ('Caprin', 'Caprin'),
    ('Avicole', 'Avicole'),
    ('Porcin', 'Porcin'),
    ('Autre', 'Autre'),
)

def get_next_increment():
    with connection.cursor() as cursor:
        cursor.execute("SELECT nextval('farmer_sequence_number')")
        result = cursor.fetchone()
        return result[0]

class Farmer(models.Model):

    class Meta:
        ordering = ['name']

    # These two are unique values. UUIDs were chosen initially as IDs as they
    # allow client ID generation, less issues when working with multiple DBs, etc.
    # However, they are cumbersome to use on some situations (e.g., URLs), so we
    # also benefit from a short sequential ID that uses a Postgres sequence.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sequence_number = models.IntegerField(default=get_next_increment, editable=False, unique=True)
    #############################################################################

    external_id = models.CharField(max_length=100, db_index=True, null=True)

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=True)

    approved = models.BooleanField(default=False, db_index=True)

    modification_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)
    airtable_json = JSONField(null=True, blank=True)
    airtable_url = models.TextField(null=True)

    cgu_approved = models.BooleanField(default=False)

    name = models.TextField(null=True, blank=True)
    farm_name = models.TextField(null=True, blank=True)
    email = models.EmailField(db_index=True, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    installation_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    cultures = models.TextField(null=True, blank=True)

    lat = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)
    lon = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)

    production = ChoiceArrayField(models.CharField(max_length=100, choices=PRODUCTIONS), default=list, null=True, blank=True)
    groups = ChoiceArrayField(models.CharField(max_length=200, choices=GROUPS), default=list, null=True, blank=True)
    agriculture_types = ChoiceArrayField(models.TextField(choices=TYPE_AGRICULTURE), default=list, null=True, blank=True)

    profile_image = models.ImageField(null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    personnel = models.TextField(null=True, blank=True)

    livestock_types = ChoiceArrayField(models.TextField(choices=TYPE_LIVESTOCK), default=list, null=True, blank=True)

    livestock_number = models.TextField(null=True, blank=True)
    soil_type = models.TextField(null=True, blank=True)
    specificities = models.TextField(null=True, blank=True)
    contact_possible = models.BooleanField(default=True)

    email_for_messages_allowed = models.BooleanField(default=True)

    links = ArrayField(models.TextField(), default=list, blank=True, null=True)

    surface = models.TextField(null=True, blank=True)
    surface_cultures = models.TextField(null=True, blank=True)
    surface_meadows = models.TextField(null=True, blank=True)

    output = models.TextField(null=True, blank=True)

    onboarding_shown = models.BooleanField(default=False)

    @property
    def approved_experiments(self):
        return self.experiments.filter(state='Validé')

    @property
    def pending_experiments(self):
        return self.experiments.filter(approved=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.profile_image:
            self.profile_image = optimize_image(self.profile_image, self.profile_image.name)
        if self.email:
            self.email = get_user_model().objects.normalize_email(self.email)
        super(Farmer, self).save(force_insert, force_update, using, update_fields)

    @property
    def url_slug(self):
        url_name = quote(self.farm_name or self.name)
        return f'{url_name}--{self.sequence_number or ""}'

    @property
    def url_path(self):
        url_name = quote(self.farm_name or self.name)
        return f'/exploitation/{self.url_slug}'

    @property
    def html_link(self):
        """
        This is used in the admin panel to link to the farmer's page
        """
        if self.sequence_number and self.approved:
            unescaped_url = f'/exploitation/{self.farm_name or self.name}--{self.sequence_number}'
            return mark_safe(f'<a href="{self.url_path}" target="_blank">{unescaped_url}</a>')
        else:
            return 'Pas encore live'

    def __str__(self):
        return self.name


# This is sadly necessary because we can't use an ArrayField of ImageFields
# https://code.djangoproject.com/ticket/25756#no1
class FarmImage(models.Model):
    farmer = models.ForeignKey(Farmer, related_name='images', on_delete=models.CASCADE, null=True)
    image = models.ImageField()
    label = models.TextField(null=True, blank=True)
    copyright = models.TextField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.image = optimize_image(self.image, self.image.name)
        super(FarmImage, self).save(force_insert, force_update, using, update_fields)


def create_user_if_needed(sender, instance, **kwargs):
    if sender == Farmer and instance.email:
        email = get_user_model().objects.normalize_email(instance.email)
        existing_user = get_user_model().objects.filter(email=email).first()
        if existing_user:
            instance.user = existing_user
        else:
            random_password = get_user_model().objects.make_random_password()
            new_user = get_user_model().objects.create_user(email=email, username=email, password=random_password)
            instance.user = new_user
    if sender == Farmer and not instance.email:
        instance.user = None

models.signals.pre_save.connect(create_user_if_needed, sender=Farmer)
