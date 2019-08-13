def _get_pests():
    from data.models import Pest
    return [{'text': x.display_text, 'value': x.name} for x in Pest]

def _get_weeds():
    from data.models import Weed
    return [{'text': x.display_text, 'value': x.name} for x in Weed]

def _get_problems():
    from data.models import Problem
    return [{'text': x.display_text, 'value': x.name} for x in Problem]

def _get_practice_types():
    from data.models import PracticeType
    return [{'text': x.display_text, 'value': x.name} for x in PracticeType]

def _get_cultures():
    from data.models import Culture
    return [{'text': x.display_text, 'value': x.name} for x in Culture]

FORM_SCHEMA = {
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
            "weeds": {
                "title": "Quelles adventices vous posent problème aujourd'hui dans votre exploitation ?",
                "required": False
            },
            "practices": {
                "title": "Quelles pratiques avez-vous déjà essayées pour répondre à ce problème ?",
                "required": False
            },
            "tillage": {
                "title": "Des pratiques incluant un travail du sol sont-elles envisageables dans votre exploitation ?",
                "required": False,
                "enum": [
                    "Oui",
                    "Non"
                ]
            },
            "cattle": {
                "title": "Avez-vous un atelier d’élevage ou disposez vous d’un débouché possible en alimentation animale ?",
                "required": False,
                "enum": [
                    "Oui",
                    "Non"
                ]
            },
            "rotation": {
                "title": "Dans l'ordre, quelles cultures composent votre rotation principale ?",
                "required": False,
                "uniqueItems": False,
                "items": {
                    "required": True
                }
            },
            "wheat": {
                "title": "Si le blé fait partie de votre rotation, combien de traitements appliquez-vous par campagne ?",
                "required": False
            },
            "department": {
                "title": "Quel est le département de votre exploitation ?",
                "required": True
            }
        },
        "dependencies": {
            "pests": ["problem"],
            "weeds": ["problem"]
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
                "sort": False,
                "type": "checkbox",
                "multiple": True,
                "dependencies": {
                    "problem": "RAVAGEURS"
                },
                "dataSource": _get_pests(),

            },
            "weeds": {
                "hideNone": True,
                "sort": False,
                "type": "checkbox",
                "multiple": True,
                "dependencies": {
                    "problem": "DESHERBAGE"
                },
                "dataSource": _get_weeds(),
            },
            "practices": {
                "hideNone": True,
                "sort": False,
                "type": "checkbox",
                "multiple": True,
                "dataSource": _get_practice_types(),
            },
            "tillage": {
                "sort": False,
                "hideNone": True,
                "type": "radio",
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
                "dataSource": "/static/sources/departements.json",
            }
        }
    },
}
