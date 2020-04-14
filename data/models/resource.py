import uuid
from enum import Enum
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from data.utils import get_airtable_media_name, get_airtable_media_content_file

class ResourceType(Enum):
    SITE_WEB = 1
    PDF = 2
    VIDEO = 3

class Resource(models.Model):
    """
    PDFs, web sites or videos that provide more information and
    context to practices.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100)
    modification_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)

    airtable_json = JSONField(null=True, blank=True)
    airtable_url = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True)

    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    resource_type = models.IntegerField(blank=True, null=True)
    url = models.TextField()

    def get_type_name(self):
        if not self.resource_type:
            return None
        return ResourceType(self.resource_type).name

    @staticmethod
    def create_from_airtable(airtable_json, airtable_resource_images):
        url = airtable_json['fields'].get('Url')
        resource = Resource(
            external_id=airtable_json.get('id'),
            airtable_json=airtable_json,
            airtable_url='https://airtable.com/tblVb2GDuCPGUrt35/' + airtable_json.get('id') + '/',
            name=airtable_json['fields'].get('Nom'),
            description=airtable_json['fields'].get('Description'),
            resource_type=Resource._get_resource_type_from_airtable(airtable_json),
            url=url,
        )
        resource_image = next((x for x in airtable_resource_images if x['fields'].get('URL_principal') in url), None)
        if resource_image:
            image_name = get_airtable_media_name(resource_image, 'logo')
            image_content_file = get_airtable_media_content_file(resource_image, 'logo')
            if image_name and image_content_file:
                resource.image.save(image_name, image_content_file, save=True)
        return resource

    @staticmethod
    def _get_resource_type_from_airtable(airtable_json):
        resource_type = airtable_json['fields'].get('Type')
        if resource_type == 'PDF':
            return ResourceType.PDF.value
        if resource_type == 'Site web':
            return ResourceType.SITE_WEB.value
        if resource_type == 'Vidéo':
            return ResourceType.VIDEO.value
        return None
