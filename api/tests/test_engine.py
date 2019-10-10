import os
from unittest.mock import Mock
import requests
from django.test import TestCase, override_settings
from api.engine import Engine
from data.models import Problem, Weed, Pest, Culture
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

        # There should be three practices with weight 1.5
        self.assertEqual(len(suggestions), 3)
        weights = list(map(lambda x: x.weight, suggestions))
        self.assertEqual(len(list(filter(lambda x: x == 1.5, weights))), 3)


    def test_cultures_weight(self):
        """
        If the user is already growing a culture, like Chanvre in this example,
        the engine should set practices introducing to that culture to zero.
        """
        practice_title = 'Introduire le chanvre dans la rotation'
        chanvre = Culture.objects.filter(display_text='Chanvre').first()

        # If we have a problem with weeds we expect to have the chanvre practice
        # with a high ranking
        answers = {"problem":"DESHERBAGE", "department":"01"}
        engine = Engine(answers, [], [])
        practices = engine.calculate_results()
        chanvre_practice = next(filter(lambda x: x.practice.title == practice_title, practices))

        self.assertEqual(chanvre_practice.weight, 1.5)

        # However, if the user says they already have chanvre in their rotation,
        # the same practice will now have 0 as weight
        answers = {"problem":"DESHERBAGE", "rotation":[chanvre.external_id], "department":"01"}
        engine = Engine(answers, [], [])
        practices = engine.calculate_results()
        chanvre_practice = next(filter(lambda x: x.practice.title == practice_title, practices))
        self.assertEqual(chanvre_practice.weight, 0.0)


    def test_pests_problem_type(self):
        """
        If the user says their problem are weeds (adventices), the three suggestions
        must address weeds.
        """
        ble = Culture.objects.filter(display_text='Blé dur').first()
        mais = Culture.objects.filter(display_text='Maïs').first()
        chanvre = Culture.objects.filter(display_text='Chanvre').first()

        answers = {"problem":"DESHERBAGE", "rotation": [ble.external_id, chanvre.external_id, mais.external_id]}
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
        ble = Culture.objects.filter(display_text='Blé dur').first()
        mais = Culture.objects.filter(display_text='Maïs').first()
        chanvre = Culture.objects.filter(display_text='Chanvre').first()

        # We make a call to get suggestions
        answers = {"problem":"DESHERBAGE", "rotation": [ble.external_id, chanvre.external_id, mais.external_id]}
        engine = Engine(answers, [], [])
        practices = engine.calculate_results()
        response_items = engine.get_suggestions(practices)

        # We get the first suggestion - we will blacklist it later and ensure
        # it is no longer proposed.
        blacklisted_suggestion_id = str(response_items[0].practice.id)
        engine = Engine(answers, [blacklisted_suggestion_id], [])
        practices = engine.calculate_results()
        response_items = engine.get_suggestions(practices)

        # Now let's verify that the suggestions no longer include the
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
        ble = Culture.objects.filter(display_text='Blé dur').first()
        mais = Culture.objects.filter(display_text='Maïs').first()
        chanvre = Culture.objects.filter(display_text='Chanvre').first()

        # We make a call to get suggestions
        answers = {"problem":"DESHERBAGE", "rotation": [ble.external_id, chanvre.external_id, mais.external_id]}
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

    def test_weed_whitelist(self):
        """
        A practice can have a limited number of whitelisted weeds it can be applied
        to. As an example, practice "Faucher une culture fourragère " can only be relevant
        for Rumex.
        """
        practice_title = "Faucher une culture fourragère"
        rumex = Weed.objects.filter(display_text='Rumex').first()
        chardon = Weed.objects.filter(display_text='Chardon des champs').first()
        ble = Culture.objects.filter(display_text='Blé dur').first()

        # First we check the weignt without using RUMEX. We expect the weight to be
        # zero since the whitelist is not upheld
        answers = {"problem":"DESHERBAGE", "rotation": [ble.external_id], "cattle": "Oui"}
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        self.assertEqual(result.weight, 0)

        # Now we add RUMEX. The same practice should have a non-zero weight
        answers = {
            "problem":"DESHERBAGE",
            "weeds": "{0},{1}".format(str(chardon.external_id), str(rumex.external_id)),
            "rotation": [ble.external_id],
            "cattle": "Oui"
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        self.assertTrue(result.weight > 0)


    def test_weed_fields(self):
        """
        Three form fields can contain weed information: weeds, perennials
        and weedsGlyphosate. All must be treated the same way by the engine.
        """
        practice_title = "Faucher une culture fourragère"
        rumex = Weed.objects.filter(display_text='Rumex').first()
        chardon = Weed.objects.filter(display_text='Chardon des champs').first()
        ble = Culture.objects.filter(display_text='Blé dur').first()

        answers = {
            "problem":"DESHERBAGE",
            "weeds": "{0},{1}".format(str(chardon.external_id), str(rumex.external_id)),
            "rotation": [ble.external_id],
            "cattle": "Oui"
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result_weeds = next(filter(lambda x: x.practice.title == practice_title, results))

        answers = {
            "problem":"DESHERBAGE",
            "perennials": "{0},{1}".format(str(chardon.external_id), str(rumex.external_id)),
            "rotation": [ble.external_id],
            "cattle": "Oui"
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result_perennials = next(filter(lambda x: x.practice.title == practice_title, results))

        self.assertEqual(result_weeds.weight, result_perennials.weight)

        answers = {
            "problem":"DESHERBAGE",
            "weedsGlyphosate": "{0},{1}".format(str(chardon.external_id), str(rumex.external_id)),
            "rotation": [ble.external_id],
            "cattle": "Oui"
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result_weeds_glypho = next(filter(lambda x: x.practice.title == practice_title, results))

        self.assertEqual(result_weeds.weight, result_weeds_glypho.weight)


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
        chardon = Weed.objects.filter(display_text='Chardon des champs').first()
        ble = Culture.objects.filter(display_text='Blé dur').first()

        # First we check the weignt without using CHARDON in the response
        answers = {"problem":"DESHERBAGE", "rotation": [ble.external_id]}
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        initial_weight = result.weight

        # Now we add CHARDON in the response and get the results
        answers = {
            "problem":"DESHERBAGE",
            "weeds": "{0}".format(str(chardon.external_id)),
            "rotation": [ble.external_id],
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        new_weight = result.weight

        # We need to make sure the new weight has taken into account the
        # multiplier for CHARDON
        self.assertEqual(new_weight, initial_weight * chardon_multiplier)

    def test_pest_whitelist(self):
        """
        A practice can have a limited number of whitelisted pests it can be applied
        to. As an example, practice "Lutter contre la pyrale du maïs au moyen de
        lâchers de trichogrammes" can only be relevant for pyrale.
        """
        practice_title = "Lutter contre la pyrale du maïs au moyen de lâchers de trichogrammes"
        pyrales = Pest.objects.filter(display_text='Pyrales').first()
        mais = Culture.objects.filter(display_text='Maïs').first()

        # First we check the weignt without using PYRALES. We expect the weight to be
        # zero since the whitelist is not upheld
        answers = {
            "problem":"RAVAGEURS",
            "rotation": [mais.external_id],
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        self.assertEqual(result.weight, 0)

        # Now we add PYRALES. The same practice should have a non-zero weight
        answers = {
            "problem":"RAVAGEURS",
            "pests": "{0}".format(pyrales.external_id),
            "rotation": [mais.external_id],
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        self.assertTrue(result.weight > 0)

    def test_pest_multipliers(self):
        """
        A practice can be more (or less) useful to address certain pests, this
        is specified in the pest_multipliers field of the practice model.
        The practice "Associer un colza avec un couvert de légumineuses"
        has a multiplier for the pest Charançon, here we check that said multiplier
        is taken into account by the engine.
        """
        practice_title = "Associer un colza avec un couvert de légumineuses"
        charancon = Pest.objects.filter(display_text='Charançons').first()
        colza = Culture.objects.filter(display_text='Colza').first()
        charancon_multiplier = 1.3

        # First we check the weignt without using CHARANCONS in the response
        answers = {
            "problem":"RAVAGEURS",
            "rotation": [colza.external_id],
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        initial_weight = result.weight

        # Now we add CHARANCONS in the response and get the results
        answers = {
            "problem":"RAVAGEURS",
            "pests": "{0}".format(str(charancon.external_id)),
            "rotation": [colza.external_id],
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        new_weight = result.weight

        # We need to make sure the new weight has taken into account the
        # multiplier for CHARANCONS
        self.assertEqual(new_weight, initial_weight * charancon_multiplier)


    def test_culture_whitelist(self):
        """
        A practice can have a limited number of whitelisted cultures it can be applied
        to. As an example, practice "Détruire les résidus de cannes de maïs" can only be
        relevant for MAIS.
        """
        practice_title = "Détruire les résidus de cannes de maïs"
        pyrales = Pest.objects.filter(display_text='Pyrales').first()
        ble = Culture.objects.filter(display_text='Blé dur').first()
        mais = Culture.objects.filter(display_text='Maïs').first()

        # First we check the weight without using MAIS. We expect the weight to be
        # zero since the whitelist is not upheld
        answers = {
            "problem":"RAVAGEURS",
            "pests": "{0}".format(str(pyrales.external_id)),
            "tillage": "TRAVAIL_DU_SOL",
            "rotation": [ble.external_id]
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        self.assertEqual(result.weight, 0)

        # Now we add PYRALES. The same practice should have a non-zero weight
        answers = {
            "problem":"RAVAGEURS",
            "pests": "{0}".format(str(pyrales.external_id)),
            "tillage": "TRAVAIL_DU_SOL",
            "rotation": [ble.external_id, mais.external_id]
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        self.assertTrue(result.weight > 0)


    def test_culture_multipliers(self):
        """
        A practice can be more (or less) useful to address certain cultures, this
        is specified in the culture_multipliers field of the practice model.
        The practice "Exploiter l'inter-rang pour réduire la place disponible aux
        adventices" has a multiplier for the culture COLZA, here we check that said
        multiplier is taken into account by the engine.
        """
        practice_title = "Exploiter l'inter-rang pour réduire la place disponible aux adventices"
        colza = Culture.objects.filter(display_text='Colza').first()
        colza_multiplier = 1.2

        # First we check the weignt without using COLZA in the response
        answers = {"problem":"DESHERBAGE", "rotation": []}
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        initial_weight = result.weight

        # Now we add COLZA in the response and get the results
        answers = {"problem":"DESHERBAGE", "rotation": [colza.external_id]}
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        new_weight = result.weight

        # We need to make sure the new weight has taken into account the
        # multiplier for COLZA
        self.assertEqual(new_weight, initial_weight * colza_multiplier)


    def test_problem_glyphosate(self):
        """
        If a user chooses glyphosate as their problem, the practices
        that target glyphosate should have a higher score. An exemple of
        these practices is:
        "Défanner les pomme des terre avec un produit de biocontrôle"
        """
        practice_title = 'Défanner les pomme des terre avec un produit de biocontrôle'
        pomme_de_terre = Culture.objects.filter(display_text='Pomme de terre').first()

        # First we make a request without specifying glyphosate as the main problem
        answers = {"problem":"DESHERBAGE", "rotation": [pomme_de_terre.external_id]}
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        initial_weight = result.weight

        # First we make a request without specifying glyphosate as the main problem
        answers = {"problem":"GLYPHOSATE", "rotation": [pomme_de_terre.external_id]}
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        self.assertGreater(result.weight, 0)
        self.assertGreater(result.weight, initial_weight)


    def test_glyphosate_multiplier(self):
        """
        Certain practices have a specific multiplier depending on the use
        of glyphosate that the user has. For example, the practice "Déchaumages
        répétés" has a multiplier.
        """
        glyphosate_bonus = 1.4
        practice_title = 'Déchaumages répétés'
        rumex = Weed.objects.filter(display_text='Rumex').first()
        lin_hiver = Culture.objects.filter(display_text='Lin hiver').first()

        # First we make a request without specifying the use of glyphosate
        answers = {
            "problem":"GLYPHOSATE",
            "weeds": "{0}".format(str(rumex.external_id)),
            "tillage": "TRAVAIL_PROFOND",
            "rotation": [lin_hiver.external_id],
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        initial_weight = result.weight

        # First we make a request without specifying glyphosate as the main problem
        answers = {
            "problem":"GLYPHOSATE",
            "glyphosate": "VIVACES",
            "weeds": "{0}".format(str(rumex.external_id)),
            "tillage": "TRAVAIL_PROFOND",
            "rotation": [lin_hiver.external_id],
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        self.assertGreater(result.weight, 0)
        self.assertEqual(result.weight, initial_weight * glyphosate_bonus)


    def test_mutliple_groups(self):
        """
        https://github.com/betagouv/peps/issues/16
        We need to ensure no practices belonging to the same practice group
        are selected.
        """
        rumex = Weed.objects.filter(display_text='Rumex').first()
        chardon = Weed.objects.filter(display_text='Chardon des champs').first()

        answers = {
            "problem":"GLYPHOSATE",
            "glyphosate": "VIVACES,COUVERTS",
            "weeds": "{0},{1}".format(str(chardon.external_id), str(rumex.external_id)),
            "tillage": "TRAVAIL_PROFOND",
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        suggestions = engine.get_suggestions(results)
        suggested_groups = []
        for practice in map(lambda x: x.practice, suggestions):
            practice_groups = list(practice.practice_groups.all())
            for group in practice_groups:
                self.assertNotIn(group, suggested_groups)
                suggested_groups.append(group)


    def test_livestock_need(self):
        """
        Certain practices can only be suggested when the user has livestock.
        If they don't, they should be set to zero.
        One example of this is "Faire pâturer les couverts et les repousses"
        """
        practice_title = 'Faire pâturer les couverts et les repousses'
        rumex = Weed.objects.filter(display_text='Rumex').first()
        chardon = Weed.objects.filter(display_text='Chardon des champs').first()

        # First we try with livestock, the score should be greater than zero
        answers = {
            "problem":"GLYPHOSATE",
            "weeds": "{0},{1}".format(str(rumex.external_id), str(chardon.external_id)),
            "cattle": "Oui",
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        self.assertGreater(result.weight, 0)

        # Now we try without cattle, the score should be zero
        answers = {
            "problem":"GLYPHOSATE",
            "weeds": "{0},{1}".format(str(chardon.external_id), str(rumex.external_id)),
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        result = next(filter(lambda x: x.practice.title == practice_title, results))
        self.assertEqual(result.weight, 0)


    def test_tillage_types(self):
        """
        Tillage (travail de sol) can be deep or shallow. The practices that need
        deep tillage should only be proposed if the user can do deep tillage. Same
        goes for shallow tillage.
        """
        deep_tillage_practice_title = 'Positionner un labour stratégiquement'
        shallow_tillage_practice_title = 'Désherbage mécanique en plein en début de saison pour cultures de printemps'

        rumex = Weed.objects.filter(display_text='Rumex').first()
        ble = Culture.objects.filter(display_text='Blé dur').first()
        lin_hiver = Culture.objects.filter(display_text='Lin hiver').first()
        ble_printemps = Culture.objects.filter(display_text='Blé tendre de printemps').first()

        # If the user can't do any tillage, both practices should be at zero score
        answers = {
            "problem":"GLYPHOSATE",
            "weeds": "{0}".format(str(rumex.external_id)),
            "tillage": None,
            "rotation": [ble.external_id, lin_hiver.external_id, ble_printemps.external_id],
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        deep_tillage_result = next(filter(lambda x: x.practice.title == deep_tillage_practice_title, results))
        shallow_tillage_result = next(filter(lambda x: x.practice.title == shallow_tillage_practice_title, results))

        self.assertEqual(deep_tillage_result.weight, 0)
        self.assertEqual(shallow_tillage_result.weight, 0)

        # If the user can do shallow tillage, the shallow tillage practice
        # should be above zero, whereas the deep tillage practice should be at zero
        answers = {
            "problem":"GLYPHOSATE",
            "weeds": "{0}".format(str(rumex.external_id)),
            "tillage": 'TRAVAIL_DU_SOL',
            "rotation": [ble.external_id, lin_hiver.external_id, ble_printemps.external_id],
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        deep_tillage_result = next(filter(lambda x: x.practice.title == deep_tillage_practice_title, results))
        shallow_tillage_result = next(filter(lambda x: x.practice.title == shallow_tillage_practice_title, results))

        self.assertEqual(deep_tillage_result.weight, 0)
        self.assertGreater(shallow_tillage_result.weight, 0)

        # If the user can do deep tillage, both practices should be above zero
        answers = {
            "problem":"GLYPHOSATE",
            "weeds": "{0}".format(str(rumex.external_id)),
            "tillage": 'TRAVAIL_PROFOND',
            "rotation": [ble.external_id, lin_hiver.external_id, ble_printemps.external_id],
        }
        engine = Engine(answers, [], [])
        results = engine.calculate_results()
        deep_tillage_result = next(filter(lambda x: x.practice.title == deep_tillage_practice_title, results))
        shallow_tillage_result = next(filter(lambda x: x.practice.title == shallow_tillage_practice_title, results))

        self.assertGreater(deep_tillage_result.weight, 0)
        self.assertGreater(shallow_tillage_result.weight, 0)


    def test_unbalanced_rotation(self):
        """
        If the user has <=25% of cultures of either spring or fall, they will need
        to balance their rotation. We must propose practices that help balance this
        out.
        """
        # Spring cultures:
        mais = 'recsPtaEneeYVoEWx'
        tournesol = 'rec5MHmc9xIgAg8ha'
        soja = 'recwHs4aAiZc9okg9'

        # Fall cultures:
        ble = 'recuVebqXEqCg8kK0'
        orge = 'recfGVtMZSz05Rfl8'

        # Summer cultures
        colza = 'recZj4cTO0dwcYhbe'

        # This practice balances the sowing period and should be proposed when having an unbalanced rotation
        practice_name = 'Favoriser l\'alternance de cultures à semis de printemps et d\'automne'

        # In this example, we have only 25% of fall cultures: an unbalanced rotation
        answers = {
            "problem": "DESHERBAGE",
            "tillage": "TRAVAIL_PROFOND",
            "rotation": [mais, tournesol, soja, ble],
        }
        engine = Engine(answers, [], [])
        unbalanced_result = next(filter(lambda x: x.practice.title == practice_name, engine.calculate_results()))

        # Now we balance it out, having half fall, half spring rotation
        answers = {
            "problem": "DESHERBAGE",
            "tillage": "TRAVAIL_PROFOND",
            "rotation": [ mais, tournesol, orge, ble],
        }
        engine = Engine(answers, [], [])
        balanced_result = next(filter(lambda x: x.practice.title == practice_name, engine.calculate_results()))

        # The practice weight when the rotation was unbalanced must be higher
        self.assertGreater(unbalanced_result.weight, balanced_result.weight)

        # Note that the threshold is 25%, so having an unbalanced rotation of 2-1 (33%)
        # should count as a balanced rotation
        answers = {
            "problem": "DESHERBAGE",
            "tillage": "TRAVAIL_PROFOND",
            "rotation": [ mais, tournesol, ble],
        }
        engine = Engine(answers, [], [])
        result = next(filter(lambda x: x.practice.title == practice_name, engine.calculate_results()))
        self.assertEqual(balanced_result.weight, result.weight)

        # We should only look at spring and fall cultures when we apply this logic.
        # In this case we have 40% fall, 40% spring, and 20% end-of-summer. Despite
        # having a sowing period of less than 25%, since it is not fall nor spring we
        # still consider this a balanced culture.
        answers = {
            "problem": "DESHERBAGE",
            "tillage": "TRAVAIL_PROFOND",
            "rotation": [ mais, tournesol, ble, orge, colza],
        }
        engine = Engine(answers, [], [])
        result = next(filter(lambda x: x.practice.title == practice_name, engine.calculate_results()))
        self.assertEqual(balanced_result.weight, result.weight)

        # In this case we have 25% summer, 25% spring and 50% fall. This should
        # be considered an unbalanced rotation because spring is <= 25%
        answers = {
            "problem": "DESHERBAGE",
            "tillage": "TRAVAIL_PROFOND",
            "rotation": [ tournesol, ble, orge, colza],
        }
        engine = Engine(answers, [], [])
        result = next(filter(lambda x: x.practice.title == practice_name, engine.calculate_results()))
        self.assertEqual(unbalanced_result.weight, result.weight)


    def test_large_rotation(self):
        """
        If there are more than six cultures in the rotation of a user, practices with
        added cultures should be handicaped.
        """
        practice_name = 'Faucher une culture fourragère'

        mais = 'recsPtaEneeYVoEWx'
        tournesol = 'rec5MHmc9xIgAg8ha'
        soja = 'recwHs4aAiZc9okg9'
        ble = 'recuVebqXEqCg8kK0'
        orge = 'recfGVtMZSz05Rfl8'
        ble_hiver = 'recmm8lo1bGXCYSA3'
        colza = 'recZj4cTO0dwcYhbe'
        rumex = 'rec2wnpJOAJzUFe5v'

        # When having 6 or less cultures, there is no handicap
        answers = {
            'problem': 'DESHERBAGE',
            'rotation': [mais, tournesol, ble, orge],
            'weeds': rumex,
            "cattle": "Oui",
        }
        engine = Engine(answers, [], [])
        result = next(filter(lambda x: x.practice.title == practice_name, engine.calculate_results()))
        initial_weight = result.weight

        # When having 6 or more, a handicap of 0.9 will be applied to cultures that
        # add a new culture to the rotation
        answers = {
            'problem': 'DESHERBAGE',
            'rotation': [mais, tournesol, ble, orge, soja, ble_hiver, colza],
            'weeds': rumex,
            "cattle": "Oui",
        }
        engine = Engine(answers, [], [])
        result = next(filter(lambda x: x.practice.title == practice_name, engine.calculate_results()))
        large_rotation_weight = result.weight

        self.assertEqual(initial_weight * 0.9, large_rotation_weight)



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
        'Pratiques%2FGlyphosate?view=Grid%20view': '/testdata/practices_glyphosate.json',
        'Glyphosate?view=Grid%20view': '/testdata/glyphosate.json',
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
