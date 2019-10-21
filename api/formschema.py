def get_form_schema():
    return {
        "schema": {
            "description": "Optimisez votre système de culture",
            "type": "object",
            "properties": {
                "problem": {
                    "title": "Quel problème souhaitez-vous résoudre actuellement ?",
                    "required": False
                },
                "pests": {
                    "title": "Quels ravageurs vous posent problème aujourd'hui dans votre exploitation ?",
                    "required": False
                },
                "glyphosate": {
                    "title": "Quel est votre principal usage du glyphosate ?",
                    "required": False
                },
                "weeds": {
                    "title": "Quelles adventices vous posent problème aujourd'hui dans votre exploitation ?",
                    "required": False
                },
                "weedsGlyphosate": {
                    "title": "Quelles adventices vous posent problème aujourd'hui dans votre exploitation ?",
                    "required": False
                },
                "perennials": {
                    "title": "Quelles vivaces vous posent problème aujourd'hui dans votre exploitation ?",
                    "required": False
                },
                "practices": {
                    "title": "Quelles pratiques avez-vous déjà essayées pour répondre à ce problème ?",
                    "required": False
                },
                "tillage": {
                    "title": "Quels types de travail du sol pouvez-vous intégrer dans votre système ?",
                    "required": False,
                },
                "cattle": {
                    "title": "Avez-vous un atelier d’élevage ou disposez vous d’un débouché possible en alimentation animale ?",
                    "required": False,
                    "enum": [
                        "Oui",
                        "Non",
                    ]
                },
                "rotation": {
                    "title": "Dans l'ordre, quelles cultures composent la rotation des parcelles sur lesquelles vous rencontrez ce problème ?",
                    "required": False,
                    "uniqueItems": False,
                    "items": {
                        "required": True
                    }
                },
                "wheat": {
                    "title": "Pour le blé, combien de traitements appliquez-vous par campagne ?",
                    "required": False
                },
                "department": {
                    "title": "Quel est le département de votre exploitation ?",
                    "required": False
                },
                "groups": {
                    "title": "Faites-vous partie de groupes ou d'initiatives travaillant sur la réduction des produits phytosanitaires ?",
                    "required": False,
                    "logAnswer": True,
                },
                "referer": {
                    "title": "Comment avez-vous connu Peps ?",
                    "required": False,
                    "logAnswer": True,
                },
            },
            "dependencies": {
                "pests": ["problem"],
                "weeds": ["problem"],
                "weedsGlyphosate": ["glyphosate"],
                "perennials": ["glyphosate"],
                "glyphosate": ["problem"],
                "wheat": ["rotation"],
            }
        },
        "options": {
            "form": {
                "attributes": {
                    "method": "post",
                    "action": "/api/practices"
                }
            },
            "fields": {
                "problem": {
                    "sort": False,
                    "hideNone": True,
                    "type": "radio",
                    "focus": False,
                    "emptySelectFirst": False,
                    "dataSource": _get_problems(),
                },
                "pests": {
                    "hideNone": True,
                    "sort": True,
                    "type": "checkbox",
                    "multiple": True,
                    "dependencies": {
                        "problem": "RAVAGEURS"
                    },
                    "dataSource": _get_pests(),
                },
                "weeds": {
                    "hideNone": True,
                    "sort": True,
                    "type": "checkbox",
                    "multiple": True,
                    "dependencies": {
                        "problem": ["DESHERBAGE"],
                    },
                    "dataSource": _get_weeds(),
                },
                "weedsGlyphosate": {
                    "hideNone": True,
                    "sort": True,
                    "type": "checkbox",
                    "multiple": True,
                    "dependencies": {
                        "glyphosate": ["COUVERTS", "PARCELLES", "PRAIRIES", "AUTRES"],
                    },
                    "dataSource": _get_weeds(),
                },
                "perennials": {
                    "hideNone": True,
                    "sort": True,
                    "type": "checkbox",
                    "multiple": True,
                    "dependencies": {
                        "glyphosate": ["VIVACES"]
                    },
                    "dataSource": _get_perennials(),
                },
                "glyphosate": {
                    "hideNone": True,
                    "sort": False,
                    "type": "radio",
                    "multiple": False,
                    "dependencies": {
                        "problem": "GLYPHOSATE"
                    },
                    "dataSource": _get_glyphosate_uses(),
                },
                "practices": {
                    "hideNone": True,
                    "sort": True,
                    "type": "checkbox",
                    "multiple": True,
                    "dataSource": _get_practice_types(),
                },
                "tillage": {
                    "hideNone": True,
                    "sort": False,
                    "type": "radio",
                    "multiple": True,
                    "dataSource": [
                        {'text': 'Tous types de travail du sol', 'value': 'TRAVAIL_PROFOND'},
                        {'text': 'Travail superficiel uniquement', 'value': 'TRAVAIL_DU_SOL'},
                        {'text': 'Aucun travail du sol', 'value': 'NONE'},
                    ],
                },
                "cattle": {
                    "sort": False,
                    "hideNone": True,
                    "type": "radio",
                },
                "rotation": {
                    "type": "array",
                    "toolbarSticky": True,
                    "items": {
                        "type": "select",
                        "dataSource": _get_cultures(),
                    }
                },
                "wheat": {
                    "dependencies": {
                        "rotation": ["recuVebqXEqCg8kK0", "recmm8lo1bGXCYSA3", "recSmDBTPyv0R1Rik"],
                    },
                    "sort": False,
                    "hideNone": True,
                    "type": "radio",
                    "dataSource": [
                        {"text": "Je n'applique pas de traitement", "value": "1.0"},
                        {"text": "1 à 2", "value": "0.8"},
                        {"text": "3 à 5", "value": "0.6"},
                        {"text": "5 à 8", "value": "0.4"},
                        {"text": "Plus de 8", "value": "0.15"},
                        {"text": "Je ne sais pas", "value": "0.1"},
                    ]
                },
                "department": {
                    "type": "select",
                    "dataSource": [
                        {"value": "01", "text": "01 - Ain"},
                        {"value": "02", "text": "02 - Aisne"},
                        {"value": "03", "text": "03 - Allier"},
                        {"value": "04", "text": "04 - Alpes-de-Haute-Provence"},
                        {"value": "05", "text": "05 - Hautes-alpes"},
                        {"value": "06", "text": "06 - Alpes-maritimes"},
                        {"value": "07", "text": "07 - Ardèche"},
                        {"value": "08", "text": "08 - Ardennes"},
                        {"value": "09", "text": "09 - Ariège"},
                        {"value": "10", "text": "10 - Aube"},
                        {"value": "11", "text": "11 - Aude"},
                        {"value": "12", "text": "12 - Aveyron"},
                        {"value": "13", "text": "13 - Bouches-du-Rhône"},
                        {"value": "14", "text": "14 - Calvados"},
                        {"value": "15", "text": "15 - Cantal"},
                        {"value": "16", "text": "16 - Charente"},
                        {"value": "17", "text": "17 - Charente-maritime"},
                        {"value": "18", "text": "18 - Cher"},
                        {"value": "19", "text": "19 - Corrèze"},
                        {"value": "2a", "text": "2a - Corse-du-sud"},
                        {"value": "2b", "text": "2b - Haute-Corse"},
                        {"value": "21", "text": "21 - Côte-d'Or"},
                        {"value": "22", "text": "22 - Côtes-d'Armor"},
                        {"value": "23", "text": "23 - Creuse"},
                        {"value": "24", "text": "24 - Dordogne"},
                        {"value": "25", "text": "25 - Doubs"},
                        {"value": "26", "text": "26 - Drôme"},
                        {"value": "27", "text": "27 - Eure"},
                        {"value": "28", "text": "28 - Eure-et-loir"},
                        {"value": "29", "text": "29 - Finistère"},
                        {"value": "30", "text": "30 - Gard"},
                        {"value": "31", "text": "31 - Haute-garonne"},
                        {"value": "32", "text": "32 - Gers"},
                        {"value": "33", "text": "33 - Gironde"},
                        {"value": "34", "text": "34 - Hérault"},
                        {"value": "35", "text": "35 - Ille-et-vilaine"},
                        {"value": "36", "text": "36 - Indre"},
                        {"value": "37", "text": "37 - Indre-et-loire"},
                        {"value": "38", "text": "38 - Isère"},
                        {"value": "39", "text": "39 - Jura"},
                        {"value": "40", "text": "40 - Landes"},
                        {"value": "41", "text": "41 - Loir-et-cher"},
                        {"value": "42", "text": "42 - Loire"},
                        {"value": "43", "text": "43 - Haute-loire"},
                        {"value": "44", "text": "44 - Loire-atlantique"},
                        {"value": "45", "text": "45 - Loiret"},
                        {"value": "46", "text": "46 - Lot"},
                        {"value": "47", "text": "47 - Lot-et-garonne"},
                        {"value": "48", "text": "48 - Lozère"},
                        {"value": "49", "text": "49 - Maine-et-loire"},
                        {"value": "50", "text": "50 - Manche"},
                        {"value": "51", "text": "51 - Marne"},
                        {"value": "52", "text": "52 - Haute-marne"},
                        {"value": "53", "text": "53 - Mayenne"},
                        {"value": "54", "text": "54 - Meurthe-et-moselle"},
                        {"value": "55", "text": "55 - Meuse"},
                        {"value": "56", "text": "56 - Morbihan"},
                        {"value": "57", "text": "57 - Moselle"},
                        {"value": "58", "text": "58 - Nièvre"},
                        {"value": "59", "text": "59 - Nord"},
                        {"value": "60", "text": "60 - Oise"},
                        {"value": "61", "text": "61 - Orne"},
                        {"value": "62", "text": "62 - Pas-de-calais"},
                        {"value": "63", "text": "63 - Puy-de-dôme"},
                        {"value": "64", "text": "64 - Pyrénées-atlantiques"},
                        {"value": "65", "text": "65 - Hautes-Pyrénées"},
                        {"value": "66", "text": "66 - Pyrénées-orientales"},
                        {"value": "67", "text": "67 - Bas-rhin"},
                        {"value": "68", "text": "68 - Haut-rhin"},
                        {"value": "69", "text": "69 - Rhône"},
                        {"value": "70", "text": "70 - Haute-saône"},
                        {"value": "71", "text": "71 - Saône-et-loire"},
                        {"value": "72", "text": "72 - Sarthe"},
                        {"value": "73", "text": "73 - Savoie"},
                        {"value": "74", "text": "74 - Haute-savoie"},
                        {"value": "75", "text": "75 - Paris"},
                        {"value": "76", "text": "76 - Seine-maritime"},
                        {"value": "77", "text": "77 - Seine-et-marne"},
                        {"value": "78", "text": "78 - Yvelines"},
                        {"value": "79", "text": "79 - Deux-sèvres"},
                        {"value": "80", "text": "80 - Somme"},
                        {"value": "81", "text": "81 - Tarn"},
                        {"value": "82", "text": "82 - Tarn-et-garonne"},
                        {"value": "83", "text": "83 - Var"},
                        {"value": "84", "text": "84 - Vaucluse"},
                        {"value": "85", "text": "85 - Vendée"},
                        {"value": "86", "text": "86 - Vienne"},
                        {"value": "87", "text": "87 - Haute-vienne"},
                        {"value": "88", "text": "88 - Vosges"},
                        {"value": "89", "text": "89 - Yonne"},
                        {"value": "90", "text": "90 - Territoire de belfort"},
                        {"value": "91", "text": "91 - Essonne"},
                        {"value": "92", "text": "92 - Hauts-de-seine"},
                        {"value": "93", "text": "93 - Seine-Saint-Denis"},
                        {"value": "94", "text": "94 - Val-de-marne"},
                        {"value": "95", "text": "95 - Val-d'oise"},
                        {"value": "971", "text": "971 - Guadeloupe"},
                        {"value": "972", "text": "972 - Martinique"},
                        {"value": "973", "text": "973 - Guyane"},
                        {"value": "974", "text": "974 - La réunion"},
                        {"value": "976", "text": "976 - Mayotte"}
                    ],
                },
                "groups": {
                    "hideNone": True,
                    "sort": False,
                    "type": "checkbox",
                    "multiple": True,
                    "dataSource": [
                        {'text': 'DEPHY', 'value': 'groupe_DEPHY'},
                        {'text': '30000', 'value': 'groupe_30000'},
                        {'text': 'GIEE', 'value': 'groupe_GIEE'},
                        {'text': 'Groupe de chambre d\'agriculture', 'value': 'groupe_chambre_agriculture'},
                        {'text': 'Groupe de coopérative ou négoce', 'value': 'groupe_cooperative_negoce'},
                        {'text': 'Je suis en AB ou en conversion AB', 'value': 'groupe_conversion_ab'},
                        {'text': 'Autre', 'value': 'groupe_autre'},
                        {'text': 'Aucun', 'value': 'groupe_aucun'},
                    ],
                },
                "referer": {
                    "hideNone": True,
                    "sort": False,
                    "type": "checkbox",
                    "multiple": True,
                    "dataSource": [
                        {'text': 'Moteur de recherche (Google, Bing, etc.)', 'value': 'referer_moteur_recherche'},
                        {'text': 'Réseaux sociaux (Facebook, Twitter)', 'value': 'referer_reseaux_sociaux'},
                        {'text': 'Bouche à oreille', 'value': 'referer_bouche_a_oreille'},
                        {'text': 'Presse', 'value': 'referer_presse'},
                        {'text': 'Par ma coopérative ou mon négoce', 'value': 'referer_cooperative_negoce'},
                        {'text': 'Par ma Chambre d\'Agriculture', 'value': 'referer_chambre_agriculture'},
                        {'text': 'Par un agriculteur', 'value': 'referer_agriculteur'},
                        {'text': 'Via un atelier sur mon territoire', 'value': 'referer_aterlier'},
                        {'text': 'Par la DDT', 'value': 'referer_ddt'},
                        {'text': 'Autre', 'value': 'referer_autre'},
                    ],
                },
            }
        },
    }


def _get_pests():
    from data.models import Pest
    return [{'text': x.display_text, 'value': x.external_id} for x in Pest.objects.all()]

def _get_weeds():
    from data.models import Weed
    return [{'text': x.display_text, 'value': x.external_id} for x in Weed.objects.all()]

def _get_perennials():
    from data.models import Weed
    return [{'text': x.display_text, 'value': x.external_id} for x in Weed.objects.all() if x.nature == 1]

def _get_problems():
    from data.models import Problem
    return [{'text': x.display_text, 'value': x.name} for x in Problem]

def _get_practice_types():
    from data.models import PracticeType
    form_types = PracticeType.objects.filter(penalty__lte=1.0)
    return [{'text': x.display_text, 'value': x.get_category_name()} for x in form_types]

def _get_cultures():
    from data.models import Culture
    return [{'text': x.display_text, 'value': x.external_id} for x in Culture.objects.all()]

def _get_glyphosate_uses():
    from data.models import GlyphosateUses
    return [{'text': x.display_text, 'value': x.name} for x in GlyphosateUses]
