from django.test import TestCase
from data.airtablevalidators import validate_cultures, validate_glyphosate_uses, validate_pests
from data.airtablevalidators import validate_practice_types, validate_practices, validate_weeds

class TestValidators(TestCase):
    """
    This test class will ensure the validators used for Airtable data
    work properly
    """

    def test_culture_validation(self):
        # This is an example of a complete culture, there should be no errors
        json = [{
            "id": "recuVebqXEqCg8kK0",
            "fields": {
                "Name": "Blé dur",
                "Enum code": "BLE",
            },
        }]
        errors = validate_cultures(json)
        self.assertEqual(len(errors), 0)

        # If the name is missing, we expect an error
        json = [{
            "id": "recuVebqXEqCg8kK0",
            "fields": {
                "Enum code": "BLE",
            },
        }]
        errors = validate_cultures(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Culture ID recuVebqXEqCg8kK0 n\'a pas de nom (colonne Name)')

        # If the enum is missing, we expect an error
        json = [{
            "id": "recuVebqXEqCg8kK0",
            "fields": {
                "Name": "Blé dur",
            },
        }]
        errors = validate_cultures(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Culture "Blé dur" (ID recuVebqXEqCg8kK0) manque l\'enum code (colonne Enum code)')

        # If the enum is not part of the known cultures, we expect an error
        json = [{
            "id": "recuVebqXEqCg8kK0",
            "fields": {
                "Name": "Blé dur",
                "Enum code": "UNKNOWN_CODE",
            },
        }]
        errors = validate_cultures(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Culture "Blé dur" (ID recuVebqXEqCg8kK0) a un code enum qui n\'est pas connu du backend')


    def test_glyphosate_uses_validation(self):
        # This is an example of a complete glyphosate use, there should be no errors
        json = [{
            "id": "recmbzruq8M4v7uW8",
            "fields": {
                "Name": "Nettoyage des parcelles reverdies",
                "Enum code": "PARCELLES",
            },
        }]
        errors = validate_glyphosate_uses(json)
        self.assertEqual(len(errors), 0)

        # If the name is missing, we expect an error
        json = [{
            "id": "recmbzruq8M4v7uW8",
            "fields": {
                "Enum code": "PARCELLES",
            },
        }]
        errors = validate_glyphosate_uses(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'L\'usage de glyphosate ID recmbzruq8M4v7uW8 n\'a pas de nom (colonne Name)')

        # If the enum is missing, we expect an error
        json = [{
            "id": "recmbzruq8M4v7uW8",
            "fields": {
                "Name": "Nettoyage des parcelles reverdies",
            },
        }]
        errors = validate_glyphosate_uses(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'L\'usage de glyphosate "Nettoyage des parcelles reverdies" (ID recmbzruq8M4v7uW8) manque l\'enum code (colonne Enum code)')

        # If the enum is not part of the known cultures, we expect an error
        json = [{
            "id": "recmbzruq8M4v7uW8",
            "fields": {
                "Name": "Nettoyage des parcelles reverdies",
                "Enum code": "UNKNOWN_CODE",
            },
        }]
        errors = validate_glyphosate_uses(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'L\'usage de glyphosate "Nettoyage des parcelles reverdies" (ID recmbzruq8M4v7uW8) a un code enum qui n\'est pas connu du backend')


    def test_pests_validation(self):
        # This is an example of a complete pest, there should be no errors
        json = [{
            "id": "recqwipvZ8hYkqoW2",
            "fields": {
                "Name": "Mélighétes",
                "Enum code": "MELIGETHES",
            },
        }]
        errors = validate_pests(json)
        self.assertEqual(len(errors), 0)

        # If the name is missing, we expect an error
        json = [{
            "id": "recqwipvZ8hYkqoW2",
            "fields": {
                "Name": "",
                "Enum code": "MELIGETHES",
            },
        }]
        errors = validate_pests(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Ravageur ID recqwipvZ8hYkqoW2 n\'a pas de nom (colonne Name)')

        # If the enum is missing, we expect an error
        json = [{
            "id": "recqwipvZ8hYkqoW2",
            "fields": {
                "Name": "Mélighétes",
            },
        }]
        errors = validate_pests(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Ravageur "Mélighétes" (ID recqwipvZ8hYkqoW2) manque l\'enum code (colonne Enum code)')

        # If the enum is not part of the known cultures, we expect an error
        json = [{
            "id": "recqwipvZ8hYkqoW2",
            "fields": {
                "Name": "Mélighétes",
                "Enum code": "UNKNOWN_CODE",
            },
        }]
        errors = validate_pests(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Ravageur "Mélighétes" (ID recqwipvZ8hYkqoW2) a un code enum qui n\'est pas connu du backend')


    def test_weeds_validation(self):
        # This is an example of a complete weed, there should be no errors
        json = [{
            "id": "recjzIBqwGkton9Ed",
            "fields": {
                "Name": "Ray-grass",
                "Enum code": "RAY_GRASS",
            },
        }]
        errors = validate_weeds(json)
        self.assertEqual(len(errors), 0)

        # If the name is missing, we expect an error
        json = [{
            "id": "recjzIBqwGkton9Ed",
            "fields": {
                "Enum code": "RAY_GRASS",
            },
        }]
        errors = validate_weeds(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Adventice ID recjzIBqwGkton9Ed n\'a pas de nom (colonne Name)')

        # If the enum is missing, we expect an error
        json = [{
            "id": "recjzIBqwGkton9Ed",
            "fields": {
                "Name": "Ray-grass",
            },
        }]
        errors = validate_weeds(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Adventice "Ray-grass" (ID recjzIBqwGkton9Ed) manque l\'enum code (colonne Enum code)')

        # If the enum is not part of the known cultures, we expect an error
        json = [{
            "id": "recjzIBqwGkton9Ed",
            "fields": {
                "Name": "Ray-grass",
                "Enum code": "UNKNOWN_CODE",
            },
        }]
        errors = validate_weeds(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Adventice "Ray-grass" (ID recjzIBqwGkton9Ed) a un code enum qui n\'est pas connu du backend')


    def test_practice_types(self):
        # This is an example of a complete practice type, there should be no errors
        json = [{
            "id": "rec8HRoPa3LnI95oU",
            "fields": {
                "Name": "Réduction des doses",
                "Enum code": "REDUCTION_DOSES",
                "Malus": 0.4,
            },
        }]
        errors = validate_practice_types(json)
        self.assertEqual(len(errors), 0)

        # If the name is missing, we expect an error
        json = [{
            "id": "rec8HRoPa3LnI95oU",
            "fields": {
                "Enum code": "REDUCTION_DOSES",
                "Malus": 0.4,
            },
        }]
        errors = validate_practice_types(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Type de pratique ID rec8HRoPa3LnI95oU n\'a pas de nom (colonne Name)')

        # If the enum is missing, we expect an error
        json = [{
            "id": "rec8HRoPa3LnI95oU",
            "fields": {
                "Name": "Réduction des doses",
                "Malus": 0.4,
            },
        }]
        errors = validate_practice_types(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Type de pratique "Réduction des doses" (ID rec8HRoPa3LnI95oU) manque l\'enum code (colonne Enum code)')

        # If the enum is not part of the known cultures, we expect an error
        json = [{
            "id": "rec8HRoPa3LnI95oU",
            "fields": {
                "Name": "Réduction des doses",
                "Enum code": "UNKNOWN_CODE",
                "Malus": 0.4,
            },
        }]
        errors = validate_practice_types(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Type de pratique "Réduction des doses" (ID rec8HRoPa3LnI95oU) a un code enum qui n\'est pas connu du backend')

        # If the malus is not between 0 and 1, we expect an error
        json = [{
            "id": "rec8HRoPa3LnI95oU",
            "fields": {
                "Name": "Réduction des doses",
                "Enum code": "REDUCTION_DOSES",
                "Malus": 1.4,
            },
        }]
        errors = validate_practice_types(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Type de pratique "Réduction des doses" (ID rec8HRoPa3LnI95oU) a un malus invalide (ça doit être entre 0 et 1)')


    def test_practice_validation(self):
        # This is an example of a complete practice, there should be no errors
        json = [{
            "id": "recopQwOR1Bxr4m5S",
            "fields": {
                "Nom": "[vigne] Désherber mécanique le cavaillon",
                "Description": "Il existe divers outils pour désherber le pied des vignes.",
                "CTA lien": ["recPIJIM77lSOEwfR"],
                "Matériel": "Scalpeurs, houes rotatives, ",
                "Période de travail": "Toute l'année",
                "Impact": "50% de réduction des herbicides",
                "CTA title": "Comparez les outils",
                "Élevage multiplicateur": 1,
                "Nécessite travail du sol": True,
                "Difficulté": 0.7,
                "Vente directe multiplicateur": 1.15,
                "Marges de manoeuvre": ["recRcRPuPF8QsGt4Z", "reclHkrRmtx5tHbcm"],
                "Problèmes adressés": ["DESHERBAGE"],
                "Cultures whitelist": ["recT3CrK0EqgCGL8z"],
                "Facteur clé de succès": "Utiliser l'équipement le mieux adapté aux conditions climatiques",
                "Types": ["reciTfZiZI2otTUFN"],
            },
        }]
        errors = validate_practices(json)
        self.assertEqual(len(errors), 0)

        # If there is no name, description, CTA link, CTA label, difficulty or types we should get an error
        json = [{
            "id": "recopQwOR1Bxr4m5S",
            "fields": {
                "Matériel": "Scalpeurs, houes rotatives, ",
                "Période de travail": "Toute l'année",
                "Impact": "50% de réduction des herbicides",
                "Élevage multiplicateur": 1,
                "Nécessite travail du sol": True,
                "Vente directe multiplicateur": 1.15,
                "Marges de manoeuvre": ["recRcRPuPF8QsGt4Z", "reclHkrRmtx5tHbcm"],
                "Problèmes adressés": ["DESHERBAGE"],
                "Cultures whitelist": ["recT3CrK0EqgCGL8z"],
                "Facteur clé de succès": "Utiliser l'équipement le mieux adapté aux conditions climatiques",
            },
        }]
        errors = validate_practices(json)
        self.assertEqual(len(errors), 6)
        self.assertTrue(any(x.message == 'Pratique ID recopQwOR1Bxr4m5S n\'a pas de titre (colonne Nom)' for x in errors))
        self.assertTrue(any(x.message == 'Pratique "None" (ID recopQwOR1Bxr4m5S) manque la description (colonne Description)' for x in errors))
        self.assertTrue(any(x.message == 'Pratique "None" (ID recopQwOR1Bxr4m5S) n\'a pas de lien CTA (colonne CTA lien)' for x in errors))
        self.assertTrue(any(x.message == 'Pratique "None" (ID recopQwOR1Bxr4m5S) n\'a pas de titre CTA (colonne CTA title)' for x in errors))
        self.assertTrue(any(x.message == 'Pratique "None" (ID recopQwOR1Bxr4m5S) n\'a pas de type (colonne Types)' for x in errors))
        self.assertTrue(any(x.message == 'Pratique "None" (ID recopQwOR1Bxr4m5S) n\'a pas de difficulté (colonne Difficutlé)' for x in errors))
