import json
import os
import datetime
import pytz
from urllib.parse import quote_plus
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_api_key.models import APIKey
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from data.models import Farmer, Message

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

class TestApiMessages(TestCase):

    def setUp(self):
        _populate_database()
        self.client = APIClient(enforce_csrf_checks=False)
        self.api_key, self.key = APIKey.objects.create_key(name='test-key')

    def test_unauthenticated_messages(self):
        """
        The messages endpoint is not available to unauthenticated requests
        """
        self.client.logout()
        response = self.client.get(reverse('messages'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_messages_all(self):
        """
        For Philippe, the request should have two messages
        """
        self.client.logout()
        self.client.login(username="Philippe", password="12345")

        response = self.client.get(reverse('messages'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = json.loads(response.content.decode())
        self.assertEqual(len(body), 1)

        message = body[0]
        self.assertEqual(message['subject'], 'Hello Philippe')
        self.assertEqual(message['body'], 'How you doin?')
        self.assertEqual(message['recipient']['name'], 'Philippe')

    def test_get_messages_since(self):
        """
        We can get the messages for a user since a specific date. For Edouard,
        he should only have one message since 2020-01-01.
        """
        self.client.logout()
        self.client.login(username="Edouard", password="12345")

        date = datetime.datetime(2019, 1, 1, 1, tzinfo=pytz.timezone('Europe/Paris'))
        url = "{0}?since={1}".format(reverse('messages'), quote_plus(date.isoformat()))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = json.loads(response.content.decode())
        self.assertEqual(len(body), 1)

        message = body[0]
        self.assertEqual(message['subject'], 'Hello Philippe')
        self.assertEqual(message['body'], 'How you doin?')
        self.assertEqual(message['recipient']['name'], 'Philippe')

    def test_get_messages_since_bad_date(self):
        """
        We can get the messages for a user since a specific date, but we will
        obtain a Bar Request if we don't specify a parseable date
        """
        self.client.logout()
        self.client.login(username="Edouard", password="12345")

        url = "{0}?since={1}".format(reverse('messages'), quote_plus('This is a bad date'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_send_message(self):
        """
        Pierre sends a message to Agnès
        """
        self.client.logout()
        self.client.login(username="Pierre", password="12345")

        pierre = Farmer.objects.get(name="Pierre")
        agnes = Farmer.objects.get(name="Agnès")

        payload = {
            'subject': 'Hey Agnès',
            'body': 'Ça va?',
            'recipient': agnes.id,
        }
        response = self.client.post(reverse('messages'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        body = json.loads(response.content.decode())
        self.assertEqual(body['sender']['name'], 'Pierre')
        self.assertEqual(body['sender']['id'], str(pierre.id))
        self.assertEqual(body['recipient']['name'], 'Agnès')
        self.assertEqual(body['recipient']['id'], str(agnes.id))

        db_message = Message.objects.get(pk=body['id'])
        self.assertEqual(db_message.id, body['id'])

    def test_mark_message_as_read_unauthenticated(self):
        self.client.logout()
        message = Message.objects.first()
        response = self.client.post(reverse('mark_as_read'), [
            message.id,
        ], format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mark_message_as_read_unauthorized(self):
        """
        If we try to mark as read messages that don't exist or do not belong
        to us, the API will ignore those messages, failing silently. The return
        value will not contain the serialization of those methods
        """
        edouard = Farmer.objects.get(name="Edouard")
        philippe = Farmer.objects.get(name="Philippe")
        message = Message.objects.filter(sender=edouard, recipient=philippe).first()

        self.client.logout()
        self.client.login(username="Pierre", password="12345")

        # Since Edouard sent this message, he can't set it as read
        # So the response will not include any messages
        response = self.client.post(reverse('mark_as_read'), [
            message.id,
        ], format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        self.assertEqual(len(body), 0)

        # We ensure the message is not read
        message = Message.objects.filter(sender=edouard).first()
        self.assertTrue(message.new)

    def test_mark_message_as_read(self):
        """
        Philippe can set his own message as read
        """
        self.client.logout()
        self.client.login(username="Philippe", password="12345")

        edouard = Farmer.objects.get(name="Edouard")
        philippe = Farmer.objects.get(name="Philippe")
        message = Message.objects.get(sender=edouard, recipient=philippe)

        response = self.client.post(reverse('mark_as_read'), [
            message.id,
        ], format='json')

        # The body should include the modified message with the read date
        body = json.loads(response.content.decode())
        self.assertEqual(len(body), 1)
        self.assertFalse(body[0]['new'])

        # We ensure the message in the DB is read
        message = Message.objects.get(sender=edouard, recipient=philippe)
        self.assertFalse(message.new)

    def test_mark_message_as_read_twice(self):
        """
        If we mark as read a message that has previously already been marked as read,
        the message won't be modified.
        """
        self.client.logout()
        self.client.login(username="Agnès", password="12345")

        edouard = Farmer.objects.get(name="Edouard")
        agnes = Farmer.objects.get(name="Agnès")
        message = Message.objects.get(sender=edouard, recipient=agnes)

        # Agnès will set the message as read for the first time
        response = self.client.post(reverse('mark_as_read'), [
            message.id,
        ], format='json')

        # The body should include the modified message with the read date
        body = json.loads(response.content.decode())
        self.assertEqual(len(body), 1)

        # Now we do it as second time. This time, the modiication won't be taken
        # into account and the reply will be empty
        response = self.client.post(reverse('mark_as_read'), [
            message.id,
        ], format='json')
        body = json.loads(response.content.decode())
        self.assertEqual(len(body), 0)



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

    # Message sent from Edouard to Philippe
    edouard = Farmer.objects.get(name="Edouard")
    philippe = Farmer.objects.get(name="Philippe")
    Message(
        sender=edouard,
        recipient=philippe,
        subject="Hello Philippe",
        body="How you doin?"
    ).save()

    # Message sent from Edouard to Philippe
    edouard = Farmer.objects.get(name="Edouard")
    agnes = Farmer.objects.get(name="Agnès")
    Message(
        sender=edouard,
        recipient=agnes,
        subject="Hello Agnès",
        body="Everything OK?",
        sent_at=datetime.datetime(2019, 1, 1, tzinfo=pytz.timezone('Europe/Paris'))
    ).save()
