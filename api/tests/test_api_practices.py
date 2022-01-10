import json
import os
from unittest import skip
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_api_key.models import APIKey
from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from data.models import Practice, Category, Resource

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

@override_settings(AIRTABLE_REQUEST_INTERVAL_SECONDS=0.0)
@skip("Redirection en place vers rex-agri")
class TestApi(TestCase):

    def setUp(self):
        _populate_database()
        self.client = APIClient(enforce_csrf_checks=False)
        self.api_key, self.key = APIKey.objects.create_key(name='test-key')


    def test_get_categories(self):
        """
        Tests the categories API endpoint.
        """

        self.client.logout()
        response = self.client.get(reverse('get_categories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # There must be three categories
        body = json.loads(response.content.decode())
        self.assertEqual(len(body), 3)

        # The image URL for the categories must be present
        self.assertEqual(body[0]['image'], 'http://testserver/media/test-image.jpg')


    def test_resource_image(self):
        """
        Tests that the resources have the correct image URL.
        """

        self.client.logout()
        response = self.client.get(reverse('get_categories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = json.loads(response.content.decode())
        resource = body[0].get('practices')[0].get('main_resource')

        self.assertIsNotNone(resource)
        self.assertEqual(resource['image'], 'http://testserver/media/test-image.jpg')


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

    for category_id in ('rec82929kfas9i', 'rec0098afaooka', 'recppasf09aii'):
        category = Category(
            external_id=category_id,
            practice_external_ids=['recZxlcM61qaDoOkc']
        )
        category.image.save(image_name, ContentFile(image_bytes), save=True)
        category.save()
        category.practices.add(Practice.objects.filter(external_id='recZxlcM61qaDoOkc').first())

class MockResponse:
    """
    Utility class to mock external library responses.
    """
    def __init__(self, json_content, status_code=200):
        self.json_content = json_content
        self.status_code = status_code

    def json(self):
        return self.json_content
