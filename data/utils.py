
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
    is_image = payload[0].get('type') and 'image' in payload[0].get('type')

    if is_image:
        # Since we will later optimize the image into a jpg, the extension we will use will
        # always be .jpg
        extension = 'jpg'
    else:
        extension = filename.split('.')[-1]

    return media_id + '.' + extension if media_id and filename else None

def get_airtable_media_content_file(json_payload, field_name=None):
    media_url = get_airtable_media_url(json_payload, field_name)
    payload = json_payload['fields'].get(field_name) if field_name else json_payload

    if not payload:
        return None

    payload = [payload] if not isinstance(payload, list) else payload
    file_type = payload[0].get('type')
    image_format = 'jpeg'

    if not media_url:
        return None
    try:
        media_response = requests.get(media_url)
        media_content = media_response.content
        if image_format and 'image' in file_type:
            pillow_image = Img.open(BytesIO(media_content))
            pillow_image = _optimize_image(pillow_image)

            output = BytesIO()
            pillow_image.save(output, optimize=True, format=image_format)
            media_content = output.getvalue()

        if media_content:
            return ContentFile(media_content)
    except Exception as _:
        return None

def _optimize_image(pillow_image):
    """
    This method will perform several transformation to the image
    with the goal of optimizing its size and setting the correct
    rotation.
    """
    pillow_image = _rotate_image(pillow_image)
    pillow_image = _resize_image(pillow_image)
    pillow_image = _remove_alpha_channel(pillow_image)

    return pillow_image

def _rotate_image(pillow_image):
    orientation_tag = next(filter(lambda x: ExifTags.TAGS[x] == 'Orientation', ExifTags.TAGS), None)
    exif_data = pillow_image._getexif()

    if not orientation_tag or not exif_data:
        return pillow_image

    orientation = dict(exif_data.items()).get(orientation_tag)

    if orientation == 3:
        return pillow_image.rotate(180, expand=True)
    if orientation == 6:
        return pillow_image.rotate(270, expand=True)
    if orientation == 8:
        return pillow_image.rotate(90, expand=True)
    return pillow_image

def _resize_image(pillow_image):
    max_size = 2000
    needs_resize = pillow_image.width > max_size or pillow_image.height > max_size
    if not needs_resize:
        return pillow_image

    if pillow_image.width >= pillow_image.height:
        new_width = max_size
        new_height = max_size * pillow_image.height / pillow_image.width
    else:
        new_width = max_size * pillow_image.width / pillow_image.height
        new_height = max_size

    return pillow_image.resize((int(new_width), int(new_height)))

def _remove_alpha_channel(pillow_image):
    if pillow_image.mode in ('RGBA', 'LA'):
        background = Img.new(pillow_image.mode[:-1], pillow_image.size, '#FFFFFF')
        background.paste(pillow_image, pillow_image.split()[-1])
        pillow_image = background
    return pillow_image


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
