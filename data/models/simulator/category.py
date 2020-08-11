import uuid
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from data.utils import get_airtable_media_name, get_airtable_media_content_file
from .practice import Practice

class Category(models.Model):
    """
    This model represents a category containing practices. Usually these are shown in
    the landing page.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100)
    modification_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(null=True)

    airtable_json = JSONField(null=True, blank=True)
    airtable_url = models.TextField(null=True, blank=True)

    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    practice_external_ids = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    practices = models.ManyToManyField(Practice)

    @staticmethod
    def create_from_airtable(airtable_json):
        category = Category(
            external_id=airtable_json.get('id'),
            airtable_json=airtable_json,
            airtable_url='https://airtable.com/tblJ8W5fjnatj4hki/' + airtable_json.get('id') + '/',
            title=airtable_json['fields'].get('Title').strip(),
            description=airtable_json['fields'].get('Description'),
            practice_external_ids=airtable_json['fields'].get('Practices'),
        )
        image_name = get_airtable_media_name(airtable_json, 'Image')
        image_content_file = get_airtable_media_content_file(airtable_json, 'Image')
        if image_name and image_content_file:
            category.image.save(image_name, image_content_file, save=True)
        return category
