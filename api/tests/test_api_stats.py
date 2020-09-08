import json
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from data.models import Farmer, Experiment, Message

class TestStats(TestCase):

    def setUp(self):
        _populate_database()
        self.client = APIClient(enforce_csrf_checks=False)

    def test_get_stats(self):
        """
        Tests the endpoint for stats
        """
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())

        self.assertEqual(body['approvedExperimentCount'], 4)
        self.assertEqual(body['approvedFarmerCount'], 3)
        self.assertEqual(body['contactCount'], 3)

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

    philippe = Farmer.objects.get(name="Philippe")
    pierre = Farmer.objects.get(name="Pierre")
    agnes = Farmer.objects.get(name="Agnès")
    edouard = Farmer.objects.get(name="Edouard")

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

    # Message exchange between Philippe and Pierre
    Message(
        sender=philippe,
        recipient=pierre,
    ).save()
    Message(
        sender=pierre,
        recipient=philippe,
    ).save()
    Message(
        sender=philippe,
        recipient=pierre,
    ).save()

    # Message exchange between Agnès and Edouard
    Message(
        sender=edouard,
        recipient=agnes,
    ).save()
    Message(
        sender=agnes,
        recipient=edouard,
    ).save()

    # Single message from Agnès Pierre
    Message(
        sender=agnes,
        recipient=pierre,
    ).save()
