import json
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase, tag
from django.urls import reverse
from django.contrib.auth import get_user_model
from data.models import Farmer, Experiment, Theme

class TestThemes(TestCase):

    def setUp(self):
        _populate_database()
        self.client = APIClient(enforce_csrf_checks=False)

    @tag('DEBUG')
    def test_get_active_themes(self):
        """
        Tests the endpoint for themes. Should return
        only active themes
        """
        response = self.client.get(reverse('get_themes'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())

        self.assertEqual(len(body), 2)

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

    philippe = Farmer.objects.get(name="Philippe")
    pierre = Farmer.objects.get(name="Pierre")
    agnes = Farmer.objects.get(name="Agnès")
    edouard = Farmer.objects.get(name="Edouard")

    # Approved experiments
    for experiment_name in ('Faux semis', 'Allongement', 'Lâchés de tricos'):
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

    # Active themes
    desherbage_theme = Theme(
        name="Désherbage",
        active=True,
        description="Description désherbage",
    )
    desherbage_theme.save()
    desherbage_theme.experiments.set([
        Experiment.objects.get(name="Faux semis"),
        Experiment.objects.get(name="Allongement"),
    ])
    

    tricos_theme = Theme(
        name="Les tricos",
        active=True,
        description="Description tricos",
    )
    tricos_theme.save()
    tricos_theme.experiments.set([
        Experiment.objects.get(name="Lâchés de tricos"),
    ])
    

    autres_theme = Theme(
        name="Autres",
        active=False,
        description="Description autres",
    )
    autres_theme.save()
    autres_theme.experiments.set([
        Experiment.objects.get(name="Vente directe"), # not approved yet
        Experiment.objects.get(name="Culture de millet"),
    ])
    
