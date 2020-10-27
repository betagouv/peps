import json
import os
import base64
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_api_key.models import APIKey
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from data.models import Farmer, Experiment

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

@override_settings(AIRTABLE_REQUEST_INTERVAL_SECONDS=0.0)
class TestApi(TestCase):

    def setUp(self):
        _populate_database()
        self.client = APIClient(enforce_csrf_checks=False)
        self.api_key, self.key = APIKey.objects.create_key(name='test-key')

    def test_unauthenticated_farmer_list(self):
        """
        Tests the endpoint for the farmer list unauthenticated. Only
        approved farmers should show up.
        """
        self.client.logout()
        response = self.client.get(reverse('get_farmers'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = json.loads(response.content.decode())
        self.assertEqual(len(body), 3)

        for farmer in body:
            self.assertTrue(farmer['approved'])

    def test_authenticated_unapproved_farmer_list(self):
        """
        Tests the endpoint for the farmer list logged in as an unapproved farmer. The
        farmer will show up if they are logged in - even though they are unapproved
        """
        # We log in as Edouard, an unapproved farmer
        self.client.logout()
        self.client.login(username='Edouard', password="12345")

        # We should have his serialized data in the response, along with other approved farmers
        response = self.client.get(reverse('get_farmers'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        self.assertEqual(len(body), 4)
        json_edouard = next(filter(lambda x: x['name'] == 'Edouard', body), None)
        self.assertIsNotNone(json_edouard)

    def test_authenticated_approved_farmer_list(self):
        """
        Tests the endpoint for the farmer list logged in as an approved farmer.
        Only approved farmers will show up.
        """
        # We log in as Philippe, an approved farmer
        self.client.logout()
        self.client.login(username='Philippe', password="12345")

        response = self.client.get(reverse('get_farmers'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())

        self.assertEqual(len(body), 3)

        for farmer in body:
            self.assertTrue(farmer['approved'])

    def test_unauthenticated_farmer_experiments(self):
        """
        When getting the farmer list as an unauthenticated user, only
        approved experiments will be shown.
        """
        self.client.logout()

        response = self.client.get(reverse('get_farmers'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())

        experiments = [item for sublist in map(lambda x: x.get('experiments', []), body) for item in sublist]

        for experiment in experiments:
            self.assertTrue(experiment['approved'])

    def test_authenticated_farmer_approved_experiments(self):
        """
        When getting the farmer list as a farmer who has only
        approved experiments, all experiments returned must be approved.
        """
        self.client.logout()
        self.client.login(username='Agnès', password="12345")

        response = self.client.get(reverse('get_farmers'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())

        experiments = [item for sublist in map(lambda x: x.get('experiments', []), body) for item in sublist]

        for experiment in experiments:
            self.assertTrue(experiment['approved'])

    def test_authenticated_farmer_unapproved_experiments(self):
        """
        When getting the farmer list as a farmer who has some
        unapproved experiments, he'll be able to see them alongside
        their approved ones.
        """
        self.client.logout()
        self.client.login(username='Pierre', password="12345")

        response = self.client.get(reverse('get_farmers'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        pierre = next(filter(lambda x: x['name'] == 'Pierre', body))

        self.assertEqual(len(pierre['experiments']), 4)

        unapproved_experiment = next(filter(lambda x: not x['approved'], pierre['experiments']), None)
        self.assertIsNotNone(unapproved_experiment)

    def test_farmer_patch_unauthenticated(self):
        """
        Ensures we are not able to modify a farmer if we are not logged in
        """
        self.client.logout()
        farmer = Farmer.objects.get(name="Agnès")
        payload = {'name': 'Agnieszka'}
        url = reverse('farmer_update', kwargs={'pk':str(farmer.id)})
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_farmer_patch_unauthorized(self):
        """
        Ensures we are not able to modify a farmer if we are not said farmer
        """
        self.client.logout()
        self.client.login(username='Pierre', password="12345")

        farmer = Farmer.objects.get(name="Agnès")
        payload = {'name': 'Agnieszka'}
        url = reverse('farmer_update', kwargs={'pk':str(farmer.id)})
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_farmer_patch_success(self):
        """
        Ensures a farmer is able to modify its own profile
        """
        self.client.logout()
        self.client.login(username='Agnès', password="12345")

        farmer = Farmer.objects.get(name="Agnès")
        payload = {'name': 'Agnieszka'}
        url = reverse('farmer_update', kwargs={'pk':str(farmer.id)})
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        Farmer.objects.get(name="Agnieszka")
        self.assertRaises(ObjectDoesNotExist, lambda: Farmer.objects.get(name="Agnès"))

    def test_farmer_patch_experiments(self):
        """
        The farmers endpoint is not the place to modify experiments,
        it should be done in the experiments endpoint.

        Due to https://github.com/encode/django-rest-framework/issues/1655,
        we still get a 200 OK response, but the field should not be modified.
        """
        self.client.logout()
        self.client.login(username='Pierre', password="12345")

        farmer = Farmer.objects.get(name="Pierre")
        payload = {'experiments': []}
        url = reverse('farmer_update', kwargs={'pk':str(farmer.id)})
        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Farmer.objects.get(name="Pierre").experiments.count(), 4)

    def test_farmer_post_unavailable(self):
        """
        We cannot create farmers via the API, they must pass through
        the admin or the register process
        """
        self.client.logout()
        self.client.login(username='Philippe', password='12345')

        payload = {'name': 'Test', 'lat': 0.0, 'lon': 0.0}
        farmer = Farmer.objects.get(name="Philippe")
        url = reverse('farmer_update', kwargs={'pk':str(farmer.id)})

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_farmer_put_unavailable(self):
        """
        Ensures we only propose patch to modify an XP
        """
        self.client.logout()
        self.client.login(username='Philippe', password='12345')

        payload = {'name': 'Philippe', 'lat': 0.0, 'lon': 0.0}
        farmer = Farmer.objects.get(name="Philippe")
        url = reverse('farmer_update', kwargs={'pk':str(farmer.id)})

        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_farmer_images(self):
        """
        We can add or remove images from the farmer profile
        """
        self.client.logout()
        self.client.login(username='Philippe', password='12345')

        farmer = Farmer.objects.get(name="Philippe")
        url = reverse('farmer_update', kwargs={'pk':str(farmer.id)})
        image_name = 'test-image.jpg'
        image_base_64 = None
        with open(CURRENT_DIR + '/' + image_name, 'rb') as image:
            image_base_64 = base64.b64encode(image.read()).decode('utf-8')

        # We start with zero images
        self.assertEqual(Farmer.objects.get(name="Philippe").images.count(), 0)

        # Add an image
        payload = {'images': [{'image':  "data:image/png;base64," + image_base_64, 'label': 'hello world'}]}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Farmer.objects.get(name="Philippe").images.count(), 1)
        self.assertEqual(Farmer.objects.get(name="Philippe").images.first().label, 'hello world')

        # Remove the image
        payload = {'images': []}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Farmer.objects.get(name="Philippe").images.count(), 0)


    def test_email_serialization(self):
        """
        The email should be included in the serialization
        if the farmer is logged. It should not be visible
        for other farmers
        """
        # When not logged in, no farmer should have their email serialized
        self.client.logout()
        response = self.client.get(reverse('get_farmers'))
        body = json.loads(response.content.decode())

        for json_farmer in body:
            self.assertIsNone(json_farmer['email'])

        # When I login, my email should be shown for my farmer, but not for others
        self.client.login(username='Edouard', password="12345")
        response = self.client.get(reverse('get_farmers'))
        body = json.loads(response.content.decode())

        for json_farmer in body:
            if json_farmer['name'] == 'Edouard':
                self.assertEqual(json_farmer['email'], 'Edouard@farmer.com')
            else:
                self.assertIsNone(json_farmer['email'])


    def test_phone_number_serialization(self):
        """
        The phone number should be included in the serialization
        if the farmer is logged. It should not be visible
        for other farmers
        """
        # When not logged in, no farmer should have their phone number serialized
        self.client.logout()
        response = self.client.get(reverse('get_farmers'))
        body = json.loads(response.content.decode())

        for json_farmer in body:
            self.assertIsNone(json_farmer['phone_number'])

        # When I login, my phone number should be shown for my farmer, but not for others
        self.client.login(username='Edouard', password="12345")
        response = self.client.get(reverse('get_farmers'))
        body = json.loads(response.content.decode())

        for json_farmer in body:
            if json_farmer['name'] == 'Edouard':
                self.assertEqual(json_farmer['phone_number'], '012345678')
            else:
                self.assertIsNone(json_farmer['phone_number'])


    def test_onboarding_shown_serialization(self):
        """
        The onboarding shown should be included in the serialization
        if the farmer is logged. It should not be visible
        for other farmers
        """
        # When not logged in, no farmer should have the onboarding data serialized
        self.client.logout()
        response = self.client.get(reverse('get_farmers'))
        body = json.loads(response.content.decode())

        for json_farmer in body:
            self.assertIsNone(json_farmer['onboarding_shown'])

        # When I login, my onboarding status should be shown for my farmer, but not for others
        self.client.login(username='Edouard', password="12345")
        response = self.client.get(reverse('get_farmers'))
        body = json.loads(response.content.decode())

        for json_farmer in body:
            if json_farmer['name'] == 'Edouard':
                self.assertEqual(json_farmer['onboarding_shown'], False)
            else:
                self.assertIsNone(json_farmer['onboarding_shown'])

    def test_email_read_only(self):
        """
        The email should not be modifiable with the API
        """
        self.client.logout()
        self.client.login(username='Agnès', password="12345")

        farmer = Farmer.objects.get(name="Agnès")
        payload = {'email': 'new@email.com'}
        url = reverse('farmer_update', kwargs={'pk':str(farmer.id)})
        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Farmer.objects.get(name="Agnès").email, 'Agnès@farmer.com')

    def test_update_phone_number(self):
        """
        The logged farmer can change his/her phone number
        """
        self.client.logout()
        self.client.login(username='Agnès', password="12345")

        farmer = Farmer.objects.get(name="Agnès")
        payload = {'phone_number': '987654321'}
        url = reverse('farmer_update', kwargs={'pk':str(farmer.id)})
        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Farmer.objects.get(name="Agnès").phone_number, '987654321')

    def test_update_onboarding_data(self):
        """
        The logged farmer can change his/her onboarding_shown property
        """
        self.client.logout()
        self.client.login(username='Agnès', password="12345")

        farmer = Farmer.objects.get(name="Agnès")
        payload = {'onboarding_shown': True}
        url = reverse('farmer_update', kwargs={'pk':str(farmer.id)})
        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Farmer.objects.get(name="Agnès").onboarding_shown, True)

    def test_set_null_onboarding_data(self):
        """
        The logged farmer can't set None to the onboarding_shown property
        """
        self.client.logout()
        self.client.login(username='Agnès', password="12345")

        farmer = Farmer.objects.get(name="Agnès")
        payload = {'onboarding_shown': None}
        url = reverse('farmer_update', kwargs={'pk':str(farmer.id)})
        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_individual_by_sequence_number(self):
        """
        Tests the endpoint for fetching the individual farmer
        by sequence number
        """
        self.client.logout()
        philippe = Farmer.objects.get(name="Philippe")
        response = self.client.get(reverse('get_farmer', kwargs={'sequence_number': philippe.sequence_number}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = json.loads(response.content.decode())
        self.assertEqual(body.get('name'), 'Philippe')

    def test_retrieve_briefs(self):
        """
        Tests the endpoint for fetching the short farmer representation
        """
        self.client.logout()
        response = self.client.get(reverse('get_farmer_briefs'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = json.loads(response.content.decode())
        self.assertEqual(len(body), 3)

def _populate_database():
    get_user_model().objects.create_superuser(username='testsuperuser', password='12345')

    # Approved farmers
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

    # Unapproved farmers
    get_user_model().objects.create_user("Edouard", email="Edouard@farmer.com", password="12345")
    Farmer(
        name="Edouard",
        email="Edouard@farmer.com",
        lat=0.0,
        lon=0.0,
        approved=False,
        phone_number='012345678'
    ).save()

    # Approved experiments
    for experiment_name in ('Faux semis', 'Allongement', 'Lâchés de trichos'):
        experiment = Experiment(
            name=experiment_name,
            farmer=Farmer.objects.filter(name='Pierre').first(),
            state='Validé',
        )
        experiment.save()

    Experiment(
        name="Culture de millet",
        farmer=Farmer.objects.filter(name='Edouard').first(),
        state='Validé',
    ).save()

    # Unapproved experiments
    Experiment(
        name="Vente directe",
        farmer=Farmer.objects.filter(name='Pierre').first(),
        state='Brouillon',
    ).save()

    Experiment(
        name="Couvert de sarrasin",
        farmer=Farmer.objects.filter(name='Edouard').first(),
        state='Brouillon',
    ).save()
