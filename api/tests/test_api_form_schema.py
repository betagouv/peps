import json
import os
from unittest.mock import MagicMock
import datetime
import dateutil
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_api_key.models import APIKey
from django.conf import settings
from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from data.adapters import PracticesAirtableAdapter
from data.models import Practice, DiscardAction
from data.models import Category, Resource, Farmer, Experiment
from api.utils import AsanaUtils

# In these tests we will mock some protected functions so we'll need to access them
# pylint: disable = protected-access

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

@override_settings(AIRTABLE_REQUEST_INTERVAL_SECONDS=0.0)
class TestApiFormSchema(TestCase):

    def setUp(self):
        _populate_database()
        self.client = APIClient(enforce_csrf_checks=False)
        self.api_key, self.key = APIKey.objects.create_key(name='test-key')


    def test_form_schema_unauthenticated(self):
        """
        Tests the form schema API endpoint without authentication,
        which should work since it is an open endpoint.
        """
        self.client.logout()
        response = self.client.get(reverse('form_schema'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_form_schema_session_auth(self):
        """
        Tests the form schema API using the session (user specific)
        authentication. Note the CSRF token is not enforced on tests.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('form_schema'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        self.assertIn('schema', body)
        self.assertIn('options', body)


    def test_form_schema_api_key_auth(self):
        """
        Tests the form_schema API using the Api key, meant to identify
        projects and apps, not users.
        """
        self.client.logout()
        response = self.client.get(
            reverse('form_schema'),
            **{'HTTP_AUTHORIZATION': 'Api-Key ' + self.key},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        self.assertIn('schema', body)
        self.assertIn('options', body)


def _populate_database():
    User.objects.create_user(username='testuser', password='12345')
    User.objects.create_superuser(username='testsuperuser', password='12345')
