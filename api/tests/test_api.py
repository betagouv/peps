import json
from unittest.mock import MagicMock
import datetime
import dateutil
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_api_key.models import APIKey
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from data.adapters import AirtableAdapter
from data.models import Practice
from api.views import SendEmailView, SendTaskView

# In these tests we will mock some protected functions so we'll need to access them
# pylint: disable = protected-access

@override_settings(AIRTABLE_REQUEST_INTERVAL_SECONDS=0.0)
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


    def test_email_unauthenticated(self):
        """
        Tests the email API endpoint without authentication,
        which should not work.
        """

        self.client.logout()
        original_function = SendEmailView._send_email
        SendEmailView._send_email = MagicMock(return_value={'test': True})
        try:
            response = self.client.post(
                reverse('send_email'),
                {
                    'email': 'fake@email.com',
                    'first_name': 'Jean',
                    'problem': 'désherbage',
                    'practices': ['recZxlcM61qaDoOkc', 'recYK5ljTyL3b18J3', 'recvSDrARAcmKogbD'],
                },
                format='json',
            )
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            SendEmailView._send_email.assert_not_called()
        finally:
            SendEmailView._send_email = original_function


    def test_email_api_key_auth(self):
        """
        Tests the email API using the Api key, meant to identify
        projects and apps, not users.
        """
        self.client.logout()
        original_function = SendEmailView._send_email
        SendEmailView._send_email = MagicMock(return_value=MockResponse({'test': True}))
        try:
            response = self.client.post(
                reverse('send_email'),
                {
                    'email': 'fake@email.com',
                    'first_name': 'Jean',
                    'problem': 'désherbage',
                    'practices': ['recZxlcM61qaDoOkc', 'recYK5ljTyL3b18J3', 'recvSDrARAcmKogbD'],
                },
                format='json',
                **{'HTTP_AUTHORIZATION': 'Api-Key ' + self.key},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            SendEmailView._send_email.assert_called_once()
            body = json.loads(response.content.decode())
            self.assertIn('test', body)

        finally:
            SendEmailView._send_email = original_function


    def test_email_invalid_practices(self):
        """
        Tests the email API endpoint when invalid practices are sent. Only
        three valid ones can be user at this moment.
        """
        self.client.logout()
        original_function = SendEmailView._send_email
        SendEmailView._send_email = MagicMock(return_value=MockResponse({'test': True}))
        practice_sets = [
            ['recZxlcM61qaDoOkc', 'recYK5ljTyL3b18J3'],
            [],
            ['recZxlcM61qaDoOkc', 'recZxlcM61qaDoOkc', 'invalid_id'],
            ['recZxlcM61qaDoOkc', 'recZxlcM61qaDoOkc', 'invalid_id', 'invalid_id_2'],
        ]
        try:
            for practices in practice_sets:
                response = self.client.post(
                    reverse('send_email'),
                    {
                        'email': 'fake@email.com',
                        'first_name': 'Jean',
                        'problem': 'désherbage',
                        'practices': practices,
                    },
                    format='json',
                    **{'HTTP_AUTHORIZATION': 'Api-Key ' + self.key},
                )
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                SendEmailView._send_email.assert_not_called()

        finally:
            SendEmailView._send_email = original_function


    def test_task_unauthenticated(self):
        """
        Tests the task API endpoint without authentication,
        which should not work.
        """

        self.client.logout()
        original_function = SendTaskView._send_task
        SendTaskView._send_task = MagicMock()
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
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            SendTaskView._send_task.assert_not_called()
        finally:
            SendTaskView._send_task = original_function


    def test_task_api_key_auth(self):
        """
        Tests the task API using the Api key, meant to identify
        projects and apps, not users.
        """
        self.client.logout()
        original_function = SendTaskView._send_task
        SendTaskView._send_task = MagicMock()
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
            SendTaskView._send_task.assert_called_once_with('1143885392507417', 'Jean-Michel', notes, date)

        finally:
            SendTaskView._send_task = original_function


    def test_task_incomplete_info(self):
        """
        Tests the task API endpoint without the complete information.
        """

        self.client.logout()
        original_function = SendTaskView._send_task
        SendTaskView._send_task = MagicMock()

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
            SendTaskView._send_task.assert_not_called()

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
            SendTaskView._send_task.assert_not_called()

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
            SendTaskView._send_task.assert_called_once()

        finally:
            SendTaskView._send_task = original_function


    def test_task_invalid_date(self):
        """
        Tests the task API endpoint with an invalid date.
        """

        self.client.logout()
        original_function = SendTaskView._send_task
        SendTaskView._send_task = MagicMock()

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
            SendTaskView._send_task.assert_not_called()
        finally:
            SendTaskView._send_task = original_function



def _populate_database():
    User.objects.create_user(username='testuser', password='12345')
    for external_id in ('recZxlcM61qaDoOkc', 'recYK5ljTyL3b18J3', 'recvSDrARAcmKogbD'):
        Practice(
            external_id=external_id,
            modification_date=timezone.now(),
        ).save()


class MockResponse:
    """
    Utility class to mock external library responses.
    """
    def __init__(self, json_content, status_code=200):
        self.json_content = json_content
        self.status_code = status_code

    def json(self):
        return self.json_content
