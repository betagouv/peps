import os
from unittest.mock import MagicMock
from unittest import skip
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_api_key.models import APIKey
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from data.adapters import PracticesAirtableAdapter

# In these tests we will mock some protected functions so we'll need to access them
# pylint: disable = protected-access

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

@override_settings(AIRTABLE_REQUEST_INTERVAL_SECONDS=0.0)
@skip("Redirection en place vers rex-agri")
class TestApiAirtable(TestCase):

    def setUp(self):
        _populate_database()
        self.client = APIClient(enforce_csrf_checks=False)
        self.api_key, self.key = APIKey.objects.create_key(name='test-key')


    def test_refresh_airtable_form_unauthenticated(self):
        """
        Tests the refresh data without authentication,
        which should not work. We mock Airtable's API
        to carry this test out.
        """
        self.client.logout()
        original_function = PracticesAirtableAdapter.update
        PracticesAirtableAdapter.update = MagicMock()
        try:
            response = self.client.post(reverse('refresh_data'), {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            PracticesAirtableAdapter.update.assert_not_called()
        finally:
            PracticesAirtableAdapter.update = original_function


    def test_refresh_airtable_form_session_auth(self):
        """
        Tests the refresh data authenticated as non-admin,
        which should not work. We mock Airtable's API
        to carry this test out.
        """
        self.client.login(username='testuser', password='12345')
        original_function = PracticesAirtableAdapter.update
        PracticesAirtableAdapter.update = MagicMock()
        try:
            response = self.client.post(reverse('refresh_data'), {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            PracticesAirtableAdapter.update.assert_not_called()
        finally:
            PracticesAirtableAdapter.update = original_function


    def test_refresh_airtable_form_session_admin_auth(self):
        """
        Tests the refresh data endpoint using the session (user specific)
        authentication. We mock Airtable's API to carry this test out.
        """
        self.client.login(username='testsuperuser', password='12345')
        original_function = PracticesAirtableAdapter.update
        PracticesAirtableAdapter.update = MagicMock()
        try:
            response = self.client.post(reverse('refresh_data'), {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            PracticesAirtableAdapter.update.assert_called_once()
        finally:
            PracticesAirtableAdapter.update = original_function


    def test_refresh_airtable_form_api_key_auth(self):
        """
        Tests the refresh data endpoint using the Api key, meant to identify
        projects and apps, not users. We mock Airtable's API to carry
        this test out.
        """
        self.client.logout()
        original_function = PracticesAirtableAdapter.update
        PracticesAirtableAdapter.update = MagicMock()
        try:
            response = self.client.post(
                reverse('refresh_data'),
                format='json',
                **{'HTTP_AUTHORIZATION': 'Api-Key ' + self.key},
            )
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            PracticesAirtableAdapter.update.assert_not_called()
        finally:
            PracticesAirtableAdapter.update = original_function

def _populate_database():
    get_user_model().objects.create_user(username='testuser', password='12345')
    get_user_model().objects.create_superuser(username='testsuperuser', password='12345')
