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
    def setUp(self):
        _populate_database()

    def test_farmers_serialized(self):
        """
        We check that farmers have been correctly serialized
        """
        self.assertEqual(Farmer.objects.count(), 8)

    def test_experiments_serialized(self):
        """
        We check that experiments have been correctly serialized
        """
        self.assertEqual(Experiment.objects.count(), 8)

    def test_experiments_have_images(self):
        """
        We check that images are in the experiment objects
        """
        xp_with_images = Experiment.objects.filter(name='Mise en place d\'un canal de vente directe de foins').first()
        self.assertTrue(xp_with_images.images.all().count() > 0)

    def test_experiments_have_videos(self):
        """
        We check that videos are in the experiment objects
        """
        xp_with_videos = Experiment.objects.filter(name='Test de la culture du Chia ').first()
        self.assertTrue(xp_with_videos.videos.all().count() > 0)

def _populate_database():
    # We need to mock the 'requests.get' function to get our test
    # data instead of the real deal.
    original_get = requests.get
    get_request_mock = Mock(side_effect=_get_mock_airtable)
    requests.get = get_request_mock

    # We can now call the function that will populate the DB for us
    ExperimentsAirtableAdapter.update()

    # We restore the mocks back to their original value
    requests.get = original_get


def _get_mock_airtable(*args, **_):
    """
    Return value should be of type requests.Response
    """
    if not args:
        return None
    request_url = args[0]

    mock_paths = {
        'Agriculteur?view=Grid%20view': '/testdata/farmers.json',
        'XP?view=Grid%20view': '/testdata/experiments.json',
    }
    for url, path in mock_paths.items():
        if url in request_url:
            with open(CURRENT_DIR + path, 'r') as file:
                return MockResponse(file.read(), 200)

    if '.jpg' in request_url or '.JPG' in request_url or '.jpeg' in request_url or '.JPEG' in request_url:
        with open(CURRENT_DIR + '/test-image.jpg', 'rb') as image:
            return MockResponse(image.read(), 200)

    if '.png' in request_url or '.PNG' in request_url:
        with open(CURRENT_DIR + '/test-image.png', 'rb') as image:
            return MockResponse(image.read(), 200)

    if '.m4v' in request_url or '.M4V' in request_url:
        with open(CURRENT_DIR + '/test-video.m4v', 'rb') as image:
            return MockResponse(image.read(), 200)

class MockResponse:
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code

    @property
    def text(self):
        return self.content
