
import time
import json
import requests
from django.conf import settings
from django.core.files.base import ContentFile

def get_airtable_image_url(json_payload, field_name=None):
    payload = json_payload['fields'].get(field_name) if field_name else json_payload
    if not payload:
        return None
    payload = [payload] if not isinstance(payload, list) else payload
    return payload[0].get('url')

def get_airtable_image_name(json_payload, field_name=None):
    payload = json_payload['fields'].get(field_name) if field_name else json_payload
    if not payload:
        return None
    payload = [payload] if not isinstance(payload, list) else payload
    image_id = payload[0].get('id') or ''
    filename = payload[0].get('filename') or ''
    extension = filename.split('.')[-1]
    return image_id + '.' + extension if image_id and filename else None

def get_airtable_image_content_file(json_payload, field_name=None):
    image_url = get_airtable_image_url(json_payload, field_name)
    if not image_url:
        return None
    try:
        image_content = requests.get(image_url)
        return ContentFile(image_content.content)
    except Exception as _:
        return None

def _get_airtable_data(url, base, offset=None):
    time.sleep(settings.AIRTABLE_REQUEST_INTERVAL_SECONDS) # lazy way to throttle, sorry
    base_url = 'https://api.airtable.com/v0/' + base + '/'
    headers = {
        'Authorization': 'Bearer ' + settings.AIRTABLE_API_KEY,
        'Accept': 'application/json',
    }

    url_params = ''
    if offset:
        divider = '&' if '?' in url else '?'
        url_params = '%soffset=%s' % (divider, offset)

    response = requests.get(base_url + url + url_params, headers=headers)
    if not response.status_code == 200:
        print('Terrible error while fetching: ' + url)
        return {}
    json_response = json.loads(response.text)
    records = json_response['records']
    offset = json_response.get('offset')
    if offset:
        return records + _get_airtable_data(url, base, offset)
    return records