import json
import os
import base64
from unittest.mock import MagicMock
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_api_key.models import APIKey
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from data.models import Farmer, Experiment
from api.utils import AsanaUtils


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

@override_settings(AIRTABLE_REQUEST_INTERVAL_SECONDS=0.0)
class TestApi(TestCase):

    def setUp(self):
        _populate_database()
        self.client = APIClient(enforce_csrf_checks=False)
        self.api_key, self.key = APIKey.objects.create_key(name='test-key')

    def test_xp_patch_unauthenticated(self):
        """
        Ensures we are not able to modify an XP if we are not logged in
        """
        self.client.logout()
        experiment = Experiment.objects.get(name='Allongement')
        payload = {'objectives': 'Lorem ipsum'}
        url = reverse('experiment_update', kwargs={'pk': str(experiment.id)})
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_xp_patch_unauthorized(self):
        """
        Ensures we are not able to modify an XP if we are not its author
        """
        self.client.logout()
        # this farmer is not the creator of the XP
        self.client.login(username='Philippe', password='12345')

        experiment = Experiment.objects.get(name='Allongement')
        payload = {'objectives': 'Lorem ipsum'}
        url = reverse('experiment_update', kwargs={'pk': str(experiment.id)})

        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_xp_put_unavailable(self):
        """
        Ensures we only propose patch to modify an XP
        """
        self.client.logout()
        # this farmer is the creator of the XP
        self.client.login(username='Pierre', password='12345')

        experiment = Experiment.objects.get(name='Allongement')
        payload = {'objectives': 'Lorem ipsum'}
        url = reverse('experiment_update', kwargs={'pk': str(experiment.id)})

        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_xp_patch_success(self):
        """
        Ensures the author is able to modify an XP
        """
        self.client.logout()
        # this farmer is the creator of the XP
        self.client.login(username='Pierre', password='12345')

        experiment = Experiment.objects.get(name='Allongement')
        payload = {'objectives': 'Lorem ipsum', 'tags': ['Autonomie', 'Adventices']}
        url = reverse('experiment_update', kwargs={'pk': str(experiment.id)})

        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Experiment.objects.get(name='Allongement').objectives, 'Lorem ipsum')
        self.assertIn('Autonomie', Experiment.objects.get(name='Allongement').tags)
        self.assertIn('Adventices', Experiment.objects.get(name='Allongement').tags)

    def test_xp_post_unauthenticated(self):
        """
        Ensures we are not able to create an XP if we are not logged in
        """
        self.client.logout()
        payload = {'objectives': 'Lorem ipsum'}
        url = reverse('experiment_create')

        try:
            original_asana_function = AsanaUtils.send_task

            AsanaUtils.send_task = MagicMock()

            response = self.client.post(url, payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            AsanaUtils.send_task.assert_not_called()
        finally:
            AsanaUtils.send_task = original_asana_function

    def test_xp_post_unauthorized(self):
        """
        Ensures a user without a farmer profile is not able to create an XP
        """
        self.client.logout()
        payload = {'objectives': 'Lorem ipsum'}
        url = reverse('experiment_create')

        self.client.login(username='testuser', password='12345')

        try:
            original_asana_function = AsanaUtils.send_task

            AsanaUtils.send_task = MagicMock()

            response = self.client.post(url, payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            AsanaUtils.send_task.assert_not_called()
        finally:
            AsanaUtils.send_task = original_asana_function

    def test_xp_post_success(self):
        """
        Ensures a farmer can create an XP
        """
        self.client.logout()
        payload = {'objectives': 'Lorem ipsum', 'name': 'Lorem ipsum'}
        url = reverse('experiment_create')

        self.client.login(username='Agnès', password='12345')

        try:
            original_asana_function = AsanaUtils.send_task
            AsanaUtils.send_task = MagicMock()

            response = self.client.post(url, payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            AsanaUtils.send_task.assert_called_once()

        finally:
            AsanaUtils.send_task = original_asana_function

    def test_post_validation_state(self):
        """
        Ensures a newly created XP set to "En attente de validation" sends an Asana notification
        """
        self.client.logout()
        payload = {'objectives': 'Lorem ipsum', 'name': 'Lorem ipsum', 'state': 'En attente de validation'}
        url = reverse('experiment_create')

        self.client.login(username='Agnès', password='12345')

        try:
            original_asana_function = AsanaUtils.send_task
            AsanaUtils.send_task = MagicMock()

            response = self.client.post(url, payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            self.assertEqual(AsanaUtils.send_task.call_count, 2)

        finally:
            AsanaUtils.send_task = original_asana_function

    def test_patch_validation_state(self):
        """
        Ensures a draft XP converted into "En attente de validation" sends an Asana notification
        """
        self.client.logout()
        self.client.login(username='Agnès', password='12345')

        try:
            original_asana_function = AsanaUtils.send_task
            AsanaUtils.send_task = MagicMock()

            experiment = Experiment.objects.get(name='Association de cultures')
            payload = {'state': 'En attente de validation'}
            url = reverse('experiment_update', kwargs={'pk': str(experiment.id)})
            self.client.patch(url, payload, format='json')

            AsanaUtils.send_task.assert_called_once()

        finally:
            AsanaUtils.send_task = original_asana_function

    def test_xp_images(self):
        """
        We can add or remove images from the experiment object
        """
        self.client.logout()
        self.client.login(username='Pierre', password='12345')

        experiment = Experiment.objects.get(name="Allongement")
        url = reverse('experiment_update', kwargs={'pk':str(experiment.id)})

        image_name = 'test-image.jpg'
        image_base_64 = None
        with open(CURRENT_DIR + '/' + image_name, 'rb') as image:
            image_base_64 = base64.b64encode(image.read()).decode('utf-8')

        # We start with zero images
        self.assertEqual(Experiment.objects.get(name="Allongement").images.count(), 0)

        # Add an image
        payload = {'images': [{'image':  "data:image/png;base64," + image_base_64, 'label': 'hello world'}]}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Experiment.objects.get(name="Allongement").images.count(), 1)
        self.assertEqual(Experiment.objects.get(name="Allongement").images.first().label, 'hello world')

        images_json = response.data['images']
        self.assertEqual(len(images_json), 1)
        self.assertEqual(images_json[0]['label'], 'hello world')

        # Add a second image
        image_name = 'test-image-2.jpg'
        image_base_64 = None
        with open(CURRENT_DIR + '/' + image_name, 'rb') as image:
            image_base_64 = base64.b64encode(image.read()).decode('utf-8')
        images_json.append({'image': "data:image/png;base64," + image_base_64, 'label': 'new image!'})

        payload = {'images': images_json}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Experiment.objects.get(name="Allongement").images.count(), 2)
        self.assertEqual(Experiment.objects.get(name="Allongement").images.order_by('label').last().label, 'new image!')

        images_json = response.data['images']
        self.assertEqual(len(images_json), 2)
        self.assertEqual(len(list(filter(lambda x: x['label'] == 'new image!', images_json))), 1)
        self.assertEqual(len(list(filter(lambda x: x['label'] == 'hello world', images_json))), 1)

        # Remove the image
        payload = {'images': []}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Experiment.objects.get(name="Allongement").images.count(), 0)

    def test_xp_videos(self):
        """
        We can add or remove videos from the experiment object
        """
        self.client.logout()
        self.client.login(username='Pierre', password='12345')

        experiment = Experiment.objects.get(name="Allongement")
        url = reverse('experiment_update', kwargs={'pk':str(experiment.id)})

        video_name = 'test-video.m4v'
        video_base_64 = None
        with open(CURRENT_DIR + '/' + video_name, 'rb') as video:
            video_base_64 = base64.b64encode(video.read()).decode('utf-8')

        # We start with zero videos
        self.assertEqual(Experiment.objects.get(name="Allongement").videos.count(), 0)

        # Add an video
        payload = {'videos': [{'video':  "data:video/mp4;base64," + video_base_64, 'label': 'hello world'}]}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Experiment.objects.get(name="Allongement").videos.count(), 1)
        self.assertEqual(Experiment.objects.get(name="Allongement").videos.first().label, 'hello world')

        # Remove the video
        payload = {'videos': []}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Experiment.objects.get(name="Allongement").videos.count(), 0)

    def test_xp_retrieve_briefs(self):
        """
        Tests the endpoint for fetching the XP briefs
        """
        self.client.logout()
        response = self.client.get(reverse('get_xp_briefs'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = json.loads(response.content.decode())

        # Only approved XPs should be here
        self.assertEqual(len(body), 3)

        for experiment in body:
            self.assertTrue(experiment['name'] != "Association de cultures")


def _populate_database():
    get_user_model().objects.create_user(username='testuser', password='12345')
    get_user_model().objects.create_superuser(username='testsuperuser', password='12345')

    for farmer_name in ('Philippe', 'Pierre', 'Agnès'):
        email = farmer_name + "@farmer.com"
        get_user_model().objects.create_user(farmer_name, email=email, password="12345")

        farmer = Farmer(
            name=farmer_name,
            lat=45.1808,
            lon=1.893,
            email=email,
            approved=True,
        )
        farmer.save()

    for experiment_name in ('Faux semis', 'Allongement', 'Lâchés de trichos'):
        experiment = Experiment(
            name=experiment_name,
            farmer=Farmer.objects.filter(name='Pierre').first(),
            state='Validé',
        )
        experiment.save()

    Experiment(
        name="Association de cultures",
        farmer=Farmer.objects.filter(name='Agnès').first(),
        state="Brouillon"
    ).save()
