from django.test import TestCase
from data.airtablevalidators import validate_cultures, validate_glyphosate_uses, validate_pests
from data.airtablevalidators import validate_practice_types, validate_practices, validate_weeds
from data.airtablevalidators import validate_categories, validate_weed_practices, validate_pest_practices
from data.airtablevalidators import validate_culture_practices, validate_department_practices
from data.airtablevalidators import validate_departments, validate_glyphosate_practices, validate_practice_groups
from data.airtablevalidators import validate_mechanisms

# Here we test error messages that can be longer than Pylint limit.
# pylint: disable=line-too-long

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
            },
        }]
        errors = validate_cultures(json)
        self.assertEqual(len(errors), 0)

        # If the name is missing, we expect an error
        json = [{
            "id": "recuVebqXEqCg8kK0",
            "fields": {
            },
        }]
        errors = validate_cultures(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Culture ID recuVebqXEqCg8kK0 n\'a pas de nom (colonne Name)')


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
            },
        }]
        errors = validate_pests(json)
        self.assertEqual(len(errors), 0)

        # If the name is missing, we expect an error
        json = [{
            "id": "recqwipvZ8hYkqoW2",
            "fields": {
                "Name": "",
            },
        }]
        errors = validate_pests(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Ravageur ID recqwipvZ8hYkqoW2 n\'a pas de nom (colonne Name)')


    def test_weeds_validation(self):
        # This is an example of a complete weed, there should be no errors
        json = [{
            "id": "recjzIBqwGkton9Ed",
            "fields": {
                "Name": "Ray-grass",
            },
        }]
        errors = validate_weeds(json)
        self.assertEqual(len(errors), 0)

        # If the name is missing, we expect an error
        json = [{
            "id": "recjzIBqwGkton9Ed",
            "fields": {
            },
        }]
        errors = validate_weeds(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].message, 'Adventice ID recjzIBqwGkton9Ed n\'a pas de nom (colonne Name)')


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
                "Nom court": "Désherber mécanique cavaillon",
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

        # If there is no name, short name, description, CTA link, CTA label, difficulty or types we should get an error
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
        self.assertEqual(len(errors), 7)
        self.assertTrue(any(x.message == 'Pratique ID recopQwOR1Bxr4m5S n\'a pas de titre (colonne Nom)' for x in errors))
        self.assertTrue(any(x.message == 'Pratique "None" (ID recopQwOR1Bxr4m5S) manque la description (colonne Description)' for x in errors))
        self.assertTrue(any(x.message == 'Pratique "None" (ID recopQwOR1Bxr4m5S) manque le nom court (colonne Nom court)' for x in errors))
        self.assertTrue(any(x.message == 'Pratique "None" (ID recopQwOR1Bxr4m5S) n\'a pas de lien CTA (colonne CTA lien)' for x in errors))
        self.assertTrue(any(x.message == 'Pratique "None" (ID recopQwOR1Bxr4m5S) n\'a pas de titre CTA (colonne CTA title)' for x in errors))
        self.assertTrue(any(x.message == 'Pratique "None" (ID recopQwOR1Bxr4m5S) n\'a pas de type (colonne Types)' for x in errors))
        self.assertTrue(any(x.message == 'Pratique "None" (ID recopQwOR1Bxr4m5S) n\'a pas de difficulté (colonne Difficulté)' for x in errors))

        # If there is nothing among "matériel, période de travail, impact, bénéfices supplémentaires, or facteur clé de succès"
        # we should get an error
        json = [{
            "id": "recopQwOR1Bxr4m5S",
            "fields": {
                "Nom": "[vigne] Désherber mécanique le cavaillon",
                "Nom court": "Désherber mécanique cavaillon",
                "Description": "Il existe divers outils pour désherber le pied des vignes.",
                "CTA lien": ["recPIJIM77lSOEwfR"],
                "CTA title": "Comparez les outils",
                "Élevage multiplicateur": 1,
                "Nécessite travail du sol": True,
                "Difficulté": 0.7,
                "Vente directe multiplicateur": 1.15,
                "Marges de manoeuvre": ["recRcRPuPF8QsGt4Z", "reclHkrRmtx5tHbcm"],
                "Problèmes adressés": ["DESHERBAGE"],
                "Cultures whitelist": ["recT3CrK0EqgCGL8z"],
                "Types": ["reciTfZiZI2otTUFN"],
            },
        }]
        errors = validate_practices(json)
        self.assertEqual(len(errors), 1)
        message = 'La pratique "[vigne] Désherber mécanique le cavaillon" (ID recopQwOR1Bxr4m5S) n\'a aucune information additionelle. Il faut au moins une parmi : matériel, période de travail, impact, bénéfices supplémentaires, ou facteur clé de succès'
        self.assertTrue(errors[0].message == message)


    def test_category_validation(self):
        # This is an example of a complete category, there should be no errors
        json = [{
            "id": "recTr8uZvM2uLu9Mo",
            "fields": {
                "Title": "À faire cet hiver",
                "Description": "Lorem Ipsum",
                "Image": [{
                    "id": "attb4AWbDRteZVVks",
                    "url": "https://dl.airtable.com/.attachments/b477ef6bacc441b1368f6bdfdab3935f/270d62dc/a-faire-cet-hiver.jpg",
                    "filename": "a-faire-cet-hiver.jpg",
                    "size": 157238,
                    "type": "image/jpeg",
                }],
                "Practices": ["rec5RshLKLcZfQ2t9", "recD7QrzTgOBT5OHl", "receGroWCXTPC5kat"]
            }
        }]
        errors = validate_categories(json)
        self.assertEqual(len(errors), 0)

        # If there is no title, image or practices we should get an error
        json = [{
            "id": "recTr8uZvM2uLu9Mo",
            "fields": {
                "Description": "Lorem Ipsum",
            }
        }]
        errors = validate_categories(json)
        self.assertEqual(len(errors), 3)
        self.assertTrue(any(x.message == 'La categorie ID recTr8uZvM2uLu9Mo n\'a pas de title (colonne Title)' for x in errors))
        self.assertTrue(any(x.message == 'La categorie "None" (ID recTr8uZvM2uLu9Mo) n\'a pas d\'image (colonne Image)' for x in errors))
        self.assertTrue(any(x.message == 'La categorie "None" (ID recTr8uZvM2uLu9Mo) n\'a pas de pratiques assignées (colonne Practices)' for x in errors))

        # If there is no description we should get a non-fatal error
        json = [{
            "id": "recTr8uZvM2uLu9Mo",
            "fields": {
                "Title": "À faire cet hiver",
                "Image": [{
                    "id": "attb4AWbDRteZVVks",
                    "url": "https://dl.airtable.com/.attachments/b477ef6bacc441b1368f6bdfdab3935f/270d62dc/a-faire-cet-hiver.jpg",
                    "filename": "a-faire-cet-hiver.jpg",
                    "size": 157238,
                    "type": "image/jpeg",
                }],
                "Practices": ["rec5RshLKLcZfQ2t9", "recD7QrzTgOBT5OHl", "receGroWCXTPC5kat"]
            }
        }]
        errors = validate_categories(json)
        self.assertEqual(len(errors), 1)
        message = 'La categorie "À faire cet hiver" (ID recTr8uZvM2uLu9Mo) n\'a pas de description (colonne Description)'
        self.assertTrue(errors[0].message == message)


    def test_weed_practice_validation(self):
        # This is an example of a complete weed-practice relation, there should be no errors
        json = [{
            "id": "recQWS46mDL7nD8xS",
            "fields": {
                "Adventice": ["recjzIBqwGkton9Ed"],
                "Multiplicateur": 1.05,
                "Pratique": ["recswKhe3JNRErR0L"],
                "Name": "Ray-grass - Collecter les menues pailles"
            },
        }]
        errors = validate_weed_practices(json)
        self.assertEqual(len(errors), 0)

        # If the weed array or the practice array is empty, or a missing multiplier, we should get errors
        json = [{
            "id": "recQWS46mDL7nD8xS",
            "fields": {
                "Adventice": [],
                "Pratique": [],
                "Name": "Ray-grass - Collecter les menues pailles"
            }
        }]
        errors = validate_weed_practices(json)
        self.assertEqual(len(errors), 3)
        self.assertTrue(any(x.message == 'La relation adventice-pratique ID recQWS46mDL7nD8xS n\'a pas d\'adventice (colonne Adventice)' for x in errors))
        self.assertTrue(any(x.message == 'La relation adventice-pratique ID recQWS46mDL7nD8xS n\'a pas de pratique (colonne Pratique)' for x in errors))
        self.assertTrue(any(x.message == 'La relation adventice-pratique ID recQWS46mDL7nD8xS n\'a pas de multiplicateur (colonne Multiplicateur)' for x in errors))

        # However, a multiplier of zero is valid
        json = [{
            "id": "recQWS46mDL7nD8xS",
            "fields": {
                "Adventice": ["recjzIBqwGkton9Ed"],
                "Multiplicateur": 0,
                "Pratique": ["recswKhe3JNRErR0L"],
                "Name": "Ray-grass - Collecter les menues pailles"
            },
        }]
        errors = validate_weed_practices(json)
        self.assertEqual(len(errors), 0)


    def test_pest_practice_validation(self):
        # This is an example of a complete pest-practice relation, there should be no errors
        json = [{
            "id": "recGjZXNbp00qNxfp",
            "fields": {
                "Ravageur": ["recEbpaMFaFY4mtG6"],
                "Multiplicateur": 1.1,
                "Pratique": ["recX4K4zviP1C1fG7"],
                "Name": "Altises - Faire paturer les couverts et les repousses"
            },
        }]
        errors = validate_pest_practices(json)
        self.assertEqual(len(errors), 0)

        # If the pest array or the practice array is empty, or a missing multiplier, we should get errors
        json = [{
            "id": "recGjZXNbp00qNxfp",
            "fields": {
                "Ravageur": [],
                "Pratique": [],
                "Name": "Altises - Faire paturer les couverts et les repousses"
            },
        }]
        errors = validate_pest_practices(json)
        self.assertEqual(len(errors), 3)
        self.assertTrue(any(x.message == 'La relation ravageur-pratique ID recGjZXNbp00qNxfp n\'a pas de ravageur (colonne Ravageur)' for x in errors))
        self.assertTrue(any(x.message == 'La relation ravageur-pratique ID recGjZXNbp00qNxfp n\'a pas de pratique (colonne Pratique)' for x in errors))
        self.assertTrue(any(x.message == 'La relation ravageur-pratique ID recGjZXNbp00qNxfp n\'a pas de multiplicateur (colonne Multiplicateur)' for x in errors))

        # However, a multiplier of zero is valid
        json = [{
            "id": "recGjZXNbp00qNxfp",
            "fields": {
                "Ravageur": ["recEbpaMFaFY4mtG6"],
                "Multiplicateur": 0,
                "Pratique": ["recX4K4zviP1C1fG7"],
                "Name": "Altises - Faire paturer les couverts et les repousses"
            },
        }]
        errors = validate_pest_practices(json)
        self.assertEqual(len(errors), 0)


    def test_culture_practice_validation(self):
        # This is an example of a complete culture-practice relation, there should be no errors
        json = [{
            "id": "reca8x23dr3kk57uX",
            "fields": {
                "Culture": ["recuVebqXEqCg8kK0"],
                "Multiplicateur": 1.2,
                "Pratique": ["recze8GDGOm8i4ul9"],
                "Name": "Blé dur - Semer l'inter-rang pour réduire la place disponible aux adventices"
            },
        }]
        errors = validate_culture_practices(json)
        self.assertEqual(len(errors), 0)

        # If the culture array or the practice array is empty, or a missing multiplier, we should get errors
        json = [{
            "id": "reca8x23dr3kk57uX",
            "fields": {
                "Culture": [],
                "Pratique": [],
                "Name": "Blé dur - Semer l'inter-rang pour réduire la place disponible aux adventices"
            },
        }]
        errors = validate_culture_practices(json)
        self.assertEqual(len(errors), 3)
        self.assertTrue(any(x.message == 'La relation culture-pratique ID reca8x23dr3kk57uX n\'a pas de culture (colonne Culture)' for x in errors))
        self.assertTrue(any(x.message == 'La relation culture-pratique ID reca8x23dr3kk57uX n\'a pas de pratique (colonne Pratique)' for x in errors))
        self.assertTrue(any(x.message == 'La relation culture-pratique ID reca8x23dr3kk57uX n\'a pas de multiplicateur (colonne Multiplicateur)' for x in errors))

        # However, a multiplier of zero is valid
        json = [{
            "id": "reca8x23dr3kk57uX",
            "fields": {
                "Culture": ["recuVebqXEqCg8kK0"],
                "Multiplicateur": 0,
                "Pratique": ["recze8GDGOm8i4ul9"],
                "Name": "Blé dur - Semer l'inter-rang pour réduire la place disponible aux adventices"
            },
        }]
        errors = validate_culture_practices(json)
        self.assertEqual(len(errors), 0)


    def test_department_practice_validation(self):
        # This is an example of a complete department-practice relation, there should be no errors
        json = [{
            "id": "recqYTBrTU2q8Vnu3",
            "fields": {
                "Pratique": ["recA8s2p2PC2FBg9c"],
                "Departement": ["rec516ccAAAKrRJ5y"],
                "Multiplicateur": 1,
                "Name": "10 - Profiter de l'action des auxiliaires sur le puceron de l'épi"
            },
        }]
        errors = validate_department_practices(json)
        self.assertEqual(len(errors), 0)

        # If the department array or the practice array is empty, or a missing multiplier, we should get errors
        json = [{
            "id": "recqYTBrTU2q8Vnu3",
            "fields": {
                "Pratique": [],
                "Departement": [],
                "Name": "10 - Profiter de l'action des auxiliaires sur le puceron de l'épi"
            },
        }]
        errors = validate_department_practices(json)
        self.assertEqual(len(errors), 3)
        self.assertTrue(any(x.message == 'La relation departement-pratique ID recqYTBrTU2q8Vnu3 n\'a pas de departement (colonne Departement)' for x in errors))
        self.assertTrue(any(x.message == 'La relation departement-pratique ID recqYTBrTU2q8Vnu3 n\'a pas de pratique (colonne Pratique)' for x in errors))
        self.assertTrue(any(x.message == 'La relation departement-pratique ID recqYTBrTU2q8Vnu3 n\'a pas de multiplicateur (colonne Multiplicateur)' for x in errors))

        # However, a multiplier of zero is valid
        json = [{
            "id": "recqYTBrTU2q8Vnu3",
            "fields": {
                "Pratique": ["recA8s2p2PC2FBg9c"],
                "Departement": ["rec516ccAAAKrRJ5y"],
                "Multiplicateur": 0,
                "Name": "10 - Profiter de l'action des auxiliaires sur le puceron de l'épi"
            },
        }]
        errors = validate_department_practices(json)
        self.assertEqual(len(errors), 0)


    def test_glyphosate_practice_validation(self):
        # This is an example of a complete glyphosate-practice relation, there should be no errors
        json = [{
            "id": "recjpT1JvxfvHgbTd",
            "fields": {
                "Glyphosate": ["recoU540M3R2rEN8U"],
                "Multiplicateur": 1.2,
                "Pratique": ["recfhdTh4CvU7nDUO", "reccdlRtfXVIVKrvx", "recYovWX4T3Gw1Tqt"],
            },
        }]
        errors = validate_glyphosate_practices(json)
        self.assertEqual(len(errors), 0)

        # If the glyphosate array or the practice array is empty, or a missing multiplier, we should get errors
        json = [{
            "id": "recjpT1JvxfvHgbTd",
            "fields": {
                "Glyphosate": [],
                "Pratique": [],
            },
        }]
        errors = validate_glyphosate_practices(json)
        self.assertEqual(len(errors), 3)
        self.assertTrue(any(x.message == 'La relation glyphosate-pratique ID recjpT1JvxfvHgbTd n\'a pas de glyphosate (colonne Glyphosate)' for x in errors))
        self.assertTrue(any(x.message == 'La relation glyphosate-pratique ID recjpT1JvxfvHgbTd n\'a pas de pratique (colonne Pratique)' for x in errors))
        self.assertTrue(any(x.message == 'La relation glyphosate-pratique ID recjpT1JvxfvHgbTd n\'a pas de multiplicateur (colonne Multiplicateur)' for x in errors))

        # However, a multiplier of zero is valid
        json = [{
            "id": "recjpT1JvxfvHgbTd",
            "fields": {
                "Glyphosate": ["recoU540M3R2rEN8U"],
                "Multiplicateur": 0,
                "Pratique": ["recfhdTh4CvU7nDUO", "reccdlRtfXVIVKrvx", "recYovWX4T3Gw1Tqt"],
            },
        }]
        errors = validate_glyphosate_practices(json)
        self.assertEqual(len(errors), 0)


    def test_department_validation(self):
        # This is an example of a complete department, there should be no errors
        json = [{
            "id": "rec7I8nS0qhrSRyPO",
            "fields": {
                "Numéro": "01",
                "Nom": "Ain"
            },
        }]
        errors = validate_departments(json)
        self.assertEqual(len(errors), 0)

        # If the name or number is missing we should get errors
        json = [{
            "id": "rec7I8nS0qhrSRyPO",
            "fields": {
            },
        }]
        errors = validate_departments(json)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any(x.message == 'Le departement ID rec7I8nS0qhrSRyPO n\'a pas de numéro (colonne Numéro)' for x in errors))
        self.assertTrue(any(x.message == 'Le departement ID rec7I8nS0qhrSRyPO n\'a pas de nom (colonne Nom)' for x in errors))


    def test_practice_group_validation(self):
        # This is an example of a complete practice group, there should be no errors
        json = [{
            "id": "recj2WyF3EHI5nYk1",
            "fields": {
                "Nom": "Couvert d'interculture",
                "Pratiques": ["recrD49Ih5S54FOhq", "recWr7fObtkAZW0X8"],
                "Description": "Le développement pendant l'interculture..."
            },
        }]
        errors = validate_practice_groups(json)
        self.assertEqual(len(errors), 0)

        # If the name is missing we should get a fatal error
        json = [{
            "id": "recj2WyF3EHI5nYk1",
            "fields": {
                "Pratiques": ["recrD49Ih5S54FOhq", "recWr7fObtkAZW0X8"],
                "Description": "Le développement pendant l'interculture..."
            },
        }]
        errors = validate_practice_groups(json)
        self.assertEqual(len(errors), 1)
        self.assertEqual('La famille ID recj2WyF3EHI5nYk1 n\'a pas de nom (colonne Nom)', errors[0].message)
        self.assertEqual(True, errors[0].fatal)

        # If the practices or description is missing we should get non-fatal errors
        json = [{
            "id": "recj2WyF3EHI5nYk1",
            "fields": {
                "Nom": "Couvert d'interculture",
            },
        }]
        errors = validate_practice_groups(json)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any(x.message == 'La famille Couvert d\'interculture (ID recj2WyF3EHI5nYk1) n\'a pas de pratiques (colonne Pratiques)' for x in errors))
        self.assertTrue(any(x.message == 'La famille Couvert d\'interculture (ID recj2WyF3EHI5nYk1) n\'a pas de description (colonne Description)' for x in errors))
        self.assertTrue(all(not x.fatal for x in errors))


    def test_mechanism_validation(self):
        # This is an example of a complete mechanism, there should be no errors
        json = [{
            "id": "recTNvJsPzzqEZS3q",
            "fields": {
                "Name": "Attirer le bioagresseur sur d'autres plantes",
                "Pratiques": ["recyMe1cHBaIrm58o"],
                "Description": "Les ravageurs peuvent être détournés...",
                "types": "Levier d'évitement, esquive",
                "Problème": ["Ravageurs"]
            },
        }]
        errors = validate_mechanisms(json)
        self.assertEqual(len(errors), 0)

        # If the name is missing we should a fatal error
        json = [{
            "id": "recTNvJsPzzqEZS3q",
            "fields": {
                "Pratiques": ["recyMe1cHBaIrm58o"],
                "Description": "Les ravageurs peuvent être détournés...",
                "types": "Levier d'évitement, esquive",
                "Problème": ["Ravageurs"]
            },
        }]
        errors = validate_mechanisms(json)
        self.assertEqual(len(errors), 1)
        self.assertTrue(any(x.message == 'La marge de manoeuvre ID recTNvJsPzzqEZS3q n\'a pas de nom (colonne Name)' for x in errors))
        self.assertTrue(all(x.fatal for x in errors))

        # If the description or practices is missing we should non-fatal errors
        json = [{
            "id": "recTNvJsPzzqEZS3q",
            "fields": {
                "Name": "Attirer le bioagresseur sur d'autres plantes",
                "Pratiques": [],
                "types": "Levier d'évitement, esquive",
                "Problème": ["Ravageurs"]
            },
        }]
        errors = validate_mechanisms(json)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any(x.message == 'La marge de manoeuvre Attirer le bioagresseur sur d\'autres plantes (ID recTNvJsPzzqEZS3q) n\'a pas de description (colonne Description)' for x in errors))
        self.assertTrue(any(x.message == 'La marge de manoeuvre Attirer le bioagresseur sur d\'autres plantes (ID recTNvJsPzzqEZS3q) n\'a pas de pratiques (colonne Pratiques)' for x in errors))
        self.assertTrue(all(not x.fatal for x in errors))
