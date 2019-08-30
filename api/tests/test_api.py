import json
from unittest.mock import MagicMock
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_api_key.models import APIKey
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from data.adapters import AirtableAdapter

class TestApi(TestCase):

    def setUp(self):
        _populate_database()
        self.client = APIClient(enforce_csrf_checks=False)
        self.api_key, self.key = APIKey.objects.create_key(name='test-key')



    def test_unathenticated_user(self):
        """
        Tests the rankings API without authentication,
        which should not work
        """
        self.client.logout()
        response = self.client.post(
            reverse('calculate_rankings'),
            json={},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_rankings_session_auth(self):
        """
        Tests the rankings API using the session (user specific)
        authentication. Note the CSRF token is not enforced on tests.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('calculate_rankings'),
            {"answers": {"problem": "DESHERBAGE", "rotation": [], "department": "01"}, "practice_blacklist": []},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        self.assertIn('practices', body)
        self.assertIn('suggestions', body)


    def test_rankings_api_key_auth(self):
        """
        Tests the rankings API using the Api key, meant to identify
        projects and apps, not users.
        """
        self.client.logout()
        response = self.client.post(
            reverse('calculate_rankings'),
            {"answers": {"problem": "DESHERBAGE", "rotation": [], "department": "01"}, "practice_blacklist": []},
            format='json',
            **{'HTTP_AUTHORIZATION': 'Api-Key ' + self.key},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        self.assertIn('practices', body)
        self.assertIn('suggestions', body)


    def test_refresh_airtable_unauthenticated(self):
        """
        Tests the refresh data without authentication,
        which should not work. We mock Airtable's API
        to carry this test out.
        """
        self.client.logout()
        original_function = AirtableAdapter.update_practices
        AirtableAdapter.update_practices = MagicMock()
        try:
            response = self.client.post(reverse('refresh_data'), {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            AirtableAdapter.update_practices.assert_not_called()
        finally:
            AirtableAdapter.update_practices = original_function


    def test_refresh_airtable_session_auth(self):
        """
        Tests the refresh data endpoint using the session (user specific)
        authentication. We mock Airtable's API to carry this test out.
        """
        self.client.login(username='testuser', password='12345')
        original_function = AirtableAdapter.update_practices
        AirtableAdapter.update_practices = MagicMock()
        try:
            response = self.client.post(reverse('refresh_data'), {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            AirtableAdapter.update_practices.assert_called_once()
        finally:
            AirtableAdapter.update_practices = original_function


    def test_refresh_airtable_api_key_auth(self):
        """
        Tests the refresh data endpoint using the Api key, meant to identify
        projects and apps, not users. We mock Airtable's API to carry
        this test out.
        """
        self.client.logout()
        original_function = AirtableAdapter.update_practices
        AirtableAdapter.update_practices = MagicMock()
        try:
            response = self.client.post(
                reverse('refresh_data'),
                format='json',
                **{'HTTP_AUTHORIZATION': 'Api-Key ' + self.key},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            AirtableAdapter.update_practices.assert_called_once()
        finally:
            AirtableAdapter.update_practices = original_function


    def test_form_schema_unauthenticated(self):
        """
        Tests the form schema API endpoint without authentication,
        which should not work.
        """
        self.client.logout()
        response = self.client.get(reverse('form_schema'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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
