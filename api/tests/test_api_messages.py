import json
import os
import base64
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_api_key.models import APIKey
from django.test import TestCase, tag
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from data.models import Farmer, Message

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

class TestApiMessages(TestCase):

    def setUp(self):
        _populate_database()
        self.client = APIClient(enforce_csrf_checks=False)
        self.api_key, self.key = APIKey.objects.create_key(name='test-key')

    @tag('DEBUG')
    def test_unauthenticated_messages(self):
        """
        The messages endpoint is not available to unauthenticated requests
        """
        self.client.logout()
        response = self.client.get(reverse('messages'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag('DEBUG')
    def test_messages_all(self):
        """
        For Philippe, the message should appear in his inbox
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


    @tag('DEBUG')
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


def _populate_database():
    User.objects.create_superuser(username='testsuperuser', password='12345')

    # Approved farmers
    for farmer_name in ('Philippe', 'Pierre', 'Agnès'):
        email = farmer_name + "@farmer.com"
        User.objects.create_user(farmer_name, email=email, password="12345")
        farmer = Farmer(
            name=farmer_name,
            lat=45.1808,
            lon=1.893,
            email=email,
            approved=True,
        )
        farmer.save()

    # Unapproved farmers
    User.objects.create_user("Edouard", email="Edouard@farmer.com", password="12345")
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
