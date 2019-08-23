import os
from unittest.mock import Mock
import requests
from django.test import TestCase
from data.adapters import AirtableAdapter
from api.engine import Engine

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

class TestEngine(TestCase):
    def setUp(self):
        _populate_database()

    def test_suggestion_rankings(self):
        """
        We check that the weight of the proposed suggestions is correct
        """
        answers = {"problem": "MALADIES_FONGIQUES", "rotation": [], "department": "01"}
        engine = Engine(answers, [])
        practices = engine.calculate_results()
        suggestions = engine.get_suggestions(practices)

        # There should be one practice with weight 1.5 and two with 1.0
        self.assertEqual(len(suggestions), 3)
        weights = list(map(lambda x: x.weight, suggestions))
        self.assertIn(1.5, weights)
        self.assertEqual(len(list(filter(lambda x: x == 1.0, weights))), 2)


    def test_cultures(self):
        """
        If the user is already growing a culture, like Chanvre in this example,
        the engine should set practices introducing to that culture to zero.
        """
        practice_title = 'Introduire le chanvre dans la rotation'

        # If we have a problem with weeds we expect to have the chanvre practice
        # with a high ranking
        answers = {"problem":"DESHERBAGE", "department":"01"}
        engine = Engine(answers, [])
        practices = engine.calculate_results()
        chanvre_practice = next(filter(lambda x: x.practice.title == practice_title, practices))
        self.assertEqual(chanvre_practice.weight, 1.0)

        # However, if the user says they already have chanvre in their rotation,
        # the same practice will now have 0 as weight
        answers = {"problem":"DESHERBAGE", "rotation":["CHANVRE"], "department":"01"}
        engine = Engine(answers, [])
        practices = engine.calculate_results()
        chanvre_practice = next(filter(lambda x: x.practice.title == practice_title, practices))
        self.assertEqual(chanvre_practice.weight, 0.0)


def _populate_database():
    """
    The data used for these tests was taken from Airtable on
    August 23rd.
    """
    # We need to mock the 'requests.get' function to get our test
    # data instead of the real deal.
    original_get = requests.get
    get_request_mock = Mock(side_effect=_get_mock_airtable)
    requests.get = get_request_mock

    # We can now call the function that will populate the DB for us
    AirtableAdapter.update_practices()

    # We restore the mocks back to their original value
    requests.get = original_get


def _get_mock_airtable(*args, **_):
    """
    Return value should be of type requests.Response
    """
    if not args:
        return None
    request_url = args[0]
    mock_paths = {
        'Pratiques?view=Grid%20view': '/testdata/practices.json',
        'Types%20de%20sol?view=Grid%20view': '/testdata/soil_types.json',
        'Pratiques%2FSol?view=Grid%20view': '/testdata/practices_soil.json',
        'Cultures?view=Grid%20view': '/testdata/cultures.json',
        'Pratiques%2FDepartements?view=Grid%20view': '/testdata/practices_departments.json',
        'Departements?view=Grid%20view': '/testdata/departments.json',
        'Adventices?view=Grid%20view': '/testdata/weeds.json',
        'Ravageurs?view=Grid%20view': '/testdata/pests.json',
        'Familles?view=Grid%20view': '/testdata/practice_groups.json',
        'Marges%20de%20manoeuvre?view=Grid%20view': '/testdata/mechanisms.json',
        'Liens?view=Grid%20view': '/testdata/resources.json',
    }
    for url, path in mock_paths.items():
        if url in request_url:
            with open(CURRENT_DIR + path, 'r') as file:
                return MockResponse(file.read(), 200)

class MockResponse:
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code

    @property
    def text(self):
        return self.content
