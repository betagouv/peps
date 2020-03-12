import os
import time
import json
import traceback
import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PRACTICES_BASE = settings.AIRTABLE_PRACTICES_BASE
XP_BASE = settings.AIRTABLE_XP_BASE
MOCK_PATHS = {
    PRACTICES_BASE + '/Pratiques?view=Grid%20view': '/testdata/practices.json',
    PRACTICES_BASE + '/Types%20de%20sol?view=Grid%20view': '/testdata/soil_types.json',
    PRACTICES_BASE + '/Pratiques%2FSol?view=Grid%20view': '/testdata/practices_soil.json',
    PRACTICES_BASE + '/Pratiques%2FCultures?view=Grid%20view': '/testdata/practices_cultures.json',
    PRACTICES_BASE + '/Cultures?view=Grid%20view': '/testdata/cultures.json',
    PRACTICES_BASE + '/Pratiques%2FDepartements?view=Grid%20view': '/testdata/practices_departments.json',
    PRACTICES_BASE + '/Departements?view=Grid%20view': '/testdata/departments.json',
    PRACTICES_BASE + '/Pratiques%2FAdventices?view=Grid%20view': '/testdata/practices_weeds.json',
    PRACTICES_BASE + '/Adventices?view=Grid%20view': '/testdata/weeds.json',
    PRACTICES_BASE + '/Pratiques%2FRavageurs?view=Grid%20view': '/testdata/practices_pests.json',
    PRACTICES_BASE + '/Ravageurs?view=Grid%20view': '/testdata/pests.json',
    PRACTICES_BASE + '/Familles?view=Grid%20view': '/testdata/practice_groups.json',
    PRACTICES_BASE + '/Marges%20de%20manoeuvre?view=Grid%20view': '/testdata/mechanisms.json',
    PRACTICES_BASE + '/Liens?view=Grid%20view': '/testdata/resources.json',
    PRACTICES_BASE + '/logos?view=Grid%20view': '/testdata/resource_images.json',
    PRACTICES_BASE + '/Types%20de%20pratique?view=Grid%20view': '/testdata/practice_types.json',
    PRACTICES_BASE + '/Pratiques%2FGlyphosate?view=Grid%20view': '/testdata/practices_glyphosate.json',
    PRACTICES_BASE + '/Glyphosate?view=Grid%20view': '/testdata/glyphosate.json',
    PRACTICES_BASE + '/Categories?view=Grid%20view': '/testdata/categories.json',
    XP_BASE + '/Agriculteur?view=Grid%20view': '/testdata/farmers.json',
    XP_BASE + '/XP?view=Grid%20view': '/testdata/experiments.json',
}

class Command(BaseCommand):
    help = 'Updates the test data with the info from Airtable'

    def handle(self, *args, **options):
        for url, path in MOCK_PATHS.items():
            try:
                self.stdout.write(self.style.HTTP_SUCCESS('Fetching %s' % url))
                json_data = {'records': _get_airtable_data(url)}
                with open(BASE_DIR + '/api/tests' + path, 'w+') as file:
                    file.write(json.dumps(json_data))
            except Exception as _:
                print(traceback.format_exc())
                raise CommandError('Failed fetching "%s"' % url)

        self.stdout.write(self.style.SUCCESS('Successfully generated test data'))


def _get_airtable_data(url, offset=None):
    time.sleep(settings.AIRTABLE_REQUEST_INTERVAL_SECONDS) # lazy way to throttle, sorry
    base_url = 'https://api.airtable.com/v0/'
    headers = {
        'Authorization': 'Bearer ' + settings.AIRTABLE_API_KEY,
        'Accept': 'application/json',
    }

    url_params = ''
    if offset:
        divider = '&' if '?' in url else '?'
        url_params = '%soffset=%s' % (divider, offset)

    response = requests.get(base_url + url + url_params, headers=headers)
    print(base_url + url + url_params)
    if not response.status_code == 200:
        raise Exception
    json_response = json.loads(response.text)
    records = json_response['records']
    offset = json_response.get('offset')
    if offset:
        return records + _get_airtable_data(url, offset)
    return records
