def get_form_schema():
    return {
        "schema": {
            "description": "Optimisez votre système de culture",
            "type": "object",
            "properties": {
                "problem": {
                    "title": "Sur quel sujet pouvons-nous vous aider ?",
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
                "tillage": {
                    "title": "Quels types de travail du sol souhaitez-vous intégrer dans votre système ?",
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
                    "title": "Quelles cultures composent la rotation des parcelles sur lesquelles vous rencontrez ce problème ?",
                    "required": False,
                    "uniqueItems": False,
                    "items": {
                        "required": True
                    }
                },
            },
            "dependencies": {
                "pests": ["problem"],
                "weeds": ["problem"],
                "weedsGlyphosate": ["glyphosate"],
                "perennials": ["glyphosate"],
                "glyphosate": ["problem"],
            },
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
                    },
                    "toolbar": {
                        "actions": [{
                            "label": "Ajoutez une culture",
                            "action": "add",
                        }],
                    },
                    "actionbar": {
                        "actions": [{
                            "action": "up",
                            "enabled": False,
                        }, {
                            "action": "down",
                            "enabled": False,
                        }]
                    },
                },
            }
        },
        "practices_form": {
            "schema": {
                "description": "Vos réponses à ces questions vont permettre d'identifier trois pratiques alternatives adaptées à votre problématique ainsi qu'à votre exploitation ",
                "type": "object",
                "properties": {
                    "problem": {
                        "title": "Sur quel sujet pouvons-nous vous aider ?",
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
                    "tillage": {
                        "title": "Quels types de travail du sol souhaitez-vous intégrer dans votre système ?",
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
                        "title": "Quelles cultures composent la rotation des parcelles sur lesquelles vous rencontrez ce problème ?",
                        "required": False,
                        "uniqueItems": False,
                        "items": {
                            "required": True
                        }
                    },
                    "department": {
                        "title": "Quel est le département de votre exploitation ?",
                        "required": False
                    },
                },
                "dependencies": {
                    "pests": ["problem"],
                    "weeds": ["problem"],
                    "weedsGlyphosate": ["glyphosate"],
                    "perennials": ["glyphosate"],
                    "glyphosate": ["problem"],
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
                        },
                        "toolbar": {
                            "actions": [{
                                "label": "Ajoutez une culture",
                                "action": "add",
                            }],
                        },
                        "actionbar": {
                            "actions": [{
                                "action": "up",
                                "enabled": False,
                            }, {
                                "action": "down",
                                "enabled": False,
                            }]
                        },
                    },
                    "department": {
                        "noneLabel": "Sélectionnez",
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
                },
            },
        },

        "contact_form": {
            "schema": {
                "type": "object",
                "description": "Notre équipe pourrait éventuellement être amenée à vous contacter pour avoir votre avis sur Peps et discuter davantage des pratiques adaptées pour votre situation",
                "hideOnMobile": True,
                "properties": {
                    "name": {
                        "title": "Nom et prénom",
                        "type": "string",
                    },
                    "email": {
                        "title": "Adresse email",
                        "type": "string",
                    },
                    "phone": {
                        "title": "Numéro téléphone",
                        "type": "string",
                    },
                },
            },
            "options": {
                "form": {
                    "attributes": {
                        "method": "post",
                        "action": "/api/contact"
                    }
                },
                "fields": {
                    "name": {
                        "placeholder": "Nom Prénom",
                    },
                    "email": {
                        "placeholder": "nom@adresse.com",
                    },
                    "phone": {
                        "placeholder": "06 12 34 56 78",
                    },
                },
            },
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
    return [{'text': x.display_text, 'value': x.name} for x in Problem if x.display_text != 'Autres']

def _get_cultures():
    from data.models import SimulatorCulture
    return [{'text': x.display_text, 'value': x.external_id} for x in SimulatorCulture.objects.all()]

def _get_glyphosate_uses():
    from data.models import GlyphosateUses
    return [{'text': x.display_text, 'value': x.name} for x in GlyphosateUses]
