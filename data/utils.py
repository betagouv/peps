
import time
import json
import requests
from io import BytesIO
from PIL import Image as Img
from PIL import ExifTags
from django.conf import settings
from django.core.files.base import ContentFile

def get_airtable_media_url(json_payload, field_name=None):
    payload = json_payload['fields'].get(field_name) if field_name else json_payload
    if not payload:
        return None
    payload = [payload] if not isinstance(payload, list) else payload
    return payload[0].get('url')

def get_airtable_media_name(json_payload, field_name=None):
    payload = json_payload['fields'].get(field_name) if field_name else json_payload
    if not payload:
        return None
    payload = [payload] if not isinstance(payload, list) else payload
    media_id = payload[0].get('id') or ''
    filename = payload[0].get('filename') or ''
    extension = filename.split('.')[-1]
    return media_id + '.' + extension if media_id and filename else None

def get_airtable_media_content_file(json_payload, field_name=None):
    media_url = get_airtable_media_url(json_payload, field_name)
    payload = json_payload['fields'].get(field_name) if field_name else json_payload

    if not payload:
        return None

    payload = [payload] if not isinstance(payload, list) else payload
    file_type = payload[0].get('type')

    if not media_url:
        return None
    try:
        media_content = _correct_image_rotation(requests.get(media_url).content, file_type)
        return ContentFile(media_content)
    except Exception as _:
        return None

def _correct_image_rotation(image_content, file_type):
    if not file_type or not 'image' in file_type:
        return image_content

    image_format = file_type.split('/')[1] if len(file_type.split('/')) > 0 else None

    if not image_content:
        return image_content

    pillow_image = Img.open(BytesIO(image_content))
    orientation_tag = None

    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            orientation_tag = orientation

    if not pillow_image or not orientation_tag or not pillow_image._getexif():
        return image_content

    exif = dict(pillow_image._getexif().items())
    orientation = exif.get(orientation_tag)

    if not orientation:
        return image_content

    if orientation == 3:
        pillow_image = pillow_image.rotate(180, expand=True)
    elif orientation == 6:
        pillow_image = pillow_image.rotate(270, expand=True)
    elif orientation == 8:
        pillow_image = pillow_image.rotate(90, expand=True)
    else:
        return image_content

    output = BytesIO()
    try:
        pillow_image.save(output, format=image_format)
    except Exception as _:
        print(_)
        return image_content

    return output.getvalue()

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
