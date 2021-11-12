import os
from unittest.mock import MagicMock
import datetime
import dateutil
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_api_key.models import APIKey
from django.conf import settings
from django.core.files.base import ContentFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from api.utils import AsanaUtils

# In these tests we will mock some protected functions so we'll need to access them
# pylint: disable = protected-access

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

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
                },
                format='json',
                **{'HTTP_AUTHORIZATION': 'Api-Key ' + self.key},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            date = datetime.datetime(2019, 10, 9, 12, 2, 17, tzinfo=dateutil.tz.tzlocal())
            problem = 'Contacter un conseiller'
            name = 'Jean-Michel'
            tel = '07 77 08 81 79'
            responses = 'What help do you need?\nNothing'
            notes = '{0}\n\n{1} a partagé son information de contact.\n\nNum tel : {2}\n\nRéponses :\n{3}'.format(problem, name, tel, responses)
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


def _populate_database():
    get_user_model().objects.create_user(username='testuser', password='12345')
    get_user_model().objects.create_superuser(username='testsuperuser', password='12345')
