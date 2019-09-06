import os
from unittest.mock import Mock
import requests
from django.test import TestCase, override_settings
from api.engine import Engine
from data.models import Problem
from data.adapters import AirtableAdapter

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

@override_settings(AIRTABLE_REQUEST_INTERVAL_SECONDS=0.0)
class TestEngine(TestCase):
    def setUp(self):
        _populate_database()

    def test_suggestion_rankings(self):
        """
        We check that the weight of the proposed suggestions is correct
        """
        answers = {"problem": "MALADIES_FONGIQUES", "rotation": [], "department": "01"}
        engine = Engine(answers, [], [])
        practices = engine.calculate_results()
        suggestions = engine.get_suggestions(practices)

        # There should be one practice with weight 1.5 and two with 1.0
        self.assertEqual(len(suggestions), 3)
        weights = list(map(lambda x: x.weight, suggestions))
        self.assertEqual(len(list(filter(lambda x: x == 1.0, weights))), 1)
        self.assertEqual(len(list(filter(lambda x: x == 1.5, weights))), 2)


    def test_cultures_weight(self):
        """
        If the user is already growing a culture, like Chanvre in this example,
        the engine should set practices introducing to that culture to zero.
        """
        practice_title = 'Introduire le chanvre dans la rotation'

        # If we have a problem with weeds we expect to have the chanvre practice
        # with a high ranking
        answers = {"problem":"DESHERBAGE", "department":"01"}
        engine = Engine(answers, [], [])
        practices = engine.calculate_results()
        chanvre_practice = next(filter(lambda x: x.practice.title == practice_title, practices))
        self.assertEqual(chanvre_practice.weight, 1.5)

        # However, if the user says they already have chanvre in their rotation,
        # the same practice will now have 0 as weight
        answers = {"problem":"DESHERBAGE", "rotation":["CHANVRE"], "department":"01"}
        engine = Engine(answers, [], [])
        practices = engine.calculate_results()
        chanvre_practice = next(filter(lambda x: x.practice.title == practice_title, practices))
        self.assertEqual(chanvre_practice.weight, 0.0)


    def test_pests_problem_type(self):
        """
        If the user says their problem are weeds (adventices), the three suggestions
        must address weeds.
        """
        answers = {"problem":"DESHERBAGE", "rotation": ["BLE", "CHANVRE", "MAIS"]}
        engine = Engine(answers, [], [])
        practices = engine.calculate_results()
        response_items = engine.get_suggestions(practices)

        # We ensure there are three suggestions, and all three address weeds
        self.assertEqual(len(response_items), 3)
        for response_item in response_items:
            suggestion = response_item.practice
            self.assertIn(Problem['DESHERBAGE'].value, suggestion.problems_addressed)


    def test_blacklist_practices(self):
        """
        It is possible to blacklist individual practices, this test
        ensures that blacklisted practices end up with a score of zero.
        """
        # We make a call to get suggestions
        answers = {"problem":"DESHERBAGE", "rotation": ["BLE", "CHANVRE", "MAIS"]}
        engine = Engine(answers, [], [])
        practices = engine.calculate_results()
        response_items = engine.get_suggestions(practices)

        # We get the first suggestion - we will blacklist it later and ensure
        # it is no longer proposed.
        blacklisted_suggestion_id = str(response_items[0].practice.id)
        engine = Engine(answers, [blacklisted_suggestion_id], [])
        practices = engine.calculate_results()
        response_items = engine.get_suggestions(practices)

        # Now let' verify that the suggestions no longer include the
        # blacklisted practice
        suggested_ids = list(map(lambda x: str(x.practice.id), response_items))
        self.assertNotIn(blacklisted_suggestion_id, suggested_ids)

        # The blacklisted practice should have a score of zero
        blacklisted_response_item = next(filter(lambda x: str(x.practice.id) == blacklisted_suggestion_id, practices))
        self.assertEqual(blacklisted_response_item.weight, 0.0)


    def test_blacklist_types(self):
        """
        It is possible to blacklist entire practice types. This test
        ensures that practices belonging to blacklisted practice types
        have a score of zero.
        """
        # We make a call to get suggestions
        answers = {"problem":"DESHERBAGE", "rotation": ["BLE", "CHANVRE", "MAIS"]}
        engine = Engine(answers, [], [])
        practices = engine.calculate_results()
        response_items = engine.get_suggestions(practices)

        # We get the first suggestion's practice type. We will blacklist it
        # later and ensure no practices of the same type are proposed, and that
        # they are all set to zero.
        blacklisted_practice_type = str(list(response_items[0].practice.types.all())[0].id)
        engine = Engine(answers, [], [blacklisted_practice_type])
        practices = engine.calculate_results()
        response_items = engine.get_suggestions(practices)

        # Now let' verify that all the practices belonging to that type
        # have a score of zero.
        for practice_item in practices:
            practice_types_ids = list(map(lambda x: str(x.id), practice_item.practice.types.all()))
            if blacklisted_practice_type in practice_types_ids:
                self.assertEqual(practice_item.weight, 0.0)


    def test_weed_multipliers(self):
        """
        A practice can be more (or less) useful to address certain weeds, this
        is specified in the weed_multipliers field of the practice model.
        The practice "Profiter de l'action des auxiliaires sur le puceron de l'épi"
        has a multiplier for the weed Chardon, here we check that said multiplier
        is taken into account by the engine.
        """
        practice_title = "Profiter de l'action des auxiliaires sur le puceron de l'épi"
        chardon_multiplier = 0.6

        # First we check the weignt without using CHARDON in the response
        answers = {"problem":"DESHERBAGE", "rotation": ["BLE"]}
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        initial_weight = result.weight

        # Now we add CHARDON in the response and get the results
        answers = {"problem":"DESHERBAGE", "weeds": "CHARDON" ,"rotation": ["BLE"]}
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        new_weight = result.weight

        # We need to make sure the new weight has taken into account the
        # multiplier for CHARDON
        self.assertEqual(new_weight, initial_weight * chardon_multiplier)


def _populate_database():
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
        'Pratiques%2FCultures?view=Grid%20view': '/testdata/practices_cultures.json',
        'Cultures?view=Grid%20view': '/testdata/cultures.json',
        'Pratiques%2FDepartements?view=Grid%20view': '/testdata/practices_departments.json',
        'Departements?view=Grid%20view': '/testdata/departments.json',
        'Pratiques%2FAdventices?view=Grid%20view': '/testdata/practices_weeds.json',
        'Adventices?view=Grid%20view': '/testdata/weeds.json',
        'Pratiques%2FRavageurs?view=Grid%20view': '/testdata/practices_pests.json',
        'Ravageurs?view=Grid%20view': '/testdata/pests.json',
        'Familles?view=Grid%20view': '/testdata/practice_groups.json',
        'Marges%20de%20manoeuvre?view=Grid%20view': '/testdata/mechanisms.json',
        'Liens?view=Grid%20view': '/testdata/resources.json',
        'Types%20de%20pratique?view=Grid%20view': '/testdata/practice_types.json',
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
