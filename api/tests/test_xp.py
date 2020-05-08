import os
from unittest.mock import Mock
import requests
from django.test import TestCase, override_settings
from data.models import Farmer, Experiment
from data.adapters import ExperimentsAirtableAdapter

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

@override_settings(AIRTABLE_REQUEST_INTERVAL_SECONDS=0.0, MEDIA_ROOT=os.path.join(BASE_DIR, 'media/test'))
class TestXP(TestCase):
    pass

class MockResponse:
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code

    @property
    def text(self):
        return self.content
