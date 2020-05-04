import json
import os
from unittest.mock import MagicMock
import datetime
import dateutil
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_api_key.models import APIKey
from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from data.adapters import PracticesAirtableAdapter, ExperimentsAirtableAdapter
from data.models import Practice, DiscardAction
from data.models import Category, Resource, Farmer, Experiment
from api.utils import AsanaUtils

# In these tests we will mock some protected functions so we'll need to access them
# pylint: disable = protected-access

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

@override_settings(AIRTABLE_REQUEST_INTERVAL_SECONDS=0.0)
class TestApi(TestCase):

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


    def test_refresh_airtable_xp_unauthenticated(self):
        """
        Tests the refresh XP data without authentication,
        which should not work. We mock Airtable's API
        to carry this test out.
        """
        self.client.logout()
        original_function = ExperimentsAirtableAdapter.update
        ExperimentsAirtableAdapter.update = MagicMock()
        try:
            response = self.client.post(reverse('refresh_xp_data'), {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            ExperimentsAirtableAdapter.update.assert_not_called()
        finally:
            ExperimentsAirtableAdapter.update = original_function


    def test_refresh_airtable_xp_session_auth(self):
        """
        Tests the refresh XP data authenticated as non-admin,
        which should not work. We mock Airtable's API
        to carry this test out.
        """
        self.client.login(username='testuser', password='12345')
        original_function = ExperimentsAirtableAdapter.update
        ExperimentsAirtableAdapter.update = MagicMock()
        try:
            response = self.client.post(reverse('refresh_xp_data'), {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            ExperimentsAirtableAdapter.update.assert_not_called()
        finally:
            ExperimentsAirtableAdapter.update = original_function


    def test_refresh_airtable_xp_session_admin_auth(self):
        """
        Tests the refresh XP data endpoint using the session (user specific)
        authentication. We mock Airtable's API to carry this test out.
        """
        self.client.login(username='testsuperuser', password='12345')
        original_function = ExperimentsAirtableAdapter.update
        ExperimentsAirtableAdapter.update = MagicMock()
        try:
            response = self.client.post(reverse('refresh_xp_data'), {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            ExperimentsAirtableAdapter.update.assert_called_once()
        finally:
            ExperimentsAirtableAdapter.update = original_function


    def test_refresh_airtable_xp_api_key_auth(self):
        """
        Tests the refresh XP data endpoint using the Api key, meant to identify
        projects and apps, not users. We mock Airtable's API to carry
        this test out.
        """
        self.client.logout()
        original_function = ExperimentsAirtableAdapter.update
        ExperimentsAirtableAdapter.update = MagicMock()
        try:
            response = self.client.post(
                reverse('refresh_xp_data'),
                format='json',
                **{'HTTP_AUTHORIZATION': 'Api-Key ' + self.key},
            )
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            ExperimentsAirtableAdapter.update.assert_not_called()
        finally:
            ExperimentsAirtableAdapter.update = original_function


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


    def test_task_unauthenticated(self):
        """
        Tests the task API endpoint without authentication,
        which should work since it is an open endpoint.
        """

        self.client.logout()
        original_function = AsanaUtils.send_task
        AsanaUtils.send_task = MagicMock()
        try:
            response = self.client.post(
                reverse('send_task'),
                {
                    "name": "Jean-Michel",
                    "phone_number": "07 77 08 81 79",
                    "datetime": "2019-10-09T12:02:17+00:00",
                    "problem": "Contacter un conseiller",
                    "answers": {"a": 1, "b": True, "c": "Foo"},
                    "practice_id": "recKGS5iSIiD26eah",
                },
                format='json',
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            AsanaUtils.send_task.assert_called_once()
        finally:
            AsanaUtils.send_task = original_function


    def test_task_api_key_auth(self):
        """
        Tests the task API using the Api key, meant to identify
        projects and apps, not users.
        """
        self.client.logout()
        original_function = AsanaUtils.send_task
        AsanaUtils.send_task = MagicMock()
        try:
            response = self.client.post(
                reverse('send_task'),
                {
                    "name": "Jean-Michel",
                    "phone_number": "07 77 08 81 79",
                    "datetime": "2019-10-09T12:02:17+00:00",
                    "problem": "Contacter un conseiller",
                    "answers": "What help do you need?\nNothing",
                    "practice_id": "recKGS5iSIiD26eah",
                },
                format='json',
                **{'HTTP_AUTHORIZATION': 'Api-Key ' + self.key},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            date = datetime.datetime(2019, 10, 9, 12, 2, 17, tzinfo=dateutil.tz.tzlocal())
            problem = 'Contacter un conseiller'
            name = 'Jean-Michel'
            url = 'https://airtable.com/tblobpdQDxkzcllWo/recKGS5iSIiD26eah'
            tel = '07 77 08 81 79'
            responses = 'What help do you need?\nNothing'
            notes = '{0}\n\n{1} a besoin d\'aide pour implémenter la pratique {2}.\n\nNum tel : {3}\n\nRéponses :\n{4}'.format(problem, name, url, tel, responses)
            AsanaUtils.send_task.assert_called_once_with('1143885392507417', 'Jean-Michel', notes, date)

        finally:
            AsanaUtils.send_task = original_function


    def test_task_incomplete_info(self):
        """
        Tests the task API endpoint without the complete information.
        """

        self.client.logout()
        original_function = AsanaUtils.send_task
        AsanaUtils.send_task = MagicMock()

        try:
            # Without the name we should get a 400 error
            response = self.client.post(
                reverse('send_task'),
                {
                    "phone_number": "07 77 08 81 79",
                    "datetime": "2019-10-09T12:02:17+00:00",
                    "problem": "Contacter un conseiller",
                    "answers": {"a": 1, "b": True, "c": "Foo"},
                    "practice_id": "recKGS5iSIiD26eah",
                },
                format='json',
                **{'HTTP_AUTHORIZATION': 'Api-Key ' + self.key},
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            AsanaUtils.send_task.assert_not_called()

            # Without the phone number we should get a 400 error
            response = self.client.post(
                reverse('send_task'),
                {
                    "name": "John Doe",
                    "datetime": "2019-10-09T12:02:17+00:00",
                    "problem": "Contacter un conseiller",
                    "answers": {"a": 1, "b": True, "c": "Foo"},
                    "practice_id": "recKGS5iSIiD26eah",
                },
                format='json',
                **{'HTTP_AUTHORIZATION': 'Api-Key ' + self.key},
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            AsanaUtils.send_task.assert_not_called()

            # Other fields are not mandatory
            response = self.client.post(
                reverse('send_task'),
                {
                    "name": "John Doe",
                    "phone_number": "07 77 08 81 79",
                },
                format='json',
                **{'HTTP_AUTHORIZATION': 'Api-Key ' + self.key},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            AsanaUtils.send_task.assert_called_once()

        finally:
            AsanaUtils.send_task = original_function


    def test_task_invalid_date(self):
        """
        Tests the task API endpoint with an invalid date.
        """

        self.client.logout()
        original_function = AsanaUtils.send_task
        AsanaUtils.send_task = MagicMock()

        try:
            response = self.client.post(
                reverse('send_task'),
                {
                    "name": "John Doe",
                    "phone_number": "07 77 08 81 79",
                    "datetime": "INVALID DATE",
                    "problem": "Contacter un conseiller",
                    "answers": {"a": 1, "b": True, "c": "Foo"},
                    "practice_id": "recKGS5iSIiD26eah",
                },
                format='json',
                **{'HTTP_AUTHORIZATION': 'Api-Key ' + self.key},
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            AsanaUtils.send_task.assert_not_called()
        finally:
            AsanaUtils.send_task = original_function


    def test_discard_action(self):
        """
        Tests the task API endpoint used to create discard actions.
        """

        self.client.logout()

        response = self.client.post(
            reverse('discard_action'),
            {
                "practice_airtable_id": "recHLVNm0nhc2R1mN",
                "reason": "Cette pratique a été testée ou est en place sur mon exploitation",
            },
            format='json',
            **{'HTTP_AUTHORIZATION': 'Api-Key ' + self.key},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DiscardAction.objects.all().count(), 1)

        discard_action = DiscardAction.objects.first()
        self.assertEqual(discard_action.reason, 'Cette pratique a été testée ou est en place sur mon exploitation')
        self.assertEqual(discard_action.practice_airtable_id, 'recHLVNm0nhc2R1mN')


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


    def test_farmer_list(self):
        """
        Tests the endpoint for the farmer list.
        """

        self.client.logout()
        response = self.client.get(reverse('get_farmers'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = json.loads(response.content.decode())
        self.assertEqual(len(body), 3)

        for farmer_id in ('rec66629kfas9i', 'rec0098666ooka', 'rec666sf09aii'):
            self.assertEqual(len(list(filter(lambda x: x['external_id'] == farmer_id, body))), 1)

    def test_xp_patch_unauthenticated(self):
        """
        Ensures we are not able to modify an XP if we are not logged in
        """
        self.client.logout()
        experiment = Experiment.objects.get(external_id='rec33329kfas9i')
        payload = {'objectives': 'Lorem ipsum'}
        url = reverse('experiment_update', kwargs={'pk': str(experiment.id)})
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




    def test_xp_patch_unauthorized(self):
        """
        Ensures we are not able to modify an XP if we are not logged in
        """
        self.client.logout()
        farmer_external_id = 'rec0098666ooka' # this farmer is not the creator of the XP
        experiment = Experiment.objects.get(external_id='rec33329kfas9i')
        payload = {'objectives': 'Lorem ipsum'}
        url = reverse('experiment_update', kwargs={'pk': str(experiment.id)})

        self.client.login(username=farmer_external_id, password='12345')
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_xp_put_unavailable(self):
        """
        Ensures we only propose patch to modify an XP
        """
        self.client.logout()
        farmer_external_id = 'rec66629kfas9i' # this farmer is the creator of the XP
        experiment = Experiment.objects.get(external_id='rec33329kfas9i')
        payload = {'objectives': 'Lorem ipsum'}
        url = reverse('experiment_update', kwargs={'pk': str(experiment.id)})

        self.client.login(username=farmer_external_id, password='12345')

        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_xp_patch_success(self):
        """
        Ensures the author is able to modify an XP
        """
        self.client.logout()
        farmer_external_id = 'rec66629kfas9i' # this farmer is the creator of the XP
        experiment = Experiment.objects.get(external_id='rec33329kfas9i')
        payload = {'objectives': 'Lorem ipsum'}
        url = reverse('experiment_update', kwargs={'pk': str(experiment.id)})

        self.client.login(username=farmer_external_id, password='12345')

        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Experiment.objects.get(external_id='rec33329kfas9i').objectives, 'Lorem ipsum')


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
        farmer_external_id = 'rec66629kfas9i'

        self.client.login(username=farmer_external_id, password='12345')

        try:
            original_asana_function = AsanaUtils.send_task
            AsanaUtils.send_task = MagicMock()

            response = self.client.post(url, payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            AsanaUtils.send_task.assert_called_once()

        finally:
            AsanaUtils.send_task = original_asana_function


def _populate_database():
    User.objects.create_user(username='testuser', password='12345')
    User.objects.create_superuser(username='testsuperuser', password='12345')
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

    for farmer_id in ('rec66629kfas9i', 'rec0098666ooka', 'rec666sf09aii'):
        user = User.objects.create_user(username=farmer_id, password='12345')
        farmer = Farmer(
            external_id=farmer_id,
            airtable_json={'id': farmer_id},
            lat=45.1808,
            lon=1.893,
            user=user,
            approved=True,
        )
        farmer.save()

    for experiment_id in ('rec33329kfas9i', 'rec0098333ooka', 'rec3333f09aii'):
        experiment = Experiment(
            external_id=experiment_id,
            airtable_json={'id': experiment_id},
            name="Test experiment " + experiment_id,
            farmer=Farmer.objects.filter(external_id='rec66629kfas9i').first(),
            approved=True,
        )
        experiment.save()


class MockResponse:
    """
    Utility class to mock external library responses.
    """
    def __init__(self, json_content, status_code=200):
        self.json_content = json_content
        self.status_code = status_code

    def json(self):
        return self.json_content
