
import requests
from django.core.files.base import ContentFile

def get_airtable_image_url(json_payload, field_name):
    if not json_payload['fields'].get(field_name):
        return None
    return json_payload['fields'].get(field_name)[0].get('url')

def get_airtable_image_name(json_payload, field_name):
    if not json_payload['fields'].get(field_name):
        return None
    image_id = json_payload['fields'].get(field_name)[0].get('id') or ''
    filename = json_payload['fields'].get(field_name)[0].get('filename') or ''
    extension = filename.split('.')[-1]
    return image_id + '.' + extension if image_id and filename else None

def get_airtable_image_content_file(json_payload, field_name):
    image_url = get_airtable_image_url(json_payload, field_name)
    if not image_url:
        return None
    try:
        image_content = requests.get(image_url)
        return ContentFile(image_content.content)
    except Exception as _:
        return None
