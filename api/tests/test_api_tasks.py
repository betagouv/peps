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
from data.models import Practice, DiscardAction
from data.models import Resource
from api.utils import AsanaUtils

# In these tests we will mock some protected functions so we'll need to access them
# pylint: disable = protected-access

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

@override_settings(AIRTABLE_REQUEST_INTERVAL_SECONDS=0.0)
class TestApiTasks(TestCase):

    def setUp(self):
        _populate_database()
        self.client = APIClient(enforce_csrf_checks=False)
        self.api_key, self.key = APIKey.objects.create_key(name='test-key')


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
        asana_project = settings.ASANA_PROJECT
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
            AsanaUtils.send_task.assert_called_once_with(asana_project, 'Jean-Michel', notes, date)

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
