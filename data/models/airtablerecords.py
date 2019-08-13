import uuid
import json
import time
from dateutil.relativedelta import relativedelta
import requests
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

class AirtableRecords(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pratiques = JSONField()
    marges = JSONField()
    soil_types = JSONField()
    soil_pratiques = JSONField()
    cultures = JSONField()
    culture_types = JSONField()
    departments = JSONField()
    departments_pratiques = JSONField()
    weeds = JSONField()
    pests = JSONField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_fetch_date = models.DateTimeField()

    cache_time = relativedelta(years=30)

    @staticmethod
    def get_default():
        saved_entry = AirtableRecords.objects.first()

        if saved_entry and not saved_entry.cache_expired():
            return saved_entry

        if not saved_entry:
            saved_entry = AirtableRecords()

        if saved_entry.cache_expired():
            saved_entry.fetch()

        saved_entry.save()
        return saved_entry

    @staticmethod
    def refresh_data():
        saved_entry = AirtableRecords.objects.first()

        if not saved_entry:
            saved_entry = AirtableRecords()

        saved_entry.fetch()
        saved_entry.save()

    def cache_expired(self):
        now = timezone.now()
        return not self.last_fetch_date or self.last_fetch_date + self.cache_time < now

    def fetch(self):
        base_url = 'https://api.airtable.com/v0/appqlHvlvvxHDkQNY/'
        headers = {
            'Authorization': 'Bearer ' + settings.AIRTABLE_API_KEY,
            'Accept': 'application/json',
        }

        attribute_route = {
            'pratiques': base_url + 'Pratiques?view=Grid%20view',
            'marges': base_url + 'Marges%20de%20manoeuvre?view=Grid%20view',
            'soil_types': base_url + 'Types%20de%20sol?view=Grid%20view',
            'soil_pratiques': base_url + 'Pratiques%2FSol?view=Grid%20view',
            'cultures': base_url + 'Cultures?view=Grid%20view',
            'culture_types': base_url + 'Types%20de%20culture?view=Grid%20view',
            'departments_pratiques': base_url + 'Pratiques%2FDepartements?view=Grid%20view',
            'departments': base_url + 'Departements?view=Grid%20view',
            'weeds': base_url + 'Adventices?view=Grid%20view',
            'pests': base_url + 'Ravageurs?view=Grid%20view',
        }

        for key, url in attribute_route.items():
            response = requests.get(url, headers=headers)
            if not response.status_code == 200:
                print('Terrible error while fetching: ' + key)
                continue
            setattr(self, key, json.loads(response.text)['records'])
            time.sleep(0.20)

        self.last_fetch_date = timezone.now()
