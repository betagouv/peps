import json
import os
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_api_key.models import APIKey
from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from data.models import Practice
from data.models import Resource

# In these tests we will mock some protected functions so we'll need to access them
# pylint: disable = protected-access

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

@override_settings(AIRTABLE_REQUEST_INTERVAL_SECONDS=0.0)
class TestApiRankings(TestCase):

    def setUp(self):
        _populate_database()
        self.client = APIClient(enforce_csrf_checks=False)
        self.api_key, self.key = APIKey.objects.create_key(name='test-key')

    def test_unathenticated_user(self):
        """
        Tests the rankings API without authentication,
        which should work since it is an open endpoint.
        """
        self.client.logout()
        response = self.client.post(
            reverse('calculate_rankings'),
            {"answers": {"problem": "DESHERBAGE", "rotation": [], "department": "01"}, "practice_blacklist": []},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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

        # We verify that the image url is in the practice
        self.assertEqual(body['practices'][0]['practice']['image'], '/media/test-image.jpg')


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



def _populate_database():
    get_user_model().objects.create_user(username='testuser', password='12345')
    get_user_model().objects.create_superuser(username='testsuperuser', password='12345')
    image_name = 'test-image.jpg'
    image_bytes = None

    with open(CURRENT_DIR + '/' + image_name, 'rb') as image:
        image_bytes = image.read()

    resource = Resource(
        external_id='recpbs29kfas9i',
        url='https://test.test/resource.pdf'
    )
    resource.image.save(image_name, ContentFile(image_bytes), save=True)
    resource.save()

    for external_id in ('recZxlcM61qaDoOkc', 'recYK5ljTyL3b18J3', 'recvSDrARAcmKogbD'):
        practice = Practice(
            external_id=external_id,
            main_resource=resource,
        )
        practice.image.save(image_name, ContentFile(image_bytes), save=True)
        practice.save()
